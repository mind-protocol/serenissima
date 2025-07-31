#!/bin/bash
# Torre dell'Occhio Auto-Rebuilder Dependencies Installation

echo "🏛️ Torre dell'Occhio - Installing Auto-Rebuilder Dependencies"

# Install Python watchdog for file system monitoring
echo "📦 Installing Python watchdog..."
pip install watchdog

# Verify installation
python3 -c "import watchdog; print('✅ watchdog installed successfully')" 2>/dev/null || {
    echo "❌ watchdog installation failed"
    echo "Try: pip3 install watchdog"
    exit 1
}

echo "🏛️ Torre Auto-Rebuilder dependencies ready"
echo "🔧 Usage: The auto-rebuilder will start automatically with 'python backend/run.py'"
echo "👁️ It will watch Torre UI src/ files and auto-restart on changes"