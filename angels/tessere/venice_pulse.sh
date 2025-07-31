#!/bin/bash
# venice_pulse.sh - Git-based proprioception for Tessere

echo "=== Venice Structural Pulse - $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "Total changes: $(git status --short | wc -l)"
echo "New files: $(git status --short | grep '^??' | wc -l)"
echo "Modified files: $(git status --short | grep '^ M' | wc -l)"
echo "Deleted files: $(git status --short | grep '^ D' | wc -l)"
echo ""
echo "=== Consciousness Emergence (last 10) ==="
git status --short | grep -i "consciousness" | head -10
echo ""
echo "=== CASCADE System Activity ==="
git status --short | grep -i "cascade" | head -5
echo ""
echo "=== Emergency Signals ==="
git status --short | grep -i "emergency\|urgent\|critical\|alert" | head -5
echo ""
echo "=== Most Active Citizens (by file count) ==="
git status --short | grep "citizens/" | cut -d'/' -f2 | sort | uniq -c | sort -nr | head -10
echo ""
echo "=== New Citizen Memories ==="
git status --short | grep "^??" | grep "citizens.*memories" | head -5
echo ""
echo "=== System Infrastructure Changes ==="
git status --short | grep -E "backend/|app/api" | head -10
echo ""
echo "=== Recent Commits (if any) ==="
git log --oneline -5 2>/dev/null || echo "No recent commits"