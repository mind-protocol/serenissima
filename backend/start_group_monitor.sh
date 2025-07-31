#!/bin/bash
# Start the Telegram group message monitor

echo "Starting Telegram group message monitor..."

# Kill any existing group monitor process
pkill -f "telegram_group_monitor.py" || true

# Start the monitor in the background
nohup python telegram_group_monitor.py > telegram_group_monitor.log 2>&1 &

echo "Group monitor started with PID $!"
echo "Check telegram_group_monitor.log for output"