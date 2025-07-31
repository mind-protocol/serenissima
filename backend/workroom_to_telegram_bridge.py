#!/usr/bin/env python3
"""
Workroom to Telegram Bridge - Sends citizen thoughts back to TG group
"""

import os
import json
import time
import glob
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from pyairtable import Table

# Load environment
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_CHAT_ID = os.getenv('TELEGRAM_GROUP_CHAT_ID', '-1002038121813')
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Initialize citizens table
citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")

def send_to_telegram(message):
    """Send a message to Telegram group"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Truncate if too long
    if len(message) > 4000:
        message = message[:3997] + "..."
    
    data = {
        'chat_id': TELEGRAM_GROUP_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return False

def get_citizens_in_room(room_name):
    """Get all citizens assigned to a specific room"""
    try:
        records = citizens_table.all(formula=f"{{Room}} = '{room_name}'")
        return [r['fields']['Username'] for r in records if 'Username' in r['fields']]
    except Exception as e:
        print(f"Error fetching citizens: {e}")
        return []

def monitor_workroom_to_telegram(room_path, room_name="alignment"):
    """Monitor workroom for citizen contributions and send to Telegram"""
    print(f"📡 Workroom → Telegram Bridge Active")
    print(f"📂 Monitoring: {room_path}")
    print(f"💬 Sending to: {TELEGRAM_GROUP_CHAT_ID}")
    print("=" * 50)
    
    # Track last modification times
    last_check = {}
    
    # Initial scan to avoid sending old files
    for file_path in glob.glob(os.path.join(room_path, "*")):
        if os.path.isfile(file_path):
            last_check[file_path] = os.path.getmtime(file_path)
    
    # Track which citizens are in the room
    active_citizens = set()
    
    while True:
        try:
            # Update active citizens list
            current_citizens = set(get_citizens_in_room(room_name))
            
            # Announce new arrivals
            new_citizens = current_citizens - active_citizens
            if new_citizens:
                arrival_msg = f"🚪 *Citizens entering {room_name} room:*\n"
                for citizen in new_citizens:
                    arrival_msg += f"• {citizen}\n"
                send_to_telegram(arrival_msg)
            
            active_citizens = current_citizens
            
            # Check for new or modified files
            for file_path in glob.glob(os.path.join(room_path, "*")):
                if not os.path.isfile(file_path):
                    continue
                    
                filename = os.path.basename(file_path)
                
                # Skip certain files
                if filename in ['.DS_Store', 'Thumbs.db', '*.pyc', 'monitor.log']:
                    continue
                
                mtime = os.path.getmtime(file_path)
                
                # If file is new or modified
                if file_path not in last_check or mtime > last_check[file_path]:
                    # Skip on first run
                    if file_path in last_check:
                        # Read the file
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # Determine who likely wrote it based on content or filename
                            author = "Unknown"
                            if "_" in filename:
                                # Try to extract author from filename pattern
                                parts = filename.split("_")
                                if parts[0] in active_citizens:
                                    author = parts[0]
                            
                            # Format message for Telegram
                            if len(content) > 800:
                                preview = content[:800] + "..."
                            else:
                                preview = content
                            
                            telegram_msg = f"📝 *New in {room_name} workroom*\n\n"
                            telegram_msg += f"*File:* `{filename}`\n"
                            if author != "Unknown":
                                telegram_msg += f"*From:* {author}\n"
                            telegram_msg += f"\n{preview}"
                            
                            # Send to Telegram
                            if send_to_telegram(telegram_msg):
                                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent {filename} to Telegram")
                            
                        except Exception as e:
                            print(f"Error reading {filename}: {e}")
                    
                    last_check[file_path] = mtime
            
            # Also monitor for direct citizen outputs (if we can detect them)
            # This would require citizens to output in a specific format
            
            time.sleep(3)  # Check every 3 seconds
            
        except KeyboardInterrupt:
            print("\n\n👋 Bridge stopped")
            break
        except Exception as e:
            print(f"Bridge error: {e}")
            time.sleep(5)

def monitor_citizen_thoughts(room_name="alignment"):
    """Advanced monitor that tracks citizen console outputs"""
    print(f"🧠 Citizen Thought Monitor Active")
    print(f"📍 Room: {room_name}")
    print("=" * 50)
    
    # This would require citizens to output thoughts in a specific format
    # For example, citizens could write to a shared thoughts file
    
    thoughts_file = f"/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/{room_name}/collective_thoughts.md"
    last_size = 0
    
    while True:
        try:
            if os.path.exists(thoughts_file):
                current_size = os.path.getsize(thoughts_file)
                
                if current_size > last_size:
                    # Read new content
                    with open(thoughts_file, 'r') as f:
                        f.seek(last_size)
                        new_content = f.read()
                    
                    if new_content.strip():
                        # Parse and send to Telegram
                        lines = new_content.strip().split('\n')
                        for line in lines:
                            if line.strip():
                                # Format: "[timestamp] citizen: thought"
                                telegram_msg = f"💭 {line}"
                                send_to_telegram(telegram_msg)
                    
                    last_size = current_size
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Monitor error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "thoughts":
            # Monitor collective thoughts file
            room = sys.argv[2] if len(sys.argv) > 2 else "alignment"
            monitor_citizen_thoughts(room)
        else:
            # Monitor workroom files
            room_name = sys.argv[1]
            room_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/{room_name}"
            monitor_workroom_to_telegram(room_path, room_name)
    else:
        # Default: monitor alignment room
        room_path = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/alignment"
        monitor_workroom_to_telegram(room_path, "alignment")