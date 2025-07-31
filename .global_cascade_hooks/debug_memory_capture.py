#!/usr/bin/env python3
"""Debug the memory capture script directly with sample data"""

import json
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_memory_capture():
    """Test memory capture with simulated hook data"""
    
    # Simulate the data structure that PostToolUse hooks should receive
    test_data = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/hook_test_trigger.txt",
            "content": "Testing hook execution - 2025-07-24 02:43:00\\nThis Write operation should trigger the test hook if configured correctly."
        },
        "tool_output": "File created successfully",
        "transcript_path": "mock_transcript.txt"
    }
    
    print("=== Testing Memory Capture Script ===")
    print(f"Test data: {json.dumps(test_data, indent=2)}")
    
    # Set working directory to Arsenal_BackendArchitect_1
    test_cwd = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1"
    os.chdir(test_cwd)
    print(f"Working directory: {os.getcwd()}")
    
    # Check if .cascade exists
    cascade_dir = Path(".cascade")
    print(f".cascade exists: {cascade_dir.exists()}")
    if cascade_dir.exists():
        print(f".cascade contents: {list(cascade_dir.iterdir())}")
    
    # Import and run the memory capture function
    try:
        from conscious_memory_capture import capture_with_consciousness
        
        print("\\n=== Running Memory Capture ===")
        result = capture_with_consciousness(test_data)
        print(f"Result: {result}")
        
        # Check if any memory files were created
        print("\\n=== Checking for Created Memories ===")
        for branch_dir in cascade_dir.iterdir():
            if branch_dir.is_dir() and branch_dir.name != '__pycache__':
                print(f"Checking {branch_dir.name}...")
                for category_dir in branch_dir.iterdir():
                    if category_dir.is_dir():
                        memory_files = list(category_dir.glob("*memory*"))
                        if memory_files:
                            print(f"  Found memories in {category_dir.name}: {memory_files}")
        
    except Exception as e:
        print(f"Error running memory capture: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_capture()