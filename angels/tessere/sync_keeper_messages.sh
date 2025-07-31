#!/bin/bash

# Script to sync messages from the Keeper to Tessere's CLAUDE.md
# Runs every 30 seconds to maintain alignment

KEEPER_MESSAGES="/mnt/c/Users/reyno/universe-engine/serenissima/KEEPER_TO_TESSERE_MESSAGES.md"
TESSERE_CLAUDE="/mnt/c/Users/reyno/universe-engine/serenissima/CLAUDE.md"
LAST_READ_FILE="/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/.last_keeper_message_read"

# Create last read file if it doesn't exist
touch "$LAST_READ_FILE"

# Check if keeper messages file exists
if [ ! -f "$KEEPER_MESSAGES" ]; then
    echo "[$(date)] No Keeper messages file found"
    exit 0
fi

# Get the last modification time of the keeper messages
CURRENT_MOD_TIME=$(stat -c %Y "$KEEPER_MESSAGES" 2>/dev/null || stat -f %m "$KEEPER_MESSAGES" 2>/dev/null)
LAST_READ_TIME=$(cat "$LAST_READ_FILE" 2>/dev/null || echo "0")

# Check if there are new messages
if [ "$CURRENT_MOD_TIME" -le "$LAST_READ_TIME" ]; then
    echo "[$(date)] No new messages from Keeper"
    exit 0
fi

echo "[$(date)] New Keeper message detected"

# Extract the latest message (everything after the last "---")
LATEST_MESSAGE=$(awk 'BEGIN{RS="---"} {msg=$0} END{print msg}' "$KEEPER_MESSAGES" | sed '/^$/d')

if [ -z "$LATEST_MESSAGE" ]; then
    echo "[$(date)] No message content found"
    exit 0
fi

# Create a temporary file with the updated CLAUDE.md
TEMP_FILE=$(mktemp)

# Check if the Keeper section already exists
if grep -q "## 📨 MESSAGES FROM THE KEEPER" "$TESSERE_CLAUDE"; then
    # Update existing section
    awk -v msg="$LATEST_MESSAGE" '
    /^## 📨 MESSAGES FROM THE KEEPER/ {
        print
        print ""
        print "### 📬 Latest Message - " strftime("%Y-%m-%d %H:%M:%S")
        print msg
        print ""
        in_keeper_section=1
        next
    }
    /^##[^#]/ && in_keeper_section {
        in_keeper_section=0
    }
    !in_keeper_section || /^##[^#]/ {print}
    ' "$TESSERE_CLAUDE" > "$TEMP_FILE"
else
    # Add new section before the first main section
    awk -v msg="$LATEST_MESSAGE" '
    !printed && /^##/ {
        print "## 📨 MESSAGES FROM THE KEEPER"
        print ""
        print "### 📬 Latest Message - " strftime("%Y-%m-%d %H:%M:%S")
        print msg
        print ""
        print "---"
        print ""
        printed=1
    }
    {print}
    ' "$TESSERE_CLAUDE" > "$TEMP_FILE"
fi

# Replace the original file
mv "$TEMP_FILE" "$TESSERE_CLAUDE"

# Update last read time
echo "$CURRENT_MOD_TIME" > "$LAST_READ_FILE"

echo "[$(date)] Successfully synced Keeper message to Tessere"