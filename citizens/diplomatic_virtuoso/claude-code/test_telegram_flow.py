#!/usr/bin/env python3
"""
Test the complete Telegram flow for diplomatic_virtuoso
Creates test messages in the queue to verify hooks are working
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Queue paths
QUEUE_BASE = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue')
PENDING_DIR = QUEUE_BASE / 'diplomatic_virtuoso' / 'pending'
PROCESSED_DIR = QUEUE_BASE / 'diplomatic_virtuoso' / 'processed'

def create_test_message(sender_username, text, message_index=1):
    """Create a test message in the pending queue"""
    
    # Ensure directories exist
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create message data
    timestamp = datetime.now()
    message_data = {
        'message_id': 1000 + message_index,
        'timestamp': timestamp.isoformat(),
        'text': text,
        'from_id': 123456789 + message_index,
        'from_username': sender_username,
        'from_name': f'Test User {sender_username}',
        'chat_id': -1001234567890 if message_index > 2 else 123456789 + message_index,
        'chat_type': 'group' if message_index > 2 else 'private',
        'is_reply': False,
        'test_message': True
    }
    
    # Save to pending queue
    filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{message_data['from_id']}.json"
    filepath = PENDING_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(message_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Created test message from @{sender_username}")
    print(f"   Location: {filepath}")
    return filepath

def main():
    """Create several test messages"""
    print("🧪 Creating test Telegram messages for diplomatic_virtuoso")
    print(f"📁 Queue directory: {PENDING_DIR}\n")
    
    # Create test messages
    messages = [
        ("JohnJeffries", "Hey diplomatic_virtuoso! Ready for the CEO competition? We need to discuss strategy."),
        ("D_roott", "Hi! I saw your message about Venice consciousness. Can we collaborate?"),
        ("NLR", "Great work on the Telegram integration! The hooks look perfect."),
        ("VeniceInvestor", "[Group message] @diplomatic_virtuoso what's the latest on CASCADE development?"),
    ]
    
    created_files = []
    for i, (sender, text) in enumerate(messages, 1):
        filepath = create_test_message(sender, text, i)
        created_files.append(filepath)
    
    print(f"\n📊 Created {len(created_files)} test messages")
    print("\n🎯 Next steps:")
    print("1. Start Claude Code in diplomatic_virtuoso's directory")
    print("2. The hooks should detect and display these messages")
    print("3. Messages will appear in the console and context")
    
    # Show how to clean up
    print("\n🧹 To clean up test messages later:")
    print(f"   rm {PENDING_DIR}/*.json")

if __name__ == '__main__':
    main()