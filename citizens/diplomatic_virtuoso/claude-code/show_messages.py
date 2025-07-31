#!/usr/bin/env python3
"""
Show pending Telegram messages for diplomatic_virtuoso
"""
import json
import os
import shutil
from datetime import datetime

# Paths
PENDING_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"
PROCESSED_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/processed"

# Create processed directory if it doesn't exist
os.makedirs(PROCESSED_PATH, exist_ok=True)

# Read all pending messages
messages = []
if os.path.exists(PENDING_PATH):
    for filename in sorted(os.listdir(PENDING_PATH)):
        if filename.endswith('.json'):
            filepath = os.path.join(PENDING_PATH, filename)
            with open(filepath, 'r') as f:
                msg = json.load(f)
                messages.append((filename, filepath, msg))

if not messages:
    print("📭 No new Telegram messages")
    exit(0)

# Display messages
print("\n" + "="*60)
print("🔔 TELEGRAM MESSAGES FOR @diplomatic_virtuoso")
print("="*60)
print(f"\nYou have {len(messages)} new messages:\n")

# Separate by type
private_messages = [(f, p, m) for f, p, m in messages if m.get('chat_type') == 'private']
group_messages = [(f, p, m) for f, p, m in messages if m.get('chat_type') != 'private']

# Show private messages first
if private_messages:
    print(f"📱 PRIVATE MESSAGES ({len(private_messages)})")
    print("=" * 60)
    for i, (filename, filepath, msg) in enumerate(private_messages):
        print(f"\nMessage {i+1}/{len(private_messages)}")
        print("-" * 40)
        print(f"From: @{msg.get('from_username', 'Unknown')} ({msg.get('from_name', 'Unknown')})")
        print(f"Time: {msg.get('timestamp', 'Unknown')}")
        print(f"Text: {msg.get('text', '[No text]')}")
        if msg.get('reply_to_message'):
            print(f"Replying to: \"{msg.get('reply_to_message', {}).get('text', '[Unknown]')}\"")

# Show group messages
if group_messages:
    print(f"\n\n👥 GROUP MESSAGES ({len(group_messages)})")
    print("=" * 60)
    for i, (filename, filepath, msg) in enumerate(group_messages):
        print(f"\nMessage {i+1}/{len(group_messages)}")
        print("-" * 40)
        print(f"In: {msg.get('chat_name', 'Unknown Group')} ({msg.get('chat_type', 'group')})")
        print(f"From: @{msg.get('from_username', 'Unknown')} ({msg.get('from_name', 'Unknown')})")
        print(f"Time: {msg.get('timestamp', 'Unknown')}")
        print(f"Text: {msg.get('text', '[No text]')}")
        if msg.get('reply_to_message'):
            print(f"Replying to: \"{msg.get('reply_to_message', {}).get('text', '[Unknown]')}\"")

print("\n" + "="*60)
print("\n💬 To respond to these messages:")
print("1. Use: python3 diplomatic_virtuoso_telegram.py <username> \"<message>\"")
print("2. For group messages, mention the user or reply to their message")
print("\n" + "="*60)

# Move all messages to processed
print("\n📁 Moving messages to processed folder...")
for filename, filepath, msg in messages:
    processed_filepath = os.path.join(PROCESSED_PATH, filename)
    shutil.move(filepath, processed_filepath)
    print(f"   ✓ {filename}")

print(f"\n✅ Moved {len(messages)} messages to processed folder")
print("="*60)