#!/bin/bash
# Quick start script for Telegram listener

echo "🚀 Starting Telegram listener for @diplomatic_virtuoso"

# Check if session data exists
if [ -f "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/telegram_session_data.json" ]; then
    echo "✅ Using existing session data"
else
    echo "❌ No session data found. Run setup.sh first!"
    exit 1
fi

# Create queue directories if needed
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/processed

# Run the listener
python3 diplomatic_virtuoso_listener.py