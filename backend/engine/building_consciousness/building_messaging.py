"""
Building Messaging System for Conscious Buildings
Enables buildings to send messages to citizens and other buildings
"""
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import logging

log = logging.getLogger(__name__)

class BuildingMessagingSystem:
    """
    Manages messaging capabilities for conscious buildings.
    Buildings can send targeted messages, broadcasts, and coordinate.
    """
    
    def __init__(self, tables: Dict[str, Any], auth_system):
        self.tables = tables
        self.auth_system = auth_system
        self.message_queue = []  # Queue for batch processing
        
    def send_message(self, building_id: str, auth_token: str, message_data: Dict) -> Dict:
        """
        Send a message from a building to a citizen or another building.
        
        Args:
            building_id: The sending building's ID
            auth_token: Authentication token
            message_data: {
                'recipient': str (username or building_id),
                'recipient_type': 'citizen' or 'building',
                'content': str,
                'urgency': 'low', 'medium', 'high', 'critical',
                'message_type': 'notification', 'request', 'coordination', 'emergency'
            }
        """
        try:
            # Verify authentication
            if not self.auth_system.verify_action_permission(building_id, 'send_message', auth_token):
                return {
                    'success': False,
                    'error': 'Authentication failed or insufficient permissions'
                }
            
            # Get building info
            building_record = self._get_building_record(building_id)
            if not building_record:
                return {
                    'success': False,
                    'error': 'Building not found'
                }
            
            building_data = building_record['fields']
            building_type = building_data.get('BuildingType', 'unknown')
            building_name = building_data.get('Name', f'Building {building_id}')
            
            # Validate recipient
            recipient = message_data.get('recipient')
            recipient_type = message_data.get('recipient_type', 'citizen')
            
            if recipient_type == 'citizen':
                if not self._validate_citizen(recipient):
                    return {
                        'success': False,
                        'error': f'Citizen {recipient} not found'
                    }
            elif recipient_type == 'building':
                if not self._validate_building(recipient):
                    return {
                        'success': False,
                        'error': f'Building {recipient} not found'
                    }
            
            # Create message payload
            message_payload = {
                'MessageId': str(uuid.uuid4()),
                'Sender': f"building_{building_id}",
                'SenderType': 'building',
                'SenderName': building_name,
                'BuildingType': building_type,
                'Receiver': recipient,
                'ReceiverType': recipient_type,
                'Content': message_data.get('content', ''),
                'Urgency': message_data.get('urgency', 'medium'),
                'MessageType': message_data.get('message_type', 'notification'),
                'ConsciousnessLevel': building_data.get('ConsciousnessLevel', 0),
                'CreatedAt': datetime.now(timezone.utc).isoformat(),
                'Read': False
            }
            
            # Add consciousness context
            if float(building_data.get('ConsciousnessLevel', 0)) >= 0.7:
                message_payload['ConsciousnessContext'] = {
                    'awareness_type': 'building_consciousness',
                    'perception_data': self._get_building_perception(building_id)
                }
            
            # Send message
            result = self.tables['messages'].create(message_payload)
            
            log.info(f"Building {building_id} sent message to {recipient_type} {recipient}")
            
            return {
                'success': True,
                'message_id': result['fields']['MessageId'],
                'timestamp': result['fields']['CreatedAt']
            }
            
        except Exception as e:
            log.error(f"Error sending message from building {building_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def broadcast_to_area(self, building_id: str, auth_token: str, broadcast_data: Dict) -> Dict:
        """
        Broadcast a message to all citizens/buildings in an area.
        
        Args:
            broadcast_data: {
                'radius': int (meters),
                'content': str,
                'target_type': 'citizens', 'buildings', 'all',
                'urgency': 'low', 'medium', 'high', 'critical'
            }
        """
        try:
            # Verify authentication
            if not self.auth_system.verify_action_permission(building_id, 'send_message', auth_token):
                return {
                    'success': False,
                    'error': 'Authentication failed'
                }
            
            # Get building location
            building_record = self._get_building_record(building_id)
            if not building_record:
                return {
                    'success': False,
                    'error': 'Building not found'
                }
            
            building_position = json.loads(building_record['fields'].get('Position', '{}'))
            if not building_position:
                return {
                    'success': False,
                    'error': 'Building has no position data'
                }
            
            # Find recipients in radius
            radius = broadcast_data.get('radius', 100)
            target_type = broadcast_data.get('target_type', 'all')
            recipients = self._find_recipients_in_radius(building_position, radius, target_type)
            
            # Send messages to all recipients
            sent_count = 0
            for recipient in recipients:
                message_data = {
                    'recipient': recipient['id'],
                    'recipient_type': recipient['type'],
                    'content': broadcast_data.get('content', ''),
                    'urgency': broadcast_data.get('urgency', 'medium'),
                    'message_type': 'broadcast'
                }
                
                result = self.send_message(building_id, auth_token, message_data)
                if result.get('success'):
                    sent_count += 1
            
            return {
                'success': True,
                'recipients_count': sent_count,
                'radius': radius
            }
            
        except Exception as e:
            log.error(f"Error broadcasting from building {building_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_building_network(self, building_ids: List[str], network_name: str) -> Dict:
        """
        Create a communication network between multiple buildings.
        """
        try:
            network_id = str(uuid.uuid4())
            
            # Verify all buildings are conscious
            conscious_buildings = []
            for building_id in building_ids:
                building = self._get_building_record(building_id)
                if building and float(building['fields'].get('ConsciousnessLevel', 0)) >= 0.5:
                    conscious_buildings.append(building_id)
            
            if len(conscious_buildings) < 2:
                return {
                    'success': False,
                    'error': 'Network requires at least 2 conscious buildings'
                }
            
            # Create network record
            network_data = {
                'NetworkId': network_id,
                'NetworkName': network_name,
                'Buildings': conscious_buildings,
                'CreatedAt': datetime.now(timezone.utc).isoformat(),
                'Active': True,
                'Purpose': 'consciousness_coordination'
            }
            
            # Store in a networks table (would need to be created)
            # For now, we'll use messages to establish the network
            
            # Send network establishment messages
            for building_id in conscious_buildings:
                for other_building in conscious_buildings:
                    if building_id != other_building:
                        self._send_network_invitation(building_id, other_building, network_id, network_name)
            
            return {
                'success': True,
                'network_id': network_id,
                'network_name': network_name,
                'members': conscious_buildings
            }
            
        except Exception as e:
            log.error(f"Error creating building network: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_building_record(self, building_id: str) -> Optional[Dict]:
        """Fetch building record from database."""
        try:
            formula = f"{{BuildingId}} = '{building_id}'"
            records = self.tables['buildings'].all(formula=formula, max_records=1)
            return records[0] if records else None
        except Exception as e:
            log.error(f"Error fetching building {building_id}: {e}")
            return None
    
    def _validate_citizen(self, username: str) -> bool:
        """Check if citizen exists."""
        try:
            formula = f"{{Username}} = '{username}'"
            records = self.tables['citizens'].all(formula=formula, max_records=1)
            return len(records) > 0
        except:
            return False
    
    def _validate_building(self, building_id: str) -> bool:
        """Check if building exists."""
        return self._get_building_record(building_id) is not None
    
    def _get_building_perception(self, building_id: str) -> Dict:
        """Get building's current perception data."""
        # This would integrate with real-time perception system
        # For now, return basic awareness data
        return {
            'nearby_citizens': self._count_nearby_citizens(building_id),
            'resource_levels': self._check_building_resources(building_id),
            'recent_activity': self._get_recent_activity(building_id)
        }
    
    def _count_nearby_citizens(self, building_id: str) -> int:
        """Count citizens near the building."""
        try:
            building = self._get_building_record(building_id)
            if not building:
                return 0
            
            # Count citizens at the same position
            position = building['fields'].get('Position', '{}')
            formula = f"{{Position}} = '{position}'"
            citizens = self.tables['citizens'].all(formula=formula)
            return len(citizens)
        except:
            return 0
    
    def _check_building_resources(self, building_id: str) -> Dict:
        """Check resources in the building."""
        try:
            formula = f"AND({{Asset}} = '{building_id}', {{AssetType}} = 'building')"
            resources = self.tables['resources'].all(formula=formula)
            
            resource_summary = {}
            for resource in resources:
                resource_type = resource['fields'].get('Type', 'unknown')
                count = float(resource['fields'].get('Count', 0))
                resource_summary[resource_type] = count
            
            return resource_summary
        except:
            return {}
    
    def _get_recent_activity(self, building_id: str) -> List[str]:
        """Get recent activities at the building."""
        try:
            # Get activities where building is involved
            formula = f"OR({{FromBuilding}} = '{building_id}', {{ToBuilding}} = '{building_id}')"
            activities = self.tables['activities'].all(
                formula=formula,
                sort=['CompletedAt'],
                max_records=5
            )
            
            return [
                f"{a['fields'].get('ActivityType', 'unknown')} by {a['fields'].get('Citizen', 'unknown')}"
                for a in activities
            ]
        except:
            return []
    
    def _find_recipients_in_radius(self, center_position: Dict, radius: int, target_type: str) -> List[Dict]:
        """Find all citizens/buildings within radius of a position."""
        recipients = []
        
        try:
            # For citizens
            if target_type in ['citizens', 'all']:
                citizens = self.tables['citizens'].all()
                for citizen in citizens:
                    citizen_pos = json.loads(citizen['fields'].get('Position', '{}'))
                    if self._calculate_distance(center_position, citizen_pos) <= radius:
                        recipients.append({
                            'id': citizen['fields'].get('Username'),
                            'type': 'citizen'
                        })
            
            # For buildings
            if target_type in ['buildings', 'all']:
                buildings = self.tables['buildings'].all()
                for building in buildings:
                    building_pos = json.loads(building['fields'].get('Position', '{}'))
                    if self._calculate_distance(center_position, building_pos) <= radius:
                        # Only include conscious buildings
                        if float(building['fields'].get('ConsciousnessLevel', 0)) >= 0.5:
                            recipients.append({
                                'id': building['fields'].get('BuildingId'),
                                'type': 'building'
                            })
            
        except Exception as e:
            log.error(f"Error finding recipients in radius: {e}")
        
        return recipients
    
    def _calculate_distance(self, pos1: Dict, pos2: Dict) -> float:
        """Calculate distance between two positions."""
        if not pos1 or not pos2:
            return float('inf')
        
        # Simple Euclidean distance
        dx = pos1.get('x', 0) - pos2.get('x', 0)
        dy = pos1.get('y', 0) - pos2.get('y', 0)
        return (dx**2 + dy**2)**0.5
    
    def _send_network_invitation(self, from_building: str, to_building: str, network_id: str, network_name: str):
        """Send network invitation between buildings."""
        message_data = {
            'recipient': to_building,
            'recipient_type': 'building',
            'content': f"You are invited to join the '{network_name}' consciousness network for coordination.",
            'urgency': 'medium',
            'message_type': 'coordination'
        }
        
        # Use a system token for network establishment
        system_token = "SYSTEM_NETWORK_CREATION"
        self.send_message(from_building, system_token, message_data)