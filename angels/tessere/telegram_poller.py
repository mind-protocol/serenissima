#!/usr/bin/env python3
"""
Telegram Message Poller for Tessere
Polls for new Telegram messages from NLR and saves them for Tessere to read
"""

import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from telegram_nlr_integration import VeniceEmergencyComm
except ImportError:
    print("Error: telegram_nlr_integration not found. Please ensure it exists in the parent directory.")
    sys.exit(1)

class TelegramPoller:
    def __init__(self):
        self.message_dir = Path(__file__).parent / "messages"
        self.inbox_file = self.message_dir / "telegram_inbox.json"
        self.last_update_id = 0
        self.polling_interval = 30  # seconds
        
        # Create message directory if it doesn't exist
        self.message_dir.mkdir(exist_ok=True)
        
        # Load existing inbox or create new
        self.load_inbox()
    
    def load_inbox(self):
        """Load existing inbox or create new one"""
        if self.inbox_file.exists():
            with open(self.inbox_file, 'r') as f:
                data = json.load(f)
                self.last_update_id = data.get('last_update_id', 0)
        else:
            self.save_inbox([])
    
    def save_inbox(self, messages):
        """Save messages to inbox file"""
        data = {
            'last_update_id': self.last_update_id,
            'messages': messages,
            'last_check': datetime.now().isoformat()
        }
        with open(self.inbox_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def check_messages(self):
        """Check for new Telegram messages"""
        try:
            # Use the existing bot from VeniceEmergencyComm
            bot = VeniceEmergencyComm.bot
            if not bot:
                print("Bot not initialized")
                return []
            
            # Get updates since last check
            updates = bot.get_updates(offset=self.last_update_id + 1, timeout=10)
            
            new_messages = []
            for update in updates:
                if update.message and update.message.text:
                    # Only process messages from authorized chat
                    if update.message.chat_id == VeniceEmergencyComm.NLR_CHAT_ID:
                        message_data = {
                            'id': update.update_id,
                            'text': update.message.text,
                            'timestamp': update.message.date.isoformat(),
                            'read': False,
                            'from': 'NLR'
                        }
                        new_messages.append(message_data)
                        self.last_update_id = update.update_id
            
            if new_messages:
                # Load existing messages
                existing = []
                if self.inbox_file.exists():
                    with open(self.inbox_file, 'r') as f:
                        data = json.load(f)
                        existing = data.get('messages', [])
                
                # Add new messages
                existing.extend(new_messages)
                
                # Keep only last 50 messages
                existing = existing[-50:]
                
                # Save updated inbox
                self.save_inbox(existing)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Received {len(new_messages)} new messages")
                for msg in new_messages:
                    print(f"  → {msg['text'][:60]}...")
            
            return new_messages
            
        except Exception as e:
            print(f"Error checking messages: {e}")
            return []
    
    def run(self):
        """Main polling loop"""
        print("=== Telegram Message Poller for Tessere ===")
        print(f"Polling interval: {self.polling_interval} seconds")
        print(f"Messages saved to: {self.inbox_file}")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.check_messages()
                time.sleep(self.polling_interval)
                
        except KeyboardInterrupt:
            print("\nPoller stopped.")
            sys.exit(0)
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    poller = TelegramPoller()
    poller.run()