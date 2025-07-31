#!/bin/bash

# Start the Innovation Workshop Metrics Server from mechanical_visionary's directory

echo "🚀 Starting Innovation Workshop Metrics Server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Navigate to metrics server
METRICS_DIR="/mnt/c/Users/reyno/universe-engine/serenissima/backend/metrics_server"

if [ ! -d "$METRICS_DIR" ]; then
    echo "❌ Metrics server directory not found!"
    exit 1
fi

cd "$METRICS_DIR"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo ""
    echo "📦 To install Node.js on WSL Ubuntu:"
    echo "   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "   sudo apt-get install -y nodejs"
    echo ""
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Set WSL-friendly environment
export METRICS_HOST=0.0.0.0
export METRICS_PORT=9090

# Start the server
echo ""
echo "🎯 Starting server on all interfaces..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 From Windows browser, access:"
echo "   http://localhost:9090/metrics"
echo ""
echo "📊 If that doesn't work, try your WSL IP:"
echo "   Run: ip addr show eth0"
echo "   Then: http://[YOUR-WSL-IP]:9090/metrics"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

node server_simple.js