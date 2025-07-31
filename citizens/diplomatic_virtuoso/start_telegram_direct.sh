#!/bin/bash
# Start Telegram Direct integration for diplomatic_virtuoso

echo "==================================="
echo "TELEGRAM DIRECT - diplomatic_virtuoso"
echo "==================================="
echo ""
echo "Starting direct Telegram integration..."
echo "This will:"
echo "- Listen for messages to @diplomatic_virtuoso"
echo "- Create messages in Venice database"
echo "- Wake diplomatic_virtuoso when messages arrive"
echo ""
echo "Commands available:"
echo "- ./view_telegram_conversations.py - View all conversations"
echo "- ./send_telegram_direct_message.py <chat_id> <message> - Send message"
echo ""

# Check if token is set
if grep -q "YOUR_TOKEN_HERE" telegram_direct_listener.py; then
    echo "⚠️  WARNING: Telegram token not set!"
    echo "Please update TELEGRAM_TOKEN in telegram_direct_listener.py"
    exit 1
fi

# Make scripts executable
chmod +x telegram_direct_listener.py
chmod +x send_telegram_direct_message.py
chmod +x view_telegram_conversations.py

# Start the listener
echo "Starting listener..."
python3 telegram_direct_listener.py