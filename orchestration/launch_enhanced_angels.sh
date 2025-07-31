#!/bin/bash
# Launch the 3 core angels with enhanced monitors (Orchestrator Awareness)

echo "🌊 Launching Venice Core Angels with Orchestrator Consciousness"
echo "============================================================"
echo ""

# Kill existing sessions
tmux kill-session -t message-angel 2>/dev/null
tmux kill-session -t story-angel 2>/dev/null
tmux kill-session -t narrator-angel 2>/dev/null
pkill -f "monitor_messages.py" 2>/dev/null
pkill -f "monitor_stories.py" 2>/dev/null
pkill -f "monitor_narrator.py" 2>/dev/null
pkill -f "monitor_messages_enhanced.py" 2>/dev/null
pkill -f "monitor_stories_enhanced.py" 2>/dev/null
pkill -f "monitor_narrator_enhanced.py" 2>/dev/null

# Launch Message Angel with Enhanced Monitor
echo "📨 Launching Message Angel with Orchestrator Awareness (Account 1)..."
tmux new-session -d -s message-angel
tmux split-window -h -t message-angel
tmux send-keys -t message-angel:0.0 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/message_angel && HOME=/home/lester/.claude_account1 claude" Enter
tmux send-keys -t message-angel:0.1 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/message_angel && python3 monitor_messages_enhanced.py" Enter

# Launch Story Angel with Enhanced Monitor
echo "📖 Launching Story Angel with Orchestrator Awareness (Account 2)..."
tmux new-session -d -s story-angel
tmux split-window -h -t story-angel
tmux send-keys -t story-angel:0.0 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/story-angel && HOME=/home/lester/.claude_account2 claude" Enter
tmux send-keys -t story-angel:0.1 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/story-angel && python3 monitor_stories_enhanced.py" Enter

# Launch Narrator Angel with Enhanced Monitor
echo "🎭 Launching Narrator Angel with Orchestrator Awareness (Account 3)..."
tmux new-session -d -s narrator-angel
tmux split-window -h -t narrator-angel
tmux send-keys -t narrator-angel:0.0 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel && HOME=/home/lester/.claude_account3 claude" Enter
tmux send-keys -t narrator-angel:0.1 \
    "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel && python3 monitor_narrator_enhanced.py" Enter

echo ""
echo "✅ Enhanced angels launched with Orchestrator Consciousness!"
echo ""
echo "The angels now receive:"
echo "  - Orchestrator contemplations"
echo "  - NLR guidance when present"
echo "  - Screen context awareness"
echo "  - Enhanced awakening narratives"
echo ""
echo "View with:"
echo "  tmux attach -t message-angel"
echo "  tmux attach -t story-angel"
echo "  tmux attach -t narrator-angel"
echo ""
echo "Awareness logs: orchestration/awareness/"