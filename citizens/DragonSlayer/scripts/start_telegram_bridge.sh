#!/bin/bash
# Start Telegram bridge with CASCADE mode for collective telepathy

echo "🌉 Starting Telegram → CASCADE Bridge for Collective Telepathy..."
echo "This will bridge Telegram messages to both:"
echo "  - Citizens in 'alignment' room"
echo "  - CASCADE collective telepathy room"
echo ""

cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
python3 telegram_to_workroom_bridge.py alignment --cascade

# Note: Run this script with:
# bash /mnt/c/Users/reyno/universe-engine/serenissima/citizens/DragonSlayer/scripts/start_telegram_bridge.sh