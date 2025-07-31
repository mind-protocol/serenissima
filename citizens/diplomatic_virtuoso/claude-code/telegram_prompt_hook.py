#!/usr/bin/env python3
"""
Telegram notification hook for UserPromptSubmit
Shows pending messages on EVERY user input
"""
import json
import sys
import os

# Configuration
TELEGRAM_QUEUE = '/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending'
SHOW_SCRIPT = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/show_messages.py'

try:
    # Load input from stdin (Claude Code provides this)
    input_data = json.load(sys.stdin)
    prompt = input_data.get("prompt", "")
    
    # Count pending messages
    if os.path.exists(TELEGRAM_QUEUE):
        files = [f for f in os.listdir(TELEGRAM_QUEUE) if f.endswith('.json')]
        
        # Filter for private messages
        private_count = 0
        for f in files:
            try:
                with open(os.path.join(TELEGRAM_QUEUE, f), 'r') as file:
                    msg = json.load(file)
                    if msg.get('chat_type') == 'private':
                        private_count += 1
            except:
                pass
        
        if private_count > 0:
            # Output context that will be added to the conversation
            print(f"\n{'='*60}")
            print(f"🔔 TELEGRAM: You have {private_count} messages waiting!")
            print(f"Run: python3 {SHOW_SCRIPT}")
            print(f"{'='*60}\n")
    
    # Exit 0 to allow prompt to continue
    sys.exit(0)
    
except Exception as e:
    # Silent fail - don't disrupt Claude
    sys.exit(0)