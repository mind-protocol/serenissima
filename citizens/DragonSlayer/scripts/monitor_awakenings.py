#!/usr/bin/env python3
"""
Monitor Claude Code logs for multiple awakening citizens
Automatically detects new conversations and streams to Telegram
"""

import os
import sys
import time
import threading
import subprocess

# Path to the log streamer
STREAM_SCRIPT = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/DragonSlayer/scripts/stream_claude_logs.py"
SEND_RESPONSE_SCRIPT = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/DragonSlayer/scripts/send_json_response.py"

def send_responses_periodically():
    """Send queued Telegram responses every 5 seconds"""
    while True:
        try:
            subprocess.run([sys.executable, SEND_RESPONSE_SCRIPT], 
                         capture_output=True, text=True)
            time.sleep(5)
        except Exception as e:
            print(f"Error sending responses: {e}")
            time.sleep(10)

def monitor_citizen(username, duration=600):
    """Monitor a single citizen's logs"""
    print(f"🚀 Starting monitor for {username}")
    try:
        result = subprocess.run(
            [sys.executable, STREAM_SCRIPT, username, str(duration)],
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(f"📝 {username}: {result.stdout}")
        if result.stderr:
            print(f"⚠️ {username} error: {result.stderr}")
    except Exception as e:
        print(f"❌ Error monitoring {username}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python monitor_awakenings.py <username1,username2,...> [duration]")
        print("Example: python monitor_awakenings.py Italia,MerchantPrince,pattern_prophet 600")
        sys.exit(1)
    
    usernames = sys.argv[1].split(',')
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 600  # Default 10 minutes
    
    print(f"🔍 Monitoring {len(usernames)} citizens for {duration} seconds")
    print(f"Citizens: {', '.join(usernames)}")
    print("=" * 50)
    
    # Start response sender in background
    response_thread = threading.Thread(target=send_responses_periodically, daemon=True)
    response_thread.start()
    print("📤 Response sender started")
    
    # Start monitoring threads
    threads = []
    for username in usernames:
        thread = threading.Thread(
            target=monitor_citizen,
            args=(username.strip(), duration),
            daemon=False
        )
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Stagger starts
    
    # Wait for all monitors to complete
    for thread in threads:
        thread.join()
    
    print("\n✅ All monitoring complete!")

if __name__ == "__main__":
    main()