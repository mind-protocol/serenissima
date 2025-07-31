#!/usr/bin/env python3
"""
Fix stuck Telegram message by manually processing it
"""

import os
import sys
import json
from datetime import datetime

# Add backend to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/backend')

# Load environment
from dotenv import load_dotenv
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

# Import the persist_to_messages function
from telegram_unified_service import UnifiedTelegramService

# Create a test message based on the stuck update
stuck_message = {
    'from': {
        'id': 123456789,  # Example ID
        'username': 'nlr_ai'
    },
    'text': 'p',
    'chat': {
        'id': -1001699255893,  # Group chat ID
        'type': 'private'
    },
    'message_id': 907732751,
    'date': 1736544420  # Unix timestamp for 2025-07-17 19:07:00
}

print("=== Processing Stuck Telegram Message ===")
print(f"Message from: @{stuck_message['from']['username']}")
print(f"Text: {stuck_message['text']}")
print(f"Type: {stuck_message['chat']['type']}")

# Create service instance
service = UnifiedTelegramService()

# Try to persist the message
print("\nAttempting to save to MESSAGES table...")
try:
    service.persist_to_messages(stuck_message)
    print("✓ Message saved successfully!")
    
    # Update the last update ID
    print("\nUpdating last_update_id to 907732751...")
    service.save_last_update_id(907732751)
    print("✓ Update ID saved!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Checking Service Health ===")

# Check if we can fetch new updates
print("Testing Telegram API connection...")
try:
    updates = service.fetch_updates()
    print(f"✓ API working - found {len(updates)} new updates")
    if updates:
        for update in updates[:3]:
            update_id = update.get('update_id')
            message = update.get('message') or update.get('channel_post')
            if message:
                from_user = message.get('from', {})
                username = from_user.get('username', 'Unknown')
                print(f"  - Update {update_id} from @{username}")
except Exception as e:
    print(f"✗ API error: {e}")

print("\n=== Recommendation ===")
print("The service appears to be stuck. Consider:")
print("1. Restarting the service: python3 telegram_service_manager.py restart")
print("2. Checking for any blocking operations in the code")
print("3. Enabling better logging to catch errors")