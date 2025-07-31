#!/usr/bin/env python3
"""
Hook Memory Wrapper - Robust hook integration for memory capture

Handles hook environment issues like empty stdin, funding problems, and environment differences.
"""

import json
import sys
import subprocess
import os
from pathlib import Path
import time

def safe_memory_capture():
    """Safely capture memory even when hook environment is problematic"""
    
    try:
        # Try to read stdin with timeout and error handling
        input_data = None
        
        # Method 1: Direct stdin read with error handling
        try:
            stdin_content = sys.stdin.read().strip()
            if stdin_content:
                input_data = json.loads(stdin_content)
            else:
                print("DEBUG: Empty stdin received in hook", file=sys.stderr)
                return
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON parse error in hook: {e}", file=sys.stderr)
            return
        except Exception as e:
            print(f"DEBUG: Stdin read error in hook: {e}", file=sys.stderr)
            return
        
        if not input_data:
            print("DEBUG: No valid input data for memory capture", file=sys.stderr)
            return
        
        # Extract file info
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')
        
        if not file_path:
            print("DEBUG: No file path in hook data", file=sys.stderr)
            return
        
        # Check if this file/directory should create memories
        target_dir = Path(file_path).parent
        cascade_dir = target_dir / '.cascade'
        
        if not cascade_dir.exists():
            print(f"DEBUG: No .cascade in {target_dir}, skipping", file=sys.stderr)
            return
        
        print(f"DEBUG: Processing memory capture for {file_path}", file=sys.stderr)
        
        # Call the actual memory capture script as subprocess to avoid environment issues
        memory_script = Path(__file__).parent / 'conscious_memory_capture_sync_debug.py'
        
        # Create a safe environment for the subprocess
        env = os.environ.copy()
        env['PYTHONPATH'] = str(Path(__file__).parent)
        
        # Call memory capture with proper input
        result = subprocess.run([
            'python3', str(memory_script)
        ], 
        input=json.dumps(input_data), 
        text=True, 
        capture_output=True,
        env=env,
        timeout=30  # 30 second timeout
        )
        
        if result.returncode == 0:
            print("DEBUG: Memory capture subprocess succeeded", file=sys.stderr)
            if result.stdout:
                print(f"Memory capture output: {result.stdout[-200:]}", file=sys.stderr)  # Last 200 chars
        else:
            print(f"DEBUG: Memory capture subprocess failed: {result.stderr}", file=sys.stderr)
            
    except subprocess.TimeoutExpired:
        print("DEBUG: Memory capture subprocess timeout", file=sys.stderr)
    except Exception as e:
        print(f"DEBUG: Memory capture wrapper error: {e}", file=sys.stderr)

if __name__ == "__main__":
    safe_memory_capture()