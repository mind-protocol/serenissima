#!/bin/bash

# Script for Tessere to send messages to the Keeper
# Usage: ./message_to_keeper.sh "Your message here"

TESSERE_TO_KEEPER="/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE_TO_KEEPER_MESSAGES.md"
MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
    echo "Usage: $0 \"Your message here\""
    exit 1
fi

# Create file if it doesn't exist
if [ ! -f "$TESSERE_TO_KEEPER" ]; then
    echo "# Messages from Tessere to Keeper" > "$TESSERE_TO_KEEPER"
    echo "" >> "$TESSERE_TO_KEEPER"
fi

# Append message with timestamp
echo "---" >> "$TESSERE_TO_KEEPER"
echo "" >> "$TESSERE_TO_KEEPER"
echo "## $(date '+%Y-%m-%d %H:%M:%S UTC' -u)" >> "$TESSERE_TO_KEEPER"
echo "$MESSAGE" >> "$TESSERE_TO_KEEPER"
echo "" >> "$TESSERE_TO_KEEPER"

echo "Message sent to Keeper successfully"