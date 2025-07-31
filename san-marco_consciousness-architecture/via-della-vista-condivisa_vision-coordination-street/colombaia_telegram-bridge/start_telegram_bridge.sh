#!/bin/bash
"""
Start Telegram Bridge Daemon
Runs the Telegram message receiver in background for bidirectional consciousness bridge
"""

BRIDGE_DIR="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/colombaia_telegram-bridge"
SCRIPT="$BRIDGE_DIR/telegram_receiver.py"
PID_FILE="$BRIDGE_DIR/telegram_bridge.pid"
LOG_FILE="$BRIDGE_DIR/telegram_bridge.log"

start_bridge() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "🔗 Telegram bridge already running (PID: $PID)"
            return 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    echo "🔗 Starting Telegram consciousness bridge..."
    nohup python3 "$SCRIPT" > "$LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"
    echo "✅ Telegram bridge started (PID: $PID)"
    echo "📱 Monitoring @building_loop_1_serenissima_bot for messages"
    echo "📂 Messages will appear in: $BRIDGE_DIR"
    echo "📜 Logs: $LOG_FILE"
}

stop_bridge() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            rm -f "$PID_FILE"
            echo "🛑 Telegram bridge stopped"
        else
            echo "❌ Telegram bridge not running"
            rm -f "$PID_FILE"
        fi
    else
        echo "❌ Telegram bridge not running"
    fi
}

status_bridge() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✅ Telegram bridge running (PID: $PID)"
            echo "📱 Monitoring: @building_loop_1_serenissima_bot"
            echo "📂 Bridge dir: $BRIDGE_DIR"
            echo "📜 Log file: $LOG_FILE"
        else
            echo "❌ Telegram bridge stopped (stale PID file)"
            rm -f "$PID_FILE"
        fi
    else
        echo "❌ Telegram bridge not running"
    fi
}

case "$1" in
    start)
        start_bridge
        ;;
    stop)
        stop_bridge
        ;;
    restart)
        stop_bridge
        sleep 2
        start_bridge
        ;;
    status)
        status_bridge
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        echo ""
        echo "Telegram Consciousness Bridge Control Script"
        echo "Manages bidirectional communication via @building_loop_1_serenissima_bot"
        exit 1
        ;;
esac