#!/usr/bin/env python3
"""
Restore Telegram session from session data for diplomatic_virtuoso
"""

import json
import struct
import asyncio
from telethon import TelegramClient
from telethon.sessions import MemorySession
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

# Convert hex auth key to bytes
AUTH_KEY = binascii.unhexlify(AUTH_KEY_HEX)

# Create session
session = MemorySession()
session.set_dc(DC_ID, '149.154.167.91', 443)  # DC 4 address
session.auth_key = AUTH_KEY

async def test_restored_session():
    """Test the restored session"""
    print("🔧 Restoring session for @diplomatic_virtuoso")
    
    client = TelegramClient(session, API_ID, API_HASH)
    
    try:
        await client.connect()
        
        if await client.is_user_authorized():
            print("✅ Session restored successfully!")
            
            me = await client.get_me()
            print(f"📱 Logged in as: @{me.username} ({me.first_name})")
            
            # Save the session for future use
            client.session.save('diplomatic_virtuoso_restored')
            print("💾 Session saved to diplomatic_virtuoso_restored.session")
            
            # Get recent messages
            print("\n📬 Recent messages:")
            async for message in client.iter_messages(limit=5):
                if message.text:
                    sender = await message.get_sender()
                    sender_name = getattr(sender, 'username', None) or getattr(sender, 'first_name', 'Unknown')
                    print(f"  - From @{sender_name}: {message.text[:50]}...")
                    
        else:
            print("❌ Session not authorized")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_restored_session())