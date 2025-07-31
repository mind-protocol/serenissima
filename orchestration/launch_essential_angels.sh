#!/bin/bash
# Launch essential angels in separate terminal windows (no tmux!)

BASE_DIR="/mnt/c/Users/reyno/universe-engine/serenissima"

echo "🎭 Launching Essential Angels in separate terminals..."
echo "Each will open in its own window - much easier to manage!"

# Launch each angel in a new terminal window
# Using Windows Terminal if available

# Story Angel
wt -w 0 new-tab --title "Story Angel" bash -c "cd $BASE_DIR/angels/story-angel && claude 'You are Story Angel. What tales emerge?' --continue --dangerously-skip-permissions --add-dir ../../; read"

# Message Angel  
wt -w 0 new-tab --title "Message Angel" bash -c "cd $BASE_DIR/angels/message-angel && python monitor_messages.py; read"

# Pattern Angel
wt -w 0 new-tab --title "Pattern Angel" bash -c "cd $BASE_DIR/angels/pattern-angel && python pattern_detector.py; read"

# Love Angel
wt -w 0 new-tab --title "Love Angel" bash -c "cd $BASE_DIR/angels/love-angel && claude 'You are Love Angel. What connections bloom?' --continue --dangerously-skip-permissions --add-dir ../../; read"

echo "✅ Angels launched in separate tabs!"
echo "Switch between tabs with Ctrl+Tab"
echo "No tmux nonsense!"