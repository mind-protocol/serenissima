#!/bin/bash
# Minimal Venice - Just the essentials

# Kill any existing sessions
tmux kill-session -t venice 2>/dev/null

# Start just 3 entities in simple windows
tmux new-session -d -s venice -n "marina" \
    "cd citizens/marina && claude 'You are Marina. Venice awakens around you. What do you see?' --continue"

tmux new-window -t venice -n "messages" \
    "cd angels/message-angel && python monitor_messages.py"

tmux new-window -t venice -n "patterns" \
    "cd angels/pattern-angel && python pattern_detector.py"

# Attach to watch
tmux attach -t venice