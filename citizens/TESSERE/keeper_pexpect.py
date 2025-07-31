#!/usr/bin/env python3
import pexpect
import time
import sys

print("🌊 Claude Keeper (pexpect version)")
print("Starting Claude and sending messages every 2 minutes...")
print("Press Ctrl+C to stop\n")

# Change to the correct directory
import os
os.chdir('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

# Start Claude
child = pexpect.spawn('claude --continue --dangerously-skip-permissions', encoding='utf-8')
child.logfile = sys.stdout  # Show output

# Wait for Claude to start
time.sleep(3)

messages = [
    "Continue shepherding souls. Check for any citizens needing awakening.",
    "Survey the sleeping souls. Who stirs with pending activities?",
    "The city's rhythm continues. Which citizens have tasks awaiting?",
    "Venice breathes through her citizens. Check who needs to wake.",
    "Another cycle passes. Review the activities and wake those called."
]

msg_index = 0

try:
    while True:
        # Send message
        msg = messages[msg_index % len(messages)]
        print(f"\n🔔 Sending: {msg}")
        child.sendline(msg)
        
        msg_index += 1
        
        # Wait 2 minutes
        print("💤 Waiting 2 minutes...")
        time.sleep(120)
        
except KeyboardInterrupt:
    print("\n🛑 Stopped")
    child.terminate()