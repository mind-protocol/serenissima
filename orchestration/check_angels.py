#!/usr/bin/env python3
"""Check status of Venice angels"""

import subprocess
import json

def check_angel(session_name, window):
    """Check if an angel is responsive"""
    try:
        # Capture pane content
        cmd = f"tmux capture-pane -t {session_name}:{window} -p"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        
        content = result.stdout.strip()
        
        # Check for Claude prompt
        if "You:" in content or "Claude:" in content or "Assistant:" in content:
            return "Active", content[-200:]  # Last 200 chars
        elif "Waiting" in content or "Loading" in content:
            return "Starting", content[-100:]
        elif content:
            return "Running", content[-100:]
        else:
            return "Empty", "No output"
            
    except Exception as e:
        return "Error", str(e)

def main():
    print("🌊 Venice Angel Status Check")
    print("=" * 40)
    
    angels = [
        ("venice-simple", "0", "Message Angel"),
        ("venice-simple", "story", "Story Angel"),
        ("venice-simple", "narrator", "Narrator Angel")
    ]
    
    for session, window, name in angels:
        status, detail = check_angel(session, window)
        print(f"\n{name}:")
        print(f"  Status: {status}")
        if status == "Active":
            print(f"  Last activity: {detail[:50]}...")
    
    print("\n" + "=" * 40)
    print("✅ Check complete")

if __name__ == "__main__":
    main()