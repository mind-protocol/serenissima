#!/bin/bash
# Start the Claude Instance Monitor in background

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_FILE="$SCRIPT_DIR/instance_monitor.log"
PID_FILE="$SCRIPT_DIR/instance_monitor.pid"

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "Instance monitor already running (PID: $OLD_PID)"
        exit 1
    fi
fi

# Start the monitor
echo "Starting Claude Instance Monitor..."
nohup python3 "$SCRIPT_DIR/claude_instance_monitor.py" > "$LOG_FILE" 2>&1 &
PID=$!

# Save PID
echo $PID > "$PID_FILE"

echo "Monitor started (PID: $PID)"
echo "Log file: $LOG_FILE"
echo "Output: $SCRIPT_DIR/active_instances.json"