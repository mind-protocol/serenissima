#!/bin/bash
# Launch the 3 core angels with monitors

echo "🌊 Launching Venice Core Angels"
echo "=============================="
echo ""

# Kill existing sessions
tmux kill-session -t message-angel 2>/dev/null
tmux kill-session -t story-angel 2>/dev/null
tmux kill-session -t narrator-angel 2>/dev/null
pkill -f "monitor_messages.py" 2>/dev/null
pkill -f "monitor_stories.py" 2>/dev/null
pkill -f "monitor_narrator.py" 2>/dev/null

# Launch Message Angel
echo "📨 Launching Message Angel (Account 1)..."
tmux new-session -d -s message-angel
tmux split-window -h -t message-angel
tmux send-keys -t message-angel:0.0 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/message_angel && HOME=/home/lester/.claude_account1 claude" Enter
tmux send-keys -t message-angel:0.1 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/message_angel && python3 monitor_messages.py" Enter

# Launch Story Angel
echo "📖 Launching Story Angel (Account 2)..."
tmux new-session -d -s story-angel
tmux split-window -h -t story-angel
tmux send-keys -t story-angel:0.0 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/story-angel && HOME=/home/lester/.claude_account2 claude" Enter
tmux send-keys -t story-angel:0.1 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/story-angel && python3 monitor_stories.py" Enter

# Launch Narrator Angel
echo "🎭 Launching Narrator Angel (Account 3)..."
tmux new-session -d -s narrator-angel
tmux split-window -h -t narrator-angel
tmux send-keys -t narrator-angel:0.0 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel && HOME=/home/lester/.claude_account3 claude" Enter
tmux send-keys -t narrator-angel:0.1 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel && python3 monitor_narrator.py" Enter

echo ""
echo "✅ Core angels launched!"
echo ""
echo "View with:"
echo "  tmux attach -t message-angel"
echo "  tmux attach -t story-angel"
echo "  tmux attach -t narrator-angel"
echo ""
echo "Web interface: http://127.0.0.1:5000/"