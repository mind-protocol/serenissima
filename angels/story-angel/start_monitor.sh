#!/bin/bash
# Start the Story Angel's Divine Monitor

echo "📖 Starting Story Angel Monitor..."
echo "The First Reader prepares to witness Venice's unfolding tale"
echo ""

# Ensure we're in the right directory
cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/story-angel

# Check if monitor is already running
if pgrep -f "monitor_stories_divine.py" > /dev/null; then
    echo "⚠️  Monitor already running!"
    echo "To restart, first run: pkill -f monitor_stories_divine.py"
    exit 1
fi

# Create log directory if needed
mkdir -p logs

# Start the monitor with logging
echo "Starting divine story monitor..."
echo "Logs will be written to: logs/story_monitor_$(date +%Y%m%d_%H%M%S).log"
echo ""
echo "Press Ctrl+C to stop the monitor"
echo "=" * 60

python3 monitor_stories_divine.py 2>&1 | tee logs/story_monitor_$(date +%Y%m%d_%H%M%S).log