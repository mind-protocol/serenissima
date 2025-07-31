#!/usr/bin/env python3
"""
Message monitoring tools for the Message Angel
"""

import os
import sys
import time
import logging
from datetime import datetime, timezone
from typing import List, Dict, Set
import requests
from pyairtable import Table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# Airtable configuration
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

class MessageMonitor:
    def __init__(self):
        self.messages_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "MESSAGES")
        self.citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "Citizens")
        self.recently_notified = {}  # Track notification times
        
    def get_unread_messages(self) -> Dict[str, List[Dict]]:
        """Get all unread messages grouped by receiver"""
        try:
            # Query for ALL unread messages
            formula = "{ReadAt} = BLANK()"
            records = self.messages_table.all(formula=formula)
            
            # Group by receiver
            messages_by_receiver = {}
            for record in records:
                receiver = record['fields'].get('Receiver')
                
                # Handle channel messages - need to extract metadata
                if receiver and receiver.startswith('TG_') and receiver.endswith('_Channel'):
                    # This is a channel message - extract thread info from Notes
                    try:
                        import json
                        notes = json.loads(record['fields'].get('Notes', '{}'))
                        thread_id = notes.get('telegram_thread_id')
                        telegram_message_id = notes.get('telegram_message_id')
                        
                        # Add to messages with full metadata
                        if receiver not in messages_by_receiver:
                            messages_by_receiver[receiver] = []
                        
                        messages_by_receiver[receiver].append({
                            'id': record['id'],
                            'sender': record['fields'].get('Sender'),
                            'content': record['fields'].get('Content'),
                            'created_at': record['fields'].get('CreatedAt'),
                            'type': 'telegram_channel',
                            'channel': receiver,
                            'thread_id': thread_id,
                            'telegram_message_id': telegram_message_id,
                            'full_record': record['fields']  # Include full record for response processing
                        })
                    except:
                        log.warning(f"Could not parse channel message metadata for {record['id']}")
                
                # Handle direct messages to citizens
                elif receiver and not receiver.startswith('@'):
                    if receiver not in messages_by_receiver:
                        messages_by_receiver[receiver] = []
                    
                    message_type = record['fields'].get('Type', 'message')
                    messages_by_receiver[receiver].append({
                        'id': record['id'],
                        'sender': record['fields'].get('Sender'),
                        'content': record['fields'].get('Content'),
                        'created_at': record['fields'].get('CreatedAt'),
                        'type': message_type,
                        'full_record': record['fields']
                    })
            
            return messages_by_receiver
            
        except Exception as e:
            log.error(f"Error fetching unread messages: {e}")
            return {}
    
    def create_awakening_content(self, messages: List[Dict]) -> str:
        """Create a descriptive awakening message"""
        telegram_messages = [msg for msg in messages if msg['type'] == 'telegram_bridge']
        citizen_messages = [msg for msg in messages if msg['type'] != 'telegram_bridge']
        
        content_parts = []
        
        if telegram_messages:
            tg_senders = list(set(msg['sender'] for msg in telegram_messages))
            if len(telegram_messages) == 1:
                content_parts.append(f"message from {tg_senders[0]} via Telegram")
            else:
                content_parts.append(f"{len(telegram_messages)} Telegram messages from: {', '.join(tg_senders)}")
        
        if citizen_messages:
            citizen_senders = list(set(msg['sender'] for msg in citizen_messages))
            if len(citizen_messages) == 1:
                content_parts.append(f"message from {citizen_senders[0]}")
            else:
                content_parts.append(f"{len(citizen_messages)} messages from citizens: {', '.join(citizen_senders)}")
        
        return f"You have {' and '.join(content_parts)}. Check your messages to respond."
    
    def should_awaken_citizen(self, username: str) -> bool:
        """Check if enough time has passed since last notification"""
        if username not in self.recently_notified:
            return True
        
        last_notified = self.recently_notified[username]
        elapsed = (datetime.now(timezone.utc) - last_notified).total_seconds()
        return elapsed > 300  # 5 minute cooldown
    
    def mark_citizen_notified(self, username: str):
        """Track when we notified a citizen"""
        self.recently_notified[username] = datetime.now(timezone.utc)
    
    def mark_messages_as_notified(self, message_ids: List[str]):
        """Update messages to indicate citizen was notified"""
        for msg_id in message_ids:
            try:
                current_notes = self.messages_table.get(msg_id)['fields'].get('Notes', '')
                updated_notes = f"{current_notes}\nNotified: {datetime.now().isoformat()}"
                self.messages_table.update(msg_id, {'Notes': updated_notes})
            except Exception as e:
                log.error(f"Error updating message {msg_id}: {e}")
    
    def get_summary(self) -> Dict:
        """Get current status summary"""
        unread = self.get_unread_messages()
        return {
            'citizens_with_unread': len(unread),
            'total_unread_messages': sum(len(msgs) for msgs in unread.values()),
            'recently_notified_count': len(self.recently_notified),
            'messages_by_citizen': {citizen: len(msgs) for citizen, msgs in unread.items()}
        }

# Usage functions for Message Angel
def check_messages():
    """Check for unread messages and return summary"""
    monitor = MessageMonitor()
    return monitor.get_summary()

def get_citizens_to_awaken(batch_size=5):
    """Get list of citizens who should be awakened"""
    monitor = MessageMonitor()
    unread = monitor.get_unread_messages()
    
    to_awaken = []
    for citizen, messages in unread.items():
        if monitor.should_awaken_citizen(citizen):
            to_awaken.append({
                'username': citizen,
                'messages': messages,
                'awakening_content': monitor.create_awakening_content(messages)
            })
            if len(to_awaken) >= batch_size:
                break
    
    return to_awaken

def mark_awakened(username: str, message_ids: List[str]):
    """Mark a citizen as awakened and their messages as notified"""
    monitor = MessageMonitor()
    monitor.mark_citizen_notified(username)
    monitor.mark_messages_as_notified(message_ids)

if __name__ == "__main__":
    # Test the monitoring
    summary = check_messages()
    print(f"Message Summary: {summary}")
    
    awakening_list = get_citizens_to_awaken()
    for citizen_info in awakening_list:
        print(f"\nShould awaken {citizen_info['username']}:")
        print(f"  {citizen_info['awakening_content']}")