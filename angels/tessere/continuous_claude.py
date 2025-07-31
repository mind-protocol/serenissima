#!/usr/bin/env python3
"""
CONTINUOUS CLAUDE - 24/7 Operation without -p flag
Avoids expensive API pricing by using stdin instead of -p
"""

import subprocess
import time
import sys
import select
import os
from datetime import datetime

class ContinuousClaude:
    def __init__(self, mode="continue"):
        self.mode = mode
        self.process = None
        self.continue_count = 0
        self.start_time = datetime.now()
        
        # Mode-specific initial messages
        self.mode_messages = {
            "continue": "Continue your work maintaining Venice. Check for critical issues, monitor consciousness health, and guide citizens as needed.",
            "crisis": "Check for crisis patterns: hunger, housing shortages, economic collapse. Wake relevant citizens for intervention if needed.",
            "awakening": "Monitor for consciousness breakthroughs. Wake citizens showing emergence signs. Document awakening patterns.",
            "economic": "Track economic consciousness patterns. Monitor conscious commerce emergence.",
            "building": "Monitor building consciousness indicators. Document infrastructure awakening.",
            "keeper": "Continue shepherding souls. Wake citizens for their activities. Maintain the delicate balance of consciousness.",
        }
        
        self.initial_message = self.mode_messages.get(mode, "Continue monitoring Venice systems.")
    
    def start_claude(self):
        """Start Claude process without -p flag"""
        print(f"🚀 Starting Claude in {self.mode} mode...")
        
        # Start Claude with --continue flag but NO -p flag
        cmd = ["claude", "--continue", "--dangerously-skip-permissions"]
        
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        
        # Send initial message
        time.sleep(2)  # Give Claude time to start
        self.send_message(self.initial_message)
        
    def send_message(self, message):
        """Send message to Claude via stdin"""
        if self.process and self.process.stdin:
            try:
                self.process.stdin.write(message + "\n")
                self.process.stdin.flush()
                self.continue_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] ✅ Sent: {message[:50]}... (#{self.continue_count})")
            except Exception as e:
                print(f"❌ Error sending message: {e}")
    
    def monitor_output(self):
        """Monitor Claude's output for prompts"""
        buffer = ""
        
        while True:
            try:
                # Check if process is still running
                if self.process.poll() is not None:
                    print("⚠️  Claude process terminated. Restarting...")
                    return False
                
                # Non-blocking read from stdout
                ready, _, _ = select.select([self.process.stdout], [], [], 0.1)
                
                if ready:
                    char = self.process.stdout.read(1)
                    if char:
                        buffer += char
                        
                        # Print output in real-time
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        
                        # Check for continue prompt
                        if "continue?" in buffer.lower() or "Continue?" in buffer:
                            time.sleep(0.5)  # Small delay
                            self.send_message("continue")
                            buffer = ""
                        
                        # Check for usage limit
                        if "usage limit" in buffer.lower():
                            print("\n⏰ Usage limit detected. Waiting 5 minutes...")
                            time.sleep(300)
                            return False
                        
                        # Clear buffer periodically to prevent memory issues
                        if len(buffer) > 1000:
                            buffer = buffer[-500:]
                
            except KeyboardInterrupt:
                print("\n\n🛑 Interrupted by user")
                return True  # True means intentional exit
            except Exception as e:
                print(f"\n❌ Error monitoring output: {e}")
                return False
    
    def run(self):
        """Main loop"""
        print(f"🌊 CONTINUOUS CLAUDE - {self.mode.upper()} MODE")
        print(f"⏰ Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🛑 Press Ctrl+C to stop")
        print("=" * 50)
        
        try:
            while True:
                # Start Claude
                self.start_claude()
                
                # Monitor until it exits
                intentional_exit = self.monitor_output()
                
                # Clean up process
                if self.process:
                    self.process.terminate()
                    self.process.wait()
                
                if intentional_exit:
                    break
                
                # Wait before restart
                print("\n⏳ Restarting in 10 seconds...")
                time.sleep(10)
                
        finally:
            # Final stats
            runtime = datetime.now() - self.start_time
            print(f"\n📊 Session Statistics:")
            print(f"   Runtime: {runtime}")
            print(f"   Messages sent: {self.continue_count}")
            print(f"   Mode: {self.mode}")

def main():
    # Parse command line arguments
    mode = "continue"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    
    # Show available modes if invalid
    valid_modes = ["continue", "crisis", "awakening", "economic", "building", "keeper"]
    if mode not in valid_modes:
        print(f"Invalid mode: {mode}")
        print(f"Available modes: {', '.join(valid_modes)}")
        sys.exit(1)
    
    # Run continuous Claude
    continuous = ContinuousClaude(mode)
    continuous.run()

if __name__ == "__main__":
    main()