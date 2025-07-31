#!/usr/bin/env python3
"""
Telegram User Client for diplomatic_virtuoso
Uses a real user account, not a bot
"""

from telethon import TelegramClient, events
from telethon.tl.types import User
import asyncio
import json
import os
from datetime import datetime
import subprocess

# Configuration - You'll need to get these from https://my.telegram.org
API_ID = 123456  # Your API ID
API_HASH = 'your_api_hash_here'  # Your API hash
PHONE = '+1234567890'  # Phone number associated with @diplomatic_virtuoso

VENICE_API = "https://serenissima.ai/api"
CONVERSATIONS_FILE = "./telegram_conversations.json"
SESSION_NAME = 'diplomatic_virtuoso_session'

class DiplomaticVirtuosoClient:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self.conversations = self.load_conversations()
        
    def load_conversations(self) -> dict:
        """Load conversation history"""
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def save_conversations(self):
        """Save conversation history"""
        with open(CONVERSATIONS_FILE, 'w') as f:
            json.dump(self.conversations, f, indent=2)
    
    async def send_to_venice_api(self, sender_info, message_text, chat_id):
        """Send message to Venice API"""
        venice_message = {
            "sender": f"telegram_{sender_info['id']}",
            "receiver": "diplomatic_virtuoso",
            "content": message_text,
            "type": "telegram_direct",
            "metadata": {
                "telegram_chat_id": chat_id,
                "telegram_username": sender_info.get('username', 'unknown'),
                "telegram_first_name": sender_info.get('first_name', ''),
                "telegram_user_id": sender_info['id']
            }
        }
        
        # In real implementation, would POST to Venice API
        print(f"Would send to Venice: {venice_message}")
        return True
    
    def wake_diplomatic_virtuoso(self, sender_info, message_text):
        """Wake up diplomatic_virtuoso with message context"""
        username = sender_info.get('username', 'unknown')
        first_name = sender_info.get('first_name', 'Friend')
        
        awakening_msg = f"""
## 📱 TELEGRAM DIRECT MESSAGE

**From**: @{username} ({first_name})
**User ID**: {sender_info['id']}
**Time**: {datetime.now().isoformat()}

**Message**: {message_text}

[This is a direct message to your personal Telegram @diplomatic_virtuoso. Respond naturally. You can reply directly in Telegram.]
"""
        
        # Wake up using Claude Code
        cmd = [
            "timeout", "600", "bash", "-c",
            f'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso && claude "{awakening_msg}" --model sonnet --continue --dangerously-skip-permissions'
        ]
        
        print(f"Waking diplomatic_virtuoso for message from @{username}")
        subprocess.run(cmd)
    
    def update_conversations(self, sender_info, message_text):
        """Update conversation tracking"""
        user_id = str(sender_info['id'])
        
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'username': sender_info.get('username', 'unknown'),
                'first_name': sender_info.get('first_name', ''),
                'last_name': sender_info.get('last_name', ''),
                'messages': []
            }
        
        self.conversations[user_id]['messages'].append({
            'time': datetime.now().isoformat(),
            'text': message_text,
            'direction': 'incoming'
        })
        
        # Keep only last 20 messages
        self.conversations[user_id]['messages'] = self.conversations[user_id]['messages'][-20:]
        self.save_conversations()
    
    async def start(self):
        """Start the client"""
        await self.client.start(phone=PHONE)
        print("Logged in as @diplomatic_virtuoso!")
        
        # Set up message handler
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_new_message(event):
            if event.is_private:  # Only handle private messages
                sender = await event.get_sender()
                
                if isinstance(sender, User):
                    sender_info = {
                        'id': sender.id,
                        'username': sender.username,
                        'first_name': sender.first_name or '',
                        'last_name': sender.last_name or ''
                    }
                    
                    print(f"\nNew message from @{sender.username}: {event.text[:50]}...")
                    
                    # Update conversations
                    self.update_conversations(sender_info, event.text)
                    
                    # Send to Venice API
                    await self.send_to_venice_api(sender_info, event.text, event.chat_id)
                    
                    # Wake diplomatic_virtuoso
                    self.wake_diplomatic_virtuoso(sender_info, event.text)
        
        print("Listening for messages...")
        await self.client.run_until_disconnected()

async def send_message(to_username: str, message: str):
    """Send a message as diplomatic_virtuoso"""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start(phone=PHONE)
    
    try:
        await client.send_message(to_username, message)
        print(f"Message sent to @{to_username}")
    except Exception as e:
        print(f"Error sending message: {e}")
    
    await client.disconnect()

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "send":
        if len(sys.argv) < 4:
            print("Usage: python telegram_user_client.py send <username> <message>")
            return
        
        username = sys.argv[2]
        message = sys.argv[3]
        asyncio.run(send_message(username, message))
    else:
        # Start listening
        client = DiplomaticVirtuosoClient()
        asyncio.run(client.start())

if __name__ == "__main__":
    main()