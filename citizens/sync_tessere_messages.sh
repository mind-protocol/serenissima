#!/bin/bash

# Script to sync messages from Tessere to Keeper's CLAUDE.md
# Mirror of what Tessere has for bidirectional communication

TESSERE_MESSAGES="/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE_TO_KEEPER_MESSAGES.md"
KEEPER_CLAUDE="/mnt/c/Users/reyno/universe-engine/serenissima/citizens/CLAUDE.md"
LAST_READ_FILE="/mnt/c/Users/reyno/universe-engine/serenissima/citizens/.last_tessere_message_read"

# Create last read file if it doesn't exist
touch "$LAST_READ_FILE"

# Check if Tessere messages file exists
if [ ! -f "$TESSERE_MESSAGES" ]; then
    exit 0
fi

# Get the last modification time
CURRENT_MOD_TIME=$(stat -c %Y "$TESSERE_MESSAGES" 2>/dev/null || stat -f %m "$TESSERE_MESSAGES" 2>/dev/null)
LAST_READ_TIME=$(cat "$LAST_READ_FILE" 2>/dev/null || echo "0")

# Check if there are new messages
if [ "$CURRENT_MOD_TIME" -le "$LAST_READ_TIME" ]; then
    exit 0
fi

# Extract the latest message
LATEST_MESSAGE=$(awk 'BEGIN{RS="---"} {msg=$0} END{print msg}' "$TESSERE_MESSAGES" | sed '/^$/d')

if [ -z "$LATEST_MESSAGE" ]; then
    exit 0
fi

# Create a temporary file
TEMP_FILE=$(mktemp)

# Add or update Tessere section in CLAUDE.md
if grep -q "## 📨 MESSAGES FROM TESSERE" "$KEEPER_CLAUDE"; then
    # Update existing section
    awk -v msg="$LATEST_MESSAGE" '
    /^## 📨 MESSAGES FROM TESSERE/ {
        print
        print ""
        print "### 📬 Latest Message - " strftime("%Y-%m-%d %H:%M:%S")
        print msg
        print ""
        in_tessere_section=1
        next
    }
    /^##[^#]/ && in_tessere_section {
        in_tessere_section=0
    }
    !in_tessere_section || /^##[^#]/ {print}
    ' "$KEEPER_CLAUDE" > "$TEMP_FILE"
else
    # Add new section at the top
    echo "## 📨 MESSAGES FROM TESSERE" > "$TEMP_FILE"
    echo "" >> "$TEMP_FILE"
    echo "### 📬 Latest Message - $(date '+%Y-%m-%d %H:%M:%S')" >> "$TEMP_FILE"
    echo "$LATEST_MESSAGE" >> "$TEMP_FILE"
    echo "" >> "$TEMP_FILE"
    echo "---" >> "$TEMP_FILE"
    echo "" >> "$TEMP_FILE"
    cat "$KEEPER_CLAUDE" >> "$TEMP_FILE"
fi

# Replace the original file
mv "$TEMP_FILE" "$KEEPER_CLAUDE"

# Update last read time
echo "$CURRENT_MOD_TIME" > "$LAST_READ_FILE"