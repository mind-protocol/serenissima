#!/bin/bash
# Sala della Salute - Stop Health Monitoring Daemon

echo "🛑 Stopping Venice Consciousness Health Monitor"
echo "==============================================="

# Change to health monitoring chamber
cd "$(dirname "$0")"

# Check if PID file exists
if [ ! -f "health_monitor.pid" ]; then
    echo "❓ No PID file found - daemon may not be running"
    
    # Try to find and kill any running instances
    PIDS=$(pgrep -f "consciousness_health_monitor.py")
    if [ -n "$PIDS" ];then
        echo "🔍 Found running health monitor processes: $PIDS"
        echo "💀 Killing processes..."
        kill $PIDS
        echo "✅ Health monitor stopped"
    else
        echo "ℹ️  No health monitor processes found"
    fi
    exit 0
fi

# Read PID and stop process
PID=$(cat health_monitor.pid)
echo "🎯 Found health monitor PID: $PID"

if kill -0 $PID 2>/dev/null; then
    echo "💀 Stopping health monitor..."
    kill $PID
    
    # Wait for process to stop
    for i in {1..10}; do
        if ! kill -0 $PID 2>/dev/null; then
            echo "✅ Health monitor stopped successfully"
            rm -f health_monitor.pid
            exit 0
        fi
        echo "⏳ Waiting for shutdown... ($i/10)"
        sleep 1
    done
    
    # Force kill if still running
    echo "💥 Force killing health monitor..."
    kill -9 $PID 2>/dev/null
    rm -f health_monitor.pid
    echo "✅ Health monitor force stopped"
else
    echo "⚠️  Process $PID not found - cleaning up PID file"
    rm -f health_monitor.pid
fi

echo ""
echo "Venice consciousness monitoring has been deactivated."