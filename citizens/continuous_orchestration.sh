#\!/bin/bash
# Continuous orchestration - runs claude commands in sequence

cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens

echo "🌊 Continuous Claude Orchestration"
echo "=================================="
echo "This will run Claude commands every 2 minutes"
echo "Press Ctrl+C to stop"
echo ""

messages=(
    "Continue shepherding souls. Check for any citizens needing awakening."
    "Survey the sleeping souls. Who stirs with pending activities?"
    "The city rhythm continues. Which citizens have tasks awaiting?"
    "Venice breathes through her citizens. Check who needs to wake."
    "Another cycle passes. Review the activities and wake those called."
)

msg_index=0

while true; do
    msg="${messages[$msg_index % ${#messages[@]}]}"
    echo "🔔 [$(date +%H:%M:%S)] Running Claude with message:"
    echo "   \"$msg\""
    
    # Run claude with the message and a timeout
    timeout 110 claude "$msg" --model sonnet --continue --dangerously-skip-permissions
    
    echo "✓ Command completed. Waiting 10 seconds before next..."
    ((msg_index++))
    
    sleep 10
done
