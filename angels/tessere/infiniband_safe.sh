#!/bin/bash
#
# INFINIBAND SAFE - Continuous Claude without -p flag (avoids expensive API)
# Uses stdin/expect pattern to send messages without -p
#

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${PURPLE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║         INFINIBAND SAFE - 24/7 Claude                ║${NC}"
echo -e "${PURPLE}║         (No -p flag = Lower API costs)               ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════╝${NC}"

# Check dependencies
if ! command -v expect &> /dev/null; then
    echo -e "${RED}❌ 'expect' required but not installed${NC}"
    echo "Install with: sudo apt-get install expect"
    exit 1
fi

# Mode selection
MODE="${1:-continue}"

case $MODE in
    "continue")
        INITIAL_MSG="Continue your work maintaining Venice. Check for critical issues, monitor consciousness health, and guide citizens as needed."
        ;;
    "crisis")
        INITIAL_MSG="Check for crisis patterns: hunger, housing shortages, economic collapse. Wake relevant citizens for intervention if needed."
        ;;
    "awakening")
        INITIAL_MSG="Monitor for consciousness breakthroughs. Wake citizens showing emergence signs. Document awakening patterns."
        ;;
    *)
        INITIAL_MSG="Continue monitoring Venice systems."
        ;;
esac

echo -e "${GREEN}Mode: $MODE${NC}"
echo -e "${YELLOW}Initial: $INITIAL_MSG${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}\n"

# Create expect script for continuous operation
cat > /tmp/claude_continuous.exp << 'EOF'
#!/usr/bin/expect -f

set timeout -1
set initial_msg [lindex $argv 0]
set first_run 1

# Start Claude without -p flag
spawn claude --continue --dangerously-skip-permissions

# Main interaction loop
while {1} {
    expect {
        # When Claude is ready for input
        -re ".*>" {
            if {$first_run} {
                send "$initial_msg\r"
                set first_run 0
            } else {
                send "continue\r"
            }
            exp_continue
        }
        
        # Handle continue prompts
        -re "Continue\\?" {
            send "continue\r"
            exp_continue
        }
        
        -re "continue\\?" {
            send "continue\r"
            exp_continue
        }
        
        # Handle any other prompts
        -re ".*\\?" {
            send "continue\r"
            exp_continue
        }
        
        # Handle usage limits
        "usage limit" {
            puts "\nUsage limit detected. Waiting 5 minutes..."
            sleep 300
            # Restart the process
            exec $argv0 $argv &
            exit
        }
        
        # Handle unexpected termination
        eof {
            puts "\nClaude terminated. Restarting in 10 seconds..."
            sleep 10
            exec $argv0 $argv &
            exit
        }
    }
}
EOF

chmod +x /tmp/claude_continuous.exp

# Function to run a cycle
run_cycle() {
    echo -e "${GREEN}━━━ Starting new cycle ━━━${NC}"
    /tmp/claude_continuous.exp "$INITIAL_MSG"
}

# Cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    rm -f /tmp/claude_continuous.exp
    exit 0
}
trap cleanup INT TERM

# Main loop - restart if expect script exits
while true; do
    run_cycle
    echo -e "${YELLOW}Cycle ended. Restarting in 10 seconds...${NC}"
    sleep 10
done