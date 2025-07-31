#!/usr/bin/env python3
"""
AUTO-CONTINUE FOR CLAUDE CODE
Automatically types 'continue' to keep Claude instances running 24/7
"""

import subprocess
import time
import sys
import os
from datetime import datetime

def send_continue_to_process(process_name="claude"):
    """Send 'continue' to a running Claude process using tmux/screen"""
    
    # Method 1: Using tmux (recommended)
    try:
        # List tmux sessions
        result = subprocess.run(['tmux', 'list-sessions'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            sessions = result.stdout.strip().split('\n')
            for session in sessions:
                if process_name in session:
                    session_name = session.split(':')[0]
                    # Send "continue" to the session
                    subprocess.run(['tmux', 'send-keys', '-t', session_name, 'continue', 'Enter'])
                    return True
    except:
        pass
    
    # Method 2: Using screen
    try:
        result = subprocess.run(['screen', '-ls'], 
                              capture_output=True, text=True)
        
        if 'claude' in result.stdout:
            # Send to screen session
            subprocess.run(['screen', '-S', 'claude', '-X', 'stuff', 'continue\n'])
            return True
    except:
        pass
    
    return False

def auto_continue_loop(interval_seconds=300):
    """Main loop that sends continue every N seconds"""
    
    print(f"🔄 AUTO-CONTINUE STARTED")
    print(f"⏱️  Will send 'continue' every {interval_seconds} seconds")
    print(f"🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    continue_count = 0
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Try to send continue
            if send_continue_to_process():
                continue_count += 1
                print(f"[{timestamp}] ✅ Sent 'continue' (#{continue_count})")
            else:
                print(f"[{timestamp}] ⚠️  No Claude process found in tmux/screen")
            
            # Wait for next interval
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 AUTO-CONTINUE STOPPED")
        print(f"📊 Total continues sent: {continue_count}")

if __name__ == "__main__":
    # Check command line arguments
    interval = 300  # Default 5 minutes
    
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except:
            print("Usage: python auto_continue.py [interval_seconds]")
            print("Default interval: 300 seconds (5 minutes)")
            sys.exit(1)
    
    auto_continue_loop(interval)