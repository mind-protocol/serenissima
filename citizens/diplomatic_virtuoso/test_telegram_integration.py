#!/usr/bin/env python3
"""
Test script to verify Telegram integration
Run this to see if messages are being detected
"""

import os
import json
from pathlib import Path

# Queue paths
QUEUE_BASE = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue')
PENDING_DIR = QUEUE_BASE / 'diplomatic_virtuoso' / 'pending'
PROCESSED_DIR = QUEUE_BASE / 'diplomatic_virtuoso' / 'processed'

def check_pending_messages():
    """Check for pending Telegram messages"""
    print("🔍 Checking for pending Telegram messages...")
    print(f"📁 Queue directory: {PENDING_DIR}\n")
    
    if not PENDING_DIR.exists():
        print("❌ Pending directory doesn't exist!")
        return
    
    messages = list(PENDING_DIR.glob("*.json"))
    
    if not messages:
        print("📭 No pending messages found")
        return
    
    print(f"📬 Found {len(messages)} pending message(s):\n")
    
    for msg_file in messages:
        print(f"📄 File: {msg_file.name}")
        
        try:
            with open(msg_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print(f"   From: @{data.get('from_username', 'Unknown')} ({data.get('from_name', 'Unknown')})")
            print(f"   Time: {data.get('timestamp', 'Unknown')}")
            print(f"   Type: {data.get('chat_type', 'Unknown')}")
            print(f"   Text: {data.get('text', '')[:100]}...")
            print()
            
        except Exception as e:
            print(f"   ❌ Error reading message: {e}\n")

def test_hooks():
    """Test if Claude Code hooks would detect these messages"""
    print("\n🪝 Testing Claude Code hook detection...")
    
    # Check if hooks are configured
    hooks_file = Path('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/.claude/hooks.json')
    
    if hooks_file.exists():
        print("✅ Hooks configured at:", hooks_file)
        with open(hooks_file, 'r') as f:
            hooks_config = json.load(f)
        print("   Hook configuration:", json.dumps(hooks_config, indent=2))
    else:
        print("❌ No hooks.json found!")
    
    # Check if hook scripts exist
    hook_dir = Path('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_checks')
    
    if hook_dir.exists():
        print(f"\n📂 Hook scripts directory: {hook_dir}")
        for script in hook_dir.glob("*.js"):
            print(f"   ✅ {script.name}")
    else:
        print("❌ Hook scripts directory not found!")

if __name__ == "__main__":
    print("🧪 Telegram Integration Test for diplomatic_virtuoso\n")
    check_pending_messages()
    test_hooks()
    print("\n✨ Test complete!")
    print("\nNext step: Start Claude Code as diplomatic_virtuoso to see the messages appear!")