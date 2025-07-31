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