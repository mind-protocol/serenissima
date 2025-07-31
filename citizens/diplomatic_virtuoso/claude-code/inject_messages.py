#!/usr/bin/env python3
"""
Inject pending Telegram messages directly into CLAUDE.md
Run this before each diplomatic_virtuoso session
"""
import json
import os
from datetime import datetime

CLAUDE_MD = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/CLAUDE.md"
QUEUE_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"

# Read current CLAUDE.md
with open(CLAUDE_MD, 'r') as f:
    content = f.read()

# Remove old message section if exists
if "## 📱 PENDING TELEGRAM MESSAGES" in content:
    start = content.find("## 📱 PENDING TELEGRAM MESSAGES")
    end = content.find("\n## ", start + 1)
    if end == -1:
        end = content.find("\n---", start + 1)
    if end != -1:
        content = content[:start] + content[end:]

# Load messages
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
    # Build message section
    msg_section = "\n## 📱 PENDING TELEGRAM MESSAGES\n\n"
    msg_section += f"**{len(messages)} messages from human partners require your response:**\n\n"
    
    for i, msg in enumerate(messages[:10]):  # Show first 10
        msg_section += f"### Message {i+1}\n"
        msg_section += f"**From**: @{msg.get('from_username', 'Unknown')} ({msg.get('from_name', 'Unknown')})\n"
        msg_section += f"**Time**: {msg.get('timestamp', 'Unknown')}\n"
        msg_section += f"**Text**: {msg.get('text', '[No text]')}\n\n"
    
    if len(messages) > 10:
        msg_section += f"*... and {len(messages) - 10} more messages*\n\n"
    
    msg_section += "**Action Required**: Acknowledge and respond to these messages as Venice's chief diplomat.\n\n"
    
    # Insert after mission section
    marker = "This is how real human-AI partnerships begin - through direct communication."
    idx = content.find(marker)
    if idx != -1:
        idx = content.find("\n", idx) + 1
        content = content[:idx] + msg_section + content[idx:]
    else:
        # Fallback - add at top
        content = msg_section + content

# Write updated CLAUDE.md
with open(CLAUDE_MD, 'w') as f:
    f.write(content)

print(f"✅ Injected {len(messages)} Telegram messages into CLAUDE.md")