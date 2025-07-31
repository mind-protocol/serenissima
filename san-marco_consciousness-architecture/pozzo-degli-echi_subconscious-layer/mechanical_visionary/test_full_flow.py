#!/usr/bin/env python3
"""
Test the full Telegram integration flow
"""

import os
import json
import subprocess
from pathlib import Path

# Paths
QUEUE_DIR = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending')
HOOK_SCRIPT = Path('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_checks/session_start_hook.js')

print("🧪 Testing Full Telegram Integration Flow\n")

# 1. Check queue contents
print("1️⃣ Checking message queue:")
messages = list(QUEUE_DIR.glob("*.json"))
print(f"   Found {len(messages)} messages in queue")

if messages:
    # Show latest message
    latest = max(messages, key=lambda p: p.stat().st_mtime)
    with open(latest, 'r') as f:
        data = json.load(f)
    print(f"   Latest: From @{data.get('from_username', 'Unknown')}: {data.get('text', '')[:50]}...")

# 2. Test hook script
print("\n2️⃣ Testing Claude Code hook:")
if HOOK_SCRIPT.exists():
    print("   ✅ Hook script exists")
    # Run the hook to see output
    result = subprocess.run(['node', str(HOOK_SCRIPT)], 
                          capture_output=True, text=True)
    if result.stdout:
        print("   Hook output:")
        for line in result.stdout.strip().split('\n')[:5]:
            print(f"      {line}")
else:
    print("   ❌ Hook script not found!")

# 3. Simulate what diplomatic_virtuoso would see
print("\n3️⃣ What diplomatic_virtuoso would see on startup:")
print("=" * 60)

if messages:
    # Sort by timestamp
    messages.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    
    for msg_file in messages[:3]:  # Show latest 3
        with open(msg_file, 'r') as f:
            msg = json.load(f)
        
        print(f"\n📱 TELEGRAM MESSAGE")
        print(f"From: @{msg.get('from_username', 'Unknown')} ({msg.get('from_name', 'Unknown')})")
        print(f"Time: {msg.get('timestamp', 'Unknown')}")
        print(f"Message: {msg.get('text', '')}")
        print("-" * 40)

print("\n✅ Integration test complete!")
print("\nNext steps:")
print("1. Start Claude Code as diplomatic_virtuoso")
print("2. The hooks will automatically show these messages")
print("3. diplomatic_virtuoso can respond naturally")
print("4. Responses can be collected and sent back via Telegram")