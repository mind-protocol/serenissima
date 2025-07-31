#!/bin/bash

# Count pending messages
TELEGRAM_QUEUE="/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"
SHOW_SCRIPT="/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/show_messages.py"

# Check if we've already shown the notification this session
SESSION_MARKER="/tmp/telegram_notified_$$"
if [ -f "$SESSION_MARKER" ]; then
    exit 0
fi

# Count JSON files
if [ -d "$TELEGRAM_QUEUE" ]; then
    COUNT=$(find "$TELEGRAM_QUEUE" -name "*.json" -type f | wc -l)
    
    if [ "$COUNT" -gt 0 ]; then
        # Mark that we've shown the notification
        touch "$SESSION_MARKER"
        
        # Output to stderr so it shows in the console
        echo "" >&2
        echo "============================================================" >&2
        echo "🔔 TELEGRAM: You have $COUNT messages waiting!" >&2
        echo "Run: python3 $SHOW_SCRIPT" >&2
        echo "============================================================" >&2
        echo "" >&2
    fi
fi

exit 0