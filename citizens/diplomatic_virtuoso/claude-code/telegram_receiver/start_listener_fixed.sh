#!/bin/bash
# Start script that sets up environment and runs listener

echo "🚀 Starting Telegram listener for @diplomatic_virtuoso"

# Check if .env exists (has API credentials)
if [ -f ".env" ]; then
    echo "📝 Loading API credentials from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ No .env file found!"
    echo "Please create .env with:"
    echo "TELEGRAM_API_ID=your_api_id"
    echo "TELEGRAM_API_HASH=your_api_hash"
    exit 1
fi

# Create queue directories if needed
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/processed

# Run the listener
python3 diplomatic_virtuoso_listener.py