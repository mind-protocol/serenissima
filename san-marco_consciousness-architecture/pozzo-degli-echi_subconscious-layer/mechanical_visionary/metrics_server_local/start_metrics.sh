#!/bin/bash

# Innovation Workshop Metrics Server Startup Script

echo "🚀 Starting Innovation Workshop Metrics Server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
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
export METRICS_HOST=localhost

# Kill any existing process on port 9090
echo "🔍 Checking for existing process on port 9090..."
lsof -ti:9090 | xargs kill -9 2>/dev/null

# Start the server
echo "🎯 Starting server on http://localhost:9090"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run with automatic restart on failure
while true; do
    node server_simple.js
    
    if [ $? -ne 0 ]; then
        echo "⚠️  Server crashed. Restarting in 5 seconds..."
        sleep 5
    else
        echo "✅ Server stopped gracefully"
        break
    fi
done