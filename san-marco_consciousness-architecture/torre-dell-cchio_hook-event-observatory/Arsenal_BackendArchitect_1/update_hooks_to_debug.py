#!/usr/bin/env python3
"""Update hooks to use debug wrapper temporarily"""
import json

# Read current config
with open('/home/lester/.claude.json', 'r') as f:
    config = json.load(f)

# Update PostToolUse hook to use debug wrapper
if 'hooks' in config and 'PostToolUse' in config['hooks']:
    for hook_group in config['hooks']['PostToolUse']:
        if 'hooks' in hook_group:
            for hook in hook_group['hooks']:
                if hook['type'] == 'command' and 'capture_post_tool_use.py' in hook['command']:
                    # Update to use debug wrapper
                    hook['command'] = 'python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/debug_hook_wrapper.py'
                    print(f"Updated hook to use debug wrapper")
                    break

# Write back
with open('/home/lester/.claude.json', 'w') as f:
    json.dump(config, f, indent=2)

print("Updated hooks to use debug wrapper - restart Claude Code to apply")