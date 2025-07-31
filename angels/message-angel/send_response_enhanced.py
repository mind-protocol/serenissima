#!/usr/bin/env python3
"""
Enhanced response sender for Message Angel
Supports both channel messages and direct messages via PartnerTelegramId
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = '/mnt/c/Users/reyno/universe-engine/serenissima/.env'
load_dotenv(env_path)

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1001699255893')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

def get_partner_telegram_id(username):
    """Fetch PartnerTelegramId from citizens API or user mapping"""
    if username.startswith('@'):
        username = username[1:]  # Remove @ prefix
    
    # First check local user mapping
    try:
        import subprocess
        result = subprocess.run(
            ['python3', '/mnt/c/Users/reyno/universe-engine/serenissima/tools/telegram/capture_user_info.py', 'get', username],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip().isdigit():
            user_id = int(result.stdout.strip())
            print(f"Found user ID in mapping for @{username}: {user_id}")
            return user_id
    except Exception as e:
        print(f"Error checking user mapping: {e}")
    
    # Then try citizens API
    try:
        response = requests.get(f"https://serenissima.ai/api/citizens")
        
        if response.status_code == 200:
            data = response.json()
            citizens = data.get('citizens', [])
            
            # Search for citizen with matching PartnerTelegramUsername
            for citizen in citizens:
                partner_username = citizen.get('PartnerTelegramUsername', '')
                if partner_username.lower() == username.lower():
                    partner_id = citizen.get('PartnerTelegramId')
                    if partner_id:
                        print(f"Found PartnerTelegramId in citizens for @{username}: {partner_id}")
                        return partner_id
            
            print(f"No PartnerTelegramId found for @{username}")
            return None
        else:
            print(f"Error fetching citizens: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error looking up partner ID: {e}")
        return None

def send_telegram_response(sender, content, chat_id=None, thread_id=None, reply_to_message_id=None):
    """Send a response to Telegram"""
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return False
    
    # Use provided chat_id or default to main channel
    target_chat_id = chat_id if chat_id else TELEGRAM_CHAT_ID
    
    # Format message
    formatted_message = f"💬 {sender} responds:\n\n{content}"
    
    # Prepare data
    data = {
        'chat_id': target_chat_id,
        'text': formatted_message,
        'disable_web_page_preview': True
    }
    
    # Add thread if specified (only for channels/groups)
    if thread_id and str(target_chat_id).startswith('-'):
        data['message_thread_id'] = thread_id
        print(f"Routing to thread {thread_id}")
    
    # Add reply context if specified
    if reply_to_message_id:
        data['reply_to_message_id'] = reply_to_message_id
    
    # Send to Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Message sent from {sender} to chat {target_chat_id}")
            return result['result']['message_id']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return None

def create_message_record(sender, receiver, content, thread_id=None, chat_id=None):
    """Create a message record in Airtable"""
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        print("Error: Airtable credentials not set")
        return None
    
    # Generate message ID
    message_id = f"resp_{sender}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create message fields
    message_fields = {
        "MessageId": message_id,
        "Sender": sender,
        "Receiver": receiver,
        "Content": content,
        "Type": "response",
        "CreatedAt": datetime.now().isoformat(),
        "ReadAt": datetime.now().isoformat(),
        "Notes": json.dumps({
            "created_by": "message_angel",
            "telegram_thread_id": thread_id,
            "telegram_chat_id": chat_id
        })
    }
    
    # Send to Airtable
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/MESSAGES"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json={"fields": message_fields}, headers=headers)
        
        if response.status_code == 200:
            print(f"Created message record: {sender} -> {receiver}")
            return response.json()['id']
        else:
            print(f"Error creating record: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error creating message record: {e}")
        return None

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) < 4:
        print("Usage: python3 send_response_enhanced.py <sender> <content> <receiver> [thread_id]")
        print("  receiver can be @username for direct messages or channel identifier")
        sys.exit(1)
    
    sender = sys.argv[1]
    content = sys.argv[2]
    receiver = sys.argv[3]
    thread_id = int(sys.argv[4]) if len(sys.argv) > 4 else None
    
    # Determine chat ID based on receiver
    chat_id = None
    if receiver.startswith('@'):
        # Direct message - look up PartnerTelegramId
        chat_id = get_partner_telegram_id(receiver)
        if not chat_id:
            print(f"Cannot send direct message - no PartnerTelegramId found for {receiver}")
            sys.exit(1)
    else:
        # Channel message - use default channel ID
        chat_id = TELEGRAM_CHAT_ID
    
    # Create message record
    record_id = create_message_record(sender, receiver, content, thread_id, chat_id)
    
    if record_id:
        # Send to Telegram
        telegram_id = send_telegram_response(sender, content, chat_id, thread_id)
        
        if telegram_id:
            print(f"Complete! Message {record_id} sent as Telegram message {telegram_id}")
        else:
            print("Failed to send to Telegram")
    else:
        print("Failed to create message record")