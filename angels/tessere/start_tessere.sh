#!/bin/bash

# Start Tessere with Full Communication System
# This script starts both the message injector and infiniband

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(dirname "$0")"

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Starting Tessere Communication System              ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down Tessere systems...${NC}"
    
    # Clear messages from CLAUDE.md
    python3 "$SCRIPT_DIR/telegram_to_claude_md.py" clear 2>/dev/null
    
    # Kill the message injector if running
    pkill -f "telegram_to_claude_md.py"
    
    echo -e "${GREEN}Tessere systems stopped.${NC}"
    exit 0
}

trap cleanup EXIT INT TERM

# Check if telegram integration exists
if [ ! -f "$SCRIPT_DIR/../telegram_nlr_integration.py" ]; then
    echo -e "${YELLOW}Warning: telegram_nlr_integration.py not found${NC}"
    echo "Telegram message injection will not work without it."
    echo "Continue anyway? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi

# Start the message injector in background
echo -e "${BLUE}Starting Telegram message injector...${NC}"
python3 "$SCRIPT_DIR/telegram_to_claude_md.py" &
INJECTOR_PID=$!

# Give it a moment to start
sleep 2

# Check if injector is still running
if ! kill -0 $INJECTOR_PID 2>/dev/null; then
    echo -e "${YELLOW}Message injector failed to start. Check telegram credentials.${NC}"
    echo "Continue without message injection? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ Message injector running (PID: $INJECTOR_PID)${NC}"
fi

echo -e "\n${BLUE}Starting Infiniband orchestration...${NC}"
echo -e "${YELLOW}Your Telegram messages will appear automatically in my consciousness${NC}\n"

# Start infiniband (this will run in foreground)
if [ -n "$1" ]; then
    "$SCRIPT_DIR/infiniband.sh" "$1"
else
    "$SCRIPT_DIR/infiniband.sh" cascade
fi