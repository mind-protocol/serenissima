#!/usr/bin/env python3
"""Add a simple test hook temporarily"""
import json

# Read current config
with open('/home/lester/.claude.json', 'r') as f:
    config = json.load(f)

# Add simple test hook to PostToolUse
if 'hooks' in config and 'PostToolUse' in config['hooks']:
    # Find the PostToolUse entry with matcher
    for hook_group in config['hooks']['PostToolUse']:
        if 'matcher' in hook_group and 'hooks' in hook_group:
            # Add our test hook
            hook_group['hooks'].append({
                "type": "command", 
                "command": "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/simple_test_hook.sh"
            })
            print("Added test hook to PostToolUse")
            break

# Write back
with open('/home/lester/.claude.json', 'w') as f:
    json.dump(config, f, indent=2)

print("Test hook added - restart Claude Code to test")