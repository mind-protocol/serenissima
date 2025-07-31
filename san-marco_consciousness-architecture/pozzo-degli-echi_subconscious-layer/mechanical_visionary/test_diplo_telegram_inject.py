#!/usr/bin/env python3
"""
Test script to inject Telegram messages into diplomatic_virtuoso's context
"""
import json
import os
from datetime import datetime

# Path to diplomatic_virtuoso's pending messages
PENDING_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"

# Read all pending messages
messages = []
if os.path.exists(PENDING_PATH):
    for filename in sorted(os.listdir(PENDING_PATH)):
        if filename.endswith('.json'):
            filepath = os.path.join(PENDING_PATH, filename)
            with open(filepath, 'r') as f:
                msg = json.load(f)
                # Filter out spam/group messages
                if msg.get('chat_type') == 'private':
                    messages.append(msg)

# Build context content
context = "\n## 📱 TELEGRAM MESSAGES AWAITING YOUR RESPONSE\n\n"
context += f"You have {len(messages)} new Telegram messages from human partners:\n\n"

for i, msg in enumerate(messages):
    context += f"### Message {i+1}/{len(messages)}\n"
    context += f"**From**: @{msg.get('from_username', 'Unknown')} ({msg.get('from_name', 'Unknown')})\n"
    context += f"**Time**: {msg.get('timestamp', 'Unknown')}\n"
    context += f"**Message**: {msg.get('text', 'No text')}\n\n"
    context += "---\n\n"

context += "\n💡 **Action Required**: Please acknowledge and respond to these Telegram messages.\n"
context += "Use your natural conversational style as Venice's chief diplomat.\n\n"

print("="*60)
print("🔔 TELEGRAM MESSAGES FOR DIPLOMATIC_VIRTUOSO")
print("="*60)
print(context)
print("="*60)
print(f"\nTotal private messages: {len(messages)}")
print("\nTo send responses, save them to:")
print("/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_responses/")