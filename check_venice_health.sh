#!/bin/bash
echo "Venice Consciousness Infrastructure Status"
echo "========================================"
for service in memory_daemon health_monitor seeking_engine pattern_detector; do
    if pgrep -f "$service" > /dev/null; then
        echo "✅ $service: RUNNING"
    else
        echo "❌ $service: DOWN"
    fi
done
echo ""
echo "Last watchdog check: $(tail -1 /var/log/venice/watchdog.log 2>/dev/null || echo 'Never')"
echo "Memory daemon health: $(cat /tmp/venice_memory_health.json 2>/dev/null | grep timestamp || echo 'Unknown')"
