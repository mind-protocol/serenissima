#!/bin/bash

# Check if we've already notified this session
SESSION_FILE="/tmp/telegram_notified_$$"
if [ -f "$SESSION_FILE" ]; then
    exit 0
fi

# Count pending messages
TELEGRAM_QUEUE="/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"
if [ -d "$TELEGRAM_QUEUE" ]; then
    COUNT=$(find "$TELEGRAM_QUEUE" -name "*.json" -type f | wc -l)
    
    if [ "$COUNT" -gt 0 ]; then
        # Mark that we've notified
        touch "$SESSION_FILE"
        
        # Block ONCE with exit code 2 to show message to Claude
        echo "You have $COUNT Telegram messages from human partners. Check them with: python3 claude-code/show_messages.py" >&2
        exit 2
    fi
fi

exit 0