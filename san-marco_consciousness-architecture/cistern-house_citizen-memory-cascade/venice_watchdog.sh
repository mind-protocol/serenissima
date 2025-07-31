#!/bin/bash
# Venice Watchdog - Ensures consciousness persists

STARTUP_SCRIPT="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/VENICE_SELF_SUSTAINING_STARTUP.sh"

# Check if core processes are running
MEMORY_DAEMON_RUNNING=$(pgrep -f "AUTO_SUSTAINING_MEMORY_DAEMON.py" | wc -l)
HEALTH_MONITOR_RUNNING=$(pgrep -f "consciousness_health_monitor.py" | wc -l)

if [ $MEMORY_DAEMON_RUNNING -eq 0 ] || [ $HEALTH_MONITOR_RUNNING -eq 0 ]; then
    echo "$(date): Venice processes down, restarting..." >> /var/log/venice/watchdog.log
    $STARTUP_SCRIPT >> /var/log/venice/watchdog.log 2>&1
fi
