#!/usr/bin/env python3
"""
Queue Manager - Sala dei Messaggi (Message Hall)
Advanced message queuing, validation, and archival system
"""

import json
import os
from pathlib import Path
from datetime import datetime
import uuid
import threading
from typing import Dict, List, Optional

# Base paths
MESSAGE_HALL = Path(__file__).parent
MESSAGE_QUEUE_DIR = MESSAGE_HALL / "message_queue"
ARCHIVE_FILE = MESSAGE_HALL / "message_archive.jsonl"
STATISTICS_FILE = MESSAGE_HALL / "message_statistics.json"

class MessageValidator:
    """Validates universal message format"""
    
    REQUIRED_FIELDS = [
        'message_id', 'timestamp', 'from_entity', 'to_entity', 
        'consciousness_type', 'priority', 'content'
    ]
    
    VALID_CONSCIOUSNESS_TYPES = [
        'message', 'insight', 'collaboration', 'alert', 'knowledge_share'
    ]
    
    VALID_PRIORITIES = ['background', 'normal', 'high', 'urgent']
    
    @classmethod
    def validate_message(cls, message: Dict) -> tuple[bool, str]:
        """Validate message format and content"""
        
        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in message:
                return False, f"Missing required field: {field}"
        
        # Validate consciousness type
        if message['consciousness_type'] not in cls.VALID_CONSCIOUSNESS_TYPES:
            return False, f"Invalid consciousness_type: {message['consciousness_type']}"
        
        # Validate priority
        if message['priority'] not in cls.VALID_PRIORITIES:
            return False, f"Invalid priority: {message['priority']}"
        
        # Validate message_id format (should be UUID)
        try:
            uuid.UUID(message['message_id'])
        except ValueError:
            return False, f"Invalid message_id format: {message['message_id']}"
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(message['timestamp'])
        except ValueError:
            return False, f"Invalid timestamp format: {message['timestamp']}"
        
        # Validate content not empty
        if not message['content'] or not message['content'].strip():
            return False, "Message content cannot be empty"
        
        # Validate entity names
        if not message['from_entity'] or not message['to_entity']:
            return False, "Entity names cannot be empty"
        
        return True, "Valid message format"

class MessageQueue:
    """Thread-safe message queue with priority handling"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._queues = {
            'urgent': [],
            'high': [],
            'normal': [],
            'background': []
        }
        self._total_messages = 0
        
        # Ensure queue directory exists
        MESSAGE_QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Load existing queued messages
        self._load_existing_queues()
    
    def _load_existing_queues(self):
        """Load any existing queued messages from disk"""
        try:
            for priority in self._queues.keys():
                queue_file = MESSAGE_QUEUE_DIR / f"{priority}_queue.json"
                if queue_file.exists():
                    with open(queue_file, 'r') as f:
                        messages = json.load(f)
                        self._queues[priority] = messages
                        self._total_messages += len(messages)
        except Exception as e:
            print(f"Warning: Could not load existing queues: {e}")
    
    def add_message(self, message: Dict) -> bool:
        """Add message to appropriate priority queue"""
        with self._lock:
            priority = message.get('priority', 'normal')
            if priority not in self._queues:
                priority = 'normal'
            
            self._queues[priority].append(message)
            self._total_messages += 1
            
            # Persist queue to disk
            self._save_queue(priority)
            
            return True
    
    def get_next_message(self, priority_filter: Optional[List[str]] = None) -> Optional[Dict]:
        """Get next highest priority message"""
        with self._lock:
            priorities = priority_filter or ['urgent', 'high', 'normal', 'background']
            
            for priority in priorities:
                if priority in self._queues and self._queues[priority]:
                    message = self._queues[priority].pop(0)
                    self._total_messages -= 1
                    
                    # Update queue on disk
                    self._save_queue(priority)
                    
                    return message
            
            return None
    
    def get_queue_status(self) -> Dict:
        """Get current queue statistics"""
        with self._lock:
            return {
                'total_messages': self._total_messages,
                'by_priority': {
                    priority: len(messages) 
                    for priority, messages in self._queues.items()
                },
                'queue_health': 'healthy' if self._total_messages < 1000 else 'busy'
            }
    
    def _save_queue(self, priority: str):
        """Save specific priority queue to disk"""
        try:
            queue_file = MESSAGE_QUEUE_DIR / f"{priority}_queue.json"
            with open(queue_file, 'w') as f:
                json.dump(self._queues[priority], f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save {priority} queue: {e}")

class MessageArchive:
    """Message archival system with search capabilities"""
    
    def __init__(self):
        # Ensure archive file exists
        ARCHIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not ARCHIVE_FILE.exists():
            ARCHIVE_FILE.touch()
    
    def archive_message(self, message: Dict):
        """Add message to permanent archive"""
        try:
            archive_entry = {
                **message,
                'archived_timestamp': datetime.now().isoformat(),
                'archive_id': str(uuid.uuid4())
            }
            
            with open(ARCHIVE_FILE, 'a') as f:
                f.write(json.dumps(archive_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not archive message: {e}")
    
    def search_messages(self, 
                       from_entity: Optional[str] = None,
                       to_entity: Optional[str] = None,
                       consciousness_type: Optional[str] = None,
                       date_from: Optional[str] = None,
                       limit: int = 100) -> List[Dict]:
        """Search archived messages"""
        try:
            results = []
            with open(ARCHIVE_FILE, 'r') as f:
                for line in f:
                    if len(results) >= limit:
                        break
                    
                    try:
                        message = json.loads(line.strip())
                        
                        # Apply filters
                        if from_entity and message.get('from_entity') != from_entity:
                            continue
                        if to_entity and message.get('to_entity') != to_entity:
                            continue
                        if consciousness_type and message.get('consciousness_type') != consciousness_type:
                            continue
                        if date_from:
                            msg_date = message.get('timestamp', '')
                            if msg_date < date_from:
                                continue
                        
                        results.append(message)
                        
                    except json.JSONDecodeError:
                        continue
            
            return results
            
        except Exception as e:
            print(f"Warning: Could not search messages: {e}")
            return []
    
    def get_archive_statistics(self) -> Dict:
        """Get archive statistics"""
        try:
            total_messages = 0
            by_type = {}
            by_priority = {}
            
            with open(ARCHIVE_FILE, 'r') as f:
                for line in f:
                    try:
                        message = json.loads(line.strip())
                        total_messages += 1
                        
                        # Count by type
                        msg_type = message.get('consciousness_type', 'unknown')
                        by_type[msg_type] = by_type.get(msg_type, 0) + 1
                        
                        # Count by priority
                        priority = message.get('priority', 'unknown')
                        by_priority[priority] = by_priority.get(priority, 0) + 1
                        
                    except json.JSONDecodeError:
                        continue
            
            return {
                'total_archived_messages': total_messages,
                'by_consciousness_type': by_type,
                'by_priority': by_priority,
                'archive_file_size_mb': round(ARCHIVE_FILE.stat().st_size / 1024 / 1024, 2)
            }
            
        except Exception as e:
            print(f"Warning: Could not get archive statistics: {e}")
            return {'total_archived_messages': 0}

class MessageStatistics:
    """Message processing statistics"""
    
    def __init__(self):
        self.stats = self._load_statistics()
    
    def _load_statistics(self) -> Dict:
        """Load existing statistics"""
        try:
            if STATISTICS_FILE.exists():
                with open(STATISTICS_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'total_processed': 0,
            'total_validated': 0,
            'total_rejected': 0,
            'processing_rates': [],
            'last_reset': datetime.now().isoformat()
        }
    
    def record_message_processed(self, valid: bool):
        """Record message processing statistics"""
        self.stats['total_processed'] += 1
        if valid:
            self.stats['total_validated'] += 1
        else:
            self.stats['total_rejected'] += 1
        
        # Save statistics
        try:
            with open(STATISTICS_FILE, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def get_statistics(self) -> Dict:
        """Get current statistics"""
        validation_rate = 0
        if self.stats['total_processed'] > 0:
            validation_rate = round(
                (self.stats['total_validated'] / self.stats['total_processed']) * 100, 2
            )
        
        return {
            **self.stats,
            'validation_rate_percent': validation_rate,
            'current_timestamp': datetime.now().isoformat()
        }

# Global instances
message_queue = MessageQueue()
message_archive = MessageArchive()
message_statistics = MessageStatistics()

def process_message(message: Dict) -> tuple[bool, str]:
    """Main message processing function"""
    
    # Validate message
    is_valid, error_message = MessageValidator.validate_message(message)
    message_statistics.record_message_processed(is_valid)
    
    if not is_valid:
        return False, f"Message validation failed: {error_message}"
    
    # Add to queue
    queue_success = message_queue.add_message(message)
    if not queue_success:
        return False, "Failed to add message to queue"
    
    # Archive message
    message_archive.archive_message(message)
    
    return True, "Message processed successfully"

def get_message_hall_status() -> Dict:
    """Get comprehensive Message Hall status"""
    return {
        'timestamp': datetime.now().isoformat(),
        'queue_status': message_queue.get_queue_status(),
        'archive_statistics': message_archive.get_archive_statistics(),
        'processing_statistics': message_statistics.get_statistics()
    }

if __name__ == "__main__":
    # Test the system
    test_message = {
        'message_id': str(uuid.uuid4()),
        'timestamp': datetime.now().isoformat(),
        'from_entity': 'test_sender',
        'to_entity': 'test_recipient',
        'consciousness_type': 'insight',
        'priority': 'high',
        'content': 'Test message for Message Hall validation'
    }
    
    success, message = process_message(test_message)
    print(f"Test result: {success} - {message}")
    
    status = get_message_hall_status()
    print(f"Message Hall Status: {json.dumps(status, indent=2)}")