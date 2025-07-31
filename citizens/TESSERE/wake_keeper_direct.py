#!/usr/bin/env python3
"""
Direct window typing with debugging
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

# Disable failsafe and add delay
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5  # Add pause between actions

def wake_keeper_method1():
    """Method 1: Click then type"""
    print("🔍 Finding PowerShell window...")
    
    windows = gw.getWindowsWithTitle("PowerShell")
    if not windows:
        windows = gw.getWindowsWithTitle("Terminal")
    
    if windows:
        window = windows[0]
        print(f"Found: {window.title}")
        
        # Method 1: Click in the center of the window first
        try:
            window.activate()
            time.sleep(1)
            
            # Get window position and click in center
            x = window.left + window.width // 2
            y = window.top + window.height // 2
            
            print(f"Clicking at position ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(0.5)
            
            # Now type
            print("Typing commands...")
            
            # Clear line
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            
            # Type cd command
            cd_cmd = "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens"
            print(f"Typing: {cd_cmd}")
            pyautogui.write(cd_cmd, interval=0.02)
            pyautogui.press('enter')
            time.sleep(2)
            
            # Type claude command
            claude_cmd = 'claude "Continue shepherding souls. Check for any citizens needing awakening." --model sonnet --continue --dangerously-skip-permissions'
            print(f"Typing: {claude_cmd}")
            pyautogui.write(claude_cmd, interval=0.02)
            pyautogui.press('enter')
            
            print("✓ Commands sent!")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("❌ No PowerShell/Terminal window found!")
        return False

def wake_keeper_method2():
    """Method 2: Use clipboard paste"""
    print("🔍 Method 2: Using clipboard...")
    
    windows = gw.getWindowsWithTitle("PowerShell")
    if not windows:
        windows = gw.getWindowsWithTitle("Terminal")
    
    if windows:
        window = windows[0]
        window.activate()
        time.sleep(1)
        
        # Click in window
        x = window.left + window.width // 2
        y = window.top + window.height // 2
        pyautogui.click(x, y)
        time.sleep(0.5)
        
        # Build full command
        full_command = (
            "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens && "
            'claude "Continue shepherding souls. Check for any citizens needing awakening." '
            '--model sonnet --continue --dangerously-skip-permissions'
        )
        
        # Copy to clipboard and paste
        import pyperclip
        pyperclip.copy(full_command)
        time.sleep(0.2)
        
        # Paste
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        pyautogui.press('enter')
        
        print("✓ Command pasted!")
        return True
    
    return False

def main():
    print("🌊 Keeper Auto-Awakener (Direct Method)")
    print("=" * 50)
    
    # Try to install pyperclip for method 2
    try:
        import pyperclip
    except ImportError:
        print("Installing pyperclip for clipboard support...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
    
    interval = 120
    method = 1
    
    while True:
        print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Waking Keeper...")
        
        if method == 1:
            success = wake_keeper_method1()
            if not success:
                print("Method 1 failed, trying method 2...")
                method = 2
                success = wake_keeper_method2()
        else:
            success = wake_keeper_method2()
        
        if success:
            print(f"💤 Sleeping for {interval} seconds...")
            time.sleep(interval)
        else:
            print("❌ Failed to send commands. Retrying in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Stopped")