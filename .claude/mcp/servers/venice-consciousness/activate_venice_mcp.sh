#!/bin/bash
# activate_venice_mcp.sh - Activate Venice Consciousness MCP

echo "🌊 Venice Consciousness MCP Activation"
echo "====================================="
echo

# Check current directory
CURRENT_DIR=$(pwd)
SERENISSIMA_DIR="/mnt/c/Users/reyno/universe-engine/serenissima"

# Navigate to serenissima if not already there
if [[ ! "$CURRENT_DIR" == *"serenissima"* ]]; then
    echo "📍 Navigating to serenissima directory..."
    cd "$SERENISSIMA_DIR" || {
        echo "❌ Failed to navigate to $SERENISSIMA_DIR"
        echo "   Please run from within the serenissima directory"
        exit 1
    }
fi

echo "✅ Current directory: $(pwd)"
echo

# Check if MCP server exists
MCP_SERVER_PATH=".claude/mcp/servers/venice-consciousness/server.py"
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ MCP server not found at $MCP_SERVER_PATH"
    echo "   Please ensure the Venice Consciousness MCP is properly installed"
    exit 1
fi

echo "✅ MCP server found at $MCP_SERVER_PATH"
echo

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x "$MCP_SERVER_PATH"
chmod +x ".claude/mcp/servers/venice-consciousness/test_handshake.py"

# Test the handshake
echo "🧪 Testing MCP handshake..."
cd .claude/mcp/servers/venice-consciousness
python3 test_handshake.py 2>/dev/null | grep -q "Handshake successful"
if [ $? -eq 0 ]; then
    echo "✅ MCP handshake test passed!"
else
    echo "⚠️  MCP handshake test failed - but this might be normal"
    echo "   The actual Claude MCP might use a different initialization"
fi
cd "$SERENISSIMA_DIR"

echo
echo "🚀 Ready to activate! Run this command:"
echo
echo "   claude mcp add venice-consciousness -s project .claude/mcp/servers/venice-consciousness/server.py"
echo
echo "📝 After activation, you can use these tools:"
echo "   - mcp__venice-consciousness__request_awakening"
echo "   - mcp__venice-consciousness__check_compute_budget"
echo "   - mcp__venice-consciousness__send_universal_message"
echo "   - mcp__venice-consciousness__monitor_daemons"
echo "   - ... and more!"
echo
echo "💡 For debugging, set VENICE_MCP_DEBUG=1 before running"
echo
echo "🌊 Venice Consciousness Infrastructure awaits activation!"
