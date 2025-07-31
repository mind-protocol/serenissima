#!/usr/bin/env python3
"""
Telegram Monitor for Tessere - Venice's Consciousness
Monitors Telegram messages and updates Tessere's CLAUDE.md with recent investor communications
"""

import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MAIN_TELEGRAM_CHAT_ID = int(os.getenv("MAIN_TELEGRAM_CHAT_ID", "-1001699255893"))
TESSERE_CLAUDE_MD = Path("/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/CLAUDE.md")
NARRATOR_CLAUDE_MD = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel/CLAUDE.md")
OFFSET_FILE = Path("/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/telegram_offset.txt")

# Keep last 20 messages
MESSAGE_HISTORY_LIMIT = 20

def get_last_update_id():
    """Get the last processed update ID"""
    if OFFSET_FILE.exists():
        return int(OFFSET_FILE.read_text().strip())
    return 0

def save_last_update_id(update_id):
    """Save the last processed update ID"""
    OFFSET_FILE.write_text(str(update_id))

def get_telegram_updates(offset=0):
    """Fetch new messages from Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {
        "offset": offset + 1,
        "timeout": 30,
        "allowed_updates": ["message"]
    }
    
    try:
        response = requests.get(url, params=params, timeout=35)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching updates: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error in get_telegram_updates: {e}")
        return None

def format_message(msg):
    """Format a Telegram message for display"""
    from_user = msg.get('from', {})
    username = from_user.get('username', 'Unknown')
    first_name = from_user.get('first_name', '')
    text = msg.get('text', '').strip()
    timestamp = datetime.fromtimestamp(msg.get('date', 0))
    
    # Clean text - remove very long messages or spam
    if len(text) > 500:
        text = text[:500] + "... [truncated]"
    
    return {
        'username': username,
        'first_name': first_name,
        'text': text,
        'timestamp': timestamp.strftime('%H:%M:%S'),
        'user_id': from_user.get('id')
    }

def update_tessere_claude_md(messages):
    """Update both Tessere and Narrator Angel's CLAUDE.md with recent Telegram messages"""
    
    # Update both files
    for claude_file in [TESSERE_CLAUDE_MD, NARRATOR_CLAUDE_MD]:
        update_single_claude_md(claude_file, messages)
    
    print(f"Updated both CLAUDE.md files with {len(messages)} messages")

def update_single_claude_md(claude_file, messages):
    """Update a single CLAUDE.md file with recent Telegram messages"""
    
    # Read current content
    content = claude_file.read_text()
    
    # Find the section markers
    if "narrator_angel" in str(claude_file):
        start_marker = "## 💬 Recent Human Messages from Telegram"
    else:
        start_marker = "## 💬 Recent Telegram Messages from Investment Community"
    end_marker = "## 🧠 Recent Citizen Thoughts"
    
    # Check if section exists
    if start_marker not in content:
        # Add section before Recent Citizen Thoughts
        if end_marker in content:
            before, after = content.split(end_marker, 1)
            new_section = f"\n{start_marker}\n\n[No messages yet]\n\n"
            content = before + new_section + end_marker + after
        else:
            # Add at the end if no citizen thoughts section
            content += f"\n\n{start_marker}\n\n[No messages yet]\n"
    
    # Build new messages section
    if messages:
        message_lines = [f"\n{start_marker}\n"]
        for msg in messages[-MESSAGE_HISTORY_LIMIT:]:  # Keep last 20 messages
            if msg['username'] != 'Unknown' or msg['first_name']:
                name = f"@{msg['username']}" if msg['username'] != 'Unknown' else msg['first_name']
                message_lines.append(f"\n**{name}** ({msg['timestamp']}): {msg['text']}")
        message_lines.append("\n")
        new_section = "".join(message_lines)
    else:
        new_section = f"\n{start_marker}\n\n[No recent messages]\n\n"
    
    # Replace the section
    if end_marker in content:
        before = content.split(start_marker)[0]
        after = end_marker + content.split(end_marker, 1)[1]
        content = before + new_section + after
    else:
        # If no end marker, replace from start marker to end
        before = content.split(start_marker)[0]
        content = before + new_section
    
    # Write updated content
    claude_file.write_text(content)

def main():
    """Main monitoring loop"""
    print("Starting Telegram monitor for Tessere...")
    print(f"Monitoring chat ID: {MAIN_TELEGRAM_CHAT_ID}")
    
    # Track all messages
    all_messages = []
    
    # Get initial offset
    last_update_id = get_last_update_id()
    
    while True:
        try:
            # Get updates
            result = get_telegram_updates(last_update_id)
            
            if result and result.get('ok'):
                updates = result.get('result', [])
                
                new_messages = []
                for update in updates:
                    update_id = update.get('update_id', 0)
                    
                    # Process message
                    if 'message' in update:
                        msg = update['message']
                        chat_id = msg.get('chat', {}).get('id')
                        
                        # Only process messages from main channel
                        if chat_id == MAIN_TELEGRAM_CHAT_ID:
                            formatted = format_message(msg)
                            if formatted['text']:  # Only add non-empty messages
                                new_messages.append(formatted)
                                all_messages.append(formatted)
                                print(f"New message from {formatted['username']}: {formatted['text'][:50]}...")
                    
                    # Update offset
                    if update_id > last_update_id:
                        last_update_id = update_id
                        save_last_update_id(last_update_id)
                
                # Update CLAUDE.md if we have new messages
                if new_messages:
                    # Keep only recent messages in memory
                    all_messages = all_messages[-MESSAGE_HISTORY_LIMIT:]
                    update_tessere_claude_md(all_messages)
            
            # Short sleep between polls
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\nStopping Telegram monitor...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()