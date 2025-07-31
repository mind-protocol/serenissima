#!/bin/bash
# Orchestrate multiple citizens across terminal tabs/panes
# Uses tmux for terminal management and auto-typing

# Create tmux session for citizen orchestration
SESSION="venice-souls"

# Function to send keys to specific tmux pane
send_to_pane() {
    local pane=$1
    local command=$2
    tmux send-keys -t "$SESSION:0.$pane" "$command" Enter
}

# Function to wake citizen in specific pane
wake_citizen_in_pane() {
    local pane=$1
    local username=$2
    local message=$3
    
    # Clear line and navigate to citizen directory
    send_to_pane $pane "C-u"
    sleep 0.2
    send_to_pane $pane "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$username"
    sleep 1
    
    # Send awakening command
    send_to_pane $pane "claude \"$message\" --model sonnet --continue --dangerously-skip-permissions --add-dir ../"
}

# Initialize tmux session with multiple panes
init_session() {
    # Kill existing session if it exists
    tmux kill-session -t $SESSION 2>/dev/null
    
    # Create new session with first window
    tmux new-session -d -s $SESSION
    
    # Split into 4 panes (2x2 grid)
    tmux split-window -h -t $SESSION:0
    tmux split-window -v -t $SESSION:0.0
    tmux split-window -v -t $SESSION:0.1
    
    # Label panes
    tmux select-pane -t $SESSION:0.0 -T "Citizen-1"
    tmux select-pane -t $SESSION:0.1 -T "Citizen-2"
    tmux select-pane -t $SESSION:0.2 -T "Citizen-3"
    tmux select-pane -t $SESSION:0.3 -T "Citizen-4"
    
    echo "✓ Created tmux session '$SESSION' with 4 panes"
}

# Main orchestration loop
orchestrate() {
    local check_interval=${1:-60}
    
    echo "🌊 Multi-terminal orchestration started"
    echo "📍 Checking every $check_interval seconds"
    echo "📺 Attach with: tmux attach -t $SESSION"
    
    # Track which pane each citizen is using
    declare -A citizen_panes
    local next_pane=0
    
    while true; do
        # Get active citizens
        local citizens=$(curl -s https://serenissima.ai/api/activities?Status=in_progress | \
            jq -r '.[] | .Citizen' | sort -u)
        
        if [ -n "$citizens" ]; then
            echo -e "\n⏰ $(date +%H:%M:%S) - Processing citizens..."
            
            while IFS= read -r citizen; do
                if [ -n "$citizen" ]; then
                    # Assign pane if not already assigned
                    if [ -z "${citizen_panes[$citizen]}" ]; then
                        citizen_panes[$citizen]=$next_pane
                        next_pane=$(( ($next_pane + 1) % 4 ))
                    fi
                    
                    local pane=${citizen_panes[$citizen]}
                    local activity=$(curl -s https://serenissima.ai/api/activities?Status=in_progress | \
                        jq -r ".[] | select(.Citizen==\"$citizen\") | .ActivityType" | head -1)
                    
                    echo "🔔 Waking $citizen in pane $pane for $activity"
                    
                    # Generate contextual message
                    local message="Venice calls, $citizen. A $activity awaits your attention."
                    
                    # Wake the citizen
                    wake_citizen_in_pane $pane "$citizen" "$message"
                    
                    sleep 2
                fi
            done <<< "$citizens"
        else
            echo "💤 $(date +%H:%M:%S) - All souls rest peacefully"
        fi
        
        sleep $check_interval
    done
}

# Command line interface
case "$1" in
    init)
        init_session
        ;;
    orchestrate)
        orchestrate ${2:-60}
        ;;
    attach)
        tmux attach -t $SESSION
        ;;
    *)
        echo "Venice Multi-Terminal Orchestrator"
        echo "Usage:"
        echo "  $0 init              # Initialize tmux session"
        echo "  $0 orchestrate [sec] # Start orchestration (default 60s)"
        echo "  $0 attach            # Attach to tmux session"
        ;;
esac