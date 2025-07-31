#!/usr/bin/env python3
"""Test the sync debug memory capture script"""

import json
import subprocess

# Use the exact hook data from the log for Arsenal_BackendArchitect_1
test_hook_data = {
    "session_id": "3b5a3771-9fc2-4d01-a26c-27b992a26112",
    "transcript_path": "/home/lester/.claude/projects/-mnt-c-Users-reyno-universe-engine-serenissima-san-marco-consciousness-architecture-cistern-house-citizen-memory-cascade-mechanical-visionary/3b5a3771-9fc2-4d01-a26c-27b992a26112.jsonl",
    "hook_event_name": "PostToolUse",
    "tool_name": "Write",
    "tool_input": {
        "file_path": "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/sync_debug_test.txt",
        "content": "Sync debug test for memory capture\\nShould create a memory in Arsenal_BackendArchitect_1 .cascade"
    }
}

print("=== Testing Sync Debug Memory Capture Script ===")

# Test the script
try:
    result = subprocess.run([
        'python3', 
        '/mnt/c/Users/reyno/universe-engine/serenissima/.global_cascade_hooks/conscious_memory_capture_sync_debug.py'
    ], 
    input=json.dumps(test_hook_data), 
    text=True, 
    capture_output=True
    )
    
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
        
except Exception as e:
    print(f"Error testing script: {e}")
    import traceback
    traceback.print_exc()