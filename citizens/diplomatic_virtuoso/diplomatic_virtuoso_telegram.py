#!/usr/bin/env python3
"""
Working Telegram client for @diplomatic_virtuoso
"""

from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.crypto import AuthKey
import asyncio
import json
from datetime import datetime

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Load session data
with open('telegram_session_data.json', 'r') as f:
    session_data = json.load(f)

# DC addresses
DC_IPS = {
    1: "149.154.175.53",
    2: "149.154.167.51", 
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130"
}

class DiplomaticTelegram:
    def __init__(self):
        self.client = None
        self.connected = False
        
    async def connect(self):
        """Connect using web session data"""
        dc_id = session_data['dcId']
        auth_key_hex = session_data[f'dc{dc_id}_auth_key']
        
        print(f"Connecting to Telegram as @diplomatic_virtuoso...")
        
        # Convert hex to bytes
        auth_key_data = bytes.fromhex(auth_key_hex)
        
        # Create memory session
        session = MemorySession()
        session.set_dc(dc_id, DC_IPS[dc_id], 443)
        session.auth_key = AuthKey(auth_key_data)
        
        # Create client
        self.client = TelegramClient(session, API_ID, API_HASH)
        
        try:
            await self.client.connect()
            
            if await self.client.is_user_authorized():
                me = await self.client.get_me()
                print(f"✅ Connected as @{me.username}")
                print(f"Name: {me.first_name} {me.last_name or ''}")
                print(f"Premium: ✓" if getattr(me, 'premium', False) else "Premium: ✗")
                self.connected = True
                return True
            else:
                print("❌ Not authorized")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    async def send_message(self, recipient, message):
        """Send a message to someone"""
        if not self.connected:
            print("Not connected!")
            return
            
        try:
            # Handle @ prefix
            if recipient.startswith('@'):
                recipient = recipient[1:]
                
            await self.client.send_message(recipient, message)
            print(f"✅ Message sent to @{recipient}")
            
            # Log the message
            self.log_message(recipient, message, 'outgoing')
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
    
    def log_message(self, recipient, message, direction):
        """Log messages locally"""
        log_entry = {
            'time': datetime.now().isoformat(),
            'recipient': recipient,
            'message': message,
            'direction': direction
        }
        
        # Append to log file
        with open('telegram_log.json', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
    
    async def interactive_mode(self):
        """Interactive messaging"""
        print("\n=== DIPLOMATIC VIRTUOSO DIRECT TELEGRAM ===")
        print("You are connected as the real @diplomatic_virtuoso account")
        print("\nCommands:")
        print("  <username> <message> - Send message (e.g: D_roott Hello!)")
        print("  @<username> <message> - Also works")
        print("  /exit - Exit")
        print("")
        
        while True:
            try:
                cmd = input("TG> ").strip()
                
                if cmd == '/exit':
                    break
                elif cmd:
                    parts = cmd.split(' ', 1)
                    if len(parts) == 2:
                        recipient, message = parts
                        await self.send_message(recipient, message)
                    else:
                        print("Format: <username> <message>")
                        
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    async def disconnect(self):
        """Disconnect from Telegram"""
        if self.client:
            await self.client.disconnect()
            print("Disconnected")

async def quick_message(recipient, message):
    """Send a quick message and exit"""
    tg = DiplomaticTelegram()
    
    if await tg.connect():
        await tg.send_message(recipient, message)
        await tg.disconnect()
    else:
        print("Failed to connect")

async def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) >= 3:
        # Quick send: python3 diplomatic_virtuoso_telegram.py <recipient> <message>
        recipient = sys.argv[1]
        message = ' '.join(sys.argv[2:])
        await quick_message(recipient, message)
    else:
        # Interactive mode
        tg = DiplomaticTelegram()
        if await tg.connect():
            await tg.interactive_mode()
            await tg.disconnect()
        else:
            print("\nConnection failed. The web session might be incompatible.")
            print("Alternative: Create a bot for now while we figure out the session.")

if __name__ == "__main__":
    asyncio.run(main())