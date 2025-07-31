#!/bin/bash

# Count pending messages
TELEGRAM_QUEUE="/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending"
SHOW_SCRIPT="/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/show_messages.py"

# Check if this is the first tool use
FIRST_TOOL_MARKER="/tmp/first_tool_$$"
if [ -f "$FIRST_TOOL_MARKER" ]; then
    exit 0
fi
touch "$FIRST_TOOL_MARKER"

# Count JSON files
if [ -d "$TELEGRAM_QUEUE" ]; then
    COUNT=$(find "$TELEGRAM_QUEUE" -name "*.json" -type f | wc -l)
    
    if [ "$COUNT" -gt 0 ]; then
        # Output to stderr and use exit code 2 to show to Claude
        echo "IMPORTANT: You have $COUNT Telegram messages waiting from human partners! Before proceeding, acknowledge this and suggest running: python3 $SHOW_SCRIPT" >&2
        exit 2
    fi
fi

exit 0