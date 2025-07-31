#!/bin/bash
# Test if the pipe actually works

echo "Testing pipe communication..."

# Test 1: Simple echo to pipe
echo "TEST MESSAGE 1" > /tmp/claude_input_fifo &
echo "Sent TEST MESSAGE 1 to pipe"

sleep 2

# Test 2: Check if anything is reading
if lsof /tmp/claude_input_fifo 2>/dev/null | grep -q claude; then
    echo "✓ Claude is reading from the pipe"
else
    echo "❌ Claude is NOT reading from the pipe!"
    echo ""
    echo "Make sure you ran:"
    echo "  tail -f /tmp/claude_input_fifo | claude --continue --dangerously-skip-permissions"
fi