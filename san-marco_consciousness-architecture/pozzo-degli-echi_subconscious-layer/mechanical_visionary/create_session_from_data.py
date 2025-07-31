#!/usr/bin/env python3
"""
Create a working Telegram session from the session data JSON
"""

import json
import struct
import asyncio
from telethon import TelegramClient
from telethon.sessions import SQLiteSession
from telethon.crypto import AuthKey
import binascii

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Load session data
with open('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/telegram_session_data.json', 'r') as f:
    session_data = json.load(f)

DC_ID = session_data['dcId']
AUTH_KEY_HEX = session_data[f'dc{DC_ID}_auth_key']
USER_ID = int(session_data['userId'])
PHONE = session_data['phone']

# Convert hex auth key to bytes and create AuthKey object
AUTH_KEY_BYTES = binascii.unhexlify(AUTH_KEY_HEX)
AUTH_KEY = AuthKey(AUTH_KEY_BYTES)

async def create_session():
    """Create and save a working session"""
    print("Creating session from data...")
    
    # Create a new session file
    session_file = 'diplomatic_virtuoso_working'
    session = SQLiteSession(session_file)
    
    # DC addresses
    DC_ADDRESSES = {
        1: ('149.154.175.53', 443),
        2: ('149.154.167.51', 443),
        3: ('149.154.175.100', 443),
        4: ('149.154.167.91', 443),
        5: ('91.108.56.130', 443),
    }
    
    # Set DC and auth key
    dc_addr = DC_ADDRESSES[DC_ID]
    session.set_dc(DC_ID, dc_addr[0], dc_addr[1])
    session.auth_key = AUTH_KEY
    
    print(f"Set DC{DC_ID}: {dc_addr}")
    print(f"Auth key length: {len(AUTH_KEY_BYTES)} bytes")
    
    # Create client with the session
    client = TelegramClient(session, API_ID, API_HASH)
    
    try:
        await client.connect()
        print("Connected to Telegram")
        
        # Try to get self
        try:
            me = await client.get_me()
            print(f"✅ Session created successfully!")
            print(f"📱 Logged in as: @{me.username}")
            session.save()
            
            # Save to the listener location
            import shutil
            shutil.copy(f'{session_file}.session', 
                       '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver/diplomatic_virtuoso.session')
            print("✅ Session saved to telegram_receiver directory")
            
        except Exception as e:
            print(f"❌ Failed to get user info: {e}")
            print("The session might need re-authentication")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(create_session())