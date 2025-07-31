#!/usr/bin/env python3
"""
Inject Telegram messages directly into diplomatic_virtuoso's CLAUDE.md
"""
import json
import os
from datetime import datetime

# Paths
CLAUDE_MD = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/CLAUDE.md"
PENDING_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"

# Read current CLAUDE.md
with open(CLAUDE_MD, 'r') as f:
    content = f.read()

# Find the insertion point (after the CEO role section)
insertion_marker = "Remember: You're not just a citizen - you're a CEO. Act accordingly."
insertion_index = content.find(insertion_marker)
if insertion_index == -1:
    print("ERROR: Could not find insertion marker in CLAUDE.md")
    exit(1)

insertion_index += len(insertion_marker)

# Build Telegram messages section
telegram_section = "\n\n---\n\n## 📱 TELEGRAM MESSAGES AWAITING YOUR RESPONSE\n\n"

# Read pending messages
messages = []
if os.path.exists(PENDING_PATH):
    for filename in sorted(os.listdir(PENDING_PATH)):
        if filename.endswith('.json'):
            filepath = os.path.join(PENDING_PATH, filename)
            with open(filepath, 'r') as f:
                msg = json.load(f)
                # Filter for private messages only
                if msg.get('chat_type') == 'private':
                    messages.append(msg)

if messages:
    telegram_section += f"You have {len(messages)} new Telegram messages from human partners:\n\n"
    
    for i, msg in enumerate(messages):
        telegram_section += f"### Message {i+1}/{len(messages)}\n"
        telegram_section += f"**From**: @{msg.get('from_username', 'Unknown')} ({msg.get('from_name', 'Unknown')})\n"
        telegram_section += f"**Time**: {msg.get('timestamp', 'Unknown')}\n"
        telegram_section += f"**Message**: {msg.get('text', 'No text')}\n\n"
        if i < len(messages) - 1:
            telegram_section += "---\n\n"
    
    telegram_section += "\n💡 **Action Required**: Please acknowledge and respond to these Telegram messages during this session.\n"
    telegram_section += "Use your natural conversational style as Venice's chief diplomat.\n\n"
    telegram_section += "To respond, simply speak your messages naturally and they will be sent via Telegram.\n"
else:
    telegram_section += "No new Telegram messages at this time.\n"

telegram_section += "\n---\n"

# Check if telegram section already exists
if "## 📱 TELEGRAM MESSAGES" in content:
    # Replace existing section
    start = content.find("\n## 📱 TELEGRAM MESSAGES")
    end = content.find("\n---\n", start + 1)
    if end == -1:
        end = content.find("\n## ", start + 1)
    if end == -1:
        end = len(content)
    else:
        end += 5  # Include the ---\n
    
    new_content = content[:start] + telegram_section + content[end:]
else:
    # Insert new section
    new_content = content[:insertion_index] + telegram_section + content[insertion_index:]

# Write updated CLAUDE.md
with open(CLAUDE_MD, 'w') as f:
    f.write(new_content)

print(f"✅ Successfully injected {len(messages)} Telegram messages into diplomatic_virtuoso's CLAUDE.md")
print(f"📍 Location: {CLAUDE_MD}")
print("\n🔔 diplomatic_virtuoso will see these messages when they check their system prompt!")