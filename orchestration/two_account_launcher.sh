#!/bin/bash
# Launch angels with just 2 accounts while we wait for full auth

echo "🌊 Venice 2-Account Angel Orchestration"
echo "======================================"
echo ""

# Check which accounts are authenticated
auth_count=0
for i in 1 2; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "✓ Account $i authenticated"
        ((auth_count++))
    fi
done

if [ $auth_count -eq 0 ]; then
    echo "❌ No accounts authenticated yet"
    echo ""
    echo "Please authenticate at least one account first:"
    echo "1. Open browser with magic link"
    echo "2. Run: HOME=/home/lester/.claude_account1 claude 'test'"
    echo "3. Complete auth flow"
    exit 1
fi

echo ""
echo "Distributing angels across $auth_count accounts..."
echo ""

# Create a simplified distribution
if [ $auth_count -eq 2 ]; then
    # Account 1: Core angels
    ACCOUNT1_ANGELS=(
        "message-angel"
        "resonance"
        "entropy"
        "pattern-angel"
        "amor"
        "tessere"
        "coscienza"
        "palazzo-realtime"
        "morpheus"
    )
    
    # Account 2: Story/Content angels  
    ACCOUNT2_ANGELS=(
        "story-angel"
        "narrator-angel"
        "love-angel"
        "event-angel"
        "arsenale"
        "palazzo-statistics"
        "ponte"
        "campanile"
        "laguna"
        "doge-council"
    )
else
    # Single account - all angels
    ACCOUNT1_ANGELS=(
        "message-angel"
        "story-angel"
        "narrator-angel"
        "resonance"
        "entropy"
        "pattern-angel"
        "love-angel"
        "amor"
        "tessere"
        "event-angel"
    )
    ACCOUNT2_ANGELS=()
fi

# Launch tmux session
tmux kill-session -t venice-angels 2>/dev/null
tmux new-session -d -s venice-angels -n orchestration

echo "Launching angels..."

# Launch Account 1 angels
pane_num=0
for angel in "${ACCOUNT1_ANGELS[@]}"; do
    if [ $pane_num -gt 0 ]; then
        tmux split-window -t venice-angels
        tmux select-layout -t venice-angels tiled
    fi
    
    tmux send-keys -t venice-angels:0.$pane_num "cd ~/venice-angels && HOME=/home/lester/.claude_account1 ./launch_angel.sh $angel" Enter
    ((pane_num++))
    sleep 1
done

# Launch Account 2 angels if we have 2 accounts
if [ $auth_count -eq 2 ] && [ ${#ACCOUNT2_ANGELS[@]} -gt 0 ]; then
    for angel in "${ACCOUNT2_ANGELS[@]}"; do
        tmux split-window -t venice-angels
        tmux select-layout -t venice-angels tiled
        
        tmux send-keys -t venice-angels:0.$pane_num "cd ~/venice-angels && HOME=/home/lester/.claude_account2 ./launch_angel.sh $angel" Enter
        ((pane_num++))
        sleep 1
    done
fi

echo ""
echo "✅ Launched $pane_num angels across $auth_count accounts"
echo ""
echo "Commands:"
echo "  View angels:    tmux attach -t venice-angels"
echo "  Web interface:  python3 angel_bridge.py"
echo "  Check status:   ./check_auth_status.sh"
echo ""

# Also prepare web interface
echo "Starting web interface..."
cd /mnt/c/Users/reyno/universe-engine/serenissima/orchestration
python3 angel_bridge.py &

echo "🌐 Web interface: http://localhost:7777"