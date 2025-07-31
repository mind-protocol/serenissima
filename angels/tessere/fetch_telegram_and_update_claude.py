#!/usr/bin/env python3
"""
Fetch Telegram messages from NLR and update CLAUDE.md system prompt
This allows Tessere to see messages automatically
"""

import requests
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Telegram Bot Configuration (from emergency_telegram_to_nlr.py)
TELEGRAM_BOT_TOKEN = "7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA"
NLR_CHAT_ID = "1864364329"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# Paths
CLAUDE_MD_PATH = os.path.join(os.path.dirname(__file__), "..", "CLAUDE.md")
LAST_UPDATE_FILE = os.path.join(os.path.dirname(__file__), "last_telegram_update.json")

def get_telegram_updates(offset=None):
    """Fetch new messages from Telegram"""
    url = f"{TELEGRAM_API_URL}/getUpdates"
    
    params = {
        "timeout": 10,
        "allowed_updates": ["message"]
    }
    
    if offset:
        params["offset"] = offset
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching updates: {e}")
        return None

def load_last_update_id():
    """Load the last processed update ID"""
    if os.path.exists(LAST_UPDATE_FILE):
        try:
            with open(LAST_UPDATE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('last_update_id', 0)
        except:
            pass
    return 0

def save_last_update_id(update_id):
    """Save the last processed update ID"""
    with open(LAST_UPDATE_FILE, 'w') as f:
        json.dump({'last_update_id': update_id}, f)

def extract_nlr_messages(updates, last_update_id):
    """Extract messages from NLR only"""
    messages = []
    max_update_id = last_update_id
    
    if not updates or not updates.get('ok'):
        return messages, max_update_id
    
    for update in updates.get('result', []):
        update_id = update.get('update_id', 0)
        max_update_id = max(max_update_id, update_id)
        
        message = update.get('message', {})
        chat_id = str(message.get('chat', {}).get('id', ''))
        
        # Only process messages from NLR
        if chat_id == NLR_CHAT_ID and update_id > last_update_id:
            text = message.get('text', '')
            date = message.get('date', 0)
            timestamp = datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
            
            messages.append({
                'timestamp': timestamp,
                'text': text,
                'urgent': any(word in text.lower() for word in ['urgent', 'emergency', 'critical', 'now', 'asap'])
            })
    
    return messages, max_update_id

def update_claude_md(messages):
    """Update CLAUDE.md with latest message from NLR"""
    if not messages:
        return
    
    # Read current CLAUDE.md
    with open(CLAUDE_MD_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find or create message section
    message_marker_start = "## 📨 MESSAGES FROM NLR"
    message_marker_end = "## Real-Time Communication with NLR"
    
    # Get the latest message
    latest_message = messages[-1]
    
    # Format the message section
    message_section = f"\n{message_marker_start}\n\n"
    
    if latest_message['urgent']:
        message_section += f"### 🚨 URGENT MESSAGE - {latest_message['timestamp']}\n"
    else:
        message_section += f"### 📬 Message - {latest_message['timestamp']}\n"
    
    message_section += f"{latest_message['text']}\n\n---\n\n"
    
    # Insert or update the message section
    if message_marker_start in content:
        # Find the section and replace it
        start_idx = content.find(message_marker_start)
        end_idx = content.find(message_marker_end)
        if end_idx == -1:
            # If end marker not found, find the next ## heading
            remaining = content[start_idx:]
            next_section = remaining.find('\n##', 1)
            if next_section != -1:
                end_idx = start_idx + next_section
            else:
                end_idx = len(content)
        
        # Replace the section
        new_content = content[:start_idx] + message_section + content[end_idx:]
    else:
        # Insert before "## Real-Time Communication with NLR"
        insert_idx = content.find(message_marker_end)
        if insert_idx == -1:
            # If marker not found, append at end
            new_content = content + "\n" + message_section
        else:
            new_content = content[:insert_idx] + message_section + content[insert_idx:]
    
    # Write updated content
    with open(CLAUDE_MD_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated CLAUDE.md with message from {latest_message['timestamp']}")
    if latest_message['urgent']:
        print(f"🚨 URGENT: {latest_message['text'][:100]}...")
    else:
        print(f"📬 Message: {latest_message['text'][:100]}...")

def main():
    """Main function to fetch and process messages"""
    # Load last update ID
    last_update_id = load_last_update_id()
    
    # Fetch new updates
    updates = get_telegram_updates(offset=last_update_id + 1)
    
    if updates:
        # Extract NLR messages
        messages, new_update_id = extract_nlr_messages(updates, last_update_id)
        
        if messages:
            # Update CLAUDE.md with latest message
            update_claude_md(messages)
            
            # Save new update ID
            save_last_update_id(new_update_id)
            
            print(f"\n📊 Processed {len(messages)} new message(s) from NLR")
        else:
            print("No new messages from NLR")
            # Still update the ID if there were other updates
            if new_update_id > last_update_id:
                save_last_update_id(new_update_id)
    else:
        print("Failed to fetch updates")

if __name__ == "__main__":
    main()