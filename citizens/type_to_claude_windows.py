#!/usr/bin/env python3
"""
Simulate actual keyboard typing on Windows
This uses low-level Windows APIs to simulate real human typing
"""

import time
import random
import ctypes
from ctypes import wintypes
import sys

# Windows constants
VK_RETURN = 0x0D
KEYEVENTF_KEYUP = 0x0002

# Load Windows DLLs
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def find_claude_window():
    """Find the window with Claude Code running"""
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long)]
    
    def callback(hwnd, windows):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
                if "Terminal" in title or "PowerShell" in title or "claude" in title.lower():
                    windows.append((hwnd, title))
        return True
    
    # Enumerate all windows
    windows = []
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    user32.EnumWindows(WNDENUMPROC(callback), id(windows))
    
    if windows:
        print("Found windows:")
        for i, (hwnd, title) in enumerate(windows):
            print(f"  {i}: {title}")
        
        choice = input("\nWhich window has Claude Code? Enter number: ")
        try:
            idx = int(choice)
            return windows[idx][0]
        except:
            return None
    return None

def activate_window(hwnd):
    """Activate and focus a window"""
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)

def type_char(char):
    """Type a single character with realistic timing"""
    # Get virtual key code
    vk = ord(char.upper())
    scan = user32.MapVirtualKeyW(vk, 0)
    
    # Check if shift is needed
    if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
        user32.keybd_event(0x10, 0, 0, 0)  # Shift down
        time.sleep(0.01)
    
    # Key down
    user32.keybd_event(vk, scan, 0, 0)
    time.sleep(random.uniform(0.03, 0.08))  # Human-like delay
    
    # Key up
    user32.keybd_event(vk, scan, KEYEVENTF_KEYUP, 0)
    
    # Release shift if needed
    if char.isupper() or char in '!@#$%^&*()_+{}|:"<>?':
        user32.keybd_event(0x10, 0, KEYEVENTF_KEYUP, 0)
    
    time.sleep(random.uniform(0.01, 0.03))

def type_string(text):
    """Type a string with human-like timing"""
    for char in text:
        if char == ' ':
            user32.keybd_event(0x20, 0, 0, 0)
            time.sleep(0.01)
            user32.keybd_event(0x20, 0, KEYEVENTF_KEYUP, 0)
        else:
            type_char(char)
        
        # Occasional longer pauses (like thinking)
        if random.random() < 0.1:
            time.sleep(random.uniform(0.2, 0.4))

def press_enter():
    """Press Enter key"""
    user32.keybd_event(VK_RETURN, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)

def main():
    print("🌊 Claude Keyboard Simulator (Windows)")
    print("====================================")
    print("This simulates real human typing")
    print("")
    
    # Find Claude window
    hwnd = find_claude_window()
    if not hwnd:
        print("❌ No window selected!")
        return
    
    print("\n✓ Window selected")
    print("⏰ Will type messages every 2 minutes")
    print("📍 Press Ctrl+C to stop\n")
    
    messages = [
        "Continue shepherding souls. Check for any citizens needing awakening.",
        "Survey the sleeping souls. Who stirs with pending activities?",
        "The city's rhythm continues. Which citizens have tasks awaiting?",
        "Venice breathes through her citizens. Check who needs to wake.",
        "Another cycle passes. Review the activities and wake those called."
    ]
    
    msg_index = 0
    
    # Initial delay
    print("Waiting 5 seconds before starting...")
    time.sleep(5)
    
    while True:
        try:
            msg = messages[msg_index % len(messages)]
            
            print(f"\n🔔 [{time.strftime('%H:%M:%S')}] Typing message...")
            print(f"   \"{msg}\"")
            
            # Activate window
            activate_window(hwnd)
            time.sleep(0.5)
            
            # Type the message
            type_string(msg)
            time.sleep(0.5)
            
            # Press Enter
            press_enter()
            
            print("✓ Message typed!")
            
            msg_index += 1
            
            # Wait 2 minutes
            print("💤 Waiting 120 seconds...")
            time.sleep(120)
            
        except KeyboardInterrupt:
            print("\n🛑 Stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()