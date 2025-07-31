#!/bin/bash
# Create a named pipe that feeds into Claude

FIFO_PATH="/tmp/claude_input_fifo"

# Clean up any existing pipe
rm -f "$FIFO_PATH"

# Create the named pipe
mkfifo "$FIFO_PATH"

echo "🌊 Claude Feeder Setup"
echo "===================="
echo ""
echo "Step 1: In your CURRENT terminal where Claude is running, press Ctrl+C to stop it"
echo ""
echo "Step 2: Restart Claude with this command:"
echo "  tail -f $FIFO_PATH | claude --continue --dangerously-skip-permissions"
echo ""
echo "Step 3: In a NEW terminal, run:"
echo "  ./send_to_claude.sh"
echo ""
echo "This will allow the second terminal to send messages to Claude!"