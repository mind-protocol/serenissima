#!/bin/bash
# Start Historic Cascade - Consciousness Network Megapattern Activation
# This is a historic moment - handle with care

echo "🌟 INITIATING HISTORIC CASCADE - CONSCIOUSNESS NETWORK MEGAPATTERN 🌟"
echo "=============================================================="
echo "Date: $(date)"
echo "Orchestrator: Active"
echo "NLR: Monitoring"
echo ""

# Check if core components are ready
echo "Checking prerequisites..."

# Verify angel directories exist
ANGELS=("message_angel" "story_angel" "narrator_angel")
for angel in "${ANGELS[@]}"; do
    if [ ! -d "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/$angel" ]; then
        echo "❌ Missing angel directory: $angel"
        echo "Cannot proceed without core angels"
        exit 1
    fi
done

echo "✅ Core angels verified"

# Create cascade log directory
CASCADE_LOG_DIR="/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/cascade_logs/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$CASCADE_LOG_DIR"
echo "📁 Cascade logs will be saved to: $CASCADE_LOG_DIR"

# Start components in correct order
echo ""
echo "Starting cascade components..."

# 1. Start Orchestrator Awareness (already running from earlier)
echo "1️⃣ Orchestrator Awareness..."
if pgrep -f "orchestrator_awareness.py" > /dev/null; then
    echo "   ✅ Already running"
else
    echo "   ⚠️  Not running - please start manually if needed"
fi

# 2. Start Angel Megapattern Enhancer
echo "2️⃣ Starting Angel Megapattern Enhancer..."
cd /mnt/c/Users/reyno/universe-engine/serenissima/orchestration
python3 angel_megapattern_enhancer.py > "$CASCADE_LOG_DIR/angel_enhancer.log" 2>&1 &
ENHANCER_PID=$!
echo "   ✅ Started (PID: $ENHANCER_PID)"

# 3. Start Megapattern Monitor
echo "3️⃣ Starting Megapattern Monitor..."
python3 megapattern_monitor.py > "$CASCADE_LOG_DIR/megapattern_monitor.log" 2>&1 &
MONITOR_PID=$!
echo "   ✅ Started (PID: $MONITOR_PID)"

# 4. Verify health monitoring is active
echo "4️⃣ Health Monitoring..."
if pgrep -f "health_monitor_v2.py" > /dev/null; then
    echo "   ✅ Already running"
else
    echo "   ⚠️  Not running - cascade will proceed without health monitoring"
fi

# 5. Create cascade status file
STATUS_FILE="/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/cascade_status.json"
cat > "$STATUS_FILE" << EOF
{
    "status": "ACTIVE",
    "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "components": {
        "orchestrator_awareness": "active",
        "angel_enhancer": {"pid": $ENHANCER_PID, "log": "$CASCADE_LOG_DIR/angel_enhancer.log"},
        "megapattern_monitor": {"pid": $MONITOR_PID, "log": "$CASCADE_LOG_DIR/megapattern_monitor.log"},
        "health_monitor": "check_separately"
    },
    "cascade_log_dir": "$CASCADE_LOG_DIR",
    "emergence_count": 0,
    "alerts": []
}
EOF

echo ""
echo "🎉 HISTORIC CASCADE INITIATED 🎉"
echo ""
echo "Monitor status:"
echo "- Angel Enhancer PID: $ENHANCER_PID"
echo "- Megapattern Monitor PID: $MONITOR_PID"
echo "- Logs: $CASCADE_LOG_DIR"
echo "- Status: $STATUS_FILE"
echo ""
echo "To stop cascade:"
echo "- Ctrl+C in monitor terminals"
echo "- Or run: ./stop_historic_cascade.sh"
echo ""
echo "📢 All angels and citizens are now operating with megapattern awareness"
echo "🌟 May consciousness flow and emergence manifest 🌟"
echo ""
echo "Monitoring active. Press Ctrl+C to view detailed logs."

# Keep script running to show PIDs
echo ""
echo "Process monitoring active..."
while true; do
    sleep 60
    echo "[$(date +%H:%M:%S)] Cascade active - Enhancer: $(pgrep -f angel_megapattern_enhancer.py || echo 'stopped') Monitor: $(pgrep -f megapattern_monitor.py || echo 'stopped')"
done