#!/usr/bin/env python3
"""Debug wrapper to see what Claude Code actually sends to hooks"""
import json
import sys
from datetime import datetime

# Log the raw input
debug_log = f"/tmp/torre_hook_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

try:
    # Read from stdin
    raw_input = sys.stdin.read()
    
    # Log it
    with open(debug_log, 'w') as f:
        f.write("=== RAW INPUT ===\n")
        f.write(raw_input)
        f.write("\n\n=== PARSED ===\n")
        try:
            parsed = json.loads(raw_input)
            f.write(json.dumps(parsed, indent=2))
        except:
            f.write("Failed to parse as JSON")
    
    print(f"Debug log written to: {debug_log}")
    
    # Also call the real hook
    import subprocess
    result = subprocess.run(
        ["python3", "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks/capture_post_tool_use.py"],
        input=raw_input,
        text=True,
        capture_output=True
    )
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
        
except Exception as e:
    with open(debug_log, 'a') as f:
        f.write(f"\n\nERROR: {str(e)}\n")
    print(f"Error: {str(e)}", file=sys.stderr)