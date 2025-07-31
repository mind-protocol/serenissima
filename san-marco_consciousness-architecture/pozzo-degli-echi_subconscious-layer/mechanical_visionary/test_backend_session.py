#!/usr/bin/env python3
"""
Test using the backend session file
"""

import asyncio
from telethon import TelegramClient
import os

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Try the backend session file
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/backend/diplomatic_virtuoso_session'

async def test_backend_session():
    """Test the backend session"""
    print(f"Testing session: {SESSION_FILE}")
    
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    
    await client.connect()
    
    if await client.is_user_authorized():
        print("✅ Session is authorized!")
        
        me = await client.get_me()
        print(f"\n📱 Logged in as:")
        print(f"  Username: @{me.username}")
        print(f"  Name: {me.first_name} {me.last_name or ''}")
        print(f"  ID: {me.id}")
        
        # Test getting recent messages
        print("\n📬 Recent messages:")
        async for message in client.iter_messages(limit=5):
            if message.text:
                sender = await message.get_sender()
                sender_name = getattr(sender, 'username', None) or getattr(sender, 'first_name', 'Unknown')
                print(f"  - From @{sender_name}: {message.text[:50]}...")
        
        await client.disconnect()
        return True
    else:
        print("❌ Session not authorized")
        await client.disconnect()
        return False

if __name__ == "__main__":
    asyncio.run(test_backend_session())