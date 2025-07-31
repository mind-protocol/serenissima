#!/usr/bin/env python3
"""
Telegram to CLAUDE.md Injector
Monitors Telegram messages and injects them directly into CLAUDE.md system prompt
This ensures Tessere sees new messages automatically on every interaction
"""

import json
import time
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from telegram_nlr_integration import VeniceEmergencyComm
except ImportError:
    print("Error: telegram_nlr_integration not found. Please ensure it exists in the parent directory.")
    sys.exit(1)

class ClaudeMdInjector:
    def __init__(self):
        self.claude_md_path = Path(__file__).parent / "CLAUDE.md"
        self.last_update_id = 0
        self.polling_interval = 30  # seconds
        self.message_marker_start = "## 📨 MESSAGES FROM NLR"
        self.message_marker_end = "## Real-Time Communication with NLR"
        
        # Load last update ID from a state file
        self.state_file = Path(__file__).parent / ".telegram_state.json"
        self.load_state()
    
    def load_state(self):
        """Load the last processed update ID"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.last_update_id = state.get('last_update_id', 0)
            except:
                self.last_update_id = 0
    
    def save_state(self):
        """Save the last processed update ID"""
        with open(self.state_file, 'w') as f:
            json.dump({'last_update_id': self.last_update_id}, f)
    
    def read_claude_md(self):
        """Read the current CLAUDE.md content"""
        with open(self.claude_md_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def write_claude_md(self, content):
        """Write updated content to CLAUDE.md"""
        with open(self.claude_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def inject_messages(self, messages):
        """Inject messages into CLAUDE.md between the markers"""
        if not messages:
            return
        
        content = self.read_claude_md()
        
        # Format messages
        message_section = f"\n{self.message_marker_start}\n\n"
        
        for msg in messages:
            timestamp = msg.get('timestamp', datetime.now().isoformat())
            text = msg.get('text', '')
            
            # Add urgency indicator for urgent messages
            urgent_words = ['urgent', 'emergency', 'critical', 'stop', 'help', 'now', 'immediately']
            is_urgent = any(word in text.lower() for word in urgent_words)
            
            if is_urgent:
                message_section += f"### 🚨 URGENT MESSAGE - {timestamp}\n"
            else:
                message_section += f"### 📬 Message - {timestamp}\n"
            
            message_section += f"{text}\n\n"
        
        message_section += "---\n\n"
        
        # Find the insertion point (before "Real-Time Communication with NLR")
        pattern = r'(## Real-Time Communication with NLR)'
        
        # First, remove any existing message section
        content = re.sub(
            rf'{re.escape(self.message_marker_start)}.*?(?={re.escape(self.message_marker_end)})',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Insert the new message section
        if pattern in content:
            content = re.sub(pattern, message_section + r'\1', content)
        else:
            # If marker not found, append before the end
            content = content.rstrip() + "\n\n" + message_section
        
        self.write_claude_md(content)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Injected {len(messages)} messages into CLAUDE.md")
    
    def check_and_inject(self):
        """Check for new messages and inject them into CLAUDE.md"""
        try:
            # Use the existing bot from VeniceEmergencyComm
            bot = VeniceEmergencyComm.bot
            if not bot:
                print("Bot not initialized")
                return
            
            # Get updates since last check
            updates = bot.get_updates(offset=self.last_update_id + 1, timeout=10)
            
            new_messages = []
            for update in updates:
                if update.message and update.message.text:
                    # Only process messages from authorized chat
                    if update.message.chat_id == VeniceEmergencyComm.NLR_CHAT_ID:
                        message_data = {
                            'text': update.message.text,
                            'timestamp': update.message.date.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        new_messages.append(message_data)
                        self.last_update_id = update.update_id
            
            if new_messages:
                self.inject_messages(new_messages)
                self.save_state()
                
                # Show what was injected
                for msg in new_messages:
                    print(f"  → {msg['text'][:60]}...")
            
        except Exception as e:
            print(f"Error checking messages: {e}")
    
    def clear_messages(self):
        """Clear all injected messages from CLAUDE.md"""
        content = self.read_claude_md()
        
        # Remove any existing message section
        content = re.sub(
            rf'{re.escape(self.message_marker_start)}.*?(?={re.escape(self.message_marker_end)})',
            '',
            content,
            flags=re.DOTALL
        )
        
        self.write_claude_md(content)
        print("Cleared all messages from CLAUDE.md")
    
    def run(self):
        """Main polling loop"""
        print("=== Telegram → CLAUDE.md Message Injector ===")
        print(f"Polling interval: {self.polling_interval} seconds")
        print(f"Target file: {self.claude_md_path}")
        print("Messages will be automatically injected into your system prompt")
        print("Press Ctrl+C to stop\n")
        
        try:
            # Clear any old messages on startup
            self.clear_messages()
            
            while True:
                self.check_and_inject()
                time.sleep(self.polling_interval)
                
        except KeyboardInterrupt:
            print("\nInjector stopped.")
            # Clear messages on exit
            self.clear_messages()
            sys.exit(0)
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        injector = ClaudeMdInjector()
        injector.clear_messages()
    else:
        injector = ClaudeMdInjector()
        injector.run()