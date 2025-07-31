#!/usr/bin/env python3
"""
Telegram notification hook - informs about messages without blocking
"""
import json
import sys
import os

# Only run once per session
SESSION_MARKER = f"/tmp/telegram_notified_{os.getppid()}"
if os.path.exists(SESSION_MARKER):
    sys.exit(0)

# Count messages
QUEUE_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"
if os.path.exists(QUEUE_PATH):
    count = len([f for f in os.listdir(QUEUE_PATH) if f.endswith('.json')])
    if count > 0:
        # Mark as notified
        open(SESSION_MARKER, 'w').close()
        
        # Output notification that will be added to context
        print(f"\n📱 Telegram: {count} messages waiting. Run: python3 claude-code/show_messages.py\n")

# Always exit 0 - never block
sys.exit(0)