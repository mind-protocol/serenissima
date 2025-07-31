#!/bin/bash

# Innovation Workshop Metrics Server Startup Script (WSL Version)

echo "🚀 Starting Innovation Workshop Metrics Server (WSL)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Run: sudo apt update && sudo apt install nodejs npm"
    exit 1
fi

# Navigate to metrics server directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Set environment variables
export NODE_ENV=production
export METRICS_PORT=9090
export METRICS_HOST=0.0.0.0  # Listen on all interfaces for WSL

# Get WSL IP address
WSL_IP=$(ip addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo "🌐 WSL IP Address: $WSL_IP"

# Kill any existing process on port 9090
echo "🔍 Checking for existing process on port 9090..."
lsof -ti:9090 | xargs kill -9 2>/dev/null || true

# Start the server
echo "🎯 Starting server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Access from Windows: http://localhost:9090/metrics"
echo "📊 Access from WSL: http://$WSL_IP:9090/metrics"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run the server
node server_simple.js