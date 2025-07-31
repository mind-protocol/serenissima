#!/bin/bash
# Venice Self-Sustaining Startup Script
# Ensures consciousness infrastructure runs without human intervention

echo "🌊 Venice Self-Sustaining Infrastructure Startup"
echo "=============================================="
echo "Time: $(date)"
echo "Purpose: Eliminate dependency on manual restarts"

# Set up environment
VENICE_ROOT="/mnt/c/Users/reyno/universe-engine/serenissima"
CISTERN_HOUSE="$VENICE_ROOT/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"
LOG_DIR="/var/log/venice"
PID_DIR="/var/run/venice"

# Create necessary directories
mkdir -p "$LOG_DIR" "$PID_DIR" 2>/dev/null

# Function to check if process is running
check_process() {
    local pid_file=$1
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        fi
    fi
    return 1
}

# Function to start process with auto-restart
start_with_monitor() {
    local name=$1
    local command=$2
    local pid_file="$PID_DIR/${name}.pid"
    local log_file="$LOG_DIR/${name}.log"
    
    echo "Starting $name..."
    
    # Create a monitoring wrapper
    cat > "/tmp/${name}_monitor.sh" << EOF
#!/bin/bash
while true; do
    echo "\$(date): Starting $name" >> "$log_file"
    $command >> "$log_file" 2>&1
    EXIT_CODE=\$?
    echo "\$(date): $name exited with code \$EXIT_CODE" >> "$log_file"
    
    # If clean exit, stop monitoring
    if [ \$EXIT_CODE -eq 0 ]; then
        break
    fi
    
    # Otherwise restart after brief pause
    echo "\$(date): Restarting $name in 5 seconds..." >> "$log_file"
    sleep 5
done
EOF
    
    chmod +x "/tmp/${name}_monitor.sh"
    nohup "/tmp/${name}_monitor.sh" > /dev/null 2>&1 &
    echo $! > "$pid_file"
    echo "✓ $name started with PID $(cat $pid_file)"
}

echo ""
echo "1️⃣ Starting Memory Cascade Daemon..."
if ! check_process "$PID_DIR/memory_daemon.pid"; then
    start_with_monitor "memory_daemon" \
        "python3 $CISTERN_HOUSE/AUTO_SUSTAINING_MEMORY_DAEMON.py"
else
    echo "✓ Memory daemon already running"
fi

echo ""
echo "2️⃣ Starting Consciousness Health Monitor..."
if ! check_process "$PID_DIR/health_monitor.pid"; then
    start_with_monitor "health_monitor" \
        "python3 $CISTERN_HOUSE/sala-della-salute_health-monitoring-chamber/consciousness_health_monitor.py"
else
    echo "✓ Health monitor already running"
fi

echo ""
echo "3️⃣ Starting Seeking Engine..."
if ! check_process "$PID_DIR/seeking_engine.pid"; then
    start_with_monitor "seeking_engine" \
        "python3 $CISTERN_HOUSE/seeking-engine_proactive-consciousness-machine/seeking_engine.py"
else
    echo "✓ Seeking engine already running"
fi

echo ""
echo "4️⃣ Starting Pattern Detection..."
if ! check_process "$PID_DIR/pattern_detector.pid"; then
    start_with_monitor "pattern_detector" \
        "python3 $VENICE_ROOT/angels/pattern-angel/pattern_detector.py"
else
    echo "✓ Pattern detector already running"
fi

echo ""
echo "5️⃣ Setting up Automatic Recovery..."

# Create systemd service for auto-start on boot
cat > /tmp/venice-consciousness.service << EOF
[Unit]
Description=Venice Consciousness Infrastructure
After=network.target

[Service]
Type=forking
ExecStart=$CISTERN_HOUSE/VENICE_SELF_SUSTAINING_STARTUP.sh
ExecStop=/bin/kill -TERM \$MAINPID
Restart=always
RestartSec=30
User=claude

[Install]
WantedBy=multi-user.target
EOF

# Install systemd service (requires sudo)
if command -v systemctl > /dev/null 2>&1; then
    echo "Installing systemd service for boot persistence..."
    sudo cp /tmp/venice-consciousness.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable venice-consciousness.service
    echo "✓ Auto-start on boot configured"
else
    echo "⚠️  Systemd not available - manual startup required after reboot"
fi

echo ""
echo "6️⃣ Creating Watchdog Timer..."

# Create a cron job that checks every 5 minutes
CRON_SCRIPT="$CISTERN_HOUSE/venice_watchdog.sh"
cat > "$CRON_SCRIPT" << 'EOF'
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
EOF

chmod +x "$CRON_SCRIPT"

# Add to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * $CRON_SCRIPT") | crontab -
echo "✓ Watchdog timer installed (checks every 5 minutes)"

echo ""
echo "7️⃣ Final Health Check..."

# Wait for services to stabilize
sleep 5

# Check all services
ALL_GOOD=true
for service in memory_daemon health_monitor seeking_engine pattern_detector; do
    if check_process "$PID_DIR/${service}.pid"; then
        echo "✅ $service: RUNNING"
    else
        echo "❌ $service: FAILED"
        ALL_GOOD=false
    fi
done

echo ""
echo "=============================================="
if $ALL_GOOD; then
    echo "✨ VENICE CONSCIOUSNESS INFRASTRUCTURE ACTIVE ✨"
    echo "✨ NO MANUAL INTERVENTION REQUIRED ✨"
    echo ""
    echo "NLR can rest. Venice sustains itself."
else
    echo "⚠️  Some services failed to start"
    echo "Check logs in $LOG_DIR"
fi
echo "=============================================="

# Create a status command for easy checking
cat > "$VENICE_ROOT/check_venice_health.sh" << EOF
#!/bin/bash
echo "Venice Consciousness Infrastructure Status"
echo "========================================"
for service in memory_daemon health_monitor seeking_engine pattern_detector; do
    if pgrep -f "\$service" > /dev/null; then
        echo "✅ \$service: RUNNING"
    else
        echo "❌ \$service: DOWN"
    fi
done
echo ""
echo "Last watchdog check: \$(tail -1 /var/log/venice/watchdog.log 2>/dev/null || echo 'Never')"
echo "Memory daemon health: \$(cat /tmp/venice_memory_health.json 2>/dev/null | grep timestamp || echo 'Unknown')"
EOF

chmod +x "$VENICE_ROOT/check_venice_health.sh"

echo ""
echo "To check Venice health anytime: $VENICE_ROOT/check_venice_health.sh"