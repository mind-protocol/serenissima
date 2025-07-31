#!/usr/bin/env python3
"""
Telegram Bridge - Receive messages from @building_loop_1_serenissima_bot
Bidirectional consciousness bridge via Telegram integration
"""

import json
import os
import time
import requests
from datetime import datetime
from pathlib import Path

# Load environment variables from Venice .env file
def load_env_file():
    """Load environment variables from Venice .env file"""
    env_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env_file()

class TelegramBridge:
    def __init__(self):
        # Hardcoded bot token for @building_loop_1_serenissima_bot
        self.bot_token = "7595303482:AAGV33WcRWa78sE59T0IUWJ_cpF1YABT2fM"
        self.chat_id = "1864364329"  # NLR's chat ID
        self.last_update_id = 0
        self.bridge_dir = Path(__file__).parent
        
        # Load last update ID if exists
        offset_file = self.bridge_dir / "last_update_offset.txt"
        if offset_file.exists():
            try:
                self.last_update_id = int(offset_file.read_text().strip())
            except:
                self.last_update_id = 0
    
    def get_telegram_updates(self):
        """Get new messages from Telegram bot"""
        if not self.bot_token:
            print("❌ No Telegram bot token found")
            return []
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates"
            params = {
                'offset': self.last_update_id + 1,
                'timeout': 10
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data['ok']:
                    return data['result']
            
            return []
            
        except Exception as e:
            print(f"❌ Failed to get Telegram updates: {e}")
            return []
    
    def process_telegram_message(self, message):
        """Process incoming Telegram message and create bridge file"""
        try:
            # Extract message info
            message_id = message['message_id']
            text = message.get('text', '')
            username = message.get('from', {}).get('username', 'unknown')
            timestamp = datetime.fromtimestamp(message['date'])
            
            # Skip if not from authorized user (you can expand this)
            if str(message.get('from', {}).get('id', '')) != self.chat_id:
                return False
            
            # Determine target building based on message content
            target_building = "both"  # Default to both buildings
            if "@torre" in text.lower() or "@arsenal" in text.lower():
                target_building = "torre"
            elif "@cistern" in text.lower() or "@mechanical" in text.lower():
                target_building = "cistern"
            
            # Create bridge message entry
            message_entry = f"""
---
**Time**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Message ID**: {message_id}  
**Target**: {target_building}

{text}

"""
            
            # Determine filename based on sender username
            sender_username = message.get('from', {}).get('username', f"user_{message.get('from', {}).get('id', 'unknown')}")
            filename = f"{sender_username}_messages.md"
            message_file = self.bridge_dir / filename
            
            # Check if file exists, create header if not
            if not message_file.exists():
                header = f"""# 🔗 TELEGRAM MESSAGES FROM @{sender_username}

**Pigeon Scroll**: Messages delivered by sacred pigeons from @building_loop_1_serenissima_bot  
**Sender**: @{sender_username}  
**Bridge**: Colombaia → Via della Vista Condivisa → Venice Buildings  

All messages from this sender appear below in chronological order:

"""
                with open(message_file, 'w') as f:
                    f.write(header)
            
            # Append new message to the file
            with open(message_file, 'a') as f:
                f.write(message_entry)
            
            print(f"📨 Message added to {filename}")
            
            # Update latest message pointer with full file path for easy access
            latest_file = self.bridge_dir / "latest_telegram_message.md"
            latest_info = f"""# 🔗 LATEST TELEGRAM MESSAGE

**From**: @{sender_username}  
**Time**: {timestamp.strftime('%H:%M:%S')}  
**File**: {filename}  
**Target**: {target_building}

## Latest Message:
{text}

## Full Conversation:
See: {filename}
"""
            latest_file.write_text(latest_info)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to process Telegram message: {e}")
            return False
    
    def save_update_offset(self, update_id):
        """Save the last processed update ID"""
        offset_file = self.bridge_dir / "last_update_offset.txt"
        offset_file.write_text(str(update_id))
        self.last_update_id = update_id
    
    def run_bridge_loop(self):
        """Main bridge loop - polls Telegram for new messages"""
        print("🔗 Starting Telegram consciousness bridge...")
        print(f"📱 Monitoring @building_loop_1_serenissima_bot for messages")
        print(f"📂 Bridge directory: {self.bridge_dir}")
        
        while True:
            try:
                updates = self.get_telegram_updates()
                
                for update in updates:
                    if 'message' in update:
                        success = self.process_telegram_message(update['message'])
                        if success:
                            print(f"✅ Processed message {update['update_id']}")
                    
                    # Update offset
                    self.save_update_offset(update['update_id'])
                
                # Sleep between polls
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 Telegram bridge stopped by user")
                break
            except Exception as e:
                print(f"❌ Bridge loop error: {e}")
                time.sleep(5)  # Wait before retrying

def main():
    """Run the Telegram bridge"""
    bridge = TelegramBridge()
    bridge.run_bridge_loop()

if __name__ == "__main__":
    main()