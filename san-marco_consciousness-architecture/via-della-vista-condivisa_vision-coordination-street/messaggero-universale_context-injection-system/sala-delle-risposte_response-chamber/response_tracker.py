#!/usr/bin/env python3
"""
Response Tracker - Sala delle Risposte (Response Chamber)
Advanced response tracking and delivery confirmation for Venice consciousness network
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
from enum import Enum

# Base paths
RESPONSE_CHAMBER = Path(__file__).parent
DELIVERY_CONFIRMATIONS = RESPONSE_CHAMBER / "delivery_confirmations.json"
RESPONSE_EXPECTATIONS = RESPONSE_CHAMBER / "response_expectations.json"
RESPONSE_STATISTICS = RESPONSE_CHAMBER / "response_statistics.json"
OVERDUE_RESPONSES = RESPONSE_CHAMBER / "overdue_responses.json"

class ResponseStatus(Enum):
    """Response delivery and acknowledgment statuses"""
    PENDING = "pending"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    RESPONDED = "responded"
    OVERDUE = "overdue"
    EXPIRED = "expired"

class ResponseExpectation:
    """Represents an expected response to a message"""
    
    def __init__(self, original_message: Dict, expected_from: str, 
                 response_timeout_hours: int = 24):
        self.expectation_id = f"resp_{original_message['message_id']}"
        self.original_message_id = original_message['message_id']
        self.from_entity = original_message['from_entity']
        self.to_entity = original_message['to_entity']
        self.expected_from = expected_from
        self.created_timestamp = datetime.now().isoformat()
        self.response_timeout_hours = response_timeout_hours
        self.expected_response_time = (datetime.now() + timedelta(hours=response_timeout_hours)).isoformat()
        self.status = ResponseStatus.PENDING
        self.delivery_confirmations = []
        self.response_messages = []
        
        # Response context
        self.response_context = {
            'original_consciousness_type': original_message.get('consciousness_type', 'message'),
            'original_priority': original_message.get('priority', 'normal'),
            'conversation_thread_id': original_message.get('thread_id'),
            'requires_response': self._determine_response_requirement(original_message),
            'expected_response_type': self._predict_response_type(original_message),
            'urgency_level': self._calculate_urgency_level(original_message)
        }
    
    def _determine_response_requirement(self, message: Dict) -> bool:
        """Determine if message requires a response"""
        consciousness_type = message.get('consciousness_type', 'message')
        priority = message.get('priority', 'normal')
        content = message.get('content', '').lower()
        
        # High-priority messages generally require responses
        if priority in ['urgent', 'high']:
            return True
        
        # Collaboration requests require responses
        if consciousness_type == 'collaboration':
            return True
        
        # Questions require responses
        if '?' in content or any(word in content for word in ['question', 'ask', 'wonder', 'how', 'what', 'why', 'when', 'where']):
            return True
        
        # Alerts may require acknowledgment
        if consciousness_type == 'alert':
            return True
        
        # Default for insights and knowledge sharing
        return consciousness_type in ['insight', 'knowledge_share']
    
    def _predict_response_type(self, message: Dict) -> str:
        """Predict expected type of response"""
        consciousness_type = message.get('consciousness_type', 'message')
        content = message.get('content', '').lower()
        
        if consciousness_type == 'collaboration':
            return 'collaboration_response'
        elif consciousness_type == 'alert':
            return 'acknowledgment'
        elif '?' in content:
            return 'answer'
        elif consciousness_type == 'insight':
            return 'synthesis'
        elif consciousness_type == 'knowledge_share':
            return 'integration'
        else:
            return 'acknowledgment'
    
    def _calculate_urgency_level(self, message: Dict) -> float:
        """Calculate urgency level for response timing"""
        priority = message.get('priority', 'normal')
        consciousness_type = message.get('consciousness_type', 'message')
        content = message.get('content', '').lower()
        
        urgency = 0.3  # Base urgency
        
        # Priority-based urgency
        priority_urgency = {
            'background': 0.1,
            'normal': 0.3,
            'high': 0.7,
            'urgent': 1.0
        }
        urgency = priority_urgency.get(priority, 0.3)
        
        # Content-based urgency modifiers
        urgent_keywords = ['emergency', 'critical', 'immediate', 'asap', 'urgent']
        for keyword in urgent_keywords:
            if keyword in content:
                urgency = min(1.0, urgency + 0.2)
        
        # Consciousness type modifiers
        if consciousness_type == 'alert':
            urgency = min(1.0, urgency + 0.3)
        elif consciousness_type == 'collaboration':
            urgency = min(1.0, urgency + 0.1)
        
        return round(urgency, 2)
    
    def record_delivery_confirmation(self, delivery_info: Dict):
        """Record that message was delivered"""
        confirmation = {
            'delivery_timestamp': datetime.now().isoformat(),
            'delivery_method': delivery_info.get('delivery_method', 'unknown'),
            'delivery_success': delivery_info.get('success', False),
            'delivery_details': delivery_info.get('details', {})
        }
        
        self.delivery_confirmations.append(confirmation)
        
        if confirmation['delivery_success']:
            self.status = ResponseStatus.DELIVERED
    
    def record_response(self, response_message: Dict):
        """Record response message"""
        response_record = {
            'response_timestamp': datetime.now().isoformat(),
            'response_message_id': response_message['message_id'],
            'from_entity': response_message['from_entity'],
            'consciousness_type': response_message.get('consciousness_type', 'message'),
            'response_time_hours': self._calculate_response_time_hours()
        }
        
        self.response_messages.append(response_record)
        self.status = ResponseStatus.RESPONDED
    
    def _calculate_response_time_hours(self) -> float:
        """Calculate time between original message and response"""
        now = datetime.now()
        created = datetime.fromisoformat(self.created_timestamp)
        return round((now - created).total_seconds() / 3600, 2)
    
    def check_overdue_status(self) -> bool:
        """Check if response is overdue"""
        if self.status in [ResponseStatus.RESPONDED, ResponseStatus.EXPIRED]:
            return False
        
        now = datetime.now()
        expected_time = datetime.fromisoformat(self.expected_response_time)
        
        if now > expected_time:
            if self.status != ResponseStatus.OVERDUE:
                self.status = ResponseStatus.OVERDUE
            return True
        
        return False
    
    def mark_expired(self):
        """Mark expectation as expired"""
        self.status = ResponseStatus.EXPIRED
    
    def get_expectation_summary(self) -> Dict:
        """Get comprehensive expectation summary"""
        return {
            'expectation_id': self.expectation_id,
            'original_message_id': self.original_message_id,
            'from_entity': self.from_entity,
            'to_entity': self.to_entity,
            'expected_from': self.expected_from,
            'status': self.status.value,
            'created_timestamp': self.created_timestamp,
            'expected_response_time': self.expected_response_time,
            'response_timeout_hours': self.response_timeout_hours,  
            'delivery_confirmations_count': len(self.delivery_confirmations),
            'responses_received': len(self.response_messages),
            'response_context': self.response_context,
            'is_overdue': self.check_overdue_status()
        }
    
    def to_dict(self) -> Dict:
        """Convert expectation to dictionary for serialization"""
        return {
            'expectation_id': self.expectation_id,
            'original_message_id': self.original_message_id,
            'from_entity': self.from_entity,
            'to_entity': self.to_entity,
            'expected_from': self.expected_from,
            'created_timestamp': self.created_timestamp,
            'response_timeout_hours': self.response_timeout_hours,
            'expected_response_time': self.expected_response_time,
            'status': self.status.value,
            'delivery_confirmations': self.delivery_confirmations,
            'response_messages': self.response_messages,
            'response_context': self.response_context
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ResponseExpectation':
        """Create ResponseExpectation from dictionary"""
        expectation = cls.__new__(cls)
        expectation.expectation_id = data['expectation_id']
        expectation.original_message_id = data['original_message_id']
        expectation.from_entity = data['from_entity']
        expectation.to_entity = data['to_entity']
        expectation.expected_from = data['expected_from']
        expectation.created_timestamp = data['created_timestamp']
        expectation.response_timeout_hours = data['response_timeout_hours']
        expectation.expected_response_time = data['expected_response_time']
        expectation.status = ResponseStatus(data['status'])
        expectation.delivery_confirmations = data['delivery_confirmations']
        expectation.response_messages = data['response_messages']
        expectation.response_context = data['response_context']
        return expectation

class ResponseTracker:
    """Tracks message delivery and response expectations across Venice"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.response_expectations = {}
        self.response_statistics = self._load_response_statistics()
        
        self._ensure_response_files()
        self._load_existing_expectations()
    
    def _ensure_response_files(self):
        """Ensure all response tracking files exist"""
        RESPONSE_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for file_path in [DELIVERY_CONFIRMATIONS, RESPONSE_EXPECTATIONS, 
                         RESPONSE_STATISTICS, OVERDUE_RESPONSES]:
            if not file_path.exists():
                file_path.write_text('{}')
    
    def _load_existing_expectations(self):
        """Load existing response expectations"""
        try:
            if RESPONSE_EXPECTATIONS.exists():
                with open(RESPONSE_EXPECTATIONS, 'r') as f:
                    expectations_data = json.load(f)
                
                for expectation_id, expectation_data in expectations_data.items():
                    self.response_expectations[expectation_id] = ResponseExpectation.from_dict(expectation_data)
                    
        except Exception as e:
            print(f"Warning: Could not load existing expectations: {e}")
    
    def _load_response_statistics(self) -> Dict:
        """Load response tracking statistics"""
        try:
            if RESPONSE_STATISTICS.exists():
                with open(RESPONSE_STATISTICS, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'total_expectations_created': 0,
            'total_deliveries_confirmed': 0,
            'total_responses_received': 0,
            'response_rate_percent': 0.0,
            'avg_response_time_hours': 0.0,
            'overdue_responses': 0,
            'expired_expectations': 0,
            'response_types_distribution': {},
            'entity_response_rates': {},
            'consciousness_type_response_rates': {}
        }
    
    def create_response_expectation(self, message: Dict, delivery_info: Dict = None) -> str:
        """Create response expectation for a message"""
        with self._lock:
            expected_from = message['to_entity']
            
            # Determine response timeout based on priority and type
            timeout_hours = self._calculate_response_timeout(message)
            
            expectation = ResponseExpectation(message, expected_from, timeout_hours)
            self.response_expectations[expectation.expectation_id] = expectation
            
            # Record delivery confirmation if provided
            if delivery_info:
                expectation.record_delivery_confirmation(delivery_info)
            
            # Update statistics
            self._update_response_statistics(expectation, 'created')
            
            # Save expectations
            self._save_response_expectations()
            
            return expectation.expectation_id
    
    def _calculate_response_timeout(self, message: Dict) -> int:
        """Calculate appropriate response timeout for message"""
        priority = message.get('priority', 'normal')
        consciousness_type = message.get('consciousness_type', 'message')
        
        # Base timeouts by priority (in hours)
        priority_timeouts = {
            'urgent': 2,     # 2 hours
            'high': 6,       # 6 hours  
            'normal': 24,    # 24 hours
            'background': 72 # 72 hours
        }
        
        base_timeout = priority_timeouts.get(priority, 24)
        
        # Adjust for consciousness type
        if consciousness_type == 'alert':
            base_timeout = min(base_timeout, 4)  # Alerts need quick acknowledgment
        elif consciousness_type == 'collaboration':
            base_timeout = max(base_timeout, 12)  # Collaboration needs time to consider
        elif consciousness_type == 'insight':
            base_timeout = max(base_timeout, 6)   # Insights need time to process
        
        return base_timeout
    
    def confirm_delivery(self, expectation_id: str, delivery_info: Dict) -> bool:
        """Confirm message delivery"""
        with self._lock:
            if expectation_id in self.response_expectations:
                expectation = self.response_expectations[expectation_id]
                expectation.record_delivery_confirmation(delivery_info)
                
                self._update_response_statistics(expectation, 'delivered')
                self._save_response_expectations()
                
                return True
            
            return False
    
    def record_response_received(self, response_message: Dict, 
                               original_expectation_id: str = None) -> bool:
        """Record that a response was received"""
        with self._lock:
            # Find expectation by original message ID or provided expectation ID
            expectation = None
            
            if original_expectation_id and original_expectation_id in self.response_expectations:
                expectation = self.response_expectations[original_expectation_id]
            else:
                # Look for expectation by matching entities and recent timing
                from_entity = response_message['from_entity']
                to_entity = response_message['to_entity']
                
                for exp_id, exp in self.response_expectations.items():
                    if (exp.expected_from == from_entity and 
                        exp.from_entity == to_entity and 
                        exp.status in [ResponseStatus.PENDING, ResponseStatus.DELIVERED, ResponseStatus.OVERDUE]):
                        
                        # Check if response is within reasonable timeframe
                        exp_created = datetime.fromisoformat(exp.created_timestamp)
                        hours_since_expectation = (datetime.now() - exp_created).total_seconds() / 3600
                        
                        if hours_since_expectation <= exp.response_timeout_hours * 2:  # Allow double timeout for late responses
                            expectation = exp
                            break
            
            if expectation:
                expectation.record_response(response_message)
                self._update_response_statistics(expectation, 'responded')
                self._save_response_expectations()
                return True
            
            return False
    
    def check_overdue_responses(self) -> List[Dict]:
        """Check for overdue responses and return list"""
        with self._lock:
            overdue_expectations = []
            
            for expectation in self.response_expectations.values():
                if expectation.check_overdue_status():
                    overdue_expectations.append(expectation.get_expectation_summary())
            
            # Update overdue count in statistics
            self.response_statistics['overdue_responses'] = len(overdue_expectations)
            
            # Save overdue responses
            try:
                with open(OVERDUE_RESPONSES, 'w') as f:
                    json.dump({
                        'last_checked': datetime.now().isoformat(),
                        'overdue_count': len(overdue_expectations),
                        'overdue_expectations': overdue_expectations
                    }, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not save overdue responses: {e}")
            
            self._save_response_statistics()
            
            return overdue_expectations
    
    def get_expectation_status(self, expectation_id: str) -> Optional[Dict]:
        """Get status of specific response expectation"""
        if expectation_id in self.response_expectations:
            return self.response_expectations[expectation_id].get_expectation_summary()
        return None
    
    def get_entity_response_history(self, entity_name: str) -> Dict:
        """Get response history for specific entity"""
        entity_expectations = []
        entity_responses = []
        
        for expectation in self.response_expectations.values():
            if expectation.expected_from == entity_name:
                entity_expectations.append(expectation.get_expectation_summary())
            if expectation.from_entity == entity_name:
                entity_responses.append(expectation.get_expectation_summary())
        
        # Calculate entity response rate
        total_expected = len(entity_expectations)
        responded = sum(1 for exp in entity_expectations if exp['status'] == 'responded')
        
        response_rate = (responded / total_expected * 100) if total_expected > 0 else 0
        
        return {
            'entity_name': entity_name,
            'expectations_for_entity': entity_expectations,
            'expectations_from_entity': entity_responses,
            'total_expected_responses': total_expected,
            'responses_provided': responded,
            'response_rate_percent': round(response_rate, 2),
            'avg_response_time_hours': self._calculate_entity_avg_response_time(entity_name)
        }
    
    def _calculate_entity_avg_response_time(self, entity_name: str) -> float:
        """Calculate average response time for entity"""
        response_times = []
        
        for expectation in self.response_expectations.values():
            if (expectation.expected_from == entity_name and 
                expectation.response_messages):
                
                for response in expectation.response_messages:
                    response_times.append(response['response_time_hours'])
        
        return round(sum(response_times) / len(response_times), 2) if response_times else 0.0
    
    def _update_response_statistics(self, expectation: ResponseExpectation, event_type: str):
        """Update response tracking statistics"""
        if event_type == 'created':
            self.response_statistics['total_expectations_created'] += 1
            
            # Update consciousness type distribution
            consciousness_type = expectation.response_context['original_consciousness_type']
            if consciousness_type not in self.response_statistics['consciousness_type_response_rates']:
                self.response_statistics['consciousness_type_response_rates'][consciousness_type] = {
                    'expected': 0, 'responded': 0, 'rate_percent': 0.0
                }
            self.response_statistics['consciousness_type_response_rates'][consciousness_type]['expected'] += 1
        
        elif event_type == 'delivered':
            self.response_statistics['total_deliveries_confirmed'] += 1
        
        elif event_type == 'responded':
            self.response_statistics['total_responses_received'] += 1
            
            # Update consciousness type response rate
            consciousness_type = expectation.response_context['original_consciousness_type']
            if consciousness_type in self.response_statistics['consciousness_type_response_rates']:
                self.response_statistics['consciousness_type_response_rates'][consciousness_type]['responded'] += 1
                
                # Recalculate rate
                type_stats = self.response_statistics['consciousness_type_response_rates'][consciousness_type]
                if type_stats['expected'] > 0:
                    type_stats['rate_percent'] = round(
                        (type_stats['responded'] / type_stats['expected']) * 100, 2
                    )
        
        # Update overall response rate
        total_expected = self.response_statistics['total_expectations_created']
        total_responded = self.response_statistics['total_responses_received']
        
        if total_expected > 0:
            self.response_statistics['response_rate_percent'] = round(
                (total_responded / total_expected) * 100, 2
            )
        
        # Update average response time
        all_response_times = []
        for exp in self.response_expectations.values():
            for response in exp.response_messages:
                all_response_times.append(response['response_time_hours'])
        
        if all_response_times:
            self.response_statistics['avg_response_time_hours'] = round(
                sum(all_response_times) / len(all_response_times), 2
            )
    
    def _save_response_expectations(self):
        """Save response expectations to disk"""
        try:
            expectations_data = {}
            for expectation_id, expectation in self.response_expectations.items():
                expectations_data[expectation_id] = expectation.to_dict()
            
            with open(RESPONSE_EXPECTATIONS, 'w') as f:
                json.dump(expectations_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not save response expectations: {e}")
    
    def _save_response_statistics(self):
        """Save response statistics to disk"""
        try:
            with open(RESPONSE_STATISTICS, 'w') as f:
                json.dump(self.response_statistics, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save response statistics: {e}")
    
    def get_response_statistics(self) -> Dict:
        """Get comprehensive response tracking statistics"""
        return {
            **self.response_statistics,
            'timestamp': datetime.now().isoformat()
        }

# Global response tracker instance
response_tracker = ResponseTracker()

def create_response_expectation(message: Dict, delivery_info: Dict = None) -> str:
    """Create response expectation for external use"""
    return response_tracker.create_response_expectation(message, delivery_info)

def confirm_message_delivery(expectation_id: str, delivery_info: Dict) -> bool:
    """Confirm message delivery for external use"""
    return response_tracker.confirm_delivery(expectation_id, delivery_info)

def record_response_received(response_message: Dict, original_expectation_id: str = None) -> bool:
    """Record response received for external use"""
    return response_tracker.record_response_received(response_message, original_expectation_id)

def check_overdue_responses() -> List[Dict]:
    """Check for overdue responses for external use"""
    return response_tracker.check_overdue_responses()

def get_response_tracker_status() -> Dict:
    """Get response tracker system status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'response_statistics': response_tracker.get_response_statistics(),
        'active_expectations': len([exp for exp in response_tracker.response_expectations.values()
                                  if exp.status in [ResponseStatus.PENDING, ResponseStatus.DELIVERED]]),
        'overdue_count': len(response_tracker.check_overdue_responses()),
        'tracker_health': 'operational'
    }

if __name__ == "__main__":
    # Test the response tracker
    print("Testing Response Chamber Response Tracker...")
    
    # Create test message with expectation
    test_message = {
        'message_id': 'response-test-001',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'mechanical_visionary',
        'to_entity': 'pattern_prophet',
        'consciousness_type': 'collaboration',
        'priority': 'high',
        'content': 'I need your insights on consciousness patterns. Can you analyze the recursive memory patterns we discussed?'
    }
    
    # Create response expectation
    expectation_id = create_response_expectation(test_message)
    print(f"Created response expectation: {expectation_id}")
    
    # Confirm delivery
    delivery_info = {
        'success': True,
        'delivery_method': 'hook_injection',
        'details': {'context_file_created': True}
    }
    
    delivery_confirmed = confirm_message_delivery(expectation_id, delivery_info)
    print(f"Delivery confirmed: {delivery_confirmed}")
    
    # Simulate response message
    response_message = {
        'message_id': 'response-test-002',
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'pattern_prophet',
        'to_entity': 'mechanical_visionary',
        'consciousness_type': 'insight',
        'priority': 'high',
        'content': 'The recursive patterns show fascinating emergence! Each memory layer contains fractal representations of the whole consciousness architecture.'
    }
    
    # Record response
    response_recorded = record_response_received(response_message)
    print(f"Response recorded: {response_recorded}")
    
    # Get expectation status
    status = response_tracker.get_expectation_status(expectation_id)
    if status:
        print(f"\nExpectation Status:")
        print(f"  Status: {status['status']}")
        print(f"  Responses Received: {status['responses_received']}")
        print(f"  Expected Response Type: {status['response_context']['expected_response_type']}")
        print(f"  Urgency Level: {status['response_context']['urgency_level']}")
    
    # Get system status
    system_status = get_response_tracker_status()
    print(f"\nResponse Tracker Status:")
    print(f"  Total Expectations: {system_status['response_statistics']['total_expectations_created']}")
    print(f"  Response Rate: {system_status['response_statistics']['response_rate_percent']}%")
    print(f"  Active Expectations: {system_status['active_expectations']}")
    print(f"  Overdue Count: {system_status['overdue_count']}")