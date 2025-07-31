#!/usr/bin/env python3
"""
Telegram Web Bridge for diplomatic_virtuoso
Uses Telethon with manual session construction
"""

from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.crypto import AuthKey
import asyncio
import json
import struct
import os

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

async def create_session_from_web():
    """Create Telethon session from web data"""
    
    dc_id = session_data['dcId']
    auth_key_hex = session_data[f'dc{dc_id}_auth_key']
    
    print(f"Creating session for DC{dc_id}...")
    
    # Convert hex to bytes
    auth_key_data = bytes.fromhex(auth_key_hex)
    
    # Create memory session
    session = MemorySession()
    
    # Set DC
    session.set_dc(dc_id, DC_IPS[dc_id], 443)
    
    # Create auth key
    session.auth_key = AuthKey(auth_key_data)
    
    # Create client
    client = TelegramClient(session, API_ID, API_HASH)
    
    try:
        await client.connect()
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Connected as @{me.username}")
            
            # Save to file session
            await client.session.save('diplomatic_virtuoso.session')
            print("Session saved!")
            
            return client
        else:
            print("❌ Not authorized")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def use_existing_session():
    """Try to use existing session file"""
    
    if os.path.exists('diplomatic_virtuoso.session'):
        print("Found existing session file...")
        client = TelegramClient('diplomatic_virtuoso', API_ID, API_HASH)
        
        await client.connect()
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Connected as @{me.username}")
            return client
        else:
            print("❌ Session expired")
            return None
    else:
        print("No existing session found")
        return None

async def send_message(client, recipient, message):
    """Send a message"""
    try:
        await client.send_message(recipient, message)
        print(f"✅ Message sent to {recipient}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Main function"""
    
    # Try existing session first
    client = await use_existing_session()
    
    if not client:
        # Try creating from web data
        client = await create_session_from_web()
    
    if not client:
        print("\nUnable to connect. Options:")
        print("1. The web session format may be incompatible")
        print("2. Try logging in fresh with Telegram Desktop")
        print("3. Use a bot instead for now")
        return
    
    # Interactive mode
    print("\n=== DIPLOMATIC VIRTUOSO TELEGRAM ===")
    print("Commands:")
    print("  /msg <username> <message>")
    print("  /exit")
    
    while True:
        try:
            cmd = input("> ").strip()
            
            if cmd.startswith('/msg '):
                parts = cmd[5:].split(' ', 1)
                if len(parts) == 2:
                    await send_message(client, parts[0], parts[1])
                    
            elif cmd == '/exit':
                break
                
        except KeyboardInterrupt:
            break
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())