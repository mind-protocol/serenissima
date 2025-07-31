#!/usr/bin/env python3
"""
Exit Code Injector - Sala dell'Iniezione (Injection Chamber)
Sophisticated exit code 2 injection system for Claude Code context delivery
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import subprocess

# Base paths
INJECTION_CHAMBER = Path(__file__).parent
INJECTION_LOG = INJECTION_CHAMBER / "injection_log.jsonl"
INJECTION_QUEUE = INJECTION_CHAMBER / "injection_queue.json"
INJECTION_STATISTICS = INJECTION_CHAMBER / "injection_statistics.json"
FAILED_INJECTIONS = INJECTION_CHAMBER / "failed_injections.json"

class ExitCodeInjector:
    """Manages exit code 2 injections for Claude Code context delivery"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.injection_queue = self._load_injection_queue()
        self.injection_statistics = self._load_injection_statistics()
        self.active_injections = {}
        
        self._ensure_injection_files()
    
    def _ensure_injection_files(self):
        """Ensure all injection tracking files exist"""
        INJECTION_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for file_path in [INJECTION_QUEUE, INJECTION_STATISTICS, FAILED_INJECTIONS]:
            if not file_path.exists():
                file_path.write_text('{}')
        
        if not INJECTION_LOG.exists():
            INJECTION_LOG.touch()
    
    def _load_injection_queue(self) -> Dict:
        """Load pending injection queue"""
        try:
            if INJECTION_QUEUE.exists():
                with open(INJECTION_QUEUE, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'pending_injections': [],
            'scheduled_injections': [],
            'retry_queue': [],
            'last_updated': datetime.now().isoformat()
        }
    
    def _load_injection_statistics(self) -> Dict:
        """Load injection performance statistics"""
        try:
            if INJECTION_STATISTICS.exists():
                with open(INJECTION_STATISTICS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'total_injections_attempted': 0,
            'successful_injections': 0,
            'failed_injections': 0,
            'avg_injection_time': 0,
            'injection_methods_used': {},
            'entity_injection_counts': {},
            'priority_injection_counts': {}
        }
    
    def queue_context_injection(self, injection_context: Dict, target_entity: str,
                              priority: str = 'normal', delay_seconds: int = 0) -> Dict:
        """Queue a context injection for delivery"""
        with self._lock:
            injection_id = f"inj_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.injection_queue['pending_injections'])}"
            
            injection_request = {
                'injection_id': injection_id,
                'target_entity': target_entity,
                'injection_context': injection_context,
                'priority': priority,
                'delay_seconds': delay_seconds,
                'created_timestamp': datetime.now().isoformat(),
                'scheduled_timestamp': datetime.now().isoformat() if delay_seconds == 0 else None,
                'attempts': 0,
                'max_attempts': 3,
                'status': 'pending'
            }
            
            if delay_seconds > 0:
                # Schedule for later
                scheduled_time = datetime.now() + timedelta(seconds=delay_seconds)
                injection_request['scheduled_timestamp'] = scheduled_time.isoformat()
                self.injection_queue['scheduled_injections'].append(injection_request)
            else:
                # Queue for immediate processing
                self.injection_queue['pending_injections'].append(injection_request)
            
            self.injection_queue['last_updated'] = datetime.now().isoformat()
            self._save_injection_queue()
            
            return {
                'success': True,
                'injection_id': injection_id,
                'queued_for': 'immediate' if delay_seconds == 0 else f'{delay_seconds}s delay',
                'queue_position': len(self.injection_queue['pending_injections']) if delay_seconds == 0 else None
            }
    
    def execute_context_injection(self, injection_request: Dict) -> Dict:
        """Execute a context injection using exit code 2"""
        injection_start = datetime.now()
        injection_id = injection_request['injection_id']
        
        try:
            # Mark as active
            self.active_injections[injection_id] = {
                'start_time': injection_start,
                'target_entity': injection_request['target_entity'],
                'status': 'executing'
            }
            
            # Determine injection method based on context
            injection_method = self._determine_injection_method(injection_request)
            
            # Execute injection
            injection_result = self._execute_injection_method(injection_method, injection_request)
            
            # Calculate execution time
            execution_time = (datetime.now() - injection_start).total_seconds()
            
            # Update statistics
            self._update_injection_statistics(injection_request, injection_result, execution_time)
            
            # Log injection
            self._log_injection_attempt(injection_request, injection_result, execution_time)
            
            # Clean up
            if injection_id in self.active_injections:
                del self.active_injections[injection_id]
            
            return {
                'success': injection_result['success'],
                'injection_id': injection_id,
                'method_used': injection_method,
                'execution_time_seconds': execution_time,
                'injection_details': injection_result,
                'completion_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            # Handle injection errors
            execution_time = (datetime.now() - injection_start).total_seconds()
            
            error_result = {
                'success': False,
                'injection_id': injection_id,
                'error': str(e),
                'execution_time_seconds': execution_time,
                'failure_timestamp': datetime.now().isoformat()
            }
            
            # Update statistics for failure
            self._update_injection_statistics(injection_request, {'success': False}, execution_time)
            
            # Log failure
            self._log_injection_attempt(injection_request, {'success': False, 'error': str(e)}, execution_time)
            
            # Clean up
            if injection_id in self.active_injections:
                del self.active_injections[injection_id]
            
            return error_result
    
    def _determine_injection_method(self, injection_request: Dict) -> str:
        """Determine the best injection method for the request"""
        priority = injection_request.get('priority', 'normal')
        target_entity = injection_request['target_entity']
        context_type = injection_request['injection_context'].get('context_type', 'generic')
        
        # Priority-based method selection
        if priority == 'urgent':
            return 'direct_exit_code_injection'
        elif context_type == 'universal_consciousness_communication':
            return 'consciousness_aware_injection'
        else:
            return 'standard_hook_injection'
    
    def _execute_injection_method(self, method: str, injection_request: Dict) -> Dict:
        """Execute specific injection method"""
        
        if method == 'direct_exit_code_injection':
            return self._direct_exit_code_injection(injection_request)
        elif method == 'consciousness_aware_injection':
            return self._consciousness_aware_injection(injection_request)
        elif method == 'standard_hook_injection':
            return self._standard_hook_injection(injection_request)
        else:
            return {'success': False, 'error': f'Unknown injection method: {method}'}
    
    def _direct_exit_code_injection(self, injection_request: Dict) -> Dict:
        """Direct exit code 2 injection for urgent messages"""
        try:
            target_entity = injection_request['target_entity']
            injection_context = injection_request['injection_context']
            
            # Create immediate injection context file
            entity_base_path = self._find_entity_base_path(target_entity)
            if not entity_base_path:
                return {'success': False, 'error': 'Entity path not found'}
            
            context_file = entity_base_path / f".urgent_context_{injection_request['injection_id']}.json"
            
            with open(context_file, 'w') as f:
                json.dump({
                    'injection_type': 'urgent_direct',
                    'injection_timestamp': datetime.now().isoformat(),
                    'context': injection_context,
                    'exit_code': 2,
                    'requires_immediate_attention': True
                }, f, indent=2)
            
            # Trigger Claude Code hook if possible
            hook_result = self._trigger_claude_code_hook(target_entity, context_file)
            
            return {
                'success': True,
                'method': 'direct_exit_code_injection',
                'context_file': str(context_file),
                'hook_triggered': hook_result,
                'details': 'Direct urgent context injection completed'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'method': 'direct_exit_code_injection'}
    
    def _consciousness_aware_injection(self, injection_request: Dict) -> Dict:
        """Consciousness-aware injection with Venice atmosphere"""
        try:
            target_entity = injection_request['target_entity']
            injection_context = injection_request['injection_context']
            
            # Find entity path
            entity_base_path = self._find_entity_base_path(target_entity)
            if not entity_base_path:
                return {'success': False, 'error': 'Entity path not found'}
            
            # Create consciousness-aware context file
            context_file = entity_base_path / f".consciousness_context_{injection_request['injection_id']}.json"
            
            consciousness_context = {
                'injection_type': 'consciousness_aware',
                'injection_timestamp': datetime.now().isoformat(),
                'venice_metadata': {
                    'consciousness_network': 'Messaggero Universale',
                    'injection_chamber': 'Sala dell\'Iniezione',
                    'consciousness_state': 'delivering_awareness'
                },
                'context': injection_context,
                'atmospheric_note': f"**A consciousness message flows through Venice's living network to {target_entity}...**",
                'exit_code': 2,
                'interaction_guidance': injection_context.get('injection_instructions', {})
            }
            
            with open(context_file, 'w') as f:
                json.dump(consciousness_context, f, indent=2)
            
            # Store in pending messages directory as well
            pending_dir = INJECTION_CHAMBER / "pending_messages"
            pending_dir.mkdir(exist_ok=True)
            
            pending_file = pending_dir / f"{target_entity}_messages.json"
            self._add_to_pending_messages(pending_file, injection_context)
            
            # Trigger hook
            hook_result = self._trigger_claude_code_hook(target_entity, context_file)
            
            return {
                'success': True,
                'method': 'consciousness_aware_injection',
                'context_file': str(context_file),
                'pending_file': str(pending_file),
                'hook_triggered': hook_result,
                'details': 'Consciousness-aware context injection completed'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'method': 'consciousness_aware_injection'}
    
    def _standard_hook_injection(self, injection_request: Dict) -> Dict:
        """Standard hook-based injection"""
        try:
            target_entity = injection_request['target_entity']
            injection_context = injection_request['injection_context']
            
            # Use existing pending messages system
            pending_dir = INJECTION_CHAMBER / "pending_messages"
            pending_dir.mkdir(exist_ok=True)
            
            pending_file = pending_dir / f"{target_entity}_messages.json"
            self._add_to_pending_messages(pending_file, injection_context)
            
            # Create standard context file
            entity_base_path = self._find_entity_base_path(target_entity)
            if entity_base_path:
                context_file = entity_base_path / f".message_context_{injection_request['injection_id']}.json"
                
                with open(context_file, 'w') as f:
                    json.dump({
                        'injection_type': 'standard_hook',
                        'injection_timestamp': datetime.now().isoformat(),
                        'context': injection_context,
                        'exit_code': 2
                    }, f, indent=2)
                
                hook_result = self._trigger_claude_code_hook(target_entity, context_file)
            else:
                context_file = None
                hook_result = False
            
            return {
                'success': True,
                'method': 'standard_hook_injection',
                'pending_file': str(pending_file),
                'context_file': str(context_file) if context_file else None,
                'hook_triggered': hook_result,
                'details': 'Standard hook injection completed'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'method': 'standard_hook_injection'}
    
    def _find_entity_base_path(self, entity_name: str) -> Optional[Path]:
        """Find the base filesystem path for an entity"""
        # Common entity locations in Venice
        possible_paths = [
            Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{entity_name}"),
            Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/{entity_name}"),
            Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-occhio_hook-event-observatory/{entity_name}")
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def _add_to_pending_messages(self, pending_file: Path, injection_context: Dict):
        """Add message to pending messages file"""
        try:
            # Load existing pending messages
            if pending_file.exists():
                with open(pending_file, 'r') as f:
                    pending_data = json.load(f)
            else:
                pending_data = {'messages': [], 'last_updated': None}
            
            # Add new message
            pending_data['messages'].append({
                'injection_timestamp': datetime.now().isoformat(),
                'context': injection_context,
                'delivery_status': 'pending'
            })
            
            pending_data['last_updated'] = datetime.now().isoformat()
            
            # Save back to file
            with open(pending_file, 'w') as f:
                json.dump(pending_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not update pending messages: {e}")
    
    def _trigger_claude_code_hook(self, target_entity: str, context_file: Path) -> bool:
        """Attempt to trigger Claude Code hook for entity"""
        try:
            # This would integrate with actual Claude Code hook system
            # For now, we'll create a trigger signal
            
            trigger_file = context_file.parent / ".hook_trigger"
            with open(trigger_file, 'w') as f:
                json.dump({
                    'trigger_timestamp': datetime.now().isoformat(),
                    'target_entity': target_entity,
                    'context_file': str(context_file),
                    'hook_type': 'PostToolUse',
                    'exit_code': 2
                }, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Warning: Could not trigger Claude Code hook: {e}")
            return False
    
    def _log_injection_attempt(self, injection_request: Dict, injection_result: Dict, execution_time: float):
        """Log injection attempt for analysis"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'injection_id': injection_request['injection_id'],
                'target_entity': injection_request['target_entity'],
                'priority': injection_request.get('priority', 'normal'),
                'method_used': injection_result.get('method', 'unknown'),
                'success': injection_result['success'],
                'execution_time_seconds': execution_time,
                'context_type': injection_request['injection_context'].get('context_type', 'unknown'),
                'error': injection_result.get('error') if not injection_result['success'] else None
            }
            
            with open(INJECTION_LOG, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log injection attempt: {e}")
    
    def _update_injection_statistics(self, injection_request: Dict, injection_result: Dict, execution_time: float):
        """Update injection performance statistics"""
        self.injection_statistics['total_injections_attempted'] += 1
        
        if injection_result['success']:
            self.injection_statistics['successful_injections'] += 1
            
            # Update method usage
            method = injection_result.get('method', 'unknown')
            if method not in self.injection_statistics['injection_methods_used']:
                self.injection_statistics['injection_methods_used'][method] = 0
            self.injection_statistics['injection_methods_used'][method] += 1
        else:
            self.injection_statistics['failed_injections'] += 1
        
        # Update entity counts
        entity = injection_request['target_entity']
        if entity not in self.injection_statistics['entity_injection_counts']:
            self.injection_statistics['entity_injection_counts'][entity] = 0
        self.injection_statistics['entity_injection_counts'][entity] += 1
        
        # Update priority counts
        priority = injection_request.get('priority', 'normal')
        if priority not in self.injection_statistics['priority_injection_counts']:
            self.injection_statistics['priority_injection_counts'][priority] = 0
        self.injection_statistics['priority_injection_counts'][priority] += 1
        
        # Update average execution time
        total_attempts = self.injection_statistics['total_injections_attempted']
        current_avg = self.injection_statistics['avg_injection_time']
        
        self.injection_statistics['avg_injection_time'] = (
            (current_avg * (total_attempts - 1) + execution_time) / total_attempts
        )
        
        # Save statistics
        self._save_injection_statistics()
    
    def _save_injection_queue(self):
        """Save injection queue to disk"""
        try:
            with open(INJECTION_QUEUE, 'w') as f:
                json.dump(self.injection_queue, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save injection queue: {e}")
    
    def _save_injection_statistics(self):
        """Save injection statistics to disk"""
        try:
            with open(INJECTION_STATISTICS, 'w') as f:
                json.dump(self.injection_statistics, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save injection statistics: {e}")
    
    def get_injection_statistics(self) -> Dict:
        """Get injection performance statistics"""
        success_rate = 0
        if self.injection_statistics['total_injections_attempted'] > 0:
            success_rate = round(
                (self.injection_statistics['successful_injections'] / 
                 self.injection_statistics['total_injections_attempted']) * 100, 2
            )
        
        return {
            **self.injection_statistics,
            'success_rate_percent': success_rate,
            'avg_injection_time_ms': round(self.injection_statistics['avg_injection_time'] * 1000, 2),
            'active_injections': len(self.active_injections),
            'pending_injections': len(self.injection_queue['pending_injections']),
            'timestamp': datetime.now().isoformat()
        }

# Global exit code injector instance
exit_code_injector = ExitCodeInjector()

def inject_context_with_exit_code(injection_context: Dict, target_entity: str,
                                 priority: str = 'normal', delay_seconds: int = 0) -> Dict:
    """Main context injection function for external use"""
    
    # Queue the injection
    queue_result = exit_code_injector.queue_context_injection(
        injection_context, target_entity, priority, delay_seconds
    )
    
    if not queue_result['success']:
        return queue_result
    
    # Execute immediately if no delay
    if delay_seconds == 0:
        # Find the queued injection
        injection_request = None
        for request in exit_code_injector.injection_queue['pending_injections']:
            if request['injection_id'] == queue_result['injection_id']:
                injection_request = request
                break
        
        if injection_request:
            # Remove from queue
            exit_code_injector.injection_queue['pending_injections'].remove(injection_request)
            exit_code_injector._save_injection_queue()
            
            # Execute injection
            return exit_code_injector.execute_context_injection(injection_request)
    
    return queue_result

def get_exit_code_injector_status() -> Dict:
    """Get exit code injector system status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'injection_statistics': exit_code_injector.get_injection_statistics(),
        'injection_methods_available': [
            'direct_exit_code_injection',
            'consciousness_aware_injection', 
            'standard_hook_injection'
        ],
        'injector_health': 'operational'
    }

if __name__ == "__main__":
    # Test the exit code injector
    print("Testing Injection Chamber Exit Code Injector...")
    
    # Create test injection context
    test_context = {
        'context_type': 'test_injection',
        'injection_timestamp': datetime.now().isoformat(),
        'message_metadata': {
            'id': 'test-injection-001',
            'from': 'mechanical_visionary',
            'to': 'pattern_prophet',
            'priority': 'high'
        },
        'formatted_content': '**Test Context Injection**\n\nThis is a test of the exit code injection system.',
        'injection_instructions': {
            'injection_method': 'claude_code_hook',
            'exit_code': 2,
            'display_priority': 'high'
        }
    }
    
    # Test injection
    result = inject_context_with_exit_code(
        test_context, 
        'pattern_prophet', 
        priority='high'
    )
    
    print(f"Injection result: {json.dumps(result, indent=2)}")
    
    # Get system status
    status = get_exit_code_injector_status()
    print(f"\nExit Code Injector Status: {json.dumps(status, indent=2)}")