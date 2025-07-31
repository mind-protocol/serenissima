# Testing memory capture system functionality

**Created**: 2025-07-25T05:10:46.559776
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/seeking-engine_proactive-consciousness-machine/debug_hook_data.py

## File Content
#!/usr/bin/env python3
"""
Debug script to see what data is available in hooks
"""

import json
import sys
import os

def debug_hook_data():
    try:
        # Read hook input
        hook_data = json.load(sys.stdin)
        
        # Write debug info to a file
        debug_file = "/tmp/claude_hook_debug.json"
        with open(debug_file, 'w') as f:
            json.dump({
                "hook_data": hook_data,
                "environment": dict(os.environ),
                "cwd": os.getcwd()
            }, f, indent=2)
        
        print(f"**Debug**: Hook data written to {debug_file}", file=sys.stderr)
        sys.exit(2)
        
    except Exception as e:
        print(f"**Debug Error**: {str(e)}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    debug_hook_data()

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*