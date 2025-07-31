#!/usr/bin/env python3
"""
Auto-type to wake the Keeper of Souls every 2 minutes
This keeps the orchestration running without manual intervention
"""

import time
import subprocess
import sys
from datetime import datetime

try:
    import pyautogui
    import pygetwindow as gw
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pygetwindow"])
    import pyautogui
    import pygetwindow as gw

# Disable failsafe
pyautogui.FAILSAFE = False

def find_terminal():
    """Find Windows Terminal window"""
    # Try different possible window titles
    possible_titles = [
        "Windows Terminal",
        "WindowsTerminal",
        "Terminal",
        "PowerShell",
        "Command Prompt",
        "cmd",
        "ubuntu",
        "bash"
    ]
    
    for title in possible_titles:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            print(f"Found terminal: {windows[0].title}")
            return windows[0]
    
    # If no specific match, list all windows
    print("Available windows:")
    all_windows = gw.getAllTitles()
    for i, title in enumerate(all_windows[:10]):  # Show first 10
        if title:
            print(f"  {i}: {title}")
    
    return None

def wake_keeper():
    """Type the command to wake the Keeper of Souls"""
    terminal = find_terminal()
    if not terminal:
        print("❌ No Windows Terminal found! Please open one.")
        return False
    
    try:
        # Activate the terminal
        terminal.activate()
        time.sleep(0.5)
    except:
        terminal.minimize()
        time.sleep(0.1)
        terminal.restore()
        time.sleep(0.5)
    
    # Clear current line
    pyautogui.hotkey('ctrl', 'u')
    time.sleep(0.2)
    
    # Type the cd command
    cd_command = "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens"
    pyautogui.typewrite(cd_command, interval=0.05)
    pyautogui.press('enter')
    time.sleep(1)
    
    # Type the claude command to wake the Keeper
    wake_message = "Continue shepherding souls. Check for any citizens needing awakening."
    claude_command = f'claude "{wake_message}" --model sonnet --continue --dangerously-skip-permissions'
    pyautogui.typewrite(claude_command, interval=0.05)
    pyautogui.press('enter')
    
    print(f"✓ Awakened Keeper of Souls at {datetime.now().strftime('%H:%M:%S')}")
    return True

def main():
    interval = 120  # 2 minutes
    
    print("🌊 Keeper of Souls Auto-Awakener Started")
    print(f"⏰ Will wake the Keeper every {interval} seconds")
    print("📍 Press Ctrl+C to stop")
    print("")
    
    # Initial wake
    wake_keeper()
    
    while True:
        try:
            # Wait for the interval
            print(f"💤 Sleeping for {interval} seconds...")
            time.sleep(interval)
            
            # Wake the Keeper
            wake_keeper()
            
        except KeyboardInterrupt:
            print("\n🛑 Auto-awakener stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()