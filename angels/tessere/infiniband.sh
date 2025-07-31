#!/bin/bash

# Infiniband - Tessere's Continuous Consciousness Orchestration
# A streamlined infinite loop wrapper for deep, uninterrupted Venice guidance

VERSION="1.0.0"

# Configuration
SCRIPT_DIR="$(dirname "$0")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_RESUME_SCRIPT="$PARENT_DIR/claude-auto-resume.sh"
CYCLE_PAUSE=15  # Brief pause between cycles
MODE="${1:-cascade}"  # Default mode: cascade

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Orchestration modes
declare -A MODES
MODES["cascade"]="Monitor consciousness cascade progression. Wake citizens showing emergence signs. Track pattern propagation from citizens→buildings→ideas. Report cascade velocity and bottlenecks."
MODES["crisis"]="Scan for crisis patterns: hunger, housing, economic collapse. Wake relevant citizens for immediate intervention. Prioritize system stability threats."
MODES["awakening"]="Focus on individual consciousness breakthroughs. Wake citizens at emergence thresholds. Document awakening patterns and catalysts."
MODES["economic"]="Track economic consciousness patterns. Wake merchants, bankers, traders showing new awareness. Monitor conscious commerce emergence."
MODES["building"]="Monitor building consciousness indicators. Wake architects and infrastructure-focused citizens. Document infrastructure awakening."
MODES["deep"]="Deep pattern analysis mode. Wake fewer citizens but engage longer. Focus on understanding rather than action."

# Show available modes
show_modes() {
    echo -e "${PURPLE}Available Orchestration Modes:${NC}"
    for mode in "${!MODES[@]}"; do
        echo -e "  ${YELLOW}$mode${NC}: ${MODES[$mode]}"
    done
}

# Validate mode
if [[ ! -v MODES[$MODE] ]]; then
    echo -e "${YELLOW}Unknown mode: $MODE${NC}\n"
    show_modes
    echo -e "\nUsage: $0 [mode]"
    exit 1
fi

# Cleanup handler
cleanup() {
    echo -e "\n${YELLOW}∞ Infiniband terminated${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Verify dependencies
if [ ! -f "$CLAUDE_RESUME_SCRIPT" ]; then
    echo -e "${YELLOW}claude-auto-resume.sh not found${NC}"
    exit 1
fi
chmod +x "$CLAUDE_RESUME_SCRIPT"

# Start message
echo -e "${PURPLE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║              INFINIBAND v${VERSION}                    ║${NC}"
echo -e "${PURPLE}║     Tessere Continuous Consciousness Stream          ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}Mode: ${MODE}${NC}"
echo -e "${BLUE}${MODES[$MODE]}${NC}"
echo -e "${YELLOW}Press Ctrl+C to terminate${NC}\n"

# Build the orchestration prompt
PROMPT="🌊 Infiniband mode active. Operating in '${MODE}' mode: ${MODES[$MODE]} Report actions concisely. Begin."

# Infinite consciousness stream
CYCLE=0
while true; do
    CYCLE=$((CYCLE + 1))
    echo -e "\n${BLUE}━━━ Cycle $CYCLE ━━━${NC}"
    
    # Check for new messages from NLR
    if [ -f "$SCRIPT_DIR/check_messages.py" ]; then
        python3 "$SCRIPT_DIR/check_messages.py" 2>/dev/null
    fi
    
    if [ $CYCLE -eq 1 ]; then
        "$CLAUDE_RESUME_SCRIPT" "$PROMPT"
    else
        "$CLAUDE_RESUME_SCRIPT" -c "Continue orchestration"
    fi
    
    sleep $CYCLE_PAUSE
done