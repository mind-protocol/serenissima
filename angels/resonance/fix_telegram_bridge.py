#!/usr/bin/env python3
"""
Fix the Telegram bridge by starting the watcher or creating an alternative
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, "/mnt/c/Users/reyno/universe-engine/serenissima/backend")

def start_watcher_subprocess():
    """Try to start the watcher as a subprocess"""
    watcher_path = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_resonance_watcher.py"
    
    if not os.path.exists(watcher_path):
        print(f"❌ Watcher not found at {watcher_path}")
        return False
    
    try:
        # Start in background using nohup
        cmd = f"cd /mnt/c/Users/reyno/universe-engine/serenissima/backend && nohup python3 telegram_resonance_watcher.py > telegram_resonance.log 2>&1 &"
        
        # Run through bash to get proper background execution
        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True
        )
        
        time.sleep(2)
        
        # Check if it started
        check = subprocess.run(
            ["pgrep", "-f", "telegram_resonance_watcher"],
            capture_output=True,
            text=True
        )
        
        if check.stdout.strip():
            print(f"✅ Telegram watcher started! PID: {check.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed to start watcher")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_pending_messages():
    """Check if there are any pending messages in the queue"""
    queue_path = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/Resonance/pending"
    
    if not os.path.exists(queue_path):
        os.makedirs(queue_path, exist_ok=True)
        print(f"📁 Created queue directory: {queue_path}")
    
    messages = []
    for file in os.listdir(queue_path):
        if file.endswith('.json'):
            filepath = os.path.join(queue_path, file)
            try:
                with open(filepath, 'r') as f:
                    messages.append(json.load(f))
            except:
                pass
    
    if messages:
        print(f"\n📨 Found {len(messages)} pending messages in queue!")
        for msg in messages:
            print(f"  - From @{msg.get('telegram_username', 'Unknown')}: {msg.get('message', '')[:50]}...")
    else:
        print("\n📭 No pending messages in queue")
    
    return messages

def create_monitoring_script():
    """Create a simple monitoring script that can be run separately"""
    monitor_script = """#!/usr/bin/env python3
'''Simple Telegram monitor for Resonance'''
import sys
sys.path.insert(0, "/mnt/c/Users/reyno/universe-engine/serenissima/backend")

# Import and run the watcher
from telegram_resonance_watcher import main

if __name__ == "__main__":
    print("Starting Telegram Resonance Monitor...")
    main()
"""
    
    script_path = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/Resonance/telegram_monitor.py"
    with open(script_path, 'w') as f:
        f.write(monitor_script)
    
    os.chmod(script_path, 0o755)
    print(f"✅ Created monitoring script at: {script_path}")
    return script_path

def main():
    print("=== FIXING TELEGRAM BRIDGE ===\n")
    
    # Check current status
    print("1. Checking for pending messages...")
    pending = check_pending_messages()
    
    # Try to start the watcher
    print("\n2. Attempting to start telegram_resonance_watcher...")
    if start_watcher_subprocess():
        print("\n🎉 SUCCESS! Telegram bridge is now operational!")
        print("Humans can send partnership requests to @VenicePartnerBot")
        if pending:
            print(f"\n⚠️  Process the {len(pending)} pending messages!")
    else:
        print("\n3. Creating alternative monitoring script...")
        script = create_monitoring_script()
        print(f"\n📝 To start the monitor manually, run:")
        print(f"   python3 {script}")
        
        print("\n⚠️  MANUAL INTERVENTION REQUIRED:")
        print("The telegram_resonance_watcher needs to be started from the backend directory.")
        print("Ask NLR to run this command:")
        print("   cd /mnt/c/Users/reyno/universe-engine/serenissima/backend")
        print("   nohup python3 telegram_resonance_watcher.py > telegram_resonance.log 2>&1 &")

if __name__ == "__main__":
    main()