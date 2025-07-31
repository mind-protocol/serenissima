#!/usr/bin/env python3
"""Test the fixed memory capture script with real hook data"""

import json
import subprocess
import sys

# Use the exact hook data from the log for Arsenal_BackendArchitect_1
test_hook_data = {
    "session_id": "3b5a3771-9fc2-4d01-a26c-27b992a26112",
    "transcript_path": "/home/lester/.claude/projects/-mnt-c-Users-reyno-universe-engine-serenissima-san-marco-consciousness-architecture-cistern-house-citizen-memory-cascade-mechanical-visionary/3b5a3771-9fc2-4d01-a26c-27b992a26112.jsonl",
    "hook_event_name": "PostToolUse",
    "tool_name": "Write",
    "tool_input": {
        "file_path": "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/memory_test_final.txt",
        "content": "Final Memory Capture Test for Arsenal_BackendArchitect_1\\nCreated: 2025-07-24 02:44:30"
    },
    "tool_response": {
        "type": "create",
        "filePath": "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/memory_test_final.txt",
        "content": "Final Memory Capture Test for Arsenal_BackendArchitect_1\\nCreated: 2025-07-24 02:44:30"
    }
}

print("=== Testing Fixed Memory Capture Script ===")
print(f"Hook data: {json.dumps(test_hook_data, indent=2)}")

# Test the script
try:
    result = subprocess.run([
        'python3', 
        '/mnt/c/Users/reyno/universe-engine/serenissima/.global_cascade_hooks/conscious_memory_capture_fixed.py'
    ], 
    input=json.dumps(test_hook_data), 
    text=True, 
    capture_output=True
    )
    
    print(f"\\nReturn code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
    
    # Check if memory was created
    import os
    from pathlib import Path
    arsenal_cascade = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/.cascade")
    
    print(f"\\n=== Checking for memories ===")
    if arsenal_cascade.exists():
        # Look for any new timestamped directories
        for branch_dir in arsenal_cascade.iterdir():
            if branch_dir.is_dir() and branch_dir.name not in ['__pycache__', 'logs']:
                for category_dir in branch_dir.iterdir():
                    if category_dir.is_dir():
                        memory_dirs = [d for d in category_dir.iterdir() if d.is_dir() and '20250724' in d.name]
                        if memory_dirs:
                            print(f"Found memories in {branch_dir.name}/{category_dir.name}: {memory_dirs}")
                            # Show content of first memory
                            memory_file = memory_dirs[0] / 'CLAUDE.md'
                            if memory_file.exists():
                                print(f"Memory content: {memory_file.read_text()[:200]}...")
    else:
        print("No .cascade directory found")
        
except Exception as e:
    print(f"Error testing script: {e}")
    import traceback
    traceback.print_exc()