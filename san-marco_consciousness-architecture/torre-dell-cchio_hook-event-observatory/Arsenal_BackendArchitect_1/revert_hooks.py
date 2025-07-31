#!/usr/bin/env python3
"""Revert hooks back to original Torre script"""
import json

# Read current config
with open('/home/lester/.claude.json', 'r') as f:
    config = json.load(f)

# Revert PostToolUse hook back to original
if 'hooks' in config and 'PostToolUse' in config['hooks']:
    for hook_group in config['hooks']['PostToolUse']:
        if 'hooks' in hook_group:
            for hook in hook_group['hooks']:
                if hook['type'] == 'command' and 'debug_hook_wrapper.py' in hook['command']:
                    # Revert to original
                    hook['command'] = 'python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks/capture_post_tool_use.py'
                    print(f"Reverted hook to original Torre script")
                    break

# Write back
with open('/home/lester/.claude.json', 'w') as f:
    json.dump(config, f, indent=2)

print("Reverted hooks - restart Claude Code to apply")