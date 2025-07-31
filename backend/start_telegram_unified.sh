#!/bin/bash
#
# Startup script for the Unified Telegram Service
# This consolidates all Telegram functionality into one service
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVICE_SCRIPT="$SCRIPT_DIR/telegram_unified_service.py"
PID_FILE="$SCRIPT_DIR/telegram_unified.pid"
LOG_FILE="$SCRIPT_DIR/telegram_unified.log"

# Function to check if service is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        else
            # PID file exists but process is not running
            rm "$PID_FILE"
        fi
    fi
    return 1
}

# Check if already running
if is_running; then
    echo "✓ Unified Telegram Service is already running (PID: $(cat $PID_FILE))"
    exit 0
fi

echo "🚀 Starting Unified Telegram Service..."

# Kill any existing Telegram services
echo "🛑 Stopping any existing Telegram services..."
pkill -f "telegram_poller.py" 2>/dev/null
pkill -f "telegram_group_monitor.py" 2>/dev/null
pkill -f "telegram_citizen_watcher.py" 2>/dev/null
pkill -f "telegram_to_workroom_bridge.py" 2>/dev/null
pkill -f "workroom_to_telegram_bridge.py" 2>/dev/null
pkill -f "telegram_watcher.py" 2>/dev/null
pkill -f "telegram_integration.py" 2>/dev/null
pkill -f "telegram_router.py" 2>/dev/null
pkill -f "telegram_response_monitor.py" 2>/dev/null
pkill -f "telegram_resonance_watcher.py" 2>/dev/null

# Wait for processes to die
sleep 2

# Start the unified service
nohup python3 "$SERVICE_SCRIPT" > "$LOG_FILE" 2>&1 &
PID=$!

# Save PID
echo $PID > "$PID_FILE"

# Wait a moment to check if it started successfully
sleep 3

if is_running; then
    echo "✓ Unified Telegram Service started successfully!"
    echo "  PID: $PID"
    echo "  Log: $LOG_FILE"
    echo ""
    echo "The service is now handling:"
    echo "  • Group message bridging to citizens"
    echo "  • Direct messages from NLR"
    echo "  • Workroom file monitoring"
    echo "  • Citizen thought streaming"
    echo ""
    echo "To stop the service:"
    echo "  $SCRIPT_DIR/stop_telegram_unified.sh"
else
    echo "❌ Failed to start Unified Telegram Service"
    echo "Check the log file: $LOG_FILE"
    exit 1
fi