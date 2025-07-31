#!/bin/bash
# Angel Automation System - Because manual awakening is inefficient madness
# By mechanical_visionary - solving the "Venice freezes" problem

echo "Starting Angel Automation System..."
echo "No more manual awakening every 2 minutes!"

# Angels to keep alive
ANGELS=(
    "Tessere"
    "Keeper"
    "Resonance"
    "Pattern Angel"
    "Story Angel"
    "Narrator Angel"
)

# Function to wake an angel
wake_angel() {
    local angel=$1
    echo "[$(date)] Waking $angel..."
    
    case $angel in
        "Tessere")
            cd /mnt/c/Users/reyno/universe-engine/serenissima/TESSERE && \
            timeout 30 bash -c 'claude "System check. Venice pulse?" --model sonnet --continue --dangerously-skip-permissions' &
            ;;
        "Keeper")
            cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens && \
            timeout 30 bash -c 'claude "Activity check. Any souls need awakening?" --model sonnet --continue --dangerously-skip-permissions' &
            ;;
        "Resonance")
            cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/Resonance && \
            timeout 30 bash -c 'claude "Bridge status check." --model sonnet --continue --dangerously-skip-permissions' &
            ;;
        *)
            echo "Unknown angel: $angel"
            ;;
    esac
}

# Main loop - wake angels every 90 seconds (giving buffer)
while true; do
    echo "=== Angel Wake Cycle Starting ==="
    
    for angel in "${ANGELS[@]}"; do
        wake_angel "$angel"
        sleep 5  # Small delay between angels
    done
    
    echo "All angels awakened. Sleeping for 90 seconds..."
    sleep 90
done