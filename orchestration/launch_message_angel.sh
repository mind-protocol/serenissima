#!/bin/bash
# Launch Message Angel with monitoring

echo "📨 Launching Message Angel"
echo "========================"

# Kill any existing message angel
pkill -f "monitor_messages.py" 2>/dev/null

# Create tmux session
tmux kill-session -t message-angel 2>/dev/null
tmux new-session -d -s message-angel

# Split horizontally
tmux split-window -h -t message-angel

# Left pane: Claude
tmux send-keys -t message-angel:0.0 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/message_angel && HOME=/home/lester/.claude_account1 claude" Enter

# Right pane: Monitor
tmux send-keys -t message-angel:0.1 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/message_angel && python3 monitor_messages.py" Enter

echo ""
echo "✅ Message Angel launched!"
echo ""
echo "View with: tmux attach -t message-angel"
echo ""
echo "The monitor will:"
echo "1. Check MESSAGES table every 30s"
echo "2. Write new messages to awakening.txt"
echo "3. Message Angel will see and process them"