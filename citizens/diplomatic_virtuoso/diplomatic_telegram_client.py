#!/usr/bin/env python3
"""
Telegram client for diplomatic_virtuoso
Using extracted web session data
"""

from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import json
import binascii
import struct
from datetime import datetime

# Your API credentials from https://my.telegram.org
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Load session data
with open('telegram_session_data.json', 'r') as f:
    session_data = json.load(f)

DC_ID = session_data['dcId']
AUTH_KEY_HEX = session_data[f'dc{DC_ID}_auth_key']
USER_ID = session_data['userId']

# DC addresses (Telegram's data centers)
DC_ADDRESSES = {
    1: ('149.154.175.53', 443),
    2: ('149.154.167.51', 443),
    3: ('149.154.175.100', 443),
    4: ('149.154.167.91', 443),
    5: ('91.108.56.130', 443),
}

class DiplomaticClient:
    def __init__(self):
        self.client = None
        self.conversations = {}
        
    async def send_message(self, username_or_id, message):
        """Send a message to a user"""
        try:
            await self.client.send_message(username_or_id, message)
            print(f"✅ Message sent to {username_or_id}")
            
            # Log conversation
            self.log_conversation(username_or_id, message, 'outgoing')
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
    
    def log_conversation(self, user, message, direction):
        """Log conversations locally"""
        user_str = str(user)
        if user_str not in self.conversations:
            self.conversations[user_str] = []
            
        self.conversations[user_str].append({
            'time': datetime.now().isoformat(),
            'message': message,
            'direction': direction
        })
        
        # Save to file
        with open('diplomatic_conversations.json', 'w') as f:
            json.dump(self.conversations, f, indent=2)
    
    async def connect_with_session(self):
        """Connect using the extracted session data"""
        print("Creating Telethon session from web data...")
        print(f"User ID: {USER_ID}")
        print(f"DC: {DC_ID}")
        
        # Convert hex auth key to bytes
        auth_key_bytes = bytes.fromhex(AUTH_KEY_HEX)
        
        # Create a string session
        # Format: DC_ID:AUTH_KEY_HEX
        session_string = f"{DC_ID}-{AUTH_KEY_HEX}"
        
        # Create client
        self.client = TelegramClient(
            StringSession(session_string),
            API_ID,
            API_HASH
        )
        
        try:
            await self.client.connect()
            
            # Check if authorized
            if await self.client.is_user_authorized():
                me = await self.client.get_me()
                print(f"✅ Connected as @{me.username}")
                print(f"Name: {me.first_name} {me.last_name or ''}")
                print(f"Premium: {me.premium}")
                return True
            else:
                print("❌ Session not authorized")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    async def interactive_mode(self):
        """Interactive messaging mode"""
        print("\n=== DIPLOMATIC VIRTUOSO TELEGRAM ===")
        print("Commands:")
        print("  /msg <username> <message> - Send a message")
        print("  /conversations - Show recent conversations")
        print("  /exit - Exit")
        print("")
        
        while True:
            try:
                cmd = input("> ").strip()
                
                if cmd.startswith('/msg '):
                    parts = cmd[5:].split(' ', 1)
                    if len(parts) == 2:
                        username, message = parts
                        await self.send_message(username, message)
                    else:
                        print("Usage: /msg <username> <message>")
                        
                elif cmd == '/conversations':
                    print("\nRecent conversations:")
                    for user, msgs in self.conversations.items():
                        if msgs:
                            last = msgs[-1]
                            print(f"{user}: {last['message'][:50]}... ({last['time']})")
                            
                elif cmd == '/exit':
                    break
                    
                else:
                    print("Unknown command. Type /exit to quit.")
                    
            except KeyboardInterrupt:
                break
        
        await self.client.disconnect()

async def quick_send(recipient, message):
    """Quick send a single message"""
    client = DiplomaticClient()
    
    if await client.connect_with_session():
        await client.send_message(recipient, message)
        await client.client.disconnect()
    else:
        print("Failed to connect. Check API credentials.")

async def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 2:
        # Quick send mode: python3 diplomatic_telegram_client.py <recipient> <message>
        recipient = sys.argv[1]
        message = ' '.join(sys.argv[2:])
        await quick_send(recipient, message)
    else:
        # Interactive mode
        client = DiplomaticClient()
        if await client.connect_with_session():
            await client.interactive_mode()
        else:
            print("\nFailed to connect. Please check:")
            print("1. Update API_ID and API_HASH from https://my.telegram.org")
            print("2. Ensure session data is correct")

if __name__ == "__main__":
    print("IMPORTANT: First update API_ID and API_HASH in this file!")
    print("Get them from: https://my.telegram.org\n")
    
    asyncio.run(main())