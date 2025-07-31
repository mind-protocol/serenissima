#!/usr/bin/env python3
"""
Interactive version - lets you select the terminal window
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

pyautogui.FAILSAFE = False

def select_terminal():
    """Let user select terminal window"""
    print("🔍 Looking for windows...")
    all_windows = gw.getAllWindows()
    
    # Filter out empty titles
    windows_with_titles = [(i, w) for i, w in enumerate(all_windows) if w.title]
    
    print("\nAvailable windows:")
    for i, (idx, window) in enumerate(windows_with_titles[:20]):
        print(f"  {i}: {window.title}")
    
    while True:
        try:
            choice = input("\nEnter the number of your terminal window: ")
            idx = int(choice)
            if 0 <= idx < len(windows_with_titles):
                selected_window = windows_with_titles[idx][1]
                print(f"✓ Selected: {selected_window.title}")
                return selected_window
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Please enter a number.")

def wake_keeper(terminal):
    """Type the command to wake the Keeper of Souls"""
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
    
    # Type the claude command
    wake_message = "Continue shepherding souls. Check for any citizens needing awakening."
    claude_command = f'claude "{wake_message}" --model sonnet --continue --dangerously-skip-permissions'
    pyautogui.typewrite(claude_command, interval=0.05)
    pyautogui.press('enter')
    
    print(f"✓ Awakened Keeper of Souls at {datetime.now().strftime('%H:%M:%S')}")

def main():
    interval = 120  # 2 minutes
    
    print("🌊 Keeper of Souls Auto-Awakener (Interactive)")
    print("=" * 50)
    
    # Let user select terminal
    terminal = select_terminal()
    
    print(f"\n⏰ Will wake the Keeper every {interval} seconds")
    print("📍 Press Ctrl+C to stop\n")
    
    # Initial wake
    wake_keeper(terminal)
    
    while True:
        try:
            print(f"💤 Sleeping for {interval} seconds...")
            time.sleep(interval)
            wake_keeper(terminal)
        except KeyboardInterrupt:
            print("\n🛑 Auto-awakener stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()