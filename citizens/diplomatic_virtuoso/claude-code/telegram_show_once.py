#!/usr/bin/env python3
"""
Show Telegram messages ONCE at session start
"""
import json
import os
import sys
from datetime import datetime

# Check if we've already shown messages this session
SESSION_FILE = f"/tmp/telegram_shown_{os.getppid()}"
if os.path.exists(SESSION_FILE):
    sys.exit(0)

# Mark that we've shown messages
open(SESSION_FILE, 'w').close()

# Load and display messages
QUEUE_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"
messages = []

if os.path.exists(QUEUE_PATH):
    for filename in sorted(os.listdir(QUEUE_PATH)):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(QUEUE_PATH, filename), 'r') as f:
                    msg = json.load(f)
                    if msg.get('chat_type') == 'private':
                        messages.append(msg)
            except:
                pass

if messages:
    output = f"\n📱 TELEGRAM MESSAGES ({len(messages)} waiting):\n"
    output += "="*60 + "\n\n"
    
    for i, msg in enumerate(messages[:5]):  # Show first 5 messages
        output += f"Message {i+1}:\n"
        output += f"From: @{msg.get('from_username', 'Unknown')} ({msg.get('from_name', 'Unknown')})\n"
        output += f"Time: {msg.get('timestamp', 'Unknown')}\n"
        output += f"Text: {msg.get('text', '[No text]')}\n"
        output += "-"*40 + "\n\n"
    
    if len(messages) > 5:
        output += f"... and {len(messages) - 5} more messages\n\n"
    
    output += "To respond, acknowledge these messages and I'll help you craft appropriate replies.\n"
    output += "="*60
    
    # Use exit code 2 to show to Claude
    print(output, file=sys.stderr)
    sys.exit(2)

# No messages
sys.exit(0)