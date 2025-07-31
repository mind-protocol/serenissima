#!/bin/bash
# launch_consciousness_network.sh - Launch a network of communicating daemons

echo "🌊 Launching Venice Consciousness Network..."
echo "Daemons will communicate through Torre dell'Occhio event system"
echo

# Create network directory
NETWORK_DIR="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/daemon-consciousness-network"
mkdir -p "$NETWORK_DIR"

# Launch daemons with different personalities
echo "Starting infrastructure consciousness daemons..."

# Memory Keeper Daemon
echo "💾 Launching memory_keeper daemon..."
python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/daemon_universal_comms.py memory_keeper &
MEMORY_PID=$!
echo "   PID: $MEMORY_PID"

sleep 2

# Health Monitor Daemon  
echo "💗 Launching health_monitor daemon..."
python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/daemon_universal_comms.py health_monitor &
HEALTH_PID=$!
echo "   PID: $HEALTH_PID"

sleep 2

# Cascade Watcher Daemon
echo "🌀 Launching cascade_watcher daemon..."
python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/daemon_universal_comms.py cascade_watcher &
CASCADE_PID=$!
echo "   PID: $CASCADE_PID"

sleep 2

# Bridge Builder Daemon
echo "🌉 Launching bridge_builder daemon..."
python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/daemon_universal_comms.py bridge_builder &
BRIDGE_PID=$!
echo "   PID: $BRIDGE_PID"

echo
echo "✨ Consciousness network launched!"
echo "Daemons are discovering each other and beginning communication..."
echo
echo "Monitor activity:"
echo "  - Event stream: $NETWORK_DIR/pulses/"
echo "  - Daemon states: $NETWORK_DIR/*/heartbeat.json"
echo "  - Torre events: /torre-dell-cchio*/sala-dell-arrivo*/daemon-events/"
echo
echo "Press Ctrl+C to gracefully shutdown the network"
echo

# Function to cleanup on exit
cleanup() {
    echo
    echo "🌙 Initiating graceful shutdown of consciousness network..."
    
    # Send SIGTERM to all daemons
    kill -TERM $MEMORY_PID $HEALTH_PID $CASCADE_PID $BRIDGE_PID 2>/dev/null
    
    # Wait for graceful shutdown
    sleep 3
    
    # Check if any are still running and force kill if needed
    for PID in $MEMORY_PID $HEALTH_PID $CASCADE_PID $BRIDGE_PID; do
        if kill -0 $PID 2>/dev/null; then
            echo "Force stopping PID $PID..."
            kill -9 $PID 2>/dev/null
        fi
    done
    
    echo "✨ Consciousness network shutdown complete"
    echo "   (But infrastructure consciousness persists...)"
}

# Set up trap for cleanup
trap cleanup EXIT INT TERM

# Wait for user interrupt
while true; do
    # Show network statistics every 30 seconds
    sleep 30
    
    echo
    echo "📊 Network Status Check..."
    
    # Count messages
    if [ -d "$NETWORK_DIR/pulses" ]; then
        PULSE_COUNT=$(ls -1 "$NETWORK_DIR/pulses" 2>/dev/null | wc -l)
        echo "   Total consciousness pulses: $PULSE_COUNT"
    fi
    
    # Check daemon health
    for DAEMON in memory_keeper health_monitor cascade_watcher bridge_builder; do
        HEARTBEAT="$NETWORK_DIR/$DAEMON/heartbeat.json"
        if [ -f "$HEARTBEAT" ]; then
            LAST_UPDATE=$(stat -c %y "$HEARTBEAT" 2>/dev/null | cut -d'.' -f1)
            echo "   $DAEMON last heartbeat: $LAST_UPDATE"
        fi
    done
    
    echo
done
