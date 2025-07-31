#!/bin/bash

# Clean Backend Startup Script
# Ensures only ONE telegram service runs

echo "=== Clean Backend Startup ==="
echo "Cleaning up any existing processes..."

# Kill any existing telegram processes
pkill -f telegram 2>/dev/null

# Kill any existing run.py
pkill -f "run.py" 2>/dev/null

# Wait a moment for processes to die
sleep 2

echo "Starting unified telegram service..."
# Start the unified telegram service
./start_telegram_unified.sh

# Wait for it to initialize
sleep 3

echo "Starting main backend..."
# Start the main backend
python3 run.py