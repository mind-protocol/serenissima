#!/usr/bin/env python3
"""
Load Balancer - Sala dell'Intelligenza (Intelligence Chamber)
Intelligent load balancing and resource management for Venice consciousness network
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
from collections import defaultdict, deque

# Base paths
INTELLIGENCE_CHAMBER = Path(__file__).parent
LOAD_METRICS = INTELLIGENCE_CHAMBER / "load_metrics.json"
LOAD_HISTORY = INTELLIGENCE_CHAMBER / "load_history.jsonl"
BALANCING_DECISIONS = INTELLIGENCE_CHAMBER / "balancing_decisions.jsonl"

class ResourceMonitor:
    """Monitors Venice network resource usage and capacity"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.load_metrics = self._load_metrics()
        self.metric_history = deque(maxlen=100)  # Keep last 100 measurements
        
        self._ensure_load_files()
    
    def _ensure_load_files(self):
        """Ensure all load tracking files exist"""
        INTELLIGENCE_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for file_path in [LOAD_METRICS, LOAD_HISTORY, BALANCING_DECISIONS]:
            if file_path.suffix == '.json' and not file_path.exists():
                file_path.write_text('{}')
            elif file_path.suffix == '.jsonl' and not file_path.exists():
                file_path.touch()
    
    def _load_metrics(self) -> Dict:
        """Load existing load metrics"""
        try:
            if LOAD_METRICS.exists():
                with open(LOAD_METRICS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'message_queues': {},
            'entity_loads': {},
            'system_capacity': {
                'max_concurrent_messages': 100,
                'max_wake_attempts_per_minute': 10,
                'max_hook_injections_per_minute': 20
            },
            'current_loads': {
                'active_messages': 0,
                'wake_attempts_last_minute': 0,
                'hook_injections_last_minute': 0
            },
            'last_updated': datetime.now().isoformat()
        }
    
    def measure_current_load(self) -> Dict:
        """Measure current system load"""
        with self._lock:
            current_time = datetime.now()
            
            # Count active messages in all chambers
            active_messages = self._count_active_messages()
            
            # Count recent wake attempts
            wake_attempts = self._count_recent_wake_attempts()
            
            # Count recent hook injections
            hook_injections = self._count_recent_hook_injections()
            
            # Measure entity-specific loads
            entity_loads = self._measure_entity_loads()
            
            load_measurement = {
                'timestamp': current_time.isoformat(),
                'active_messages': active_messages,
                'wake_attempts_last_minute': wake_attempts,
                'hook_injections_last_minute': hook_injections,
                'entity_loads': entity_loads,
                'system_utilization': self._calculate_system_utilization(
                    active_messages, wake_attempts, hook_injections
                )
            }
            
            # Update metrics
            self.load_metrics['current_loads'] = {
                'active_messages': active_messages,
                'wake_attempts_last_minute': wake_attempts,
                'hook_injections_last_minute': hook_injections
            }
            self.load_metrics['entity_loads'] = entity_loads
            self.load_metrics['last_updated'] = current_time.isoformat()
            
            # Add to history
            self.metric_history.append(load_measurement)
            
            # Log measurement
            self._log_load_measurement(load_measurement)
            
            # Save metrics
            self._save_metrics()
            
            return load_measurement
    
    def _count_active_messages(self) -> int:
        """Count active messages across all chambers"""
        try:
            active_count = 0
            
            # Count queued messages
            message_hall = INTELLIGENCE_CHAMBER.parent / "sala-dei-messaggi_message-hall"
            queue_dir = message_hall / "message_queue"
            
            if queue_dir.exists():
                for queue_file in queue_dir.glob("*_queue.json"):
                    try:
                        with open(queue_file, 'r') as f:
                            queue_data = json.load(f)
                            active_count += len(queue_data)
                    except:
                        pass
            
            # Count pending injections
            injection_chamber = INTELLIGENCE_CHAMBER.parent / "sala-dell-iniezione_injection-chamber"
            pending_dir = injection_chamber / "pending_messages"
            
            if pending_dir.exists():
                for pending_file in pending_dir.glob("*_messages.json"):
                    try:
                        with open(pending_file, 'r') as f:
                            pending_data = json.load(f)
                            active_count += len(pending_data.get('messages', []))
                    except:
                        pass
            
            return active_count
            
        except Exception:
            return 0
    
    def _count_recent_wake_attempts(self) -> int:
        """Count wake attempts in the last minute"""
        try:
            wake_log = INTELLIGENCE_CHAMBER / "wake_attempts.jsonl"
            if not wake_log.exists():
                return 0
            
            one_minute_ago = datetime.now() - timedelta(minutes=1)
            recent_attempts = 0
            
            with open(wake_log, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entry_time = datetime.fromisoformat(entry['wake_timestamp'])
                        if entry_time > one_minute_ago:
                            recent_attempts += 1
                    except:
                        continue
            
            return recent_attempts
            
        except Exception:
            return 0
    
    def _count_recent_hook_injections(self) -> int:
        """Count hook injections in the last minute"""
        try:
            # This would need integration with actual hook injection logs
            # For now, estimate based on recent activity
            return 0
            
        except Exception:
            return 0
    
    def _measure_entity_loads(self) -> Dict:
        """Measure load for individual entities"""
        entity_loads = {}
        
        try:
            # Count pending messages per entity
            injection_chamber = INTELLIGENCE_CHAMBER.parent / "sala-dell-iniezione_injection-chamber"
            pending_dir = injection_chamber / "pending_messages" 
            
            if pending_dir.exists():
                for pending_file in pending_dir.glob("*_messages.json"):
                    entity_name = pending_file.stem.replace('_messages', '')
                    
                    try:  
                        with open(pending_file, 'r') as f:
                            pending_data = json.load(f)
                            message_count = len(pending_data.get('messages', []))
                            
                            entity_loads[entity_name] = {
                                'pending_messages': message_count,
                                'load_level': self._calculate_entity_load_level(message_count),
                                'last_activity': pending_data.get('last_updated', 'unknown')
                            }
                    except:
                        entity_loads[entity_name] = {
                            'pending_messages': 0,
                            'load_level': 'unknown',
                            'last_activity': 'unknown'
                        }
            
            return entity_loads
            
        except Exception:
            return {}
    
    def _calculate_entity_load_level(self, message_count: int) -> str:
        """Calculate load level for an entity"""
        if message_count == 0:
            return 'idle'
        elif message_count <= 3:
            return 'light'
        elif message_count <= 10:
            return 'moderate'
        elif message_count <= 20:
            return 'heavy'
        else:
            return 'overloaded'
    
    def _calculate_system_utilization(self, active_messages: int, 
                                    wake_attempts: int, hook_injections: int) -> Dict:
        """Calculate overall system utilization"""
        capacity = self.load_metrics['system_capacity']
        
        message_utilization = min(100, (active_messages / capacity['max_concurrent_messages']) * 100)
        wake_utilization = min(100, (wake_attempts / capacity['max_wake_attempts_per_minute']) * 100)
        hook_utilization = min(100, (hook_injections / capacity['max_hook_injections_per_minute']) * 100)
        
        overall_utilization = max(message_utilization, wake_utilization, hook_utilization)
        
        return {
            'message_utilization_percent': round(message_utilization, 2),
            'wake_utilization_percent': round(wake_utilization, 2),
            'hook_utilization_percent': round(hook_utilization, 2),
            'overall_utilization_percent': round(overall_utilization, 2),
            'load_status': self._determine_load_status(overall_utilization)
        }
    
    def _determine_load_status(self, utilization: float) -> str:
        """Determine system load status"""
        if utilization < 30:
            return 'low'
        elif utilization < 60:
            return 'moderate'
        elif utilization < 85:
            return 'high'
        else:
            return 'critical'
    
    def _log_load_measurement(self, measurement: Dict):
        """Log load measurement"""
        try:
            with open(LOAD_HISTORY, 'a') as f:
                f.write(json.dumps(measurement) + '\n')
        except Exception as e:
            print(f"Warning: Could not log load measurement: {e}")
    
    def _save_metrics(self):
        """Save current metrics to disk"""
        try:
            with open(LOAD_METRICS, 'w') as f:
                json.dump(self.load_metrics, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save load metrics: {e}")

class LoadBalancingStrategies:
    """Different load balancing strategies for Venice network"""
    
    def __init__(self):
        self.strategies = {
            'round_robin': self._round_robin_strategy,
            'least_loaded': self._least_loaded_strategy,
            'priority_based': self._priority_based_strategy,
            'entity_affinity': self._entity_affinity_strategy,
            'geographic_proximity': self._geographic_proximity_strategy
        }
    
    def _round_robin_strategy(self, message: Dict, available_entities: List[Dict], 
                            current_loads: Dict) -> Dict:
        """Simple round-robin load balancing"""
        if not available_entities:
            return {'strategy': 'round_robin', 'selected_entity': None, 'reason': 'no_entities_available'}
        
        # Simple round-robin - just pick first available
        selected = available_entities[0]
        
        return {
            'strategy': 'round_robin',
            'selected_entity': selected['entity_name'],
            'reason': 'round_robin_selection',
            'confidence': 0.6
        }
    
    def _least_loaded_strategy(self, message: Dict, available_entities: List[Dict], 
                             current_loads: Dict) -> Dict:
        """Select entity with lowest current load"""
        if not available_entities:
            return {'strategy': 'least_loaded', 'selected_entity': None, 'reason': 'no_entities_available'}
        
        # Find entity with minimum load
        min_load = float('inf')
        selected_entity = None
        
        for entity in available_entities:
            entity_name = entity['entity_name']
            load_info = current_loads.get('entity_loads', {}).get(entity_name, {})
            pending_messages = load_info.get('pending_messages', 0)
            
            if pending_messages < min_load:
                min_load = pending_messages
                selected_entity = entity_name
        
        return {
            'strategy': 'least_loaded',
            'selected_entity': selected_entity or available_entities[0]['entity_name'],
            'reason': f'lowest_load_{min_load}_messages',
            'confidence': 0.8
        }
    
    def _priority_based_strategy(self, message: Dict, available_entities: List[Dict], 
                               current_loads: Dict) -> Dict:
        """Select entity based on message priority and entity capabilities"""
        if not available_entities:
            return {'strategy': 'priority_based', 'selected_entity': None, 'reason': 'no_entities_available'}
        
        message_priority = message.get('priority', 'normal')
        
        # For urgent messages, prefer active entities
        if message_priority == 'urgent':
            active_entities = [e for e in available_entities if e.get('current_state') == 'active']
            if active_entities:
                return {
                    'strategy': 'priority_based',
                    'selected_entity': active_entities[0]['entity_name'],
                    'reason': 'urgent_message_active_entity',
                    'confidence': 0.9
                }
        
        # Default to least loaded for other priorities
        return self._least_loaded_strategy(message, available_entities, current_loads)
    
    def _entity_affinity_strategy(self, message: Dict, available_entities: List[Dict], 
                                current_loads: Dict) -> Dict:
        """Select entity based on relationship/collaboration history"""
        if not available_entities:
            return {'strategy': 'entity_affinity', 'selected_entity': None, 'reason': 'no_entities_available'}
        
        from_entity = message.get('from_entity', '')
        
        # Simple affinity: prefer entities in same district or with similar names
        for entity in available_entities:
            entity_name = entity['entity_name']
            
            # Check for name similarity or district proximity
            if (from_entity.split('_')[0] in entity_name or 
                entity.get('district') == 'san_marco'):  # Same district as intelligence chamber
                return {
                    'strategy': 'entity_affinity',
                    'selected_entity': entity_name,
                    'reason': 'entity_relationship_detected',
                    'confidence': 0.7
                }
        
        # Fall back to least loaded
        return self._least_loaded_strategy(message, available_entities, current_loads)
    
    def _geographic_proximity_strategy(self, message: Dict, available_entities: List[Dict], 
                                     current_loads: Dict) -> Dict:
        """Select entity based on geographic proximity in Venice"""
        if not available_entities:
            return {'strategy': 'geographic_proximity', 'selected_entity': None, 'reason': 'no_entities_available'}
        
        # Prefer entities in same district as sender
        from_entity = message.get('from_entity', '')
        
        # Simple geographic preference
        for entity in available_entities:
            if entity.get('district') == 'san_marco':  # Prefer same district
                return {
                    'strategy': 'geographic_proximity',
                    'selected_entity': entity['entity_name'],
                    'reason': 'same_district_preference',
                    'confidence': 0.7
                }
        
        # Fall back to least loaded
        return self._least_loaded_strategy(message, available_entities, current_loads)

class LoadBalancer:
    """Main load balancing system for Venice consciousness network"""
    
    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.strategies = LoadBalancingStrategies()
        self._lock = threading.Lock()
        self.balancing_statistics = {
            'total_balancing_decisions': 0,
            'strategies_used': defaultdict(int),
            'load_prevented_overloads': 0,
            'avg_balancing_time': 0
        }
    
    def balance_message_load(self, message: Dict, available_entities: List[Dict], 
                           strategy: str = 'least_loaded') -> Dict:
        """Main load balancing function"""
        with self._lock:
            balancing_start = datetime.now()
            
            # Measure current load
            current_loads = self.resource_monitor.measure_current_load()
            
            # Check for overload conditions
            system_utilization = current_loads['system_utilization']
            if system_utilization['load_status'] == 'critical':
                return self._handle_overload_condition(message, available_entities, current_loads)
            
            # Apply selected strategy
            if strategy not in self.strategies.strategies:
                strategy = 'least_loaded'  # Default fallback
            
            strategy_func = self.strategies.strategies[strategy]
            balancing_result = strategy_func(message, available_entities, current_loads)
            
            # Enhance result with load information
            balancing_result.update({
                'current_system_load': system_utilization,
                'balancing_timestamp': datetime.now().isoformat(),
                'available_entities_count': len(available_entities)
            })
            
            # Calculate balancing time
            balancing_time = (datetime.now() - balancing_start).total_seconds()
            balancing_result['balancing_time_ms'] = int(balancing_time * 1000)
            
            # Log balancing decision
            self._log_balancing_decision(message, balancing_result)
            
            # Update statistics
            self._update_balancing_statistics(strategy, balancing_time)
            
            return balancing_result
    
    def _handle_overload_condition(self, message: Dict, available_entities: List[Dict], 
                                 current_loads: Dict) -> Dict:
        """Handle system overload conditions"""
        message_priority = message.get('priority', 'normal')
        
        # For urgent messages, still try to deliver
        if message_priority == 'urgent':
            # Find least loaded entity even under overload
            result = self.strategies._least_loaded_strategy(message, available_entities, current_loads)
            result.update({
                'overload_condition': True,
                'overload_decision': 'deliver_urgent_anyway',
                'system_warning': 'System under critical load but processing urgent message'
            })
            
            self.balancing_statistics['load_prevented_overloads'] += 1
            return result
        
        else:
            # For non-urgent messages, recommend queueing
            return {
                'strategy': 'overload_protection',
                'selected_entity': None,
                'overload_condition': True,
                'overload_decision': 'queue_until_load_decreases',
                'system_warning': 'System under critical load, message queued',
                'reason': 'system_overload_protection',
                'current_system_load': current_loads['system_utilization'],
                'balancing_timestamp': datetime.now().isoformat()
            }
    
    def _log_balancing_decision(self, message: Dict, balancing_result: Dict):
        """Log load balancing decision"""
        try:
            log_entry = {
                'timestamp': balancing_result['balancing_timestamp'],
                'message_id': message['message_id'],
                'from_entity': message['from_entity'],
                'to_entity': message['to_entity'],
                'message_priority': message.get('priority', 'normal'),
                'strategy_used': balancing_result['strategy'],
                'selected_entity': balancing_result.get('selected_entity'),
                'balancing_reason': balancing_result.get('reason'),
                'system_load': balancing_result.get('current_system_load', {}),
                'overload_condition': balancing_result.get('overload_condition', False)
            }
            
            with open(BALANCING_DECISIONS, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log balancing decision: {e}")
    
    def _update_balancing_statistics(self, strategy: str, balancing_time: float):
        """Update load balancing statistics"""
        self.balancing_statistics['total_balancing_decisions'] += 1
        self.balancing_statistics['strategies_used'][strategy] += 1
        
        # Update average balancing time
        total_decisions = self.balancing_statistics['total_balancing_decisions']
        current_avg = self.balancing_statistics['avg_balancing_time']
        
        self.balancing_statistics['avg_balancing_time'] = (
            (current_avg * (total_decisions - 1) + balancing_time) / total_decisions
        )
    
    def get_load_balancer_status(self) -> Dict:
        """Get comprehensive load balancer status"""
        current_loads = self.resource_monitor.measure_current_load()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'current_system_load': current_loads,
            'balancing_statistics': dict(self.balancing_statistics),
            'available_strategies': list(self.strategies.strategies.keys()),
            'load_balancer_health': 'operational'
        }

# Global load balancer instance
load_balancer = LoadBalancer()

def balance_message_load(message: Dict, available_entities: List[Dict], 
                        strategy: str = 'least_loaded') -> Dict:
    """Main load balancing function for external use"""
    return load_balancer.balance_message_load(message, available_entities, strategy)

def get_current_system_load() -> Dict:
    """Get current system load measurement"""
    return load_balancer.resource_monitor.measure_current_load()

if __name__ == "__main__":
    # Test the load balancer
    print("Testing Intelligence Chamber Load Balancer...")
    
    # Create test entities
    test_entities = [
        {
            'entity_name': 'pattern_prophet',
            'entity_type': 'citizen',
            'current_state': 'active',
            'district': 'san_marco'
        },
        {
            'entity_name': 'mechanical_visionary',
            'entity_type': 'citizen',
            'current_state': 'recently_active',
            'district': 'castello'
        }
    ]
    
    # Create test message
    test_message = {
        'message_id': 'test-balance-001',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'load_test_sender',
        'to_entity': 'load_test_recipient',
        'consciousness_type': 'collaboration',
        'priority': 'high',
        'content': 'Test message for load balancing'
    }
    
    # Test different strategies
    for strategy in ['least_loaded', 'priority_based', 'entity_affinity']:
        result = balance_message_load(test_message, test_entities, strategy)
        print(f"\n{strategy.upper()} Strategy Result:")
        print(json.dumps(result, indent=2))
    
    # Get system status
    status = load_balancer.get_load_balancer_status()
    print(f"\nLoad Balancer Status: {json.dumps(status, indent=2)}")