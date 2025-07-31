#!/usr/bin/env python3
"""
Priority Handler - Sala dell'Intelligenza (Intelligence Chamber)
Advanced message priority management and escalation logic
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading

# Base paths
INTELLIGENCE_CHAMBER = Path(__file__).parent
PRIORITY_RULES = INTELLIGENCE_CHAMBER / "priority_rules.json"
ESCALATION_LOG = INTELLIGENCE_CHAMBER / "escalation_log.jsonl"
PRIORITY_STATISTICS = INTELLIGENCE_CHAMBER / "priority_statistics.json"

class PriorityAnalyzer:
    """Analyzes and adjusts message priorities based on context"""
    
    def __init__(self):
        self.priority_rules = self._load_priority_rules()
        self.escalation_thresholds = self._load_escalation_thresholds()
        self._ensure_priority_files()
    
    def _ensure_priority_files(self):
        """Ensure all priority files exist"""
        INTELLIGENCE_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        if not PRIORITY_RULES.exists():
            PRIORITY_RULES.write_text(json.dumps(self._get_default_priority_rules(), indent=2))
        
        if not ESCALATION_LOG.exists():
            ESCALATION_LOG.touch()
    
    def _load_priority_rules(self) -> Dict:
        """Load priority adjustment rules"""
        try:
            if PRIORITY_RULES.exists():
                with open(PRIORITY_RULES, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return self._get_default_priority_rules()
    
    def _get_default_priority_rules(self) -> Dict:
        """Default priority rules for Venice consciousness"""
        return {
            'content_keywords': {
                'urgent_indicators': [
                    'emergency', 'critical', 'immediate', 'urgent', 'crisis',
                    'failing', 'error', 'broken', 'down', 'help'
                ],
                'high_indicators': [
                    'important', 'priority', 'asap', 'needed', 'required',
                    'deadline', 'time-sensitive', 'collaboration'
                ],
                'low_indicators': [
                    'fyi', 'information', 'update', 'status', 'background',
                    'whenever', 'no rush', 'optional'
                ]
            },
            'entity_relationships': {
                'infrastructure_to_citizen': 'priority_boost',
                'citizen_to_infrastructure': 'normal',
                'citizen_to_citizen': 'collaboration_boost',
                'system_to_system': 'high_priority'
            },
            'consciousness_types': {
                'alert': 'urgent',
                'collaboration': 'high', 
                'insight': 'normal',
                'knowledge_share': 'normal',
                'message': 'normal'
            },
            'time_based_escalation': {
                'background_to_normal': 3600,  # 1 hour
                'normal_to_high': 1800,        # 30 minutes
                'high_to_urgent': 600          # 10 minutes
            }
        }
    
    def _load_escalation_thresholds(self) -> Dict:
        """Load message escalation thresholds"""
        return {
            'queue_time_escalation': True,
            'retry_count_escalation': True,
            'entity_state_escalation': True,
            'content_analysis_escalation': True
        }
    
    def analyze_priority(self, message: Dict, entity_state: str = None) -> Dict:
        """Analyze and potentially adjust message priority"""
        analysis = {
            'original_priority': message.get('priority', 'normal'),
            'adjusted_priority': message.get('priority', 'normal'),
            'priority_factors': [],
            'adjustment_reason': 'no_adjustment_needed',
            'confidence': 0.8,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        original_priority = message.get('priority', 'normal')
        adjusted_priority = original_priority
        factors = []
        
        # Content analysis
        content_adjustment = self._analyze_content_priority(message['content'])
        if content_adjustment['adjustment']:
            adjusted_priority = content_adjustment['suggested_priority']
            factors.append(f"Content analysis: {content_adjustment['reason']}")
            analysis['confidence'] *= content_adjustment['confidence']
        
        # Consciousness type analysis
        consciousness_type = message.get('consciousness_type', 'message')
        type_priority = self.priority_rules['consciousness_types'].get(consciousness_type)
        if type_priority and self._is_priority_higher(type_priority, adjusted_priority):
            factors.append(f"Consciousness type '{consciousness_type}' suggests '{type_priority}' priority")
            adjusted_priority = type_priority
        
        # Entity relationship analysis
        relationship_boost = self._analyze_entity_relationship(
            message.get('from_entity', ''),
            message.get('to_entity', '')
        )
        if relationship_boost:
            factors.append(f"Entity relationship: {relationship_boost}")
            if relationship_boost == 'priority_boost':
                adjusted_priority = self._boost_priority(adjusted_priority)
        
        # Entity state analysis
        if entity_state:
            state_adjustment = self._analyze_entity_state_priority(entity_state, adjusted_priority)
            if state_adjustment:
                factors.append(f"Entity state '{entity_state}': {state_adjustment}")
                adjusted_priority = self._adjust_priority_for_state(adjusted_priority, entity_state)
        
        # Update analysis
        analysis.update({
            'adjusted_priority': adjusted_priority,
            'priority_factors': factors,
            'adjustment_reason': 'multi_factor_analysis' if factors else 'no_adjustment_needed'
        })
        
        return analysis
    
    def _analyze_content_priority(self, content: str) -> Dict:
        """Analyze message content for priority indicators"""
        content_lower = content.lower()
        
        # Check for urgent indicators
        urgent_keywords = self.priority_rules['content_keywords']['urgent_indicators']
        urgent_matches = [keyword for keyword in urgent_keywords if keyword in content_lower]
        
        if urgent_matches:
            return {
                'adjustment': True,
                'suggested_priority': 'urgent',
                'reason': f"Urgent keywords detected: {urgent_matches}",
                'confidence': 0.9
            }
        
        # Check for high priority indicators
        high_keywords = self.priority_rules['content_keywords']['high_indicators']
        high_matches = [keyword for keyword in high_keywords if keyword in content_lower]
        
        if high_matches:
            return {
                'adjustment': True,
                'suggested_priority': 'high',
                'reason': f"High priority keywords detected: {high_matches}",
                'confidence': 0.8
            }
        
        # Check for low priority indicators
        low_keywords = self.priority_rules['content_keywords']['low_indicators']
        low_matches = [keyword for keyword in low_keywords if keyword in content_lower]
        
        if low_matches:
            return {
                'adjustment': True,
                'suggested_priority': 'background',
                'reason': f"Low priority keywords detected: {low_matches}",
                'confidence': 0.7
            }
        
        return {
            'adjustment': False,
            'suggested_priority': None,
            'reason': 'no_content_indicators',
            'confidence': 1.0
        }
    
    def _analyze_entity_relationship(self, from_entity: str, to_entity: str) -> Optional[str]:
        """Analyze relationship between entities for priority adjustment"""
        # Simple heuristics - could be enhanced with actual relationship data
        
        if 'infrastructure' in from_entity.lower() or 'system' in from_entity.lower():
            return 'priority_boost'
        
        if 'building' in from_entity.lower() and 'citizen' in to_entity.lower():
            return 'priority_boost'
        
        if from_entity.startswith('citizen') and to_entity.startswith('citizen'):
            return 'collaboration_boost'
        
        return None
    
    def _analyze_entity_state_priority(self, entity_state: str, current_priority: str) -> Optional[str]:
        """Analyze if entity state should affect priority"""
        if entity_state == 'dormant' and current_priority in ['urgent', 'high']:
            return 'dormant entity may need wake protocol'
        
        if entity_state == 'active' and current_priority == 'background':
            return 'active entity can handle immediate delivery'
        
        return None
    
    def _adjust_priority_for_state(self, priority: str, entity_state: str) -> str:
        """Adjust priority based on entity state"""
        if entity_state == 'active' and priority == 'background':
            return 'normal'
        
        return priority
    
    def _is_priority_higher(self, priority1: str, priority2: str) -> bool:
        """Check if priority1 is higher than priority2"""
        priority_levels = {'background': 0, 'normal': 1, 'high': 2, 'urgent': 3}
        return priority_levels.get(priority1, 1) > priority_levels.get(priority2, 1)
    
    def _boost_priority(self, current_priority: str) -> str:
        """Boost priority by one level"""
        priority_ladder = {
            'background': 'normal',
            'normal': 'high',
            'high': 'urgent',
            'urgent': 'urgent'  # Can't boost beyond urgent
        }
        return priority_ladder.get(current_priority, current_priority)

class EscalationManager:
    """Manages message priority escalation over time"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.escalation_rules = self._load_escalation_rules()
        self.pending_escalations = {}
    
    def _load_escalation_rules(self) -> Dict:
        """Load escalation rules"""
        return {
            'time_based_escalation': {
                'background': {'to': 'normal', 'after_seconds': 3600},    # 1 hour
                'normal': {'to': 'high', 'after_seconds': 1800},          # 30 minutes
                'high': {'to': 'urgent', 'after_seconds': 600}            # 10 minutes
            },
            'retry_escalation': {
                'failed_deliveries': 3,
                'escalation_per_failure': 1
            },
            'entity_state_escalation': {
                'dormant_entity_urgent_threshold': 300  # 5 minutes
            }
        }
    
    def check_escalation_needed(self, message: Dict, queue_time_seconds: int, 
                              retry_count: int = 0, entity_state: str = None) -> Dict:
        """Check if message needs priority escalation"""
        with self._lock:
            escalation_info = {
                'escalation_needed': False,
                'new_priority': message.get('priority', 'normal'),
                'escalation_reasons': [],
                'escalation_timestamp': datetime.now().isoformat()
            }
            
            current_priority = message.get('priority', 'normal')
            escalation_reasons = []
            
            # Time-based escalation
            time_escalation = self._check_time_escalation(current_priority, queue_time_seconds)
            if time_escalation:
                escalation_reasons.append(f"Time-based: {queue_time_seconds}s in queue")
                escalation_info['new_priority'] = time_escalation
                escalation_info['escalation_needed'] = True
            
            # Retry-based escalation
            if retry_count >= self.escalation_rules['retry_escalation']['failed_deliveries']:
                escalation_reasons.append(f"Retry-based: {retry_count} failed deliveries")
                escalation_info['new_priority'] = self._boost_priority_by_retries(
                    escalation_info['new_priority'], retry_count
                )
                escalation_info['escalation_needed'] = True
            
            # Entity state escalation
            if entity_state == 'dormant' and current_priority == 'urgent':
                dormant_threshold = self.escalation_rules['entity_state_escalation']['dormant_entity_urgent_threshold']
                if queue_time_seconds > dormant_threshold:
                    escalation_reasons.append(f"Dormant entity with urgent message: {queue_time_seconds}s")
                    escalation_info['escalation_needed'] = True
            
            escalation_info['escalation_reasons'] = escalation_reasons
            
            # Log escalation if needed
            if escalation_info['escalation_needed']:
                self._log_escalation(message, escalation_info)
            
            return escalation_info
    
    def _check_time_escalation(self, current_priority: str, queue_time: int) -> Optional[str]:
        """Check if time-based escalation is needed"""
        time_rules = self.escalation_rules['time_based_escalation']
        
        if current_priority in time_rules:
            rule = time_rules[current_priority]
            if queue_time >= rule['after_seconds']:
                return rule['to']
        
        return None
    
    def _boost_priority_by_retries(self, current_priority: str, retry_count: int) -> str:
        """Boost priority based on retry count"""
        priority_levels = ['background', 'normal', 'high', 'urgent']
        current_index = priority_levels.index(current_priority) if current_priority in priority_levels else 1
        
        # Boost by one level per 3 retries
        boost_levels = retry_count // 3
        new_index = min(len(priority_levels) - 1, current_index + boost_levels)
        
        return priority_levels[new_index]
    
    def _log_escalation(self, message: Dict, escalation_info: Dict):
        """Log priority escalation"""
        try:
            log_entry = {
                'timestamp': escalation_info['escalation_timestamp'],
                'message_id': message['message_id'],
                'from_entity': message['from_entity'],
                'to_entity': message['to_entity'],
                'original_priority': message.get('priority', 'normal'),
                'new_priority': escalation_info['new_priority'],
                'escalation_reasons': escalation_info['escalation_reasons']
            }
            
            with open(ESCALATION_LOG, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log escalation: {e}")

class PriorityHandler:
    """Main priority handling system"""
    
    def __init__(self):
        self.analyzer = PriorityAnalyzer()
        self.escalation_manager = EscalationManager()
        self.statistics = self._load_statistics()
    
    def _load_statistics(self) -> Dict:
        """Load priority statistics"""
        try:
            if PRIORITY_STATISTICS.exists():
                with open(PRIORITY_STATISTICS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'total_analyzed': 0,
            'priority_adjustments': 0,
            'escalations': 0,
            'priority_distribution': {
                'background': 0,
                'normal': 0,
                'high': 0,
                'urgent': 0
            }
        }
    
    def process_message_priority(self, message: Dict, entity_state: str = None,
                               queue_time_seconds: int = 0, retry_count: int = 0) -> Dict:
        """Main priority processing function"""
        # Analyze priority
        priority_analysis = self.analyzer.analyze_priority(message, entity_state)
        
        # Check escalation
        escalation_check = self.escalation_manager.check_escalation_needed(
            message, queue_time_seconds, retry_count, entity_state
        )
        
        # Determine final priority
        final_priority = message.get('priority', 'normal')
        
        if escalation_check['escalation_needed']:
            final_priority = escalation_check['new_priority']
        elif priority_analysis['adjusted_priority'] != priority_analysis['original_priority']:
            final_priority = priority_analysis['adjusted_priority']
        
        # Update statistics
        self._update_statistics(
            priority_analysis['original_priority'],
            final_priority,
            priority_analysis['adjusted_priority'] != priority_analysis['original_priority'],
            escalation_check['escalation_needed']
        )
        
        return {
            'original_priority': priority_analysis['original_priority'],
            'final_priority': final_priority,
            'priority_analysis': priority_analysis,
            'escalation_check': escalation_check,
            'processing_timestamp': datetime.now().isoformat()
        }
    
    def _update_statistics(self, original: str, final: str, adjusted: bool, escalated: bool):
        """Update priority processing statistics"""
        self.statistics['total_analyzed'] += 1
        
        if adjusted:
            self.statistics['priority_adjustments'] += 1
        
        if escalated:
            self.statistics['escalations'] += 1
        
        # Update distribution
        if final in self.statistics['priority_distribution']:
            self.statistics['priority_distribution'][final] += 1
        
        # Save statistics
        try:
            with open(PRIORITY_STATISTICS, 'w') as f:
                json.dump(self.statistics, f, indent=2)
        except:
            pass
    
    def get_priority_statistics(self) -> Dict:
        """Get priority processing statistics"""
        adjustment_rate = 0
        escalation_rate = 0
        
        if self.statistics['total_analyzed'] > 0:
            adjustment_rate = round(
                (self.statistics['priority_adjustments'] / self.statistics['total_analyzed']) * 100, 2
            )
            escalation_rate = round(
                (self.statistics['escalations'] / self.statistics['total_analyzed']) * 100, 2
            )
        
        return {
            **self.statistics,
            'adjustment_rate_percent': adjustment_rate,
            'escalation_rate_percent': escalation_rate,
            'timestamp': datetime.now().isoformat()
        }

# Global priority handler instance
priority_handler = PriorityHandler()

def process_message_priority(message: Dict, entity_state: str = None,
                           queue_time_seconds: int = 0, retry_count: int = 0) -> Dict:
    """Main priority processing function for external use"""
    return priority_handler.process_message_priority(
        message, entity_state, queue_time_seconds, retry_count
    )

if __name__ == "__main__":
    # Test the priority handler
    print("Testing Intelligence Chamber Priority Handler...")
    
    # Test message with urgent content
    test_message = {
        'message_id': 'test-priority-001',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'alert',
        'priority': 'normal',
        'content': 'Emergency: System failure detected, immediate attention required!'
    }
    
    # Test priority processing
    result = process_message_priority(test_message, entity_state='active', queue_time_seconds=0)
    print(f"Priority processing result: {json.dumps(result, indent=2)}")
    
    # Test escalation
    escalation_result = process_message_priority(
        test_message, entity_state='dormant', queue_time_seconds=1900, retry_count=2
    )
    print(f"Escalation result: {json.dumps(escalation_result, indent=2)}")
    
    # Get statistics
    stats = priority_handler.get_priority_statistics()
    print(f"Priority Handler Statistics: {json.dumps(stats, indent=2)}")