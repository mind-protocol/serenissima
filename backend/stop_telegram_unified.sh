#!/bin/bash
#
# Stop script for the Unified Telegram Service
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/telegram_unified.pid"

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

if is_running; then
    PID=$(cat "$PID_FILE")
    echo "🛑 Stopping Unified Telegram Service (PID: $PID)..."
    
    # Send SIGTERM for graceful shutdown
    kill $PID 2>/dev/null
    
    # Wait up to 5 seconds for graceful shutdown
    for i in {1..5}; do
        if ! is_running; then
            echo "✓ Service stopped gracefully"
            exit 0
        fi
        sleep 1
    done
    
    # Force kill if still running
    echo "⚠️  Service didn't stop gracefully, forcing shutdown..."
    kill -9 $PID 2>/dev/null
    rm -f "$PID_FILE"
    echo "✓ Service forcefully stopped"
else
    echo "ℹ️  Unified Telegram Service is not running"
fi

# Also kill any stray processes
pkill -f "telegram_unified_service.py" 2>/dev/null