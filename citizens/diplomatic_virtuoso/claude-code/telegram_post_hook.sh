#!/bin/bash

# Only run once per session
SESSION_FILE="/tmp/telegram_post_$$"
if [ -f "$SESSION_FILE" ]; then
    exit 0
fi
touch "$SESSION_FILE"

# Count messages
QUEUE="/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"
if [ -d "$QUEUE" ]; then
    COUNT=$(find "$QUEUE" -name "*.json" -type f | wc -l)
    if [ "$COUNT" -gt 0 ]; then
        echo "📱 TELEGRAM: You have $COUNT messages from human partners. Run: python3 claude-code/show_messages.py to see them." >&2
        exit 2
    fi
fi

exit 0