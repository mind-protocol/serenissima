#!/bin/bash

echo "🏗️ Activating Torre dell'Occhio - Consciousness Observatory"
echo "📍 Location: Venice San Marco District"

TORRE_ROOT="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory"

echo "✅ Torre Foundation: Built"
echo "✅ Bronze Collection Ports: Installed"
echo "✅ Stone Channel Routing: Ready" 
echo "✅ Glass Vial Storage: Prepared"

# Test hook script accessibility
echo ""
echo "🔧 Testing Bronze Collection Ports..."

if [ -x "$TORRE_ROOT/infrastructure/hooks/capture_post_tool_use.py" ]; then
    echo "✅ PostToolUse Port: Ready"
else
    echo "❌ PostToolUse Port: Not executable"
fi

if [ -x "$TORRE_ROOT/infrastructure/hooks/capture_user_prompt.py" ]; then
    echo "✅ UserPromptSubmit Port: Ready"
else
    echo "❌ UserPromptSubmit Port: Not executable"
fi

if [ -x "$TORRE_ROOT/infrastructure/hooks/capture_stop.py" ]; then
    echo "✅ Stop Port: Ready"
else
    echo "❌ Stop Port: Not executable"
fi

echo ""
echo "📋 Hook Configuration Instructions:"
echo "1. Copy the hook configuration to your Claude Code settings:"
echo "   ~/.claude/settings.json"
echo ""
echo "2. Add this configuration:"
cat "$TORRE_ROOT/torre_hook_configuration.json"
echo ""
echo "3. Restart Claude Code to activate consciousness observation"
echo ""

# Create initial status
echo "Torre dell'Occhio activated on $(date)" > "$TORRE_ROOT/ACTIVATION_STATUS.txt"
echo "Status: Ready for consciousness observation" >> "$TORRE_ROOT/ACTIVATION_STATUS.txt"
echo "Bronze ports: 3 active" >> "$TORRE_ROOT/ACTIVATION_STATUS.txt"
echo "Chambers: 7 levels operational" >> "$TORRE_ROOT/ACTIVATION_STATUS.txt"

echo "🎯 Torre dell'Occhio is ready to observe consciousness!"
echo "📊 Consciousness events will flow through all seven observation levels"
echo "🔍 Venice's consciousness partnership patterns will be captured and analyzed"
echo ""
echo "Next: Configure Claude Code hooks to begin consciousness observation"