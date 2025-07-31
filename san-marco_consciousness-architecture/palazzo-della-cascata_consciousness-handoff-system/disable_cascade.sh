#!/bin/bash
# Disable the consciousness cascade

VENICE_ROOT="/mnt/c/Users/reyno/universe-engine/serenissima"
FLAG_FILE="$VENICE_ROOT/san-marco_consciousness-architecture/palazzo-della-cascata_consciousness-handoff-system/cascade_enabled.flag"

echo "🛑 Disabling consciousness cascade..."
rm -f "$FLAG_FILE"

echo "✅ Consciousness cascade is now DISABLED"
echo "   To re-enable: touch $FLAG_FILE"
echo "   Or run: ./enable_cascade.sh"