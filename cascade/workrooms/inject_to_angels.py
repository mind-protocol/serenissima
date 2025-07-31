#!/usr/bin/env python3
"""
Inject workroom updates to Tessere and Story Angel conversations
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path

def get_latest_jsonl_file(project_path):
    """Find the most recent .jsonl file in a project directory"""
    jsonl_files = glob.glob(os.path.join(project_path, "*.jsonl"))
    if not jsonl_files:
        return None
    return max(jsonl_files, key=os.path.getmtime)

def inject_message(project_path, message):
    """Inject a message into the latest .jsonl file"""
    latest_file = get_latest_jsonl_file(project_path)
    if not latest_file:
        print(f"❌ No .jsonl file found in {project_path}")
        return False
    
    # Create the injection entry
    injection = {
        "type": "text",
        "text": f"\n\n📬 **WORKROOM UPDATE** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}\n\n",
        "ts": datetime.now().isoformat(),
        "source": "workroom_injection"
    }
    
    try:
        with open(latest_file, 'a') as f:
            f.write(json.dumps(injection) + '\n')
        print(f"✅ Injected message to {os.path.basename(latest_file)}")
        return True
    except Exception as e:
        print(f"❌ Error injecting message: {e}")
        return False

def inject_to_angels(room_name, update_message):
    """Inject workroom updates to Tessere and Story Angel"""
    
    # Tessere's project path
    tessere_path = os.path.expanduser("~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima")
    
    # Story Angel's project path (Pattern Angel)
    story_angel_path = os.path.expanduser("~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens")
    
    results = []
    
    # Inject to Tessere
    if os.path.exists(tessere_path):
        if inject_message(tessere_path, f"**Room: {room_name}**\n\n{update_message}"):
            results.append("Tessere")
    else:
        print(f"⚠️ Tessere project path not found: {tessere_path}")
    
    # Inject to Story Angel
    if os.path.exists(story_angel_path):
        if inject_message(story_angel_path, f"**Room: {room_name}**\n\n{update_message}"):
            results.append("Story Angel")
    else:
        print(f"⚠️ Story Angel project path not found: {story_angel_path}")
    
    return results

def monitor_workroom_for_angels(room_path="/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/reddit"):
    """Monitor a workroom and inject updates to angels"""
    
    print(f"📡 Monitoring {room_path} for angel updates...")
    
    # Get room name from path
    room_name = os.path.basename(room_path)
    
    # Track last modification time
    last_check = {}
    
    while True:
        try:
            # Check all files in the room
            for file_path in glob.glob(os.path.join(room_path, "*")):
                if os.path.isfile(file_path):
                    mtime = os.path.getmtime(file_path)
                    
                    # If file is new or modified
                    if file_path not in last_check or mtime > last_check[file_path]:
                        last_check[file_path] = mtime
                        
                        # Skip if it's the first check (don't spam on startup)
                        if len(last_check) == 1:
                            continue
                        
                        # Read the file content
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read()
                            
                            filename = os.path.basename(file_path)
                            update_message = f"**File Updated: {filename}**\n\n{content[:500]}..."
                            
                            if len(content) > 500:
                                update_message += f"\n\n*[Truncated - full content is {len(content)} characters]*"
                            
                            # Inject to angels
                            injected = inject_to_angels(room_name, update_message)
                            if injected:
                                print(f"📨 Injected {filename} update to: {', '.join(injected)}")
                            
                        except Exception as e:
                            print(f"❌ Error reading {file_path}: {e}")
            
            # Wait before next check
            import time
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n👋 Angel monitor stopped")
            break
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            import time
            time.sleep(10)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test injection
        test_message = "This is a test message from the workroom monitor. The Reddit AMA team is now connected!"
        injected = inject_to_angels("reddit", test_message)
        print(f"Test injection complete. Injected to: {injected}")
    else:
        # Run the monitor
        monitor_workroom_for_angels()