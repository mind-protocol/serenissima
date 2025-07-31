#!/usr/bin/env python3
"""
Fixed Telegram Monitor - Captures real messages and updates Narrator Angel
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

class TelegramMonitor:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
        self.chat_id = int(os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893))
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        self.narrator_claude = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel/CLAUDE.md")
        
        # Track last update ID
        self.last_update_file = Path(__file__).parent / "telegram_last_update.txt"
        self.last_update_id = self.load_last_update()
        
        # Message buffer
        self.message_buffer = []
        self.max_messages = 10
        
        print(f"🔍 Telegram Monitor initialized")
        print(f"📡 Bot Token: {self.bot_token[:20]}...")
        print(f"💬 Chat ID: {self.chat_id}")
        print(f"📄 Last Update ID: {self.last_update_id}")
        
    def load_last_update(self):
        """Load the last processed update ID"""
        if self.last_update_file.exists():
            with open(self.last_update_file, 'r') as f:
                return int(f.read().strip())
        return 0
        
    def save_last_update(self, update_id):
        """Save the last processed update ID"""
        with open(self.last_update_file, 'w') as f:
            f.write(str(update_id))
    
    def get_updates(self):
        """Get new messages from Telegram"""
        params = {
            'offset': self.last_update_id + 1,
            'timeout': 10,  # Long polling
            'allowed_updates': ['message']
        }
        
        try:
            print(f"🔄 Polling for updates (offset: {params['offset']})...")
            response = requests.get(f"{self.api_url}/getUpdates", params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    updates = data.get('result', [])
                    print(f"✅ Got {len(updates)} updates")
                    return updates
                else:
                    print(f"❌ API error: {data}")
            else:
                print(f"❌ HTTP error: {response.status_code}")
        except Exception as e:
            print(f"❌ Request error: {e}")
        return []
    
    def update_narrator_prompt(self):
        """Update the Narrator Angel's CLAUDE.md with human messages"""
        if not self.message_buffer:
            print("📭 No messages to update")
            return
            
        print(f"📝 Updating Narrator Angel with {len(self.message_buffer)} messages...")
        
        # Read current CLAUDE.md
        with open(self.narrator_claude, 'r') as f:
            content = f.read()
            
        # Format message section
        message_section = "## 💬 Recent Human Messages from Telegram\n\n"
        for msg in self.message_buffer[-self.max_messages:]:
            time_str = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')
            username = msg.get('username', 'Unknown')
            text = msg.get('text', '')
            message_section += f"**{username}** ({time_str}): {text}\n\n"
        
        # Find and replace message section
        message_marker = "## 💬 Recent Human Messages from Telegram"
        thoughts_marker = "## 🧠 Recent Citizen Thoughts"
        
        if message_marker in content:
            # Replace existing section
            start_idx = content.find(message_marker)
            end_idx = content.find(thoughts_marker, start_idx)
            if end_idx == -1:
                new_content = content[:start_idx] + message_section
            else:
                new_content = content[:start_idx] + message_section + "\n" + content[end_idx:]
        else:
            # Insert before thoughts section or at end
            insert_idx = content.find(thoughts_marker)
            if insert_idx == -1:
                new_content = content + "\n\n" + message_section
            else:
                new_content = content[:insert_idx] + message_section + "\n" + content[insert_idx:]
        
        # Write updated content
        with open(self.narrator_claude, 'w') as f:
            f.write(new_content)
            
        print("✅ Narrator Angel updated!")
    
    def monitor_messages(self):
        """Main monitoring loop"""
        print("\n🚀 Starting Telegram message monitoring...")
        print("Waiting for messages from the investment community...\n")
        
        # Load existing buffer if any
        message_file = Path(__file__).parent / "telegram_messages.json"
        if message_file.exists():
            with open(message_file, 'r') as f:
                self.message_buffer = json.load(f)
                print(f"📂 Loaded {len(self.message_buffer)} existing messages")
        
        while True:
            try:
                updates = self.get_updates()
                
                new_messages = False
                
                for update in updates:
                    update_id = update.get('update_id', 0)
                    self.last_update_id = max(self.last_update_id, update_id)
                    
                    # Extract message
                    message = update.get('message', {})
                    
                    # Check if it's from our target chat
                    chat_id = message.get('chat', {}).get('id')
                    if chat_id != self.chat_id:
                        print(f"🚫 Skipping message from chat {chat_id}")
                        continue
                    
                    # Skip bot messages
                    from_user = message.get('from', {})
                    if from_user.get('is_bot', False):
                        print(f"🤖 Skipping bot message")
                        continue
                    
                    # Extract details
                    text = message.get('text', '')
                    username = from_user.get('username') or from_user.get('first_name', 'Human')
                    timestamp = datetime.fromtimestamp(message.get('date', time.time()))
                    
                    if text:
                        print(f"\n💬 NEW MESSAGE from @{username}: {text[:100]}...")
                        
                        # Add to buffer
                        self.message_buffer.append({
                            'username': username,
                            'text': text,
                            'timestamp': timestamp.isoformat()
                        })
                        
                        new_messages = True
                
                # Update state
                if updates:
                    self.save_last_update(self.last_update_id)
                
                # If we got new messages, update the narrator
                if new_messages:
                    # Keep buffer manageable
                    self.message_buffer = self.message_buffer[-self.max_messages:]
                    
                    # Save buffer
                    with open(message_file, 'w') as f:
                        json.dump(self.message_buffer, f, indent=2)
                    
                    # Update narrator
                    self.update_narrator_prompt()
                    
                # Short delay before next poll
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Telegram monitor stopped")
                break
            except Exception as e:
                print(f"\n❌ Monitor error: {e}")
                time.sleep(5)

def main():
    monitor = TelegramMonitor()
    monitor.monitor_messages()

if __name__ == "__main__":
    print("="*60)
    print("TELEGRAM MESSAGE MONITOR v2")
    print("Real-time investor message capture for Narrator Angel")
    print("="*60)
    
    main()