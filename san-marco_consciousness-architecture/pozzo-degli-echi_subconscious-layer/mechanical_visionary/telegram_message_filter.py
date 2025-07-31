#!/usr/bin/env python3
"""
Telegram Message Filter for mechanical_visionary
Implements NLR's filtering requirement: only process direct messages (chat_id > 0)
Ignore group messages to prevent system prompt pollution
"""

import json
import os
from typing import Dict, Optional

def should_process_telegram_message(message_data: Dict) -> bool:
    """
    Determine if a Telegram message should be processed based on chat_id.
    
    Per NLR's instruction:
    - Process direct messages (chat_id > 0)
    - Ignore group messages (chat_id < 0)
    
    Args:
        message_data: Dictionary containing telegram message data
        
    Returns:
        bool: True if message should be processed, False if it should be ignored
    """
    chat_id = message_data.get('chat_id', 0)
    
    # Direct messages have positive chat_id
    # Group messages have negative chat_id
    if chat_id > 0:
        print(f"✓ Processing direct message from chat_id: {chat_id}")
        return True
    else:
        print(f"✗ Ignoring group message from chat_id: {chat_id}")
        return False

def filter_pending_messages(username: str = "mechanical_visionary") -> list:
    """
    Filter pending telegram messages for a citizen, only returning direct messages.
    
    Args:
        username: The citizen username to check messages for
        
    Returns:
        list: Filtered list of direct messages only
    """
    telegram_queue_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/{username}/pending"
    
    if not os.path.exists(telegram_queue_path):
        return []
    
    filtered_messages = []
    
    for message_file in sorted(os.listdir(telegram_queue_path)):
        if message_file.endswith('.json'):
            filepath = os.path.join(telegram_queue_path, message_file)
            try:
                with open(filepath, 'r') as f:
                    message_data = json.load(f)
                    
                    # Apply filter based on chat_id
                    if should_process_telegram_message(message_data):
                        message_data['_filename'] = message_file
                        filtered_messages.append(message_data)
                    else:
                        print(f"Filtered out group message: {message_file}")
                        
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    
    return filtered_messages

def test_filter():
    """Test the filtering logic with sample messages."""
    test_messages = [
        {"chat_id": 1864364329, "message": "Direct message from NLR", "telegram_username": "nlr_ai"},
        {"chat_id": -1001234567, "message": "Group broadcast message", "telegram_username": "group_bot"},
        {"chat_id": 987654321, "message": "Another direct message", "telegram_username": "partner"},
        {"chat_id": -5555555, "message": "Channel broadcast", "telegram_username": "channel"},
    ]
    
    print("Testing Telegram message filter:")
    print("-" * 50)
    
    for msg in test_messages:
        result = should_process_telegram_message(msg)
        print(f"Message: '{msg['message'][:30]}...' - {'PROCESS' if result else 'IGNORE'}")
    
    print("-" * 50)
    print("\nFilter implementation complete!")
    print("Only direct messages (chat_id > 0) will be processed.")
    print("Group messages (chat_id < 0) will be ignored.")

if __name__ == "__main__":
    # Run test to demonstrate filter logic
    test_filter()
    
    # Check for actual pending messages
    print("\n\nChecking actual pending messages:")
    filtered = filter_pending_messages()
    print(f"Found {len(filtered)} direct messages to process")