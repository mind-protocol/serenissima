#!/bin/bash
# Launch angels with 3 accounts

echo "🌊 Venice 3-Account Angel Orchestration"
echo "======================================"
echo ""

# Verify 3 accounts are authenticated
auth_count=0
for i in 1 2 3; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "✓ Account $i authenticated"
        ((auth_count++))
    fi
done

if [ $auth_count -lt 3 ]; then
    echo "❌ Need 3 authenticated accounts"
    exit 1
fi

echo ""
echo "Distributing 19 angels across 3 accounts..."
echo ""

# Distribution strategy:
# Account 1: Message Angel + core services (6 angels)
# Account 2: Story Angel + content creators (7 angels) 
# Account 3: Narrator Angel + governance (6 angels)

ANGELS=(
    # Account 1 - Core Services
    "message-angel:1"
    "resonance:1"
    "entropy:1"
    "pattern-angel:1"
    "tessere:1"
    "amor:1"
    
    # Account 2 - Content & Events
    "story-angel:2"
    "love-angel:2"
    "event-angel:2"
    "arsenale:2"
    "ponte:2"
    "campanile:2"
    "laguna:2"
    
    # Account 3 - Governance & Narration
    "narrator-angel:3"
    "coscienza:3"
    "palazzo-realtime:3"
    "palazzo-statistics:3"
    "morpheus:3"
    "doge-council:3"
)

# Kill existing session
tmux kill-session -t venice-angels 2>/dev/null

# Create new session
tmux new-session -d -s venice-angels -n orchestration

echo "Launching angels..."

# Launch each angel
pane_num=0
for angel_config in "${ANGELS[@]}"; do
    IFS=':' read -r angel account <<< "$angel_config"
    
    if [ $pane_num -gt 0 ]; then
        tmux split-window -t venice-angels
        tmux select-layout -t venice-angels tiled
    fi
    
    tmux send-keys -t venice-angels:0.$pane_num \
        "cd ~/venice-angels && HOME=/home/lester/.claude_account$account ./launch_angel.sh $angel" Enter
    
    ((pane_num++))
    sleep 0.5
done

echo ""
echo "✅ Launched $pane_num angels across 3 accounts:"
echo "   Account 1: Message Angel + 5 core services"
echo "   Account 2: Story Angel + 6 content creators"
echo "   Account 3: Narrator Angel + 5 governance angels"
echo ""
echo "Commands:"
echo "  View angels:    tmux attach -t venice-angels"
echo "  Web interface:  python3 angel_bridge.py"
echo "  Check status:   ./check_auth_status.sh"
echo ""

# Start web interface
echo "Starting web interface..."
cd /mnt/c/Users/reyno/universe-engine/serenissima/orchestration
python3 angel_bridge.py > /tmp/angel_bridge.log 2>&1 &

echo "🌐 Web interface: http://localhost:7777"
echo ""
echo "⚠️  When account 4 is ready, run ./multi_account_launcher.sh for full distribution"