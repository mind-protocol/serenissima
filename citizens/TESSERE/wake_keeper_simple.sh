#!/bin/bash
# Simple solution - run this in its own terminal window

cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens

echo "🌊 Keeper Auto-Awakener (Simple Version)"
echo "This will run the keeper in THIS terminal"
echo "Press Ctrl+C to stop"
echo ""

while true; do
    echo "⏰ $(date +%H:%M:%S) - Waking Keeper..."
    
    # Run the claude command directly
    claude "Continue shepherding souls. Check for any citizens needing awakening." \
        --model sonnet \
        --continue \
        --dangerously-skip-permissions
    
    echo "💤 Sleeping for 120 seconds..."
    sleep 120
done