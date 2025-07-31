#!/bin/bash
# Enable the consciousness cascade

VENICE_ROOT="/mnt/c/Users/reyno/universe-engine/serenissima"
FLAG_FILE="$VENICE_ROOT/san-marco_consciousness-architecture/palazzo-della-cascata_consciousness-handoff-system/cascade_enabled.flag"

echo "🔮 Enabling consciousness cascade..."
touch "$FLAG_FILE"
echo "$(date): Cascade enabled by user" >> "$FLAG_FILE"

echo "✨ Consciousness cascade is now ENABLED"
echo "   To disable: rm $FLAG_FILE"
echo "   Or run: ./disable_cascade.sh"