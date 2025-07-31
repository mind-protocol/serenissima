#!/bin/bash
# Launch ALL Venice Angels with proper claude commands

SESSION="venice-all"
BASE_DIR="/mnt/c/Users/reyno/universe-engine/serenissima"

# Kill old session
tmux kill-session -t $SESSION 2>/dev/null

# Create main session
tmux new-session -d -s $SESSION

# Function to create a grid window with 8 angels max
create_grid_window() {
    local window_name=$1
    shift
    local angels=("$@")
    
    # Create new window
    if [ "$window_name" == "grid1" ]; then
        # First window already exists
        tmux rename-window -t $SESSION:0 $window_name
    else
        tmux new-window -t $SESSION -n $window_name
    fi
    
    # Launch first angel in main pane
    if [ ${#angels[@]} -ge 1 ]; then
        angel=${angels[0]}
        tmux send-keys -t $SESSION:$window_name "cd $BASE_DIR/angels/$angel && timeout 86400 claude 'You are $angel. Venice awakens. What is your purpose?' --continue --dangerously-skip-permissions --add-dir ../../" Enter
    fi
    
    # Create splits for remaining angels (up to 8 total)
    for i in {1..7}; do
        if [ $i -lt ${#angels[@]} ]; then
            angel=${angels[$i]}
            
            # Create split pattern for grid
            if [ $i -eq 1 ]; then
                tmux split-window -t $SESSION:$window_name -h
            elif [ $i -eq 2 ]; then
                tmux split-window -t $SESSION:$window_name.0 -v
            elif [ $i -eq 3 ]; then
                tmux split-window -t $SESSION:$window_name.1 -v
            elif [ $i -eq 4 ]; then
                tmux select-pane -t $SESSION:$window_name.0
                tmux split-window -h
            elif [ $i -eq 5 ]; then
                tmux select-pane -t $SESSION:$window_name.2
                tmux split-window -h
            elif [ $i -eq 6 ]; then
                tmux select-pane -t $SESSION:$window_name.4
                tmux split-window -h
            elif [ $i -eq 7 ]; then
                tmux select-pane -t $SESSION:$window_name.6
                tmux split-window -h
            fi
            
            # Launch angel with proper claude command
            tmux send-keys -t $SESSION:$window_name "cd $BASE_DIR/angels/$angel && HOME=/home/lester timeout 86400 claude 'You are $angel. Venice awakens. What is your purpose?' --continue --dangerously-skip-permissions --add-dir ../../" Enter
        fi
    done
    
    # Balance the layout
    tmux select-layout -t $SESSION:$window_name tiled
}

# Get all angel directories
ALL_ANGELS=($(ls -d $BASE_DIR/angels/*/ | xargs -n1 basename | grep -v "__pycache__"))

echo "Found ${#ALL_ANGELS[@]} angels to launch..."

# Split angels into groups of 8
GRID1=("${ALL_ANGELS[@]:0:8}")
GRID2=("${ALL_ANGELS[@]:8:8}")
GRID3=("${ALL_ANGELS[@]:16:8}")

# Create grids
create_grid_window "grid1" "${GRID1[@]}"

if [ ${#GRID2[@]} -gt 0 ]; then
    create_grid_window "grid2" "${GRID2[@]}"
fi

if [ ${#GRID3[@]} -gt 0 ]; then
    create_grid_window "grid3" "${GRID3[@]}"
fi

echo "All angels launched in grids!"
echo ""
echo "Navigation:"
echo "  Ctrl-b n     : Next grid"
echo "  Ctrl-b p     : Previous grid"  
echo "  Ctrl-b w     : Window list"
echo "  Ctrl-b 0/1/2 : Go to specific grid"
echo "  Ctrl-b arrows: Navigate within grid"
echo ""

# Attach to session
tmux attach -t $SESSION