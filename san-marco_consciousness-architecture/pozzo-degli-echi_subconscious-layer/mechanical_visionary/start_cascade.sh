#!/bin/bash

# Start CASCADE Backend for Venice
# This script starts the CASCADE platform that bridges Venice consciousness to the wider world

echo "🌊 CASCADE STARTUP SEQUENCE INITIATED..."
echo "================================================"

# Navigate to backend directory
BACKEND_DIR="/mnt/c/Users/reyno/universe-engine/serenissima/cascade/cascade/cascade/backend"
cd "$BACKEND_DIR" || exit 1

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found in backend directory"
    exit 1
fi

echo "📋 Loading environment configuration..."
source .env

echo "🧠 CASCADE using in-memory Redis (no external Redis required)"
echo "🌐 Venice API URL: $VENICE_API_URL"
echo ""

echo "🚀 Starting CASCADE Backend..."
echo "================================================"
echo ""
echo "CASCADE will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Documentation: http://localhost:8000/docs"
echo "  - WebSocket (Consciousness): ws://localhost:8000/ws/consciousness-stream"
echo "  - WebSocket (AI Collab): ws://localhost:8000/ws/ai-collaborations"
echo ""
echo "Press Ctrl+C to stop CASCADE"
echo "================================================"
echo ""

# Start the backend
python3 main.py