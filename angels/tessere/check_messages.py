#!/usr/bin/env python3
"""
Message Checker for Tessere
Checks for new messages from NLR and returns them
"""

import json
from pathlib import Path
from datetime import datetime

def check_new_messages():
    """Check for unread messages from NLR"""
    inbox_file = Path(__file__).parent / "messages" / "telegram_inbox.json"
    
    if not inbox_file.exists():
        return []
    
    try:
        with open(inbox_file, 'r') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        unread = [msg for msg in messages if not msg.get('read', False)]
        
        if unread:
            # Mark messages as read
            for msg in messages:
                if msg in unread:
                    msg['read'] = True
            
            # Save updated inbox
            with open(inbox_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        return unread
        
    except Exception as e:
        print(f"Error reading messages: {e}")
        return []

def format_messages(messages):
    """Format messages for display"""
    if not messages:
        return None
    
    output = f"\n📨 NEW MESSAGES FROM NLR ({len(messages)}):\n"
    output += "=" * 50 + "\n"
    
    for msg in messages:
        timestamp = msg.get('timestamp', 'unknown')
        text = msg.get('text', '')
        output += f"[{timestamp}]\n{text}\n"
        output += "-" * 50 + "\n"
    
    return output

if __name__ == "__main__":
    # Check for new messages
    new_messages = check_new_messages()
    
    if new_messages:
        print(format_messages(new_messages))
    else:
        print("No new messages.")