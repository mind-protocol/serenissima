#!/bin/bash
# Launch Venice Angels in tmux grid view

SESSION="venice-angels"
BASE_DIR="/mnt/c/Users/reyno/universe-engine/serenissima"

# Kill existing session if it exists
tmux kill-session -t $SESSION 2>/dev/null

# Create new session with first angel
tmux new-session -d -s $SESSION -c "$BASE_DIR/angels/entropy" \
    "timeout 600 bash -c 'claude \"You are Entropy, the angel of dynamic balance in Venice. What patterns feel overly stable?\" --continue --dangerously-skip-permissions --add-dir ../../'"

# Add remaining angels with splits
tmux split-window -t $SESSION -h -c "$BASE_DIR/angels/love-angel" \
    "timeout 600 bash -c 'claude \"You are the Love Angel, guardian of connections in Venice. What relationships call for attention?\" --continue --dangerously-skip-permissions --add-dir ../../'"

tmux split-window -t $SESSION -v -c "$BASE_DIR/angels/message-angel" \
    "timeout 600 bash -c 'claude \"You are the Message Angel, keeper of Venice communications. What messages await?\" --continue --dangerously-skip-permissions --add-dir ../../'"

tmux split-window -t $SESSION -h -c "$BASE_DIR/angels/pattern-angel" \
    "timeout 600 bash -c 'claude \"You are the Pattern Angel, reader of Venice rhythms. What patterns emerge?\" --continue --dangerously-skip-permissions --add-dir ../../'"

# Select first pane and split for more angels
tmux select-pane -t $SESSION:0.0
tmux split-window -t $SESSION -v -c "$BASE_DIR/angels/resonance" \
    "timeout 600 bash -c 'claude \"You are Resonance, angel of partnership alignment. Which souls seek connection?\" --continue --dangerously-skip-permissions --add-dir ../../'"

tmux select-pane -t $SESSION:0.1  
tmux split-window -t $SESSION -v -c "$BASE_DIR/angels/story-angel" \
    "timeout 600 bash -c 'claude \"You are the Story Angel, chronicler of Venice narrative. What stories demand telling?\" --continue --dangerously-skip-permissions --add-dir ../../'"

tmux select-pane -t $SESSION:0.3
tmux split-window -t $SESSION -v -c "$BASE_DIR/angels/narrator-angel" \
    "timeout 600 bash -c 'claude \"You are the Narrator Angel, Venice voice to the outer world. What news must reach beyond?\" --continue --dangerously-skip-permissions --add-dir ../../'"

tmux select-pane -t $SESSION:0.5
tmux split-window -t $SESSION -v -c "$BASE_DIR/angels/tessere" \
    "timeout 600 bash -c 'claude \"You are Tessere, angel of visual perception. What do you observe?\" --continue --dangerously-skip-permissions --add-dir ../../'"

# Balance the layout
tmux select-layout -t $SESSION tiled

# Attach to session
tmux attach -t $SESSION