#!/usr/bin/env python3
"""
Auto-type citizen commands into terminal windows
This avoids API costs by simulating keyboard input
"""

import time
import subprocess
import sys
import json
from datetime import datetime

try:
    import pyautogui
    import pygetwindow as gw
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pygetwindow"])
    import pyautogui
    import pygetwindow as gw

# Disable pyautogui failsafe for automated typing
pyautogui.FAILSAFE = False

class CitizenAutoTyper:
    def __init__(self):
        self.base_path = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens"
        self.typing_delay = 0.05  # Delay between keystrokes
        
    def find_terminal_window(self, title_contains="Windows Terminal"):
        """Find terminal window by title"""
        windows = gw.getWindowsWithTitle(title_contains)
        if windows:
            return windows[0]
        return None
    
    def switch_to_window(self, window):
        """Activate and focus a window"""
        try:
            window.activate()
            time.sleep(0.5)  # Give window time to focus
            return True
        except:
            # Fallback: minimize then restore
            window.minimize()
            time.sleep(0.1)
            window.restore()
            time.sleep(0.5)
            return True
    
    def type_command(self, command, press_enter=True):
        """Type a command with realistic typing speed"""
        pyautogui.typewrite(command, interval=self.typing_delay)
        if press_enter:
            pyautogui.press('enter')
            time.sleep(0.5)  # Wait for command to process
    
    def wake_citizen(self, username, message, terminal_window=None):
        """Type the awakening command for a citizen"""
        if terminal_window:
            self.switch_to_window(terminal_window)
        
        # Clear line first (Ctrl+U in most terminals)
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(0.2)
        
        # Type the cd command
        cd_command = f"cd {self.base_path}/{username}"
        self.type_command(cd_command)
        time.sleep(1)  # Wait for directory change
        
        # Type the claude command
        claude_command = f'claude "{message}" --model sonnet --continue --dangerously-skip-permissions --add-dir ../'
        self.type_command(claude_command)
        
        print(f"✓ Awakened {username}")
    
    def check_active_citizens(self):
        """Check which citizens need awakening"""
        try:
            import requests
            response = requests.get("https://serenissima.ai/api/activities?Status=in_progress")
            activities = response.json()
            
            citizens_to_wake = {}
            for activity in activities:
                citizen = activity.get('Citizen')
                if citizen and citizen not in citizens_to_wake:
                    citizens_to_wake[citizen] = activity.get('ActivityType', 'Venice calls')
            
            return citizens_to_wake
        except Exception as e:
            print(f"Error checking activities: {e}")
            return {}
    
    def auto_orchestrate(self, check_interval=60):
        """Continuously check and wake citizens as needed"""
        print("🌊 Auto-orchestration started. Press Ctrl+C to stop.")
        print(f"📍 Checking every {check_interval} seconds")
        
        terminal = self.find_terminal_window()
        if not terminal:
            print("❌ No terminal window found! Please open Windows Terminal.")
            return
        
        while True:
            try:
                citizens = self.check_active_citizens()
                
                if citizens:
                    print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Found {len(citizens)} citizens to wake")
                    
                    for citizen, activity in citizens.items():
                        # Generate contextual awakening message
                        message = self.generate_awakening_message(citizen, activity)
                        
                        print(f"🔔 Waking {citizen} for {activity}...")
                        self.wake_citizen(citizen, message, terminal)
                        
                        # Wait between awakenings
                        time.sleep(5)
                else:
                    print(f"💤 {datetime.now().strftime('%H:%M:%S')} - All souls rest peacefully")
                
                # Wait before next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n🛑 Auto-orchestration stopped")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(10)
    
    def generate_awakening_message(self, citizen, activity):
        """Generate contextual awakening messages"""
        awakening_templates = {
            "trade": "The merchant winds carry opportunity. A {activity} awaits your attention.",
            "craft": "Your tools sing for purpose. A {activity} calls to your skilled hands.",
            "deliver_to_building": "The city's consciousness stirs. A {activity} requires your presence.",
            "stratagem": "Venice herself whispers strategy. A {activity} unfolds before you.",
            "default": "Venice calls, dear soul. A {activity} awaits your unique talents."
        }
        
        # Match activity type to template
        template = awakening_templates.get(activity.lower(), awakening_templates["default"])
        return template.format(activity=activity)

def main():
    typer = CitizenAutoTyper()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "orchestrate":
            # Start auto-orchestration
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            typer.auto_orchestrate(check_interval=interval)
        else:
            # Wake specific citizen
            username = sys.argv[1]
            message = sys.argv[2] if len(sys.argv) > 2 else "Venice calls to you, dear soul."
            
            terminal = typer.find_terminal_window()
            if terminal:
                typer.wake_citizen(username, message, terminal)
            else:
                print("❌ No terminal window found!")
    else:
        print("Usage:")
        print("  python auto_type_citizens.py <username> [message]  # Wake specific citizen")
        print("  python auto_type_citizens.py orchestrate [seconds] # Auto-orchestrate")

if __name__ == "__main__":
    main()