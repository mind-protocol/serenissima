#!/usr/bin/env python3
"""
Type messages into an existing Claude Code interactive session
"""

import time
import subprocess
import sys
from datetime import datetime

try:
    import pyautogui
    import pygetwindow as gw
    import pyperclip
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pygetwindow", "pyperclip"])
    import pyautogui
    import pygetwindow as gw
    import pyperclip

pyautogui.FAILSAFE = False

def find_claude_terminal():
    """Find terminal with Claude Code running"""
    print("🔍 Looking for terminal with Claude Code...")
    
    # List all windows for user to choose
    all_windows = gw.getAllWindows()
    windows_with_titles = [(i, w) for i, w in enumerate(all_windows) if w.title and w.title.strip()]
    
    print("\nWhich terminal is running Claude Code?")
    print("(Look for the one where you started 'claude' command)")
    print("\nAvailable windows:")
    
    for i, (_, window) in enumerate(windows_with_titles[:15]):
        print(f"  {i}: {window.title}")
    
    while True:
        try:
            choice = input("\nEnter number: ")
            idx = int(choice)
            if 0 <= idx < len(windows_with_titles):
                return windows_with_titles[idx][1]
        except:
            print("Please enter a valid number")

def type_to_claude(window, message):
    """Type a message into Claude Code"""
    try:
        # Activate window
        window.activate()
        time.sleep(0.5)
        
        # Click in the middle to ensure focus
        x = window.left + window.width // 2
        y = window.top + window.height // 2
        pyautogui.click(x, y)
        time.sleep(0.5)
        
        # Type the message
        print(f"📝 Typing message...")
        pyautogui.write(message, interval=0.02)
        time.sleep(0.5)
        
        # Press Enter to send
        pyautogui.press('enter')
        
        print(f"✓ Message sent at {datetime.now().strftime('%H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def type_using_clipboard(window, message):
    """Alternative: paste using clipboard"""
    try:
        window.activate()
        time.sleep(0.5)
        
        # Click to focus
        x = window.left + window.width // 2
        y = window.top + window.height // 2
        pyautogui.click(x, y)
        time.sleep(0.5)
        
        # Copy to clipboard
        pyperclip.copy(message)
        time.sleep(0.2)
        
        # Paste
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # Press Enter
        pyautogui.press('enter')
        
        print(f"✓ Message pasted at {datetime.now().strftime('%H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🌊 Claude Code Auto-Messenger")
    print("=" * 50)
    print("This will type messages into your existing Claude Code session")
    print("")
    
    # Find the Claude terminal
    terminal = find_claude_terminal()
    print(f"\n✓ Selected: {terminal.title}")
    
    # Ask for method
    print("\nWhich method to use?")
    print("1. Type character by character")
    print("2. Paste from clipboard")
    method = input("Enter 1 or 2: ").strip()
    
    use_clipboard = method == "2"
    
    # Message to send
    message = "Continue shepherding souls. Check for any citizens needing awakening."
    
    interval = 120  # 2 minutes
    print(f"\n⏰ Will send message every {interval} seconds")
    print("📍 Press Ctrl+C to stop\n")
    
    while True:
        try:
            print(f"\n🔔 Sending message...")
            
            if use_clipboard:
                success = type_using_clipboard(terminal, message)
            else:
                success = type_to_claude(terminal, message)
            
            if success:
                print(f"💤 Waiting {interval} seconds...")
                time.sleep(interval)
            else:
                print("Retrying in 10 seconds...")
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopped")
            break

if __name__ == "__main__":
    main()