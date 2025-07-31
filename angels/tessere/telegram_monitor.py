#!/usr/bin/env python3
"""
Monitor Telegram chat for human messages and update Narrator Angel's CLAUDE.md
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime
import asyncio

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
        self.chat_id = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        self.narrator_claude = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel/CLAUDE.md")
        
        # Track last update ID to avoid duplicates
        self.last_update_file = Path(__file__).parent / "telegram_last_update.txt"
        self.last_update_id = self.load_last_update()
        
        # Buffer for human messages
        self.max_messages = 10
        
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
            'timeout': 30,  # Long polling
            'allowed_updates': ['message']
        }
        
        try:
            response = requests.get(f"{self.api_url}/getUpdates", params=params, timeout=35)
            if response.status_code == 200:
                return response.json().get('result', [])
        except Exception as e:
            print(f"Error getting updates: {e}")
        return []
        
    def update_narrator_prompt(self, messages):
        """Add human messages to Narrator Angel's CLAUDE.md"""
        if not messages:
            return
            
        # Read current CLAUDE.md
        with open(self.narrator_claude, 'r') as f:
            content = f.read()
            
        # Format message section
        message_section = "## 💬 Recent Human Messages from Telegram\n\n"
        for msg in messages[-self.max_messages:]:  # Keep last N messages
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
                # No thoughts section after messages
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
            
    async def monitor_messages(self):
        """Main monitoring loop"""
        print("🔍 Monitoring Telegram messages for Narrator Angel...")
        print(f"📡 Chat ID: {self.chat_id}")
        
        # Buffer to accumulate messages
        message_buffer = []
        
        # Load existing messages if any
        message_file = Path(__file__).parent / "telegram_messages.json"
        if message_file.exists():
            with open(message_file, 'r') as f:
                message_buffer = json.load(f)
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    self.last_update_id = update.get('update_id', self.last_update_id)
                    
                    # Extract message info
                    message = update.get('message', {})
                    
                    # Only process messages from our target chat
                    if message.get('chat', {}).get('id') != self.chat_id:
                        continue
                        
                    # Skip bot messages - only human messages
                    from_user = message.get('from', {})
                    if from_user.get('is_bot', False):
                        continue
                        
                    # Extract message details
                    text = message.get('text', '')
                    username = from_user.get('username') or from_user.get('first_name', 'Human')
                    timestamp = datetime.fromtimestamp(message.get('date', time.time()))
                    
                    if text:
                        print(f"💬 {username}: {text[:100]}...")
                        
                        # Add to buffer
                        message_buffer.append({
                            'username': username,
                            'text': text,
                            'timestamp': timestamp.isoformat()
                        })
                        
                        # Keep buffer size manageable
                        message_buffer = message_buffer[-self.max_messages:]
                        
                        # Save to file
                        with open(message_file, 'w') as f:
                            json.dump(message_buffer, f, indent=2)
                        
                        # Update narrator prompt
                        self.update_narrator_prompt(message_buffer)
                
                # Save last update ID
                if updates:
                    self.save_last_update(self.last_update_id)
                    
            except KeyboardInterrupt:
                print("\n🛑 Telegram monitor stopped")
                break
            except Exception as e:
                print(f"Monitor error: {e}")
                await asyncio.sleep(5)

async def main():
    monitor = TelegramMonitor()
    await monitor.monitor_messages()

if __name__ == "__main__":
    print("="*60)
    print("TELEGRAM MESSAGE MONITOR")
    print("Feeding human messages to Narrator Angel")
    print("="*60)
    
    asyncio.run(main())