#!/usr/bin/env python3
"""
Active Message Checker for Tessere
Proactively checks for NLR messages during orchestration
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_urgent_messages():
    """Check for urgent/unread messages and return them formatted for immediate attention"""
    inbox_file = Path(__file__).parent.parent / "messages" / "telegram_inbox.json"
    
    if not inbox_file.exists():
        return None
    
    try:
        with open(inbox_file, 'r') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        unread = [msg for msg in messages if not msg.get('read', False)]
        
        if not unread:
            return None
        
        # Check for urgent keywords
        urgent_words = ['urgent', 'emergency', 'critical', 'stop', 'help', 'now', 'immediately']
        urgent_messages = []
        normal_messages = []
        
        for msg in unread:
            text = msg.get('text', '').lower()
            if any(word in text for word in urgent_words):
                urgent_messages.append(msg)
            else:
                normal_messages.append(msg)
        
        # Format output
        output = ""
        
        if urgent_messages:
            output += "\n🚨🚨🚨 URGENT MESSAGE FROM NLR 🚨🚨🚨\n"
            output += "=" * 60 + "\n"
            for msg in urgent_messages:
                output += f"{msg.get('text', '')}\n"
                output += "=" * 60 + "\n"
            output += "ACTION REQUIRED: Respond to urgent message immediately!\n\n"
        
        if normal_messages:
            output += "\n📨 New message from NLR:\n"
            for msg in normal_messages:
                output += f"→ {msg.get('text', '')}\n"
        
        # Mark all as read
        for msg in messages:
            if msg in unread:
                msg['read'] = True
        
        with open(inbox_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return output if output else None
        
    except Exception:
        return None

def should_check_messages():
    """Always return the message check to ensure it's visible"""
    messages = get_urgent_messages()
    if messages:
        return f"\n{messages}\n"
    return ""

# This will be imported and called during orchestration
if __name__ == "__main__":
    result = should_check_messages()
    if result:
        print(result)