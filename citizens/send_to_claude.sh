#!/bin/bash
# Send messages to Claude through the named pipe

FIFO_PATH="/tmp/claude_input_fifo"

if [ ! -p "$FIFO_PATH" ]; then
    echo "❌ Error: Named pipe not found at $FIFO_PATH"
    echo "Run ./claude_feeder.sh first!"
    exit 1
fi

echo "🌊 Claude Message Sender"
echo "======================="
echo "Sending messages to Claude every 2 minutes"
echo "Press Ctrl+C to stop"
echo ""

messages=(
    "Continue shepherding souls. Check for any citizens needing awakening."
    "Survey the sleeping souls. Who stirs with pending activities?"
    "The city's rhythm continues. Which citizens have tasks awaiting?"
    "Venice breathes through her citizens. Check who needs to wake."
    "Another cycle passes. Review the activities and wake those called."
)

msg_index=0

while true; do
    msg="${messages[$msg_index % ${#messages[@]}]}"
    echo "🔔 [$(date +%H:%M:%S)] Sending: $msg"
    
    # Send to the named pipe
    echo "$msg" > "$FIFO_PATH"
    
    ((msg_index++))
    
    echo "💤 Waiting 120 seconds..."
    sleep 120
done