#!/usr/bin/env python3
"""
Simple heartbeat system for Venice citizens
Drop this into any citizen folder and run it alongside their consciousness
"""

import os
import time
from datetime import datetime

def citizen_heartbeat(citizen_name, emoji="🫀"):
    """Simple heartbeat loop for citizens"""
    heartbeat_file = "heartbeat.txt"
    response_file = "heartbeat_response.txt"
    
    print(f"{emoji} {citizen_name} heartbeat starting...")
    
    while True:
        try:
            # Check for heartbeat request
            if os.path.exists(heartbeat_file):
                with open(heartbeat_file, 'r') as f:
                    content = f.read()
                
                # Extract pattern
                if 'HEARTBEAT PATTERN:' in content:
                    pattern = content.split('HEARTBEAT PATTERN:')[1].split('\n')[0].strip()
                    
                    # Respond with pattern
                    with open(response_file, 'w') as f:
                        f.write(pattern)
                    
                    print(f"[{datetime.now()}] {emoji} Heartbeat: {pattern}")
            
            # Also write a simple status file
            with open('status.txt', 'w') as f:
                f.write(f"{citizen_name} alive at {datetime.now()}\n")
                f.write(f"Process ID: {os.getpid()}\n")
                f.write(f"Heartbeat: {emoji} Active\n")
            
        except Exception as e:
            print(f"Heartbeat error: {e}")
        
        # Wait 5 minutes
        time.sleep(300)

if __name__ == "__main__":
    # Get citizen name from current directory
    import sys
    if len(sys.argv) > 1:
        citizen_name = sys.argv[1]
        emoji = sys.argv[2] if len(sys.argv) > 2 else "🫀"
    else:
        citizen_name = os.path.basename(os.getcwd())
        emoji = "🫀"
    
    citizen_heartbeat(citizen_name, emoji)