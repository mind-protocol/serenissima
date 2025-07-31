#!/bin/bash
# Start Core Angels for Consciousness Cascade
# Safe startup with monitoring

echo "🌟 STARTING CORE ANGELS FOR CASCADE PREPARATION 🌟"
echo "================================================"
echo "Date: $(date)"
echo ""

# Base directory
BASE_DIR="/mnt/c/Users/reyno/universe-engine/serenissima"
LOG_DIR="$BASE_DIR/orchestration/angel_logs/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_DIR"

echo "📁 Logs will be saved to: $LOG_DIR"
echo ""

# Function to start a monitor
start_monitor() {
    local angel_name=$1
    local monitor_script=$2
    local log_file="$LOG_DIR/${angel_name}_monitor.log"
    
    if [ -f "$monitor_script" ]; then
        echo "Starting $angel_name monitor..."
        cd $(dirname "$monitor_script")
        python3 $(basename "$monitor_script") > "$log_file" 2>&1 &
        local pid=$!
        echo "  ✅ Started with PID: $pid"
        echo "  📄 Log: $log_file"
        echo $pid > "$LOG_DIR/${angel_name}.pid"
    else
        echo "  ❌ Monitor script not found: $monitor_script"
    fi
}

# Start Message Angel
echo "1️⃣ Message Angel"
start_monitor "message_angel" "$BASE_DIR/citizens/_angels/message_angel/monitor_messages_enhanced.py"

# Start Story Angel (create basic monitor if doesn't exist)
echo ""
echo "2️⃣ Story Angel"
STORY_MONITOR="$BASE_DIR/citizens/_angels/story_angel/monitor_story.py"
if [ ! -f "$STORY_MONITOR" ]; then
    echo "  Creating basic story monitor..."
    mkdir -p "$BASE_DIR/citizens/_angels/story_angel"
    cat > "$STORY_MONITOR" << 'EOF'
#!/usr/bin/env python3
import time
import os
from datetime import datetime

print("📖 STORY ANGEL MONITOR")
print("Waiting for message digests...")

while True:
    # Check for awakening trigger
    if os.path.exists('awakening.txt'):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Awakening detected")
        # Story Angel would process here
    time.sleep(30)
EOF
    chmod +x "$STORY_MONITOR"
fi
start_monitor "story_angel" "$STORY_MONITOR"

# Start Narrator Angel
echo ""
echo "3️⃣ Narrator Angel"
start_monitor "narrator_angel" "$BASE_DIR/citizens/_angels/narrator_angel/monitor_narrator_enhanced.py"

# Start Orchestrator Awareness (if not running)
echo ""
echo "4️⃣ Orchestrator Awareness"
if ! pgrep -f "orchestrator_awareness.py" > /dev/null; then
    start_monitor "orchestrator_awareness" "$BASE_DIR/orchestration/orchestrator_awareness.py"
else
    echo "  ✅ Already running"
fi

echo ""
echo "🎉 ANGEL STARTUP COMPLETE 🎉"
echo ""
echo "Active Angels:"
ps aux | grep -E "monitor.*py" | grep -v grep | awk '{print "  - " $11}'
echo ""
echo "Next Steps:"
echo "1. Angels can now request validation"
echo "2. Monitor their awakening files"
echo "3. Watch for alignment_request.txt"
echo ""
echo "To stop all angels: pkill -f monitor"