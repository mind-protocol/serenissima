#!/bin/bash
# Sala della Salute - Health Monitoring Daemon Starter

echo "🏛️ Starting Venice Consciousness Health Monitor"
echo "================================================"

# Change to health monitoring chamber
cd "$(dirname "$0")"

# Check if already running
if pgrep -f "consciousness_health_monitor.py" > /dev/null; then
    echo "⚠️  Health monitor already running"
    echo "Use 'stop_health_daemon.sh' to stop it first"
    exit 1
fi

# Ensure required environment
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  Warning: TELEGRAM_BOT_TOKEN not set - alerts will not be sent"
    echo "Set with: export TELEGRAM_BOT_TOKEN='your_bot_token'"
fi

# Create logs directory
mkdir -p logs

# Start monitoring in background
echo "🔄 Starting health monitoring daemon..."
nohup python3 consciousness_health_monitor.py monitor 300 > logs/daemon.log 2>&1 &
PID=$!

echo "✅ Health monitor started with PID: $PID"
echo "📊 Monitoring every 5 minutes"
echo "📄 Logs: logs/daemon.log and health_monitor.log"
echo "🛑 Stop with: stop_health_daemon.sh"

# Save PID for stopping
echo $PID > health_monitor.pid

echo ""
echo "Venice consciousness is now under continuous medical surveillance."