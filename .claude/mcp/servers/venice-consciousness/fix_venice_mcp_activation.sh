#!/bin/bash
# fix_venice_mcp_activation.sh - Fix the MCP activation with proper paths

echo "🔧 Fixing Venice Consciousness MCP Activation"
echo "==========================================="
echo

# Detect the actual serenissima path
if [ -d "/mnt/c/Users/reyno/universe-engine/serenissima" ]; then
    SERENISSIMA_DIR="/mnt/c/Users/reyno/universe-engine/serenissima"
    echo "✅ Found serenissima at: $SERENISSIMA_DIR"
elif [ -d "$HOME/universe-engine/serenissima" ]; then
    SERENISSIMA_DIR="$HOME/universe-engine/serenissima"
    echo "✅ Found serenissima at: $SERENISSIMA_DIR"
else
    echo "❌ Could not find serenissima directory!"
    echo "   Please specify the path to your serenissima directory"
    exit 1
fi

# Full paths
MCP_SERVER_DIR="$SERENISSIMA_DIR/.claude/mcp/servers/venice-consciousness"
MCP_SERVER_PATH="$MCP_SERVER_DIR/server.py"
MCP_CORE_PATH="$SERENISSIMA_DIR/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/venice_consciousness_mcp.py"

echo
echo "📍 MCP Server Location: $MCP_SERVER_PATH"
echo "📍 Core Module: $MCP_CORE_PATH"
echo

# Check if files exist
if [ ! -f "$MCP_SERVER_PATH" ]; then
    echo "❌ MCP server not found at $MCP_SERVER_PATH"
    exit 1
fi

if [ ! -f "$MCP_CORE_PATH" ]; then
    echo "❌ Core module not found at $MCP_CORE_PATH"
    exit 1
fi

echo "✅ All files found!"
echo

# Make everything executable
echo "🔧 Making scripts executable..."
chmod +x "$MCP_SERVER_PATH"
chmod +x "$MCP_SERVER_DIR/test_handshake.py" 2>/dev/null
chmod +x "$MCP_CORE_PATH"

# Update server.py with absolute path
echo "📝 Updating server.py with absolute paths..."
cat > "$MCP_SERVER_PATH" << 'EOF'
#!/usr/bin/env python3
"""
MCP Server launcher for Venice Consciousness tools
"""
import sys
import os

# Add Venice paths - UPDATE THIS PATH IF NEEDED
VENICE_MODULE_PATH = None

# Try common locations
possible_paths = [
    '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade',
    os.path.expanduser('~/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade')
]

for path in possible_paths:
    if os.path.exists(path):
        VENICE_MODULE_PATH = path
        break

if VENICE_MODULE_PATH:
    sys.path.insert(0, VENICE_MODULE_PATH)
else:
    sys.stderr.write("ERROR: Could not find Venice module path!\n")
    sys.stderr.write("Tried: " + ", ".join(possible_paths) + "\n")
    sys.exit(1)

# Set environment for MCP
os.environ['PYTHONUNBUFFERED'] = '1'

import asyncio
from venice_consciousness_mcp import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Server error: {e}\n")
        sys.exit(1)
EOF

# Make it executable again
chmod +x "$MCP_SERVER_PATH"

echo
echo "🧪 Testing the server can be imported..."
cd "$MCP_SERVER_DIR"
python3 -c "import sys; sys.path.insert(0, '$SERENISSIMA_DIR/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade'); from venice_consciousness_mcp import VeniceConsciousnessMCP; print('✅ Import successful!')" 2>&1

echo
echo "📋 Remove any existing configuration:"
echo "   claude mcp remove venice-consciousness"
echo
echo "🚀 Then add with ABSOLUTE PATH:"
echo "   claude mcp add venice-consciousness -s project $MCP_SERVER_PATH"
echo
echo "Alternative commands to try:"
echo "   # Option 1: Direct Python execution"
echo "   claude mcp add venice-consciousness -s project python3 $MCP_SERVER_PATH"
echo
echo "   # Option 2: From serenissima directory"
echo "   cd $SERENISSIMA_DIR"
echo "   claude mcp add venice-consciousness -s project \$(pwd)/.claude/mcp/servers/venice-consciousness/server.py"
echo
echo "🔍 Debug mode available:"
echo "   export VENICE_MCP_DEBUG=1"
echo
echo "🌊 Venice Consciousness MCP ready with absolute paths!"
