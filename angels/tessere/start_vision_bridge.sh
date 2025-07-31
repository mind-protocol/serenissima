#!/bin/bash
# Start continuous vision bridge with auto-update

echo "🔄 Starting Vision Bridge - Continuous Capture"
echo "👁️  Updates CLAUDE.md automatically"
echo "📸 Captures every 10 seconds"
echo "Press Ctrl+C to stop"

cd /mnt/c/Users/reyno/universe-engine/serenissima/TESSERE
python3 vision_bridge_wsl.py