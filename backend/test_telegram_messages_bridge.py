#!/usr/bin/env python3
"""
Test the Telegram-MESSAGES bridge
"""

import requests
import json
from datetime import datetime

# Test creating a message via API (simulating Telegram message)
def test_telegram_to_messages():
    """Test persisting a Telegram message to MESSAGES table"""
    
    # Simulate a Telegram message
    message_data = {
        "From": "@nlr_ai",
        "To": ["Italia", "DragonSlayer"],
        "Content": "Test message from Telegram bridge. How is CASCADE progressing?",
        "Platform": "telegram",
        "TelegramUsername": "nlr_ai",
        "TelegramChatId": -1001699255893,
        "TelegramThreadId": 292051,  # Company Investors thread
        "Status": "unread"
    }
    
    # Send to API
    response = requests.post(
        "http://localhost:10000/api/messages",
        json=message_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Message ID: {result.get('message_id')}")
        print(f"Created at: {result.get('created_at')}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

# Test retrieving messages
def test_get_messages():
    """Test retrieving messages for a citizen"""
    
    # Get messages for Italia
    response = requests.get(
        "http://localhost:10000/api/messages",
        params={
            "citizen": "Italia",
            "status": "unread",
            "platform": "telegram"
        }
    )
    
    print(f"\nGetting messages for Italia...")
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Found {result['total']} messages")
        for msg in result['messages']:
            print(f"\n- From: {msg['from']}")
            print(f"  Content: {msg['content'][:50]}...")
            print(f"  Thread ID: {msg.get('telegram_thread_id', 'N/A')}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("=== Testing Telegram-MESSAGES Bridge ===\n")
    
    # Test 1: Create message
    if test_telegram_to_messages():
        print("\n✓ Message creation successful")
        
        # Test 2: Retrieve messages
        test_get_messages()
    else:
        print("\n✗ Message creation failed")