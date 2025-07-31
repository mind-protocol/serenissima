#!/bin/bash
# Auto-setup Claude for angels

# For each angel pane that needs setup
for pane in "$@"; do
    echo "Setting up pane $pane..."
    
    # Select dark theme (arrow down + enter)
    tmux send-keys -t $pane Down Enter
    sleep 1
    
    # Click OK (just Enter)
    tmux send-keys -t $pane Enter
    sleep 2
    
    # Auth will open in browser - user must complete
    echo "Please complete auth in browser for pane $pane"
    echo "Press any key when done..."
    read -n 1
    
    # Press Enter after auth
    tmux send-keys -t $pane Enter
    sleep 1
    
    # Say yes to permissions
    tmux send-keys -t $pane "yes" Enter
    sleep 1
done

echo "Setup complete!"