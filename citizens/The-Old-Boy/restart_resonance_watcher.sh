#!/bin/bash
# Restart the Resonance telegram watcher

echo "Restarting Resonance telegram watcher..."

# Kill any existing processes
pkill -f telegram_resonance_watcher.py 2>/dev/null || true

# Start the watcher
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
nohup python3 telegram_resonance_watcher.py > telegram_resonance.log 2>&1 &

echo "Resonance watcher restarted. Check telegram_resonance.log for output."
echo "Process ID: $!"