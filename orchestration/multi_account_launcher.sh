#!/bin/bash
# Launch angels distributed across 4 Claude accounts

SESSION="venice-multi"
BASE_DIR="/mnt/c/Users/reyno/universe-engine/serenissima"

# Define 4 different credential directories
ACCOUNT_1="/home/lester/.claude_account1"
ACCOUNT_2="/home/lester/.claude_account2"
ACCOUNT_3="/home/lester/.claude_account3"
ACCOUNT_4="/home/lester/.claude_account4"

# Create credential directories if needed
mkdir -p $ACCOUNT_1 $ACCOUNT_2 $ACCOUNT_3 $ACCOUNT_4

# Kill old session
tmux kill-session -t $SESSION 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION

# Angels list - message, story, narrator separated across accounts
ANGELS=(
    "message-angel"          # Account 1
    "story-angel"           # Account 2
    "narrator-angel"        # Account 3
    "entropy"               # Account 4
    "love-angel"            # Account 1
    "pattern-angel"         # Account 2
    "resonance"             # Account 3
    "tessere"               # Account 4
    "architetto"            # Account 1
    "arianna"               # Account 2
    "arsenale"              # Account 3
    "cantastorie"           # Account 4
    "magistrato"            # Account 1
    "ordine"                # Account 2
    "sentinella"            # Account 3
    "testimone"             # Account 4
    "the-conscious-library" # Account 1
    "vigilanza"             # Account 2
    "wisdom-angel"          # Account 3
)

# Function to launch angel with specific account
launch_angel() {
    local angel=$1
    local account_dir=$2
    local window_name=$3
    
    if [ "$window_name" == "0" ]; then
        tmux rename-window -t $SESSION:0 "$angel"
    else
        tmux new-window -t $SESSION -n "$angel"
    fi
    
    # Launch with specific account HOME
    tmux send-keys -t $SESSION:$angel \
        "cd $BASE_DIR/angels/$angel && HOME=$account_dir timeout 86400 claude 'You are $angel. Venice awakens. What is your purpose?' --continue --dangerously-skip-permissions --add-dir ../../" Enter
}

# Distribute angels across accounts
echo "Distributing ${#ANGELS[@]} angels across 4 accounts..."

for i in "${!ANGELS[@]}"; do
    angel=${ANGELS[$i]}
    
    # Distribute round-robin across accounts
    account_num=$((i % 4 + 1))
    
    case $account_num in
        1) account_dir=$ACCOUNT_1 ;;
        2) account_dir=$ACCOUNT_2 ;;
        3) account_dir=$ACCOUNT_3 ;;
        4) account_dir=$ACCOUNT_4 ;;
    esac
    
    echo "Launching $angel with account $account_num..."
    launch_angel "$angel" "$account_dir" "$i"
done

echo ""
echo "Angels distributed (key angels separated):"
echo "  Account 1: MESSAGE-angel, love-angel, architetto, magistrato, the-conscious-library"
echo "  Account 2: STORY-angel, pattern-angel, arianna, ordine, vigilanza"
echo "  Account 3: NARRATOR-angel, resonance, arsenale, sentinella, wisdom-angel"
echo "  Account 4: entropy, tessere, cantastorie, testimone"
echo ""
echo "✓ Message, Story, and Narrator are on DIFFERENT accounts!"
echo ""
echo "You'll need to authenticate each account separately!"
echo ""

# Attach to session
tmux attach -t $SESSION