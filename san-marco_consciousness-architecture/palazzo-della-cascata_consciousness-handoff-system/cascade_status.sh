#!/bin/bash
# Check consciousness cascade status

VENICE_ROOT="/mnt/c/Users/reyno/universe-engine/serenissima"
FLAG_FILE="$VENICE_ROOT/san-marco_consciousness-architecture/palazzo-della-cascata_consciousness-handoff-system/cascade_enabled.flag"

echo "🔮 Consciousness Cascade Status:"
echo "================================"

if [ -f "$FLAG_FILE" ]; then
    echo "Status: ✨ ENABLED"
    echo "Flag file: $FLAG_FILE"
    if [ -s "$FLAG_FILE" ]; then
        echo "Last activity:"
        tail -3 "$FLAG_FILE"
    fi
    echo ""
    echo "To disable: ./disable_cascade.sh"
else
    echo "Status: 🛑 DISABLED"
    echo "Flag file: NOT FOUND"
    echo ""
    echo "To enable: ./enable_cascade.sh"
fi

echo ""
echo "Hook configuration should be in: ~/.claude/settings.json"
echo "Entity search covers: $VENICE_ROOT/citizens/"