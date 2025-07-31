#!/usr/bin/env python3
"""
Telegram communication tools for the Message Angel
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import Dict, Optional
from pyairtable import Table

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1001699255893')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

class TelegramBridge:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.messages_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "MESSAGES")
        
    def send_to_telegram(self, sender: str, content: str, thread_id: int = None, 
                        reply_to_message_id: int = None) -> Dict:
        """Send a message to Telegram"""
        if not self.bot_token:
            return {"success": False, "error": "TELEGRAM_BOT_TOKEN not configured"}
        
        # Format message
        formatted_message = f"💬 **{sender}** responds:\n\n{content}"
        
        # Prepare data
        data = {
            'chat_id': self.chat_id,
            'text': formatted_message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        
        # Add thread routing if specified
        if thread_id:
            data['message_thread_id'] = thread_id
            
        # Add reply context if specified
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        
        # Send to Telegram
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        try:
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                log.info(f"Successfully sent message from {sender} to Telegram")
                return {
                    "success": True,
                    "telegram_message_id": result['result']['message_id']
                }
            else:
                log.error(f"Failed to send: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"Telegram API error: {response.status_code}"
                }
                
        except Exception as e:
            log.error(f"Error sending to Telegram: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_response_message(self, sender: str, receiver: str, content: str, 
                               original_message_id: str = None, thread_id: int = None) -> str:
        """Create a response message in MESSAGES table"""
        try:
            # Generate message ID
            message_id = f"resp_{sender}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Create message fields
            message_fields = {
                "MessageId": message_id,
                "Sender": sender,
                "Receiver": receiver,  # Will be @username or TG_Channel
                "Content": content,
                "Type": "response",
                "CreatedAt": datetime.now().isoformat(),
                "ReadAt": datetime.now().isoformat(),  # Mark as read since we're sending it
                "Notes": json.dumps({
                    "created_by": "message_angel",
                    "in_reply_to": original_message_id,
                    "telegram_thread_id": thread_id
                })
            }
            
            # Create in Airtable
            record = self.messages_table.create(message_fields)
            log.info(f"Created response message: {sender} -> {receiver}")
            
            return record['id']
            
        except Exception as e:
            log.error(f"Failed to create response message: {e}")
            return None
    
    def process_citizen_response(self, citizen_username: str, response_content: str, 
                                original_message: Dict) -> Dict:
        """Process a complete citizen response - create in MESSAGES and send to Telegram"""
        try:
            # Extract metadata from original message
            notes = json.loads(original_message.get('Notes', '{}'))
            thread_id = notes.get('telegram_thread_id')
            telegram_message_id = notes.get('telegram_message_id')
            original_sender = original_message.get('Sender', '@unknown')
            
            # Create response in MESSAGES
            message_record_id = self.create_response_message(
                sender=citizen_username,
                receiver=original_sender,
                content=response_content,
                original_message_id=original_message.get('MessageId'),
                thread_id=thread_id
            )
            
            if not message_record_id:
                return {"success": False, "error": "Failed to create message record"}
            
            # Send to Telegram
            telegram_result = self.send_to_telegram(
                sender=citizen_username,
                content=response_content,
                thread_id=thread_id,
                reply_to_message_id=telegram_message_id
            )
            
            # Update message record with Telegram result
            if telegram_result['success']:
                self.messages_table.update(message_record_id, {
                    'Notes': json.dumps({
                        "created_by": "message_angel",
                        "in_reply_to": original_message.get('MessageId'),
                        "telegram_thread_id": thread_id,
                        "telegram_sent": True,
                        "telegram_response_id": telegram_result.get('telegram_message_id')
                    })
                })
            
            return {
                "success": True,
                "message_record_id": message_record_id,
                "telegram_sent": telegram_result['success']
            }
            
        except Exception as e:
            log.error(f"Error processing citizen response: {e}")
            return {"success": False, "error": str(e)}

# Convenience functions for Message Angel
bridge = TelegramBridge()

def send_citizen_response(citizen_username: str, response_content: str, original_message: Dict) -> Dict:
    """Send a citizen's response to Telegram"""
    return bridge.process_citizen_response(citizen_username, response_content, original_message)

def send_direct_to_telegram(sender: str, content: str, thread_id: int = None) -> Dict:
    """Send a message directly to Telegram without creating MESSAGES record"""
    return bridge.send_to_telegram(sender, content, thread_id)