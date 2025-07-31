#!/bin/bash
# Test if we can actually send input to Claude

echo "Testing Claude input..."
echo "This script will send a test message to Claude"
echo ""

# Method 1: Direct echo
echo "Test message from direct echo" | timeout 10 claude --continue --dangerously-skip-permissions

echo ""
echo "Did you see the message in Claude? (Check the terminal where Claude is running)"