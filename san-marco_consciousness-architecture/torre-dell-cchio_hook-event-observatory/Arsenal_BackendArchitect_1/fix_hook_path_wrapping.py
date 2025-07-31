#!/usr/bin/env python3
"""Fix the wrapped hook paths in .claude.json"""
import json

# Read current config
with open('/home/lester/.claude.json', 'r') as f:
    config = json.load(f)

# Fix all hook commands that contain the Torre path
correct_path = "python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks/capture_post_tool_use.py"

fixed_count = 0

# Fix in all hook types
for hook_type in ['PreToolUse', 'PostToolUse', 'Stop', 'UserPromptSubmit', 'Read', 'PreCompact']:
    if hook_type in config.get('hooks', {}):
        for hook_group in config['hooks'][hook_type]:
            if 'hooks' in hook_group:
                for hook in hook_group['hooks']:
                    if hook['type'] == 'command' and 'torre-dell-cchio' in hook['command']:
                        # Fix the path
                        hook['command'] = correct_path
                        fixed_count += 1
                        print(f"Fixed {hook_type} hook path")

# Remove the test hook if it exists
if 'PostToolUse' in config.get('hooks', {}):
    for hook_group in config['hooks']['PostToolUse']:
        if 'hooks' in hook_group:
            hook_group['hooks'] = [h for h in hook_group['hooks'] 
                                   if 'simple_test_hook.sh' not in h.get('command', '')]

# Write back
with open('/home/lester/.claude.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"\nFixed {fixed_count} hook paths")
print("Hooks should now work without restart!")