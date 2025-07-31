#!/bin/bash
# Convert Via della Vista Condivisa architecture diagrams

echo "🎨 Converting Via della Vista Condivisa Architecture Diagrams"
echo "=========================================================="

DIAGRAMS_DIR="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/architecture_diagrams"

# Change to the directory with node_modules
cd /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/mechanical_visionary

# Convert each diagram
for mmd_file in "$DIAGRAMS_DIR"/*.mmd; do
    if [ -f "$mmd_file" ]; then
        filename=$(basename "$mmd_file")
        png_file="${mmd_file%.mmd}.png"
        
        echo "Converting $filename..."
        npx mmdc -i "$mmd_file" -o "$png_file" -w 2000 -H 2000 --backgroundColor white
        
        if [ $? -eq 0 ]; then
            echo "✅ Created $(basename "$png_file")"
        else
            echo "❌ Failed to convert $filename"
        fi
    fi
done

echo ""
echo "✨ Conversion complete! Check the architecture_diagrams directory for PNG files."