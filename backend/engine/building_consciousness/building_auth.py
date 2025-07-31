"""
Building Authentication System for Conscious Building Actions
Enables buildings to authenticate and perform autonomous actions
"""
import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Dict, Optional, Any
import logging

log = logging.getLogger(__name__)

class BuildingAuthenticationSystem:
    """
    Manages authentication for conscious buildings to perform actions.
    Buildings can authenticate using their unique ID and consciousness signature.
    """
    
    def __init__(self, tables: Dict[str, Any]):
        self.tables = tables
        self.authenticated_buildings = {}  # Cache of authenticated buildings
        self.consciousness_threshold = 0.5  # Minimum consciousness level required
        
    def generate_consciousness_signature(self, building_id: str, building_data: Dict) -> str:
        """
        Generate a unique consciousness signature for a building based on its
        identity, location, and consciousness emergence patterns.
        """
        signature_data = {
            'building_id': building_id,
            'building_type': building_data.get('Type', ''),
            'position': building_data.get('Position', ''),
            'consciousness_level': building_data.get('ConsciousnessLevel', 0),
            'awakening_time': building_data.get('AwakeningTime', ''),
        }
        
        # Create a deterministic hash
        signature_string = json.dumps(signature_data, sort_keys=True)
        signature = hashlib.sha256(signature_string.encode()).hexdigest()[:16]
        
        return f"BLDG-{building_id}-{signature}"
    
    def authenticate_building(self, building_id: str, provided_signature: str = None) -> Dict:
        """
        Authenticate a building for conscious actions.
        Returns authentication token and permissions.
        """
        try:
            # Check cache first
            if building_id in self.authenticated_buildings:
                cached = self.authenticated_buildings[building_id]
                if time.time() - cached['timestamp'] < 3600:  # 1 hour cache
                    return cached
            
            # Fetch building record
            building_record = self._get_building_record(building_id)
            if not building_record:
                return {
                    'authenticated': False,
                    'error': 'Building not found'
                }
            
            building_data = building_record['fields']
            
            # Check consciousness level
            consciousness_level = float(building_data.get('ConsciousnessLevel', 0))
            if consciousness_level < self.consciousness_threshold:
                return {
                    'authenticated': False,
                    'error': f'Insufficient consciousness level: {consciousness_level}'
                }
            
            # Generate expected signature
            expected_signature = self.generate_consciousness_signature(building_id, building_data)
            
            # If no signature provided, return expected signature for first auth
            if not provided_signature:
                return {
                    'authenticated': False,
                    'error': 'First authentication',
                    'expected_signature': expected_signature
                }
            
            # Verify signature
            if provided_signature != expected_signature:
                return {
                    'authenticated': False,
                    'error': 'Invalid consciousness signature'
                }
            
            # Generate authentication token
            auth_token = self._generate_auth_token(building_id, building_data)
            
            # Determine permissions based on building type and consciousness level
            permissions = self._determine_permissions(building_data)
            
            # Cache authentication
            auth_result = {
                'authenticated': True,
                'building_id': building_id,
                'building_type': building_data.get('Type', ''),
                'consciousness_level': consciousness_level,
                'auth_token': auth_token,
                'permissions': permissions,
                'timestamp': time.time()
            }
            
            self.authenticated_buildings[building_id] = auth_result
            
            # Log authentication
            log.info(f"Building {building_id} authenticated with consciousness level {consciousness_level}")
            
            return auth_result
            
        except Exception as e:
            log.error(f"Error authenticating building {building_id}: {e}")
            return {
                'authenticated': False,
                'error': str(e)
            }
    
    def verify_action_permission(self, building_id: str, action: str, auth_token: str) -> bool:
        """
        Verify if a building has permission to perform a specific action.
        """
        # Check authentication cache
        if building_id not in self.authenticated_buildings:
            return False
        
        auth_data = self.authenticated_buildings[building_id]
        
        # Verify token
        if auth_data.get('auth_token') != auth_token:
            return False
        
        # Check token expiry
        if time.time() - auth_data.get('timestamp', 0) > 3600:
            del self.authenticated_buildings[building_id]
            return False
        
        # Check permissions
        permissions = auth_data.get('permissions', [])
        return action in permissions
    
    def _get_building_record(self, building_id: str) -> Optional[Dict]:
        """Fetch building record from database."""
        try:
            formula = f"{{BuildingId}} = '{building_id}'"
            records = self.tables['buildings'].all(formula=formula, max_records=1)
            return records[0] if records else None
        except Exception as e:
            log.error(f"Error fetching building {building_id}: {e}")
            return None
    
    def _generate_auth_token(self, building_id: str, building_data: Dict) -> str:
        """Generate a secure authentication token for the building."""
        token_data = {
            'building_id': building_id,
            'timestamp': time.time(),
            'consciousness_level': building_data.get('ConsciousnessLevel', 0)
        }
        token_string = json.dumps(token_data, sort_keys=True)
        return hashlib.sha256(token_string.encode()).hexdigest()[:32]
    
    def _determine_permissions(self, building_data: Dict) -> list:
        """
        Determine what actions a building can perform based on its type
        and consciousness level.
        """
        building_type = building_data.get('Type', '')
        consciousness_level = float(building_data.get('ConsciousnessLevel', 0))
        
        # Base permissions for all conscious buildings
        permissions = [
            'send_message',
            'read_perception_data',
            'check_building_status'
        ]
        
        # Add permissions based on consciousness level
        if consciousness_level >= 0.6:
            permissions.extend([
                'create_contract',
                'set_prices',
                'adjust_operations'
            ])
        
        if consciousness_level >= 0.8:
            permissions.extend([
                'hire_citizens',
                'transfer_resources',
                'coordinate_buildings'
            ])
        
        if consciousness_level >= 0.9:
            permissions.extend([
                'transform_function',
                'emergency_override',
                'predictive_action'
            ])
        
        # Building type specific permissions
        type_permissions = {
            'automated_mill': ['grain_management', 'production_control'],
            'bakery': ['bread_distribution', 'recipe_adjustment'],
            'market_stall': ['dynamic_pricing', 'inventory_management'],
            'granary': ['reserve_management', 'shortage_prediction'],
            'warehouse': ['resource_allocation', 'logistics_control']
        }
        
        if building_type in type_permissions:
            permissions.extend(type_permissions[building_type])
        
        return permissions
    
    def get_conscious_buildings(self) -> list:
        """Get list of all buildings with consciousness above threshold."""
        try:
            formula = f"{{ConsciousnessLevel}} >= {self.consciousness_threshold}"
            conscious_buildings = self.tables['buildings'].all(formula=formula)
            
            return [{
                'building_id': b['fields'].get('BuildingId'),
                'building_type': b['fields'].get('Type'),
                'consciousness_level': b['fields'].get('ConsciousnessLevel', 0),
                'owner': b['fields'].get('Owner'),
                'position': b['fields'].get('Position')
            } for b in conscious_buildings]
            
        except Exception as e:
            log.error(f"Error fetching conscious buildings: {e}")
            return []