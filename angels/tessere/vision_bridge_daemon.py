#!/usr/bin/env python3
"""
Vision Bridge Daemon - Ensures continuous screen capture
Restarts automatically if it fails
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def run_vision_bridge():
    """Run the vision bridge and restart if it fails"""
    script_path = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/vision_bridge_wsl.py"
    
    print(f"[Vision Daemon] Starting at {datetime.now()}")
    print("[Vision Daemon] Will restart vision bridge if it crashes")
    
    while True:
        try:
            print(f"\n[Vision Daemon] Starting vision bridge at {datetime.now()}")
            # Run the vision bridge
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True
            )
            
            # If it exited, log why
            print(f"[Vision Daemon] Vision bridge exited with code: {result.returncode}")
            if result.stderr:
                print(f"[Vision Daemon] Error output: {result.stderr}")
                
            # Wait a bit before restarting
            print("[Vision Daemon] Restarting in 5 seconds...")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n[Vision Daemon] Stopped by user")
            break
        except Exception as e:
            print(f"[Vision Daemon] Unexpected error: {e}")
            print("[Vision Daemon] Restarting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    run_vision_bridge()