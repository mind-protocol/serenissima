#!/usr/bin/env python3
"""Fix all Torre hooks by directly updating the config file"""
import json
import re

# Read current config
with open('/home/lester/.claude.json', 'r') as f:
    content = f.read()

# The correct full path
correct_path = "python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks/capture_post_tool_use.py"

# Parse as JSON to properly update
config = json.loads(content)

# Update all hooks that contain torre-dell-cchio
if 'hooks' in config:
    for hook_type, hook_list in config['hooks'].items():
        for hook_group in hook_list:
            if 'hooks' in hook_group:
                for hook in hook_group['hooks']:
                    if 'command' in hook and 'torre-dell-cchio' in hook['command']:
                        print(f"Fixing {hook_type} hook:")
                        print(f"  Old: {hook['command']}")
                        hook['command'] = correct_path
                        print(f"  New: {hook['command']}")

# Write back
with open('/home/lester/.claude.json', 'w') as f:
    json.dump(config, f, indent=2)

print("\nAll hooks fixed! The correct path is now set.")