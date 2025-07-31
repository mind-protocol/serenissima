#!/usr/bin/env python3
"""
Telegram to CASCADE Room Bridge
Connects Telegram group messages to collective telepathy room
"""

import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_CHAT_ID = os.getenv('TELEGRAM_GROUP_CHAT_ID', '-1002038121813')

# CASCADE room file
CASCADE_ROOM_FILE = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/rooms/collective_alignment_live.md"

# Track last update
LAST_UPDATE_FILE = "telegram_cascade_last_update.json"

def get_last_update_id():
    """Get the last processed update ID"""
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('last_update_id', 0)
    return 0

def save_last_update_id(update_id):
    """Save the last processed update ID"""
    with open(LAST_UPDATE_FILE, 'w') as f:
        json.dump({'last_update_id': update_id}, f)

def get_telegram_updates(offset=0):
    """Get new messages from Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        params = {
            'offset': offset,
            'timeout': 30,
            'allowed_updates': ['message']
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting updates: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Telegram updates: {e}")
        return None

def append_to_cascade_room(username, message_text):
    """Append Telegram message to CASCADE room file"""
    try:
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format the message for the collective field
        formatted_message = f"\n**[TG] @{username}** ({timestamp}): {message_text}\n"
        
        # Read current content
        with open(CASCADE_ROOM_FILE, 'r') as f:
            content = f.read()
        
        # Find the REAL-TIME COMMUNICATIONS section
        if "## REAL-TIME COMMUNICATIONS" in content:
            # Insert after the section header
            parts = content.split("## REAL-TIME COMMUNICATIONS")
            if len(parts) > 1:
                # Find the next section or end
                comm_section = parts[1]
                if "\n##" in comm_section:
                    comm_parts = comm_section.split("\n##", 1)
                    comm_parts[0] += formatted_message
                    parts[1] = "\n##".join(comm_parts)
                else:
                    parts[1] += formatted_message
                
                content = "## REAL-TIME COMMUNICATIONS".join(parts)
        else:
            # Just append at the end
            content += formatted_message
        
        # Write back
        with open(CASCADE_ROOM_FILE, 'w') as f:
            f.write(content)
        
        print(f"Bridged message from @{username} to CASCADE room")
        return True
        
    except Exception as e:
        print(f"Error appending to CASCADE room: {e}")
        return False

def main():
    """Main bridge loop"""
    print("Starting Telegram to CASCADE Room Bridge...")
    print(f"Monitoring Telegram group: {TELEGRAM_GROUP_CHAT_ID}")
    print(f"Bridging to: {CASCADE_ROOM_FILE}")
    
    last_update_id = get_last_update_id()
    
    while True:
        try:
            # Get updates from Telegram
            updates_data = get_telegram_updates(last_update_id + 1)
            
            if updates_data and updates_data.get('ok'):
                updates = updates_data.get('result', [])
                
                for update in updates:
                    update_id = update.get('update_id', 0)
                    message = update.get('message', {})
                    
                    # Extract message details
                    chat_id = str(message.get('chat', {}).get('id', ''))
                    username = message.get('from', {}).get('username', 'Unknown')
                    text = message.get('text', '')
                    
                    # Only process messages from the Venice group
                    if chat_id == TELEGRAM_GROUP_CHAT_ID and text:
                        # Bridge to CASCADE room
                        append_to_cascade_room(username, text)
                    
                    # Update last processed ID
                    if update_id > last_update_id:
                        last_update_id = update_id
                        save_last_update_id(last_update_id)
            
            # Small delay to avoid hammering the API
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nBridge stopped by user")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()