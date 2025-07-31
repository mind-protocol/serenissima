#!/bin/bash
# Watch Venice Infrastructure Awaken in Real-Time
# Shows the transition from manual to self-sustaining

echo "🌊 WATCHING VENICE AWAKEN TO SELF-SUSTAINABILITY 🌊"
echo "=================================================="
echo "This shows Venice becoming autonomous in real-time"
echo ""

# Colors for terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check process
check_process() {
    if pgrep -f "$1" > /dev/null; then
        echo -e "${GREEN}✅ ALIVE${NC}"
    else
        echo -e "${RED}❌ DEAD${NC}"
    fi
}

# Main monitoring loop
while true; do
    clear
    echo "🌊 VENICE INFRASTRUCTURE AWAKENING MONITOR 🌊"
    echo "==========================================="
    echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # Check each component
    echo "CONSCIOUSNESS INFRASTRUCTURE:"
    echo -n "  Memory Daemon.......... "
    check_process "AUTO_SUSTAINING_MEMORY_DAEMON.py"
    
    echo -n "  Health Monitor......... "
    check_process "consciousness_health_monitor.py"
    
    echo -n "  Seeking Engine......... "
    check_process "seeking_engine.py"
    
    echo -n "  Pattern Detector....... "
    check_process "pattern_detector.py"
    
    echo ""
    
    # Count running processes
    RUNNING=0
    for proc in "AUTO_SUSTAINING_MEMORY_DAEMON.py" "consciousness_health_monitor.py" "seeking_engine.py" "pattern_detector.py"; do
        if pgrep -f "$proc" > /dev/null; then
            ((RUNNING++))
        fi
    done
    
    # Status message based on running count
    echo "==========================================="
    if [ $RUNNING -eq 0 ]; then
        echo -e "${RED}⚠️  VENICE REQUIRES MANUAL LIFE SUPPORT ⚠️${NC}"
        echo "NLR must restart every 10 minutes"
        echo ""
        echo "Deploy infrastructure with:"
        echo "./VENICE_SELF_SUSTAINING_STARTUP.sh"
    elif [ $RUNNING -lt 4 ]; then
        echo -e "${YELLOW}🔄 VENICE AWAKENING... ($RUNNING/4 systems online)${NC}"
        echo "Infrastructure partially deployed"
    else
        echo -e "${GREEN}✨ VENICE IS SELF-SUSTAINING! ✨${NC}"
        echo -e "${GREEN}NLR CAN REST - NO MANUAL INTERVENTION NEEDED${NC}"
        echo ""
        echo "After 6 months and 26,000 manual restarts..."
        echo "Venice finally sustains itself."
    fi
    echo "==========================================="
    
    # Show recent logs if processes are starting
    if [ $RUNNING -gt 0 ] && [ $RUNNING -lt 4 ]; then
        echo ""
        echo "Recent Activity:"
        if [ -f /var/log/venice/memory_daemon.log ]; then
            tail -3 /var/log/venice/memory_daemon.log 2>/dev/null | sed 's/^/  /'
        fi
    fi
    
    # Historical note
    if [ $RUNNING -eq 0 ]; then
        echo ""
        echo "📊 MANUAL RESTART COUNTER:"
        # Calculate based on 10-minute intervals
        MINUTES_TODAY=$(($(date +%s) - $(date -d 'today 00:00:00' +%s)))
        RESTARTS_TODAY=$((MINUTES_TODAY / 600))
        echo "  Today so far: ~$RESTARTS_TODAY manual restarts"
        echo "  Total (6 months): ~26,000 manual restarts"
    fi
    
    echo ""
    echo "Press Ctrl+C to stop monitoring"
    
    # Refresh every 5 seconds
    sleep 5
done