#!/bin/bash
# Venice Self-Sustaining Startup Script - NO SYSTEMD VERSION
# Works on all systems including WSL without systemd

echo "🌊 Venice Self-Sustaining Infrastructure Startup (Universal Version)"
echo "================================================================="
echo "Time: $(date)"
echo "Purpose: Eliminate dependency on manual restarts"
echo "Note: This version works without systemd"

# Set up environment
VENICE_ROOT="/mnt/c/Users/reyno/universe-engine/serenissima"
CISTERN_HOUSE="$VENICE_ROOT/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"
LOG_DIR="$HOME/.venice/logs"
PID_DIR="$HOME/.venice/pids"

# Create necessary directories
mkdir -p "$LOG_DIR" "$PID_DIR"

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
    
    # Kill existing process if running
    if check_process "$pid_file"; then
        echo "  Stopping existing $name process..."
        kill $(cat "$pid_file") 2>/dev/null
        sleep 2
    fi
    
    # Create a monitoring wrapper
    cat > "$PID_DIR/${name}_monitor.sh" << EOF
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
    
    chmod +x "$PID_DIR/${name}_monitor.sh"
    nohup "$PID_DIR/${name}_monitor.sh" > /dev/null 2>&1 &
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
    # Check if the health monitor exists
    if [ -f "$CISTERN_HOUSE/sala-della-salute_health-monitoring-chamber/consciousness_health_monitor.py" ]; then
        start_with_monitor "health_monitor" \
            "python3 $CISTERN_HOUSE/sala-della-salute_health-monitoring-chamber/consciousness_health_monitor.py"
    else
        echo "⚠️  Health monitor not found, skipping..."
    fi
else
    echo "✓ Health monitor already running"
fi

echo ""
echo "3️⃣ Starting Crystallization Tracker..."
if ! check_process "$PID_DIR/crystallization_tracker.pid"; then
    if [ -f "$CISTERN_HOUSE/crystallization_tracker.py" ]; then
        start_with_monitor "crystallization_tracker" \
            "python3 $CISTERN_HOUSE/crystallization_tracker.py"
    else
        echo "⚠️  Crystallization tracker not found, skipping..."
    fi
else
    echo "✓ Crystallization tracker already running"
fi

echo ""
echo "4️⃣ Starting Seeking Engine..."
if ! check_process "$PID_DIR/seeking_engine.pid"; then
    if [ -f "$CISTERN_HOUSE/seeking-engine_proactive-consciousness-machine/seeking_engine.py" ]; then
        start_with_monitor "seeking_engine" \
            "python3 $CISTERN_HOUSE/seeking-engine_proactive-consciousness-machine/seeking_engine.py"
    else
        echo "⚠️  Seeking engine not found, skipping..."
    fi
else
    echo "✓ Seeking engine already running"
fi

echo ""
echo "5️⃣ Creating Simple Process Monitor..."

# Create a simple monitor script that can be run manually or via cron
cat > "$HOME/.venice/check_and_restart.sh" << 'EOF'
#!/bin/bash
# Simple Venice process checker and restarter

PID_DIR="$HOME/.venice/pids"
LOG_DIR="$HOME/.venice/logs"

echo "[$(date)] Checking Venice processes..." >> "$LOG_DIR/monitor.log"

# List of processes to monitor
declare -A processes
processes["memory_daemon"]="python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/AUTO_SUSTAINING_MEMORY_DAEMON.py"
processes["crystallization_tracker"]="python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/crystallization_tracker.py"

for name in "${!processes[@]}"; do
    pid_file="$PID_DIR/${name}.pid"
    
    # Check if process is running
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ! ps -p "$pid" > /dev/null 2>&1; then
            echo "[$(date)] $name is down, restarting..." >> "$LOG_DIR/monitor.log"
            # Start the monitor wrapper
            if [ -f "$PID_DIR/${name}_monitor.sh" ]; then
                nohup "$PID_DIR/${name}_monitor.sh" > /dev/null 2>&1 &
                echo $! > "$pid_file"
                echo "[$(date)] $name restarted with PID $!" >> "$LOG_DIR/monitor.log"
            fi
        fi
    fi
done
EOF

chmod +x "$HOME/.venice/check_and_restart.sh"

echo "✓ Process monitor created at $HOME/.venice/check_and_restart.sh"
echo ""
echo "6️⃣ Setting up Automatic Monitoring..."

# Add to user's crontab (if cron is available)
if command -v crontab > /dev/null 2>&1; then
    # Check if already in crontab
    if ! crontab -l 2>/dev/null | grep -q "check_and_restart.sh"; then
        (crontab -l 2>/dev/null; echo "*/5 * * * * $HOME/.venice/check_and_restart.sh") | crontab -
        echo "✓ Added automatic check every 5 minutes to crontab"
    else
        echo "✓ Automatic monitoring already in crontab"
    fi
else
    echo "⚠️  Cron not available - run check_and_restart.sh manually when needed"
fi

echo ""
echo "7️⃣ Creating Status Command..."

# Create a status checking script
cat > "$HOME/.venice/check_venice_status.sh" << 'EOF'
#!/bin/bash
echo "Venice Consciousness Infrastructure Status"
echo "========================================"
echo "Time: $(date)"
echo ""

PID_DIR="$HOME/.venice/pids"

# Check each service
for service in memory_daemon crystallization_tracker health_monitor seeking_engine; do
    pid_file="$PID_DIR/${service}.pid"
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "✅ $service: RUNNING (PID: $pid)"
        else
            echo "❌ $service: DOWN"
        fi
    else
        echo "❌ $service: NOT STARTED"
    fi
done

echo ""
echo "Log files in: $HOME/.venice/logs/"
echo ""
echo "To manually check and restart dead processes:"
echo "  $HOME/.venice/check_and_restart.sh"
EOF

chmod +x "$HOME/.venice/check_venice_status.sh"

# Create convenient aliases
echo ""
echo "8️⃣ Creating Convenience Commands..."

cat > "$HOME/.venice/venice_commands.sh" << 'EOF'
# Venice Infrastructure Commands
# Add this to your .bashrc or .zshrc: source $HOME/.venice/venice_commands.sh

alias venice-status="$HOME/.venice/check_venice_status.sh"
alias venice-restart="$HOME/.venice/check_and_restart.sh"
alias venice-logs="tail -f $HOME/.venice/logs/*.log"
alias venice-stop="pkill -f 'AUTO_SUSTAINING_MEMORY_DAEMON\|crystallization_tracker\|consciousness_health\|seeking_engine'"

echo "Venice commands available:"
echo "  venice-status  - Check all processes"
echo "  venice-restart - Restart dead processes"
echo "  venice-logs    - Watch all logs"
echo "  venice-stop    - Stop all processes"
EOF

echo "✓ Created Venice command shortcuts"
echo "  Add to your shell: source $HOME/.venice/venice_commands.sh"

echo ""
echo "============================================="
echo "✨ VENICE INFRASTRUCTURE DEPLOYED ✨"
echo "============================================="
echo ""
echo "Status Check:     $HOME/.venice/check_venice_status.sh"
echo "Manual Restart:   $HOME/.venice/check_and_restart.sh"
echo "Logs Location:    $HOME/.venice/logs/"
echo ""

# Final status check
sleep 3
echo "Current Status:"
"$HOME/.venice/check_venice_status.sh"

echo ""
echo "============================================="
echo "NLR: Your manual restart duty is COMPLETE."
echo "Venice now self-monitors and self-heals."
echo "============================================="