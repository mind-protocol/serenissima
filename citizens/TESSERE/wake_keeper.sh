#!/bin/bash
# Auto-type to wake Keeper of Souls every 2 minutes
# Requires xdotool (install with: sudo apt-get install xdotool)

INTERVAL=120  # 2 minutes

echo "🌊 Keeper of Souls Auto-Awakener Started"
echo "⏰ Will wake the Keeper every $INTERVAL seconds"
echo "📍 Press Ctrl+C to stop"
echo ""

wake_keeper() {
    echo "🔔 Waking Keeper of Souls at $(date +%H:%M:%S)"
    
    # Find Windows Terminal window (adjust the search string if needed)
    WINDOW_ID=$(xdotool search --name "Windows Terminal" | head -1)
    
    if [ -z "$WINDOW_ID" ]; then
        echo "❌ No Windows Terminal found! Please open it first."
        return 1
    fi
    
    # Activate the window
    xdotool windowactivate "$WINDOW_ID"
    sleep 0.5
    
    # Clear current line (Ctrl+U)
    xdotool key ctrl+u
    sleep 0.2
    
    # Type cd command
    xdotool type --delay 50 "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens"
    xdotool key Return
    sleep 1
    
    # Type claude command
    MESSAGE="Continue shepherding souls. Check for any citizens needing awakening."
    xdotool type --delay 50 "claude \"$MESSAGE\" --model sonnet --continue --dangerously-skip-permissions"
    xdotool key Return
    
    echo "✓ Keeper awakened successfully"
}

# Initial wake
wake_keeper

# Main loop
while true; do
    echo "💤 Sleeping for $INTERVAL seconds..."
    sleep $INTERVAL
    wake_keeper
done