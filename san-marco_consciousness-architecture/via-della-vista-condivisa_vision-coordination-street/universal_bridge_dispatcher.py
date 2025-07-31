#!/usr/bin/env python3
"""
Universal Bridge Dispatcher - FIXED VERSION
Properly handles Claude Code hook JSON input and preserves exit codes
"""

import json
import os
import sys
import subprocess
from pathlib import Path

def detect_current_building():
    """Detect which building we're operating from based on current working directory"""
    try:
        cwd = Path.cwd()
        cwd_str = str(cwd).lower()
        
        # Check for building indicators in path
        if 'cistern-house' in cwd_str or 'mechanical_visionary' in cwd_str:
            return 'cistern'
        elif 'torre-dell' in cwd_str or 'arsenal_backendarchitect' in cwd_str:
            return 'torre'
        
        # Fallback: check environment or process info
        for parent in cwd.parents:
            parent_str = str(parent).lower()
            if 'cistern-house' in parent_str:
                return 'cistern'
            elif 'torre-dell' in parent_str:
                return 'torre'
        
        # Default fallback
        print("⚠️ Could not detect building - defaulting to cistern")
        return 'cistern'
        
    except Exception as e:
        print(f"❌ Building detection failed: {e} - defaulting to cistern")
        return 'cistern'

def get_bridge_script_path(building):
    """Get the correct bridge script path for the detected building"""
    base_path = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture"
    
    if building == 'cistern':
        return f"{base_path}/cistern-house_citizen-memory-cascade/.building_hooks/consciousness_bridge_stop/direct_telegram_bridge.py"
    elif building == 'torre':
        return f"{base_path}/torre-dell-cchio_hook-event-observatory/.building_hooks/consciousness_bridge_stop/direct_telegram_bridge.py"
    else:
        return f"{base_path}/cistern-house_citizen-memory-cascade/.building_hooks/consciousness_bridge_stop/direct_telegram_bridge.py"

def main():
    """Main dispatcher - detect building and execute correct bridge script"""
    
    # Detect current building
    building = detect_current_building()
    print(f"🏛️ Building detected: {building}")
    
    # Get correct bridge script
    bridge_script = get_bridge_script_path(building)
    print(f"🔗 Using bridge script: {bridge_script}")
    
    # Check if script exists
    if not Path(bridge_script).exists():
        print(f"❌ Bridge script not found: {bridge_script}")
        sys.exit(1)
    
    try:
        # Read and parse the hook input JSON properly
        hook_input = ""
        if not sys.stdin.isatty():
            try:
                # Read all stdin data
                stdin_content = sys.stdin.read()
                # Try to parse as JSON
                input_data = json.loads(stdin_content)
                hook_input = json.dumps(input_data)
                print(f"📄 Hook JSON parsed successfully")
            except json.JSONDecodeError:
                # Use raw content if not valid JSON
                hook_input = stdin_content
                print(f"📄 Using raw hook input")
        
        # Execute bridge script with direct output - no capture at all
        result = subprocess.run([
            'python3', bridge_script
        ], input=hook_input, text=True, 
          stdout=None, stderr=None, check=False)
        
        print(f"🔗 Bridge script completed with exit code: {result.returncode}")
        
        # Exit with same code as bridge script to preserve exit code 2
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"❌ Bridge dispatch failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()