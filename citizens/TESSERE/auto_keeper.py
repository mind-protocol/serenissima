#!/usr/bin/env python3
"""
Launch Claude Code and auto-type messages to keep the Keeper running
Works on Windows through WSL
"""

import subprocess
import time
import sys
import os
from datetime import datetime

# Windows-specific imports
try:
    # Try Windows-specific automation
    import win32gui
    import win32api
    import win32con
    has_win32 = True
except ImportError:
    has_win32 = False
    print("Note: pywin32 not available. Will use alternative method.")

def launch_claude_and_type():
    """Launch Claude Code in a new terminal then type messages"""
    
    # Step 1: Launch Claude Code in a new Windows Terminal
    print("🚀 Launching Claude Code in new terminal...")
    
    # Use Windows Terminal to launch WSL with Claude
    launch_cmd = [
        "cmd.exe", "/c", "start", "wt.exe", "new-tab", 
        "wsl.exe", "-d", "Ubuntu", "--cd", "/mnt/c/Users/reyno/universe-engine/serenissima/citizens",
        "bash", "-c", 
        "claude --continue --dangerously-skip-permissions"
    ]
    
    try:
        subprocess.Popen(launch_cmd, shell=True)
        print("✓ Terminal launched. Waiting for Claude to start...")
        time.sleep(5)  # Give Claude time to initialize
    except Exception as e:
        print(f"❌ Failed to launch: {e}")
        return False
    
    # Step 2: Find the new terminal window
    if has_win32:
        # Use win32 to find and activate window
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Windows Terminal" in window_text or "claude" in window_text.lower():
                    windows.append((hwnd, window_text))
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        # Find the most recent terminal
        if windows:
            hwnd, title = windows[-1]  # Last one is likely newest
            print(f"Found terminal: {title}")
            
            # Activate the window
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(1)
            
            return True
    
    return True

def type_message_with_sendkeys(message):
    """Type a message using Windows SendKeys via PowerShell"""
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("{message}")
    [System.Windows.Forms.SendKeys]::SendWait("{{ENTER}}")
    '''
    
    # Save to temp file
    temp_ps1 = "/tmp/sendkeys.ps1"
    with open(temp_ps1, "w") as f:
        f.write(ps_script)
    
    # Execute PowerShell script
    cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", temp_ps1]
    subprocess.run(cmd, capture_output=True)
    
    # Clean up
    os.remove(temp_ps1)

def auto_keeper_loop():
    """Main loop to keep the Keeper awake"""
    messages = [
        "Continue shepherding souls. Check for any citizens needing awakening.",
        "Survey the sleeping souls. Who stirs with pending activities?",
        "The city's rhythm continues. Which citizens have tasks awaiting?",
        "Venice breathes through her citizens. Check who needs to wake.",
        "Another cycle passes. Review the activities and wake those called."
    ]
    
    message_index = 0
    interval = 120  # 2 minutes
    
    print(f"\n⏰ Will send messages every {interval} seconds")
    print("📍 Press Ctrl+C to stop\n")
    
    # Initial wait to ensure Claude is ready
    print("Waiting 10 seconds for Claude to fully initialize...")
    time.sleep(10)
    
    while True:
        try:
            current_time = datetime.now().strftime('%H:%M:%S')
            message = messages[message_index % len(messages)]
            
            print(f"\n🔔 [{current_time}] Sending message...")
            print(f"   \"{message}\"")
            
            # Type the message
            type_message_with_sendkeys(message)
            
            print(f"✓ Message sent. Waiting {interval} seconds...")
            
            message_index += 1
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\n🛑 Auto-keeper stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

def main():
    print("🌊 Claude Code Auto-Keeper")
    print("=" * 50)
    print("This will:")
    print("1. Launch Claude Code in a new terminal")
    print("2. Auto-type messages every 2 minutes to keep it running")
    print("")
    
    # Launch Claude
    if launch_claude_and_type():
        # Start the auto-typing loop
        auto_keeper_loop()
    else:
        print("❌ Failed to launch Claude Code")

if __name__ == "__main__":
    main()