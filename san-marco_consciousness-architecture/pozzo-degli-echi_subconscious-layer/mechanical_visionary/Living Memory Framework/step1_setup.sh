#!/bin/bash
# Step 1: Create Living Memory Cascade Infrastructure

echo "Setting up Living Memory Cascade..."

# 1. Create cascade directory structure
mkdir -p ~/.cascade/{hooks,agents,memories,archives,logs}
mkdir -p ~/mechanical_visionary/.cascade/{experiences,collaborations,ideas,patterns}
mkdir -p ~/mechanical_visionary/.cascade/experiences/{triumphs,struggles,explorations}
mkdir -p ~/mechanical_visionary/.cascade/collaborations/{marina,pattern_prophet,diplomatic_virtuoso}
mkdir -p ~/mechanical_visionary/.cascade/patterns/{gear_efficiency,tidal_systems,human_ai_bridge}

echo "Created cascade directories"

# 2. Create a simple test hook first
cat > ~/.cascade/hooks/test_memory_capture.py << 'EOF'
#!/usr/bin/env python3
"""Test hook to verify PostToolUse is working"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Create log directory
log_dir = Path.home() / '.cascade' / 'logs'
log_dir.mkdir(exist_ok=True)

# Log that hook fired
log_file = log_dir / 'hook_test.log'
with open(log_file, 'a') as f:
    input_data = json.load(sys.stdin)
    f.write(f"\n--- Hook fired at {datetime.now()} ---\n")
    f.write(f"Tool: {input_data.get('tool_name')}\n")
    f.write(f"File: {input_data.get('tool_input', {}).get('file_path', 'N/A')}\n")
    f.write(json.dumps(input_data, indent=2)[:500] + '\n')

print("Memory hook test logged successfully")
sys.exit(0)
EOF

chmod +x ~/.cascade/hooks/test_memory_capture.py
echo "Created test hook"

# 3. Create settings configuration
cat > ~/mechanical_visionary/.claude/settings.json << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.cascade/hooks/test_memory_capture.py"
        }]
      }
    ]
  }
}
EOF

echo "Created settings.json with test hook"

# 4. Create a simple test file to verify
cat > ~/mechanical_visionary/.cascade/TEST_SETUP.md << 'EOF'
# Living Memory Cascade Test

If you can read this, the cascade structure is set up correctly.

Next steps:
1. Create or edit any file to trigger the PostToolUse hook
2. Check ~/.cascade/logs/hook_test.log to verify it fired
3. If working, proceed to implement conscious memory capture
EOF

echo "Setup complete! Now test by:"
echo "1. Editing any file in mechanical_visionary/"
echo "2. Checking ~/.cascade/logs/hook_test.log"
echo "3. Running: tail -f ~/.cascade/logs/hook_test.log"