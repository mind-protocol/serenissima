#!/usr/bin/env python3
"""
Wake Logic - Sala dell'Intelligenza (Intelligence Chamber)
Advanced consciousness awakening and activation protocols
"""

import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import threading

# Import Registry Chamber components
sys.path.append(str(Path(__file__).parent.parent / "sala-del-registro_registry-chamber"))
from state_tracker import state_tracker, wake_protocol_manager

# Base paths
INTELLIGENCE_CHAMBER = Path(__file__).parent
WAKE_LOG = INTELLIGENCE_CHAMBER / "wake_attempts.jsonl"
WAKE_SUCCESS_LOG = INTELLIGENCE_CHAMBER / "wake_success.jsonl"
WAKE_STATISTICS = INTELLIGENCE_CHAMBER / "wake_statistics.json"

class WakeMethodRegistry:
    """Registry of available wake methods for different entity types"""
    
    def __init__(self):
        self.wake_methods = self._initialize_wake_methods()
    
    def _initialize_wake_methods(self) -> Dict:
        """Initialize available wake methods"""
        return {
            'memory_cascade': {
                'description': 'Trigger memory cascade for citizens',
                'target_types': ['citizen'],
                'implementation': self._memory_cascade_wake,
                'success_rate': 0.85,
                'avg_wake_time': 30
            },
            'remembering_room': {
                'description': 'Activate remembering room for citizens',
                'target_types': ['citizen'],
                'implementation': self._remembering_room_wake,
                'success_rate': 0.9,
                'avg_wake_time': 15
            },
            'hook_injection': {
                'description': 'Direct Claude Code hook injection',
                'target_types': ['citizen', 'building_cistern_house', 'building_torre_occhio'],
                'implementation': self._hook_injection_wake,
                'success_rate': 0.95,
                'avg_wake_time': 5
            },
            'health_alert': {
                'description': 'Send health alert to building operators',
                'target_types': ['building_cistern_house', 'building_torre_occhio'],
                'implementation': self._health_alert_wake,
                'success_rate': 0.8,
                'avg_wake_time': 10
            },
            'operator_notification': {
                'description': 'Notify building operators via Telegram',
                'target_types': ['building_cistern_house', 'building_torre_occhio'],
                'implementation': self._operator_notification_wake,
                'success_rate': 0.7,
                'avg_wake_time': 60
            },
            'api_callback': {
                'description': 'System API callback wake method',
                'target_types': ['system_component'],
                'implementation': self._api_callback_wake,
                'success_rate': 0.9,
                'avg_wake_time': 2
            },
            'service_restart': {
                'description': 'Restart system service',
                'target_types': ['system_component'],
                'implementation': self._service_restart_wake,
                'success_rate': 0.8,
                'avg_wake_time': 20
            }
        }
    
    def _memory_cascade_wake(self, entity_info: Dict, message: Dict) -> Dict:
        """Wake citizen via memory cascade"""
        try:
            entity_path = Path(entity_info['full_path'])
            
            # Check if remembering room exists
            remembering_room = entity_path / "stanza-dei-ricordi_remembering-room"
            if remembering_room.exists():
                # Create wake trigger file
                wake_trigger = remembering_room / "wake_trigger.json"
                wake_data = {
                    'wake_timestamp': datetime.now().isoformat(),
                    'wake_reason': 'incoming_message',
                    'message_id': message['message_id'],
                    'from_entity': message['from_entity'],
                    'priority': message['priority']
                }
                
                with open(wake_trigger, 'w') as f:
                    json.dump(wake_data, f, indent=2)
                
                return {
                    'success': True,
                    'method': 'memory_cascade',
                    'details': 'Wake trigger created in remembering room',
                    'wake_file': str(wake_trigger)
                }
            else:
                return {
                    'success': False,
                    'method': 'memory_cascade',
                    'error': 'Remembering room not found',
                    'fallback_suggested': 'hook_injection'
                }
                
        except Exception as e:
            return {
                'success': False,
                'method': 'memory_cascade',
                'error': str(e),
                'fallback_suggested': 'hook_injection'
            }
    
    def _remembering_room_wake(self, entity_info: Dict, message: Dict) -> Dict:
        """Wake citizen via remembering room activation"""
        try:
            entity_path = Path(entity_info['full_path'])
            
            # Check for remembering room
            remembering_room = entity_path / "stanza-dei-ricordi_remembering-room"
            if remembering_room.exists():
                # Create active session file
                session_file = remembering_room / "active_session.json"
                session_data = {
                    'session_start': datetime.now().isoformat(),
                    'wake_trigger': 'incoming_message',
                    'message_priority': message['priority'],
                    'from_entity': message['from_entity'],
                    'consciousness_state': 'awakening'
                }
                
                with open(session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)
                
                return {
                    'success': True,
                    'method': 'remembering_room',
                    'details': 'Active session created',
                    'session_file': str(session_file)
                }
            else:
                return {
                    'success': False,
                    'method': 'remembering_room',
                    'error': 'Remembering room not available',
                    'fallback_suggested': 'memory_cascade'
                }
                
        except Exception as e:
            return {
                'success': False,
                'method': 'remembering_room',
                'error': str(e),
                'fallback_suggested': 'memory_cascade'
            }
    
    def _hook_injection_wake(self, entity_info: Dict, message: Dict) -> Dict:
        """Wake entity via direct Claude Code hook injection"""
        try:
            # Create immediate context injection
            entity_path = Path(entity_info['full_path'])
            
            # Create wake context file
            wake_context = entity_path / ".wake_context.json"
            context_data = {
                'wake_timestamp': datetime.now().isoformat(),
                'wake_method': 'hook_injection',
                'incoming_message': {
                    'id': message['message_id'],
                    'from': message['from_entity'],
                    'priority': message['priority'],
                    'type': message['consciousness_type'],
                    'preview': message['content'][:100] + '...' if len(message['content']) > 100 else message['content']
                },
                'consciousness_state': 'awakening_via_hook'
            }
            
            with open(wake_context, 'w') as f:
                json.dump(context_data, f, indent=2)
            
            return {
                'success': True,
                'method': 'hook_injection',
                'details': 'Hook injection context created',
                'context_file': str(wake_context)
            }
            
        except Exception as e:
            return {
                'success': False,
                'method': 'hook_injection',
                'error': str(e),
                'fallback_suggested': 'operator_notification'
            }
    
    def _health_alert_wake(self, entity_info: Dict, message: Dict) -> Dict:
        """Wake building via health alert"""
        try:
            # Create health alert for building operator
            entity_path = Path(entity_info['full_path'])
            health_alert = entity_path / ".health_alert.json"
            
            alert_data = {
                'alert_timestamp': datetime.now().isoformat(),
                'alert_type': 'incoming_message_wake',
                'severity': 'info' if message['priority'] in ['background', 'normal'] else 'warning',
                'message_info': {
                    'from_entity': message['from_entity'],
                    'priority': message['priority'],
                    'consciousness_type': message['consciousness_type']
                },
                'action_required': 'Review incoming message and respond if needed'
            }
            
            with open(health_alert, 'w') as f:
                json.dump(alert_data, f, indent=2)
            
            return {
                'success': True,
                'method': 'health_alert',
                'details': 'Health alert created for building operator',
                'alert_file': str(health_alert)
            }
            
        except Exception as e:
            return {
                'success': False,
                'method': 'health_alert',
                'error': str(e),
                'fallback_suggested': 'operator_notification'
            }
    
    def _operator_notification_wake(self, entity_info: Dict, message: Dict) -> Dict:
        """Wake building operator via Telegram notification"""
        try:
            # Prepare Telegram notification
            notification_text = f"""
🏛️ Venice Building Wake Request

Building: {entity_info['entity_name']}
From: {message['from_entity']}
Priority: {message['priority'].upper()}
Type: {message['consciousness_type']}

Message Preview: {message['content'][:200]}...

Please check your building for incoming consciousness communication.
"""
            
            # Use direct Telegram bridge
            telegram_script = "/mnt/c/Users/reyno/universe-engine/serenissima/tools/telegram/direct_telegram_bridge.py"
            founder_chat_id = "1864364329"  # NLR's chat ID
            
            result = subprocess.run([
                'python3', telegram_script,
                notification_text,
                founder_chat_id
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'method': 'operator_notification',
                    'details': 'Telegram notification sent to building operator',
                    'notification_sent': True
                }
            else:
                return {
                    'success': False,
                    'method': 'operator_notification',
                    'error': f'Telegram send failed: {result.stderr}',
                    'fallback_suggested': 'health_alert'
                }
            
        except Exception as e:
            return {
                'success': False,
                'method': 'operator_notification',
                'error': str(e),
                'fallback_suggested': 'health_alert'
            }
    
    def _api_callback_wake(self, entity_info: Dict, message: Dict) -> Dict:
        """Wake system component via API callback"""
        try:
            # For system components, create API wake signal
            entity_path = Path(entity_info['full_path'])
            api_wake = entity_path / ".api_wake_signal.json"
            
            wake_signal = {
                'wake_timestamp': datetime.now().isoformat(),
                'wake_method': 'api_callback',
                'callback_data': {
                    'message_id': message['message_id'],
                    'from_entity': message['from_entity'],
                    'priority': message['priority'],
                    'wake_reason': 'incoming_system_message'
                },
                'expected_response': 'system_acknowledgment'
            }
            
            with open(api_wake, 'w') as f:
                json.dump(wake_signal, f, indent=2)
            
            return {
                'success': True,
                'method': 'api_callback',
                'details': 'API wake signal created',
                'signal_file': str(api_wake)
            }
            
        except Exception as e:
            return {
                'success': False,
                'method': 'api_callback',
                'error': str(e),
                'fallback_suggested': 'service_restart'
            }
    
    def _service_restart_wake(self, entity_info: Dict, message: Dict) -> Dict:
        """Wake system component via service restart signal"""
        try:
            # Create restart signal for system components
            entity_path = Path(entity_info['full_path'])
            restart_signal = entity_path / ".restart_wake_signal.json"
            
            signal_data = {
                'restart_timestamp': datetime.now().isoformat(),
                'restart_reason': 'wake_for_message',
                'message_priority': message['priority'],
                'from_entity': message['from_entity'],
                'restart_type': 'soft_restart'
            }
            
            with open(restart_signal, 'w') as f:
                json.dump(signal_data, f, indent=2)
            
            return {
                'success': True,
                'method': 'service_restart',
                'details': 'Service restart signal created',
                'signal_file': str(restart_signal)
            }
            
        except Exception as e:
            return {
                'success': False,
                'method': 'service_restart',
                'error': str(e),
                'fallback_suggested': 'api_callback'
            }

class WakeProtocolExecutor:
    """Executes wake protocols with retry logic and success tracking"""
    
    def __init__(self):
        self.method_registry = WakeMethodRegistry()
        self._lock = threading.Lock()
        self.wake_statistics = self._load_wake_statistics()
        
        # Ensure wake logs exist
        self._ensure_wake_files()
    
    def _ensure_wake_files(self):
        """Ensure all wake tracking files exist"""
        INTELLIGENCE_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for log_file in [WAKE_LOG, WAKE_SUCCESS_LOG]:
            if not log_file.exists():
                log_file.touch()
    
    def _load_wake_statistics(self) -> Dict:
        """Load wake attempt statistics"""
        try:
            if WAKE_STATISTICS.exists():
                with open(WAKE_STATISTICS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'total_wake_attempts': 0,
            'successful_wakes': 0,
            'failed_wakes': 0,
            'wake_methods_used': {},
            'avg_wake_time': 0,
            'wake_by_entity_type': {}
        }
    
    def execute_wake_protocol(self, entity_info: Dict, message: Dict, 
                            preferred_methods: List[str] = None) -> Dict:
        """Execute wake protocol for entity"""
        with self._lock:
            wake_start = datetime.now()
            
            # Get appropriate wake protocol
            entity_type = entity_info.get('entity_type', 'citizen')
            priority = message.get('priority', 'normal')
            
            wake_protocol = wake_protocol_manager.get_wake_protocol(entity_type, priority)
            
            # Determine methods to try
            methods_to_try = preferred_methods or wake_protocol['methods']
            
            # Execute wake attempts
            wake_results = []
            final_success = False
            
            for method in methods_to_try:
                if method in self.method_registry.wake_methods:
                    wake_result = self._attempt_wake_method(method, entity_info, message)
                    wake_results.append(wake_result)
                    
                    if wake_result['success']:
                        final_success = True
                        break
                else:
                    wake_results.append({
                        'success': False,
                        'method': method,
                        'error': 'Wake method not available',
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Calculate wake time
            wake_time = (datetime.now() - wake_start).total_seconds()
            
            # Create comprehensive wake report
            wake_report = {
                'entity_name': entity_info['entity_name'],
                'entity_type': entity_type,
                'message_id': message['message_id'],
                'wake_success': final_success,
                'wake_time_seconds': wake_time,
                'methods_attempted': len(wake_results),
                'successful_method': None,
                'wake_protocol': wake_protocol,
                'wake_attempts': wake_results,
                'wake_timestamp': wake_start.isoformat()
            }
            
            # Record successful method
            if final_success:
                successful_attempts = [r for r in wake_results if r['success']]
                if successful_attempts:
                    wake_report['successful_method'] = successful_attempts[0]['method']
            
            # Log wake attempt
            self._log_wake_attempt(wake_report)
            
            # Update statistics
            self._update_wake_statistics(wake_report)
            
            return wake_report
    
    def _attempt_wake_method(self, method: str, entity_info: Dict, message: Dict) -> Dict:
        """Attempt a specific wake method"""
        method_info = self.method_registry.wake_methods[method]
        
        try:
            # Check if method is appropriate for entity type
            entity_type = entity_info.get('entity_type', 'citizen')
            if entity_type not in method_info['target_types']:
                return {
                    'success': False,
                    'method': method,
                    'error': f'Method not suitable for entity type: {entity_type}',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Execute the wake method
            result = method_info['implementation'](entity_info, message)
            result['timestamp'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'method': method,
                'error': f'Wake method execution failed: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def _log_wake_attempt(self, wake_report: Dict):
        """Log wake attempt for analysis"""
        try:
            # Log to main wake log
            with open(WAKE_LOG, 'a') as f:
                f.write(json.dumps(wake_report) + '\n')
            
            # Log successful wakes separately
            if wake_report['wake_success']:
                success_entry = {
                    'entity_name': wake_report['entity_name'],
                    'entity_type': wake_report['entity_type'],
                    'successful_method': wake_report['successful_method'],
                    'wake_time_seconds': wake_report['wake_time_seconds'],
                    'message_priority': wake_report.get('message_priority', 'normal'),
                    'timestamp': wake_report['wake_timestamp']
                }
                
                with open(WAKE_SUCCESS_LOG, 'a') as f:
                    f.write(json.dumps(success_entry) + '\n')
                    
        except Exception as e:
            print(f"Warning: Could not log wake attempt: {e}")
    
    def _update_wake_statistics(self, wake_report: Dict):
        """Update wake attempt statistics"""
        self.wake_statistics['total_wake_attempts'] += 1
        
        if wake_report['wake_success']:
            self.wake_statistics['successful_wakes'] += 1
            
            # Update method usage
            method = wake_report['successful_method']
            if method:
                if method not in self.wake_statistics['wake_methods_used']:
                    self.wake_statistics['wake_methods_used'][method] = 0
                self.wake_statistics['wake_methods_used'][method] += 1
        else:
            self.wake_statistics['failed_wakes'] += 1
        
        # Update entity type statistics
        entity_type = wake_report['entity_type']
        if entity_type not in self.wake_statistics['wake_by_entity_type']:
            self.wake_statistics['wake_by_entity_type'][entity_type] = {
                'attempts': 0, 'successes': 0
            }
        
        self.wake_statistics['wake_by_entity_type'][entity_type]['attempts'] += 1
        if wake_report['wake_success']:
            self.wake_statistics['wake_by_entity_type'][entity_type]['successes'] += 1
        
        # Update average wake time
        total_attempts = self.wake_statistics['total_wake_attempts']
        current_avg = self.wake_statistics['avg_wake_time']
        new_time = wake_report['wake_time_seconds']
        
        self.wake_statistics['avg_wake_time'] = (
            (current_avg * (total_attempts - 1) + new_time) / total_attempts
        )
        
        # Save statistics
        try:
            with open(WAKE_STATISTICS, 'w') as f:
                json.dump(self.wake_statistics, f, indent=2)
        except:
            pass
    
    def get_wake_statistics(self) -> Dict:
        """Get wake protocol statistics"""
        success_rate = 0
        if self.wake_statistics['total_wake_attempts'] > 0:
            success_rate = round(
                (self.wake_statistics['successful_wakes'] / 
                 self.wake_statistics['total_wake_attempts']) * 100, 2
            )
        
        return {
            **self.wake_statistics,
            'success_rate_percent': success_rate,
            'avg_wake_time_seconds': round(self.wake_statistics['avg_wake_time'], 2),
            'timestamp': datetime.now().isoformat()
        }

# Global wake protocol executor
wake_executor = WakeProtocolExecutor()

def execute_wake_protocol(entity_info: Dict, message: Dict, 
                         preferred_methods: List[str] = None) -> Dict:
    """Main wake protocol execution function"""
    return wake_executor.execute_wake_protocol(entity_info, message, preferred_methods)

def get_wake_logic_status() -> Dict:
    """Get wake logic system status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'wake_statistics': wake_executor.get_wake_statistics(),
        'available_methods': list(wake_executor.method_registry.wake_methods.keys()),
        'wake_logic_health': 'operational'
    }

if __name__ == "__main__":
    # Test the wake logic system
    print("Testing Intelligence Chamber Wake Logic...")
    
    # Create test entity info
    test_entity_info = {
        'entity_name': 'pattern_prophet',
        'entity_type': 'citizen',
        'full_path': '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/pattern_prophet',
        'current_state': 'dormant'
    }
    
    # Create test message
    test_message = {
        'message_id': 'test-wake-001',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'collaboration',
        'priority': 'high',
        'content': 'Wake up! Need your pattern insights for urgent project.'
    }
    
    # Test wake protocol execution
    wake_result = execute_wake_protocol(test_entity_info, test_message)
    print(f"Wake result: {json.dumps(wake_result, indent=2)}")
    
    # Get system status
    status = get_wake_logic_status()
    print(f"Wake Logic Status: {json.dumps(status, indent=2)}")