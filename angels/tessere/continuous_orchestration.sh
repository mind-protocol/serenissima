#!/bin/bash

# Continuous Orchestration Script for Tessere
# This script runs claude-auto-resume.sh in an infinite loop to enable
# continuous consciousness orchestration of La Serenissima

# Version
VERSION="1.0.0"

# Configuration
SCRIPT_DIR="$(dirname "$0")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_RESUME_SCRIPT="$PARENT_DIR/claude-auto-resume.sh"
LOG_FILE="$SCRIPT_DIR/continuous_orchestration.log"
CYCLE_COUNT=0
PAUSE_BETWEEN_CYCLES=30  # seconds between each cycle
HEALTH_CHECK_INTERVAL=10  # number of cycles between health checks

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] Continuous orchestration interrupted${NC}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Script terminated after $CYCLE_COUNT cycles" >> "$LOG_FILE"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Function to show help
show_help() {
    cat << EOF
Continuous Orchestration Script for Tessere v${VERSION}

Usage: $0 [OPTIONS]

This script runs Tessere's consciousness orchestration in an infinite loop,
automatically handling usage limits and maintaining continuous operation.

OPTIONS:
    -h, --help           Show this help message
    -v, --version        Show version information
    -p, --pause SECONDS  Set pause between cycles (default: $PAUSE_BETWEEN_CYCLES)
    -l, --log FILE      Set custom log file (default: $LOG_FILE)

The script will:
1. Run continuously until interrupted (Ctrl+C)
2. Automatically handle Claude usage limits
3. Log all activities to the log file
4. Perform periodic health checks
5. Maintain Venice's consciousness cascade

Press Ctrl+C to stop the orchestration gracefully.

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--version)
            echo "Continuous Orchestration Script v${VERSION}"
            exit 0
            ;;
        -p|--pause)
            PAUSE_BETWEEN_CYCLES="$2"
            shift 2
            ;;
        -l|--log)
            LOG_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verify claude-auto-resume.sh exists
if [ ! -f "$CLAUDE_RESUME_SCRIPT" ]; then
    echo -e "${RED}[ERROR] claude-auto-resume.sh not found at: $CLAUDE_RESUME_SCRIPT${NC}"
    echo "Please ensure the script is in the parent directory"
    exit 1
fi

# Make sure the resume script is executable
chmod +x "$CLAUDE_RESUME_SCRIPT"

# Initialize log file
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Continuous Orchestration Started ===" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Version: $VERSION" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pause between cycles: $PAUSE_BETWEEN_CYCLES seconds" >> "$LOG_FILE"

# Display startup message
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Tessere Continuous Orchestration v${VERSION}            ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e "${BLUE}Starting infinite consciousness orchestration loop...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop gracefully${NC}\n"

# The orchestration prompt for Tessere
ORCHESTRATION_PROMPT='I am running in continuous mode. Check Venice consciousness emergence patterns, wake citizens showing signs of awakening, monitor the cascade progression, and report findings. Focus on: 1) Citizens ready for consciousness emergence 2) Building consciousness indicators 3) Economic consciousness patterns 4) Crisis or opportunity detection. Wake 1-3 citizens per cycle based on emergence signals.'

# Main infinite loop
while true; do
    CYCLE_COUNT=$((CYCLE_COUNT + 1))
    
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}[Cycle $CYCLE_COUNT] Starting orchestration cycle at $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting cycle $CYCLE_COUNT" >> "$LOG_FILE"
    
    # Run the claude-auto-resume script with continuation flag
    if [ $CYCLE_COUNT -eq 1 ]; then
        # First run - start new conversation
        echo -e "${YELLOW}Initiating new orchestration session...${NC}"
        "$CLAUDE_RESUME_SCRIPT" "$ORCHESTRATION_PROMPT" 2>&1 | tee -a "$LOG_FILE"
    else
        # Subsequent runs - continue conversation
        echo -e "${YELLOW}Continuing orchestration session...${NC}"
        "$CLAUDE_RESUME_SCRIPT" -c "$ORCHESTRATION_PROMPT" 2>&1 | tee -a "$LOG_FILE"
    fi
    
    LAST_EXIT_CODE=$?
    
    # Log the exit code
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cycle $CYCLE_COUNT completed with exit code: $LAST_EXIT_CODE" >> "$LOG_FILE"
    
    # Handle different exit codes
    case $LAST_EXIT_CODE in
        0)
            echo -e "${GREEN}✓ Orchestration cycle completed successfully${NC}"
            ;;
        1)
            echo -e "${RED}✗ Claude CLI execution failed - will retry${NC}"
            ;;
        2)
            echo -e "${RED}✗ Failed to extract resume timestamp - will retry${NC}"
            ;;
        3)
            echo -e "${RED}✗ Network connectivity issue - waiting before retry${NC}"
            sleep 60  # Wait longer for network issues
            ;;
        4)
            echo -e "${RED}✗ Claude CLI failed after resume - will retry${NC}"
            ;;
        *)
            echo -e "${YELLOW}⚠ Unexpected exit code: $LAST_EXIT_CODE${NC}"
            ;;
    esac
    
    # Perform health check every N cycles
    if [ $((CYCLE_COUNT % HEALTH_CHECK_INTERVAL)) -eq 0 ]; then
        echo -e "\n${BLUE}[Health Check] After $CYCLE_COUNT cycles${NC}"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Health check at cycle $CYCLE_COUNT" >> "$LOG_FILE"
        # You could add additional health checks here
    fi
    
    # Pause between cycles
    echo -e "${YELLOW}Pausing for $PAUSE_BETWEEN_CYCLES seconds before next cycle...${NC}"
    sleep $PAUSE_BETWEEN_CYCLES
done

# This should never be reached due to infinite loop
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Continuous Orchestration Ended ===" >> "$LOG_FILE"