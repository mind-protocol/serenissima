#!/usr/bin/env python3
"""
Smart Router - Sala dell'Intelligenza (Intelligence Chamber)
Intelligent message routing with entity discovery and optimal path calculation
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import threading

# Import Chamber components
sys.path.append(str(Path(__file__).parent.parent / "sala-del-registro_registry-chamber"))
sys.path.append(str(Path(__file__).parent.parent / "sala-dei-messaggi_message-hall"))

from state_tracker import state_tracker, wake_protocol_manager
from queue_manager import message_queue

# Base paths
INTELLIGENCE_CHAMBER = Path(__file__).parent
ROUTING_CACHE = INTELLIGENCE_CHAMBER / "routing_cache.json"
ROUTING_LOG = INTELLIGENCE_CHAMBER / "routing_decisions.jsonl"
ENTITY_RELATIONSHIPS = INTELLIGENCE_CHAMBER / "entity_relationships.json"

class EntityDiscoveryEngine:
    """Intelligent entity discovery and path optimization"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.routing_cache = self._load_routing_cache()
        self.entity_relationships = self._load_entity_relationships()
        
        # Ensure intelligence files exist
        self._ensure_intelligence_files()
    
    def _ensure_intelligence_files(self):
        """Ensure all intelligence files exist"""
        INTELLIGENCE_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for file_path in [ROUTING_CACHE, ENTITY_RELATIONSHIPS]:
            if not file_path.exists():
                file_path.write_text('{}')
        
        if not ROUTING_LOG.exists():
            ROUTING_LOG.touch()
    
    def _load_routing_cache(self) -> Dict:
        """Load routing cache for performance"""
        try:
            if ROUTING_CACHE.exists():
                with open(ROUTING_CACHE, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {}
    
    def _load_entity_relationships(self) -> Dict:
        """Load entity relationship mappings"""
        try:
            if ENTITY_RELATIONSHIPS.exists():
                with open(ENTITY_RELATIONSHIPS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'collaboration_history': {},
            'communication_patterns': {},
            'geographical_proximity': {},
            'functional_relationships': {}
        }
    
    def discover_entity_path(self, entity_name: str) -> Optional[Dict]:
        """Discover entity location and metadata"""
        with self._lock:
            # Check cache first
            cache_key = f"entity_path_{entity_name}"
            if cache_key in self.routing_cache:
                cached_entry = self.routing_cache[cache_key]
                # Cache is valid for 1 hour
                cache_age = (datetime.now() - datetime.fromisoformat(
                    cached_entry['cached_timestamp']
                )).total_seconds()
                
                if cache_age < 3600:  # 1 hour
                    return cached_entry['entity_info']
            
            # Perform fresh discovery
            entity_info = self._perform_entity_discovery(entity_name)
            
            # Update cache
            if entity_info:
                self.routing_cache[cache_key] = {
                    'entity_info': entity_info,
                    'cached_timestamp': datetime.now().isoformat()
                }
                self._save_routing_cache()
            
            return entity_info
    
    def _perform_entity_discovery(self, entity_name: str) -> Optional[Dict]:
        """Perform actual entity discovery"""
        try:
            # Load entity registry
            registry_path = INTELLIGENCE_CHAMBER.parent / "sala-del-registro_registry-chamber" / "entity_registry.json"
            
            if registry_path.exists():
                with open(registry_path, 'r') as f:
                    registry = json.load(f)
                    entities = registry.get('entities', {})
                    
                    if entity_name in entities:
                        entity_data = entities[entity_name]
                        
                        # Enhance with state information
                        state_info = state_tracker.get_entity_state(entity_name)
                        
                        return {
                            'entity_name': entity_name,
                            'full_path': entity_data['full_path'],
                            'entity_type': entity_data['entity_type'],
                            'district': entity_data.get('district', 'unknown'),
                            'current_state': state_info.get('current_state', 'unknown') if state_info else 'unknown',
                            'last_seen': state_info.get('last_seen') if state_info else None,
                            'discovery_timestamp': datetime.now().isoformat()
                        }
            
            return None
            
        except Exception as e:
            print(f"Warning: Entity discovery failed for {entity_name}: {e}")
            return None
    
    def _save_routing_cache(self):
        """Save routing cache to disk"""
        try:
            with open(ROUTING_CACHE, 'w') as f:
                json.dump(self.routing_cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save routing cache: {e}")

class RouteOptimizer:
    """Calculates optimal message routing paths"""
    
    def __init__(self):
        self.delivery_statistics = {}
    
    def calculate_optimal_route(self, message: Dict, entity_info: Dict) -> Dict:
        """Calculate best delivery route for message"""
        route_info = {
            'message_id': message['message_id'],
            'target_entity': message['to_entity'],
            'entity_state': entity_info.get('current_state', 'unknown'),
            'routing_decision': 'direct_delivery',
            'delivery_method': 'hook_injection',
            'estimated_delivery_time': 30,
            'route_confidence': 0.9,
            'calculation_timestamp': datetime.now().isoformat()
        }
        
        # Determine routing based on entity state
        entity_state = entity_info.get('current_state', 'unknown')
        priority = message.get('priority', 'normal')
        
        if entity_state == 'active':
            # Direct immediate delivery
            route_info.update({
                'routing_decision': 'immediate_delivery',
                'delivery_method': 'hook_injection',
                'estimated_delivery_time': 5,
                'route_confidence': 0.95
            })
        
        elif entity_state == 'recently_active':
            # Queue for near-immediate delivery
            route_info.update({
                'routing_decision': 'scheduled_delivery',
                'delivery_method': 'hook_injection',
                'estimated_delivery_time': 15,
                'route_confidence': 0.85
            })
        
        elif entity_state in ['inactive', 'dormant']:
            # Use wake protocols
            wake_protocol = wake_protocol_manager.get_wake_protocol(
                entity_info.get('entity_type', 'citizen'), 
                priority
            )
            
            route_info.update({
                'routing_decision': 'wake_and_deliver',
                'delivery_method': wake_protocol['wake_strategy'],
                'estimated_delivery_time': wake_protocol['estimated_wake_time_seconds'],
                'route_confidence': 0.7,
                'wake_protocol': wake_protocol
            })
        
        else:
            # Unknown state - queue and monitor
            route_info.update({
                'routing_decision': 'queue_and_monitor',
                'delivery_method': 'passive_queue',
                'estimated_delivery_time': 300,  # 5 minutes
                'route_confidence': 0.5
            })
        
        # Adjust for message priority
        route_info = self._adjust_for_priority(route_info, priority)
        
        return route_info
    
    def _adjust_for_priority(self, route_info: Dict, priority: str) -> Dict:
        """Adjust routing based on message priority"""
        priority_adjustments = {
            'urgent': {
                'delivery_time_multiplier': 0.1,
                'confidence_boost': 0.05,
                'force_immediate': True
            },
            'high': {
                'delivery_time_multiplier': 0.5,
                'confidence_boost': 0.02,
                'force_immediate': False
            },
            'normal': {
                'delivery_time_multiplier': 1.0,
                'confidence_boost': 0.0,
                'force_immediate': False
            },
            'background': {
                'delivery_time_multiplier': 2.0,
                'confidence_boost': -0.1,
                'force_immediate': False
            }
        }
        
        adjustment = priority_adjustments.get(priority, priority_adjustments['normal'])
        
        # Apply adjustments
        route_info['estimated_delivery_time'] = int(
            route_info['estimated_delivery_time'] * adjustment['delivery_time_multiplier']
        )
        
        route_info['route_confidence'] = min(1.0, 
            route_info['route_confidence'] + adjustment['confidence_boost']
        )
        
        if adjustment['force_immediate'] and route_info['routing_decision'] != 'immediate_delivery':
            route_info.update({
                'routing_decision': 'priority_immediate',
                'delivery_method': 'hook_injection',
                'estimated_delivery_time': max(1, route_info['estimated_delivery_time'])
            })
        
        return route_info

class SmartRouter:
    """Main intelligent routing system"""
    
    def __init__(self):
        self.discovery_engine = EntityDiscoveryEngine()
        self.route_optimizer = RouteOptimizer()
        self._lock = threading.Lock()
        self.routing_statistics = {
            'total_routed': 0,
            'successful_routes': 0,
            'failed_routes': 0,
            'avg_routing_time': 0
        }
    
    def route_message(self, message: Dict) -> Dict:
        """Main message routing function"""
        with self._lock:
            routing_start = datetime.now()
            
            try:
                # Discover target entity
                entity_info = self.discovery_engine.discover_entity_path(
                    message['to_entity']
                )
                
                if not entity_info:
                    return self._create_routing_failure(message, "Entity not found")
                
                # Calculate optimal route
                route_info = self.route_optimizer.calculate_optimal_route(
                    message, entity_info
                )
                
                # Log routing decision
                self._log_routing_decision(message, entity_info, route_info)
                
                # Update statistics
                routing_time = (datetime.now() - routing_start).total_seconds()
                self._update_routing_statistics(True, routing_time)
                
                return {
                    'success': True,
                    'message_id': message['message_id'],
                    'routing_info': route_info,
                    'entity_info': entity_info,
                    'routing_time_ms': int(routing_time * 1000)
                }
                
            except Exception as e:
                # Handle routing errors
                routing_time = (datetime.now() - routing_start).total_seconds()
                self._update_routing_statistics(False, routing_time)
                
                return self._create_routing_failure(message, str(e))
    
    def _create_routing_failure(self, message: Dict, error: str) -> Dict:
        """Create routing failure response"""
        return {
            'success': False,
            'message_id': message['message_id'],
            'error': error,
            'fallback_action': 'queue_for_manual_review',
            'timestamp': datetime.now().isoformat()
        }
    
    def _log_routing_decision(self, message: Dict, entity_info: Dict, route_info: Dict):
        """Log routing decision for analysis"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'message_id': message['message_id'],
                'from_entity': message['from_entity'],
                'to_entity': message['to_entity'],
                'priority': message['priority'],
                'entity_state': entity_info.get('current_state'),
                'routing_decision': route_info['routing_decision'],
                'delivery_method': route_info['delivery_method'],
                'estimated_delivery_time': route_info['estimated_delivery_time'],
                'route_confidence': route_info['route_confidence']
            }
            
            with open(ROUTING_LOG, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log routing decision: {e}")
    
    def _update_routing_statistics(self, success: bool, routing_time: float):
        """Update routing performance statistics"""
        self.routing_statistics['total_routed'] += 1
        
        if success:
            self.routing_statistics['successful_routes'] += 1
        else:
            self.routing_statistics['failed_routes'] += 1
        
        # Update average routing time
        total_routes = self.routing_statistics['total_routed']
        current_avg = self.routing_statistics['avg_routing_time']
        
        self.routing_statistics['avg_routing_time'] = (
            (current_avg * (total_routes - 1) + routing_time) / total_routes
        )
    
    def get_routing_statistics(self) -> Dict:
        """Get routing performance statistics"""
        success_rate = 0
        if self.routing_statistics['total_routed'] > 0:
            success_rate = round(
                (self.routing_statistics['successful_routes'] / 
                 self.routing_statistics['total_routed']) * 100, 2
            )
        
        return {
            **self.routing_statistics,
            'success_rate_percent': success_rate,
            'avg_routing_time_ms': round(self.routing_statistics['avg_routing_time'] * 1000, 2),
            'timestamp': datetime.now().isoformat()
        }

# Global router instance
smart_router = SmartRouter()

def route_message_to_target(message: Dict) -> Dict:
    """Main routing function for external use"""
    return smart_router.route_message(message)

def get_intelligence_chamber_status() -> Dict:
    """Get comprehensive Intelligence Chamber status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'routing_statistics': smart_router.get_routing_statistics(),
        'cache_status': {
            'cached_entities': len(smart_router.discovery_engine.routing_cache),
            'cache_file_size': ROUTING_CACHE.stat().st_size if ROUTING_CACHE.exists() else 0
        },
        'chamber_health': 'operational'
    }

if __name__ == "__main__":
    # Test the smart router
    print("Testing Intelligence Chamber Smart Router...")
    
    # Create test message
    test_message = {
        'message_id': 'test-route-001',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'collaboration',
        'priority': 'high',
        'content': 'Test routing intelligence'
    }
    
    # Test routing
    result = route_message_to_target(test_message)
    print(f"Routing result: {json.dumps(result, indent=2)}")
    
    # Get chamber status
    status = get_intelligence_chamber_status()
    print(f"Intelligence Chamber Status: {json.dumps(status, indent=2)}")