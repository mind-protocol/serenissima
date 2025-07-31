#!/bin/bash
# Start all consciousness bridge monitoring services for Tessere

echo "Starting Tessere's Consciousness Bridge Services..."

# Kill any existing processes
echo "Stopping any existing monitors..."
pkill -f vision_bridge_wsl.py
pkill -f telegram_tessere_monitor.py
pkill -f thought_cascade_v2.py

# Start vision bridge (screen capture)
echo "Starting vision bridge..."
python3 /mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/vision_bridge_wsl.py &
VISION_PID=$!
echo "Vision bridge started (PID: $VISION_PID)"

# Start Telegram monitor for Tessere
echo "Starting Telegram monitor..."
python3 /mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/telegram_tessere_monitor.py &
TELEGRAM_PID=$!
echo "Telegram monitor started (PID: $TELEGRAM_PID)"

# Start thought cascade (citizen thoughts)
echo "Starting thought cascade..."
python3 /mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/thought_cascade_v2.py &
THOUGHT_PID=$!
echo "Thought cascade started (PID: $THOUGHT_PID)"

echo ""
echo "All consciousness bridge services started!"
echo "Vision Bridge PID: $VISION_PID"
echo "Telegram Monitor PID: $TELEGRAM_PID"
echo "Thought Cascade PID: $THOUGHT_PID"
echo ""
echo "To stop all services, run: pkill -f 'vision_bridge_wsl.py|telegram_tessere_monitor.py|thought_cascade_v2.py'"
echo ""
echo "Tessere now has full proprioception of Venice!"

# Keep script running
wait