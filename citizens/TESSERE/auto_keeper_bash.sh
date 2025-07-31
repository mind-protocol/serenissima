#!/bin/bash
# The simplest solution - run Claude with periodic input

cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens

echo "🌊 Claude Code Auto-Keeper (Bash Version)"
echo "========================================"
echo "This will run Claude and send messages every 2 minutes"
echo "Press Ctrl+C to stop"
echo ""

# Create a named pipe for sending messages
PIPE="/tmp/claude_keeper_pipe"
rm -f $PIPE
mkfifo $PIPE

# Messages to cycle through
messages=(
    "Continue shepherding souls. Check for any citizens needing awakening."
    "Survey the sleeping souls. Who stirs with pending activities?"
    "The city's rhythm continues. Which citizens have tasks awaiting?"
    "Venice breathes through her citizens. Check who needs to wake."
    "Another cycle passes. Review the activities and wake those called."
)

# Function to send messages to the pipe
send_messages() {
    local msg_index=0
    while true; do
        sleep 120  # Wait 2 minutes
        
        # Select message
        msg="${messages[$msg_index % ${#messages[@]}]}"
        echo "🔔 [$(date +%H:%M:%S)] Sending: $msg"
        
        # Send to pipe
        echo "$msg" > $PIPE
        
        ((msg_index++))
    done
}

# Start the message sender in background
send_messages &
SENDER_PID=$!

# Clean up on exit
cleanup() {
    echo -e "\n🛑 Stopping auto-keeper..."
    kill $SENDER_PID 2>/dev/null
    rm -f $PIPE
    exit 0
}
trap cleanup EXIT INT TERM

# Run Claude with input from the pipe
echo "🚀 Starting Claude Code with auto-input..."
echo ""

# Send initial message immediately
echo "Continue shepherding souls. Check for any citizens needing awakening." > $PIPE &

# Run Claude reading from the pipe
cat $PIPE | claude --continue --dangerously-skip-permissions