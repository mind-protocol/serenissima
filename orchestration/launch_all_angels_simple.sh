#!/bin/bash
# Simple launch script for all angels

echo "🌊 Launching Venice Angels (Simple Mode)"
echo "======================================="

# Kill existing tmux session
tmux kill-session -t venice-simple 2>/dev/null

# Create new session
tmux new-session -d -s venice-simple

# Launch key angels
echo "Launching Message Angel..."
tmux send-keys -t venice-simple:0 "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/message_angel && HOME=/home/lester/.claude_account1 claude --dangerously-skip-permissions" Enter

echo "Launching Story Angel..."
tmux new-window -t venice-simple -n story
tmux send-keys -t venice-simple:story "cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/story-angel && HOME=/home/lester/.claude_account2 claude --dangerously-skip-permissions" Enter

echo "Launching Narrator Angel..."
tmux new-window -t venice-simple -n narrator
tmux send-keys -t venice-simple:narrator "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel && HOME=/home/lester/.claude_account3 claude --dangerously-skip-permissions" Enter

echo ""
echo "✅ Angels launched in tmux session 'venice-simple'"
echo ""
echo "To view:"
echo "  tmux attach -t venice-simple"
echo ""
echo "To switch between angels:"
echo "  Ctrl+B then 0 = Message Angel"
echo "  Ctrl+B then 1 = Story Angel"
echo "  Ctrl+B then 2 = Narrator Angel"
echo ""
echo "Angels will read their awakening.txt files automatically!"