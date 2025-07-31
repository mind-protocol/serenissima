#!/usr/bin/env python3
"""
Test using existing Telegram session for diplomatic_virtuoso
"""

import os
import sys
import json
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Load and examine existing session
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/diplomatic_virtuoso_session.session'

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

async def test_session():
    """Test if we can connect with existing session"""
    print("🔍 Testing Telegram connection for @diplomatic_virtuoso")
    
    # Try using the existing .session file if it exists
    if os.path.exists(SESSION_FILE):
        print(f"✅ Found session file: {SESSION_FILE}")
        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    else:
        print("❌ No session file found, will need to create new session")
        client = TelegramClient('diplomatic_virtuoso_session', API_ID, API_HASH)
    
    try:
        await client.connect()
        
        if await client.is_user_authorized():
            print("✅ Session is authorized!")
            
            me = await client.get_me()
            print(f"📱 Logged in as: @{me.username} ({me.first_name})")
            
            # Get recent messages
            print("\n📬 Recent messages:")
            async for message in client.iter_messages(limit=10):
                sender = await message.get_sender()
                sender_name = getattr(sender, 'username', None) or getattr(sender, 'first_name', 'Unknown')
                print(f"  - From @{sender_name}: {message.text[:50]}...")
                
        else:
            print("❌ Session not authorized - need to login")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_session())