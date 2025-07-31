#!/usr/bin/env python3
"""
Monitor Telegram messages and check if they're being saved to Airtable
"""

import os
import sys
import json
import time
import requests
from datetime import datetime

# Add backend to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/backend')

# Load environment
from dotenv import load_dotenv
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

print("=== Telegram Message Monitor ===")
print(f"Bot token exists: {bool(TELEGRAM_BOT_TOKEN)}")
print(f"Airtable credentials exist: {bool(AIRTABLE_API_KEY and AIRTABLE_BASE_ID)}")

# Check last update ID from file
update_file = '/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_unified_last_update.json'
if os.path.exists(update_file):
    with open(update_file, 'r') as f:
        data = json.load(f)
        last_update_id = data.get('last_update_id', 0)
        print(f"\nLast processed update ID: {last_update_id}")

# Get recent updates from Telegram
print("\n=== Checking Recent Telegram Updates ===")
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
params = {
    'offset': last_update_id - 10,  # Get last 10 updates
    'timeout': 0
}

try:
    response = requests.get(url, params=params, timeout=10)
    if response.status_code == 200:
        data = response.json()
        updates = data.get('result', [])
        print(f"Found {len(updates)} recent updates")
        
        # Show recent messages
        for update in updates[-5:]:  # Last 5 updates
            update_id = update.get('update_id')
            message = update.get('message') or update.get('channel_post')
            if message:
                from_user = message.get('from', {})
                username = from_user.get('username', 'Unknown')
                text = message.get('text', '')[:100]
                chat_type = message.get('chat', {}).get('type')
                timestamp = datetime.fromtimestamp(message.get('date', 0))
                
                print(f"\nUpdate {update_id}:")
                print(f"  Time: {timestamp}")
                print(f"  From: @{username}")
                print(f"  Chat type: {chat_type}")
                print(f"  Text: {text}")
                print(f"  Processed: {'Yes' if update_id <= last_update_id else 'NO - SHOULD BE SAVED!'}")
                
    else:
        print(f"Telegram API error: {response.status_code}")
        
except Exception as e:
    print(f"Error fetching updates: {e}")

# Check Airtable for recent messages
print("\n=== Recent Messages in Airtable ===")
try:
    from pyairtable import Table
    messages_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "MESSAGES")
    
    # Get telegram messages from last 24 hours
    formula = "{Type} = 'telegram_bridge'"
    recent_messages = messages_table.all(formula=formula, sort=['-CreatedAt'], max_records=10)
    
    print(f"\nFound {len(recent_messages)} recent telegram_bridge messages:")
    for msg in recent_messages[:5]:
        fields = msg.get('fields', {})
        created = fields.get('CreatedAt', '')
        if created:
            # Parse the timestamp
            try:
                dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                hours_ago = (datetime.now(dt.tzinfo) - dt).total_seconds() / 3600
                print(f"\n- {fields.get('MessageId')}")
                print(f"  From: {fields.get('Sender')}")
                print(f"  Created: {created} ({hours_ago:.1f} hours ago)")
            except:
                print(f"\n- {fields.get('MessageId')} (time parse error)")
                
except Exception as e:
    print(f"Error checking Airtable: {e}")

print("\n=== Analysis ===")
print("If you see unprocessed updates above, the service may be:")
print("1. Not polling frequently enough")
print("2. Encountering errors when saving to Airtable")
print("3. Missing proper error logging")
print("\nCheck the service logs or restart it with proper logging enabled.")