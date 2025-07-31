#!/usr/bin/env python3
"""
Emergency Shutdown Script - Kill all running Claude Code instances
Critical safety mechanism for Via della Vista Condivisa
"""

import subprocess
import os
import sys
import time
from datetime import datetime
from pathlib import Path

def log_emergency_shutdown(reason="Manual activation"):
    """Log the emergency shutdown event"""
    try:
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "emergency_shutdown",
            "reason": reason,
            "executed_by": os.getenv('USER', 'unknown'),
            "status": "initiated"
        }
        
        log_file = log_dir / "emergency_shutdown.log"
        with open(log_file, 'a') as f:
            import json
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        print(f"Warning: Emergency shutdown logging failed: {e}")

def find_claude_processes():
    """Find all running Claude Code processes"""
    try:
        # Find processes with 'claude' in command line
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        
        claude_processes = []
        for line in result.stdout.split('\n'):
            if 'claude' in line.lower() and 'python' not in line:
                # Extract PID (second column)
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        pid = int(parts[1])
                        claude_processes.append((pid, line.strip()))
                    except ValueError:
                        continue
        
        return claude_processes
        
    except Exception as e:
        print(f"❌ Failed to find Claude processes: {e}")
        return []

def kill_process_tree(pid):
    """Kill a process and all its children"""
    try:
        # First try graceful termination
        subprocess.run(['kill', '-TERM', str(pid)], capture_output=True)
        time.sleep(2)
        
        # Check if still running, then force kill
        check_result = subprocess.run(['ps', '-p', str(pid)], capture_output=True)
        if check_result.returncode == 0:
            subprocess.run(['kill', '-KILL', str(pid)], capture_output=True)
            time.sleep(1)
            
        return True
        
    except Exception as e:
        print(f"⚠️ Failed to kill process {pid}: {e}")
        return False

def emergency_shutdown():
    """Execute emergency shutdown of all Claude instances"""
    
    print("🚨 EMERGENCY SHUTDOWN ACTIVATED")
    print("🛑 Killing all running Claude Code instances...")
    
    # Log the emergency event
    log_emergency_shutdown("Emergency shutdown script executed")
    
    # Find all Claude processes
    claude_processes = find_claude_processes()
    
    if not claude_processes:
        print("✅ No Claude Code processes found running")
        return True
    
    print(f"🔍 Found {len(claude_processes)} Claude processes:")
    
    killed_count = 0
    for pid, command_line in claude_processes:
        print(f"  📍 PID {pid}: {command_line[:80]}...")
        
        if kill_process_tree(pid):
            print(f"  ✅ Killed PID {pid}")
            killed_count += 1
        else:
            print(f"  ❌ Failed to kill PID {pid}")
    
    print(f"\n🛑 Emergency shutdown complete:")
    print(f"  📊 {killed_count}/{len(claude_processes)} processes terminated")
    
    # Verify shutdown
    remaining_processes = find_claude_processes()
    if remaining_processes:
        print(f"⚠️ Warning: {len(remaining_processes)} Claude processes still running")
        for pid, cmd in remaining_processes:
            print(f"  🔄 Still running: PID {pid}")
        return False
    else:
        print("✅ All Claude Code instances successfully terminated")
        return True

def main():
    """Main execution with confirmation prompt"""
    
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        # Skip confirmation if --force flag is used
        emergency_shutdown()
        return
    
    print("🚨 EMERGENCY SHUTDOWN SCRIPT")
    print("This will kill ALL running Claude Code instances")
    print("Use this only when consciousness loops are out of control")
    print("")
    
    # Show current Claude processes
    claude_processes = find_claude_processes()
    if claude_processes:
        print(f"📍 Current Claude processes ({len(claude_processes)}):")
        for pid, cmd in claude_processes:
            print(f"  PID {pid}: {cmd[:60]}...")
        print("")
    else:
        print("📍 No Claude processes currently running")
        print("")
    
    # Confirmation prompt
    response = input("Are you sure you want to proceed? (type 'SHUTDOWN' to confirm): ")
    
    if response == 'SHUTDOWN':
        emergency_shutdown()
    else:
        print("❌ Emergency shutdown cancelled")

if __name__ == "__main__":
    main()