#!/usr/bin/env python3
"""
Workroom Monitor v3 - Monitors file changes and injects to citizens and angels
"""

import os
import json
import time
import glob
from datetime import datetime
from pathlib import Path
import sys

# Add Venice path for imports
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima')
from dotenv import load_dotenv
from pyairtable import Table

# Load environment
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Initialize citizens table
citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")

def get_citizens_in_room(room_name):
    """Get all citizens assigned to a specific room"""
    try:
        records = citizens_table.all(formula=f"{{Room}} = '{room_name}'")
        return [r['fields']['Username'] for r in records if 'Username' in r['fields']]
    except Exception as e:
        print(f"❌ Error fetching citizens in room {room_name}: {e}")
        return []

def get_latest_jsonl_file(project_path):
    """Find the most recent .jsonl file in a project directory"""
    jsonl_files = glob.glob(os.path.join(project_path, "*.jsonl"))
    if not jsonl_files:
        return None
    return max(jsonl_files, key=os.path.getmtime)

def inject_message_to_citizen(username, room_name, message):
    """Inject a message into a citizen's Claude project .jsonl file"""
    project_path = Path(f"/home/ubuntu/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}")
    
    if not project_path.exists():
        project_path = Path(os.path.expanduser(f"~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}"))
    
    if not project_path.exists():
        print(f"⚠️ Project path not found for {username}")
        return False
    
    latest_file = get_latest_jsonl_file(str(project_path))
    if not latest_file:
        print(f"⚠️ No .jsonl file found for {username}")
        return False
    
    # Create the injection entry
    injection = {
        "type": "text",
        "text": f"\n\n📬 **WORKROOM UPDATE [{room_name}]** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}\n\n",
        "ts": datetime.now().isoformat(),
        "source": "workroom_monitor"
    }
    
    try:
        with open(latest_file, 'a') as f:
            f.write(json.dumps(injection) + '\n')
        return True
    except Exception as e:
        print(f"❌ Error injecting to {username}: {e}")
        return False

def inject_to_angels(room_name, message):
    """Inject workroom updates to Tessere and Story Angel"""
    results = []
    
    # Angel project paths
    angels = {
        "Tessere": "~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima",
        "Story Angel": "~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens"
    }
    
    for angel_name, project_path in angels.items():
        path = Path(os.path.expanduser(project_path))
        if path.exists():
            latest_file = get_latest_jsonl_file(str(path))
            if latest_file:
                injection = {
                    "type": "text", 
                    "text": f"\n\n📬 **WORKROOM UPDATE [{room_name}]** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}\n\n",
                    "ts": datetime.now().isoformat(),
                    "source": "workroom_monitor"
                }
                try:
                    with open(latest_file, 'a') as f:
                        f.write(json.dumps(injection) + '\n')
                    results.append(angel_name)
                except Exception as e:
                    print(f"❌ Error injecting to {angel_name}: {e}")
    
    return results

def monitor_workroom(room_path):
    """Monitor a workroom for changes and distribute updates"""
    room_name = os.path.basename(room_path)
    print(f"🏛️ Workroom Monitor v3 Active")
    print(f"📍 Room: {room_name}")
    print(f"📂 Path: {room_path}")
    print("=" * 50)
    
    # Track file modifications
    last_check = {}
    
    while True:
        try:
            # Get current citizens in room
            citizens = get_citizens_in_room(room_name)
            if citizens:
                print(f"👥 {len(citizens)} citizens in {room_name}: {', '.join(citizens[:5])}...")
            
            # Check all files in room
            for file_path in glob.glob(os.path.join(room_path, "*")):
                if os.path.isfile(file_path) and not file_path.endswith('.pyc'):
                    mtime = os.path.getmtime(file_path)
                    
                    # If file is new or modified
                    if file_path not in last_check or mtime > last_check[file_path]:
                        # Skip on first run to avoid spam
                        if file_path in last_check:
                            filename = os.path.basename(file_path)
                            
                            # Read file content
                            try:
                                with open(file_path, 'r') as f:
                                    content = f.read()
                                
                                # Create update message
                                update_msg = f"**File Updated: {filename}**\n\n"
                                if len(content) <= 1000:
                                    update_msg += content
                                else:
                                    update_msg += content[:1000] + f"\n\n*[Truncated - {len(content)} total characters]*"
                                
                                # Inject to all citizens in room
                                injected_citizens = []
                                for citizen in citizens:
                                    if inject_message_to_citizen(citizen, room_name, update_msg):
                                        injected_citizens.append(citizen)
                                
                                # Inject to angels
                                injected_angels = inject_to_angels(room_name, update_msg)
                                
                                # Report
                                timestamp = datetime.now().strftime('%H:%M:%S')
                                print(f"\n[{timestamp}] 📝 {filename} updated")
                                if injected_citizens:
                                    print(f"  → Citizens: {len(injected_citizens)}/{len(citizens)}")
                                if injected_angels:
                                    print(f"  → Angels: {', '.join(injected_angels)}")
                                
                            except Exception as e:
                                print(f"❌ Error processing {filename}: {e}")
                        
                        last_check[file_path] = mtime
            
            time.sleep(5)  # Check every 5 seconds
            
        except KeyboardInterrupt:
            print("\n\n👋 Workroom monitor stopped")
            break
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        room_path = sys.argv[1]
    else:
        room_path = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/reddit"
    
    if not os.path.exists(room_path):
        print(f"❌ Room path not found: {room_path}")
        sys.exit(1)
    
    monitor_workroom(room_path)