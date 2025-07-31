#!/usr/bin/env python3
"""
Test script to debug why Telegram messages aren't being saved to Airtable
"""

import os
import json
from datetime import datetime
from pathlib import Path
import sys

# Add backend to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/backend')

# Load environment
from dotenv import load_dotenv
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

# Get environment variables
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

print("=== Telegram to Airtable Debug Test ===")
print(f"AIRTABLE_API_KEY exists: {bool(AIRTABLE_API_KEY)}")
print(f"AIRTABLE_BASE_ID exists: {bool(AIRTABLE_BASE_ID)}")

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    print("ERROR: Missing Airtable credentials!")
    sys.exit(1)

# Try to import and initialize Airtable
try:
    from pyairtable import Table
    messages_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "MESSAGES")
    print("\n✓ Successfully connected to Airtable MESSAGES table")
except Exception as e:
    print(f"\n✗ Failed to connect to Airtable: {e}")
    sys.exit(1)

# Test creating a message
test_message = {
    "MessageId": f"test_tg_{datetime.now().strftime('%Y%m%d%H%M%S')}",
    "Sender": "@test_telegram_user",
    "Receiver": "TG_Test_Channel",
    "Content": "This is a test message from the debug script",
    "Type": "telegram_bridge",
    "CreatedAt": datetime.now().isoformat(),
    "ReadAt": None,
    "Notes": json.dumps({
        "platform": "telegram",
        "telegram_username": "test_user",
        "test": True
    })
}

print("\nAttempting to create test message:")
print(json.dumps(test_message, indent=2))

try:
    result = messages_table.create(test_message)
    print(f"\n✓ SUCCESS! Message created with ID: {result.get('id')}")
    print(f"Full record: {json.dumps(result, indent=2)}")
    
    # Try to delete the test message
    try:
        messages_table.delete(result['id'])
        print("\n✓ Test message deleted successfully")
    except:
        print("\n! Could not delete test message (manual cleanup needed)")
        
except Exception as e:
    print(f"\n✗ FAILED to create message: {e}")
    print(f"Error type: {type(e).__name__}")

# Check if we can fetch existing messages
print("\n=== Checking existing Telegram messages ===")
try:
    # Search for telegram_bridge messages
    formula = "{Type} = 'telegram_bridge'"
    telegram_messages = messages_table.all(formula=formula, max_records=5)
    print(f"\nFound {len(telegram_messages)} telegram_bridge messages (showing max 5)")
    
    for msg in telegram_messages:
        fields = msg.get('fields', {})
        print(f"\n- MessageId: {fields.get('MessageId')}")
        print(f"  Sender: {fields.get('Sender')}")
        print(f"  Receiver: {fields.get('Receiver')}")
        print(f"  Created: {fields.get('CreatedAt')}")
        
except Exception as e:
    print(f"\n✗ Failed to fetch messages: {e}")

print("\n=== Test Complete ===")