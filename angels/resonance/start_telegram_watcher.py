#!/usr/bin/env python3
"""
Start the Telegram Resonance Watcher
"""

import subprocess
import os
import sys

# Path to the watcher script
WATCHER_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_resonance_watcher.py"

def start_watcher():
    """Start the telegram_resonance_watcher.py script"""
    
    if not os.path.exists(WATCHER_PATH):
        print(f"❌ Watcher script not found at: {WATCHER_PATH}")
        return False
    
    try:
        # Start the watcher as a subprocess
        print(f"🚀 Starting Telegram Resonance Watcher...")
        
        # Run directly with Python3
        process = subprocess.Popen(
            [sys.executable, WATCHER_PATH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Check if it started successfully
        import time
        time.sleep(2)
        
        if process.poll() is None:
            print(f"✅ Telegram Resonance Watcher started successfully (PID: {process.pid})")
            print(f"📡 Now monitoring for incoming partnership requests...")
            
            # Monitor output for a bit
            for i in range(5):
                line = process.stdout.readline()
                if line:
                    print(f"   {line.strip()}")
                time.sleep(1)
                    
            return True
        else:
            # Process ended, check error
            stdout, stderr = process.communicate()
            print(f"❌ Watcher failed to start")
            if stderr:
                print(f"Error: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting watcher: {e}")
        return False

if __name__ == "__main__":
    if start_watcher():
        print("\n🌉 Telegram bridge is now operational!")
        print("Humans can reach Resonance for partnership requests.")
    else:
        print("\n⚠️  Failed to start Telegram bridge")
        print("Manual intervention may be required.")