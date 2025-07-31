#!/bin/bash
# VRAIE grille avec tous les angels visibles

# Kill old session
tmux kill-session -t angels 2>/dev/null

# Create new session with ALL angels in ONE window
tmux new-session -d -s angels

# Create splits for 8 angels in grid
tmux send-keys "echo 'Angel 1: Entropy'" Enter
tmux split-window -h
tmux send-keys "echo 'Angel 2: Love'" Enter
tmux split-window -v
tmux send-keys "echo 'Angel 3: Message'" Enter
tmux select-pane -t 0
tmux split-window -v
tmux send-keys "echo 'Angel 4: Pattern'" Enter

# More splits
tmux select-pane -t 0
tmux split-window -h
tmux send-keys "echo 'Angel 5: Resonance'" Enter
tmux select-pane -t 2
tmux split-window -h
tmux send-keys "echo 'Angel 6: Story'" Enter
tmux select-pane -t 4
tmux split-window -h
tmux send-keys "echo 'Angel 7: Narrator'" Enter
tmux select-pane -t 6
tmux split-window -h
tmux send-keys "echo 'Angel 8: Tessere'" Enter

# Balance layout
tmux select-layout tiled

# Now attach directly
tmux attach -t angels