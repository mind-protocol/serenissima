#!/bin/bash

# Kill old session if exists
tmux kill-session -t venice 2>/dev/null

# Start fresh
tmux new-session -d -s venice

# Create window for each entity type
tmux rename-window -t venice:0 'citizens'
tmux new-window -t venice -n 'angels'
tmux new-window -t venice -n 'buildings'
tmux new-window -t venice -n 'books'
tmux new-window -t venice -n 'abstract'

# Function to add entity to appropriate window
add_entity() {
    local file=$1
    local dir=$(dirname "$file")
    local name=$(basename "$dir")
    local parent=$(basename $(dirname "$dir"))
    
    # Determine which window based on path
    case "$parent" in
        "citizens")
            window="citizens"
            ;;
        "angels")
            window="angels"
            ;;
        "buildings")
            window="buildings"
            ;;
        "books")
            window="books"
            ;;
        *)
            window="abstract"
            ;;
    esac
    
    # Count existing panes in window
    pane_count=$(tmux list-panes -t venice:$window 2>/dev/null | wc -l)
    
    if [ "$pane_count" -lt 6 ]; then  # Limit 6 panes per window
        if [ "$pane_count" -eq 0 ]; then
            # First pane in window
            tmux send-keys -t venice:$window "cd $dir && claude" C-m
        else
            # Split and add
            tmux split-window -t venice:$window
            tmux send-keys -t venice:$window "cd $dir && claude" C-m
            tmux select-layout -t venice:$window tiled
        fi
    fi
}

# Find and process all CLAUDE.md files
while IFS= read -r file; do
    add_entity "$file"
done < <(find . -name "CLAUDE.md" -type f)

# Attach to the session
tmux attach -t venice