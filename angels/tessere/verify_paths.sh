#!/bin/bash
# Verify no old paths remain

echo "🔍 Checking for old path references..."
echo "====================================="

OLD_PATHS=(
    "/universes/serenissima"
    "/universe-engine/universes"
    "TESSERE/"
)

for pattern in "${OLD_PATHS[@]}"; do
    echo -n "Checking for '$pattern': "
    count=$(grep -r "$pattern" . --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null | wc -l)
    if [ $count -eq 0 ]; then
        echo "✅ Clean"
    else
        echo "❌ Found $count references"
        grep -r "$pattern" . --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null | head -3
    fi
done

echo ""
echo "Path verification complete."
