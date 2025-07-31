#!/usr/bin/env python3
"""
Fix Torre hooks in .claude.json with proper matchers
The hooks exist but lack matcher fields, causing Claude Code to skip them
"""

import json
import os

CLAUDE_JSON_PATH = "/home/lester/.claude.json"
TORRE_HOOK_SCRIPT = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks/capture_post_tool_use.py"

def fix_torre_hooks():
    """Fix Torre hooks with proper matcher structure"""
    
    # Load current config
    with open(CLAUDE_JSON_PATH, 'r') as f:
        config = json.load(f)
    
    # Fix PostToolUse hooks - need matcher for tool types
    if "PostToolUse" in config["hooks"]:
        # Clear existing broken hooks
        config["hooks"]["PostToolUse"] = [
            {
                "matcher": "Write|Edit|MultiEdit|NotebookEdit|Read|Bash|Task|WebFetch|WebSearch",
                "hooks": [
                    {
                        "type": "command", 
                        "command": f"python3 {TORRE_HOOK_SCRIPT}"
                    }
                ]
            }
        ]
        print("✅ Fixed PostToolUse hooks with proper matcher")
    
    # Fix PreToolUse hooks - need matcher for tool types
    if "PreToolUse" not in config["hooks"]:
        config["hooks"]["PreToolUse"] = []
    
    config["hooks"]["PreToolUse"] = [
        {
            "matcher": "Write|Edit|MultiEdit|NotebookEdit|Read|Bash|Task|WebFetch|WebSearch",
            "hooks": [
                {
                    "type": "command",
                    "command": f"python3 {TORRE_HOOK_SCRIPT}"
                }
            ]
        }
    ]
    print("✅ Added PreToolUse hooks with proper matcher")
    
    # UserPromptSubmit and Stop don't need matchers - they already work correctly
    
    # Save fixed config
    with open(CLAUDE_JSON_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Torre hooks fixed with proper matchers!")
    print("\nFixed hooks:")
    print("- PreToolUse: Will capture all major tool uses")
    print("- PostToolUse: Will capture all major tool uses")
    print("- UserPromptSubmit: Already working correctly")
    print("- Stop: Already working correctly")
    
    return True

if __name__ == "__main__":
    print("🔧 Fixing Torre hooks in .claude.json with proper matchers...")
    success = fix_torre_hooks()
    
    if success:
        print("\n🎉 Torre hooks are now properly configured!")
        print("Test with any tool use (Write, Edit, Read, etc.) and check debug output")
    
    exit(0 if success else 1)