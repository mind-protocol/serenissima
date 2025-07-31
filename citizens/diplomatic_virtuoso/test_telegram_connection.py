#!/usr/bin/env python3
"""
Test Telegram connection for diplomatic_virtuoso
"""

from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import json

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Load session data
with open('telegram_session_data.json', 'r') as f:
    session_data = json.load(f)

async def test_connection():
    """Test if we can connect with the session"""
    
    print("Testing Telegram connection...")
    print(f"Account: @{session_data.get('account', 'unknown')}")
    print(f"User ID: {session_data['userId']}")
    print(f"DC: {session_data['dcId']}")
    
    # Try different session formats
    auth_key = session_data[f'dc{session_data["dcId"]}_auth_key']
    
    # Method 1: Direct StringSession
    try:
        print("\nTrying StringSession format...")
        
        # Create a basic session string
        session = StringSession()
        client = TelegramClient(session, API_ID, API_HASH)
        
        # Try to connect
        await client.connect()
        
        # Check authorization
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ SUCCESS! Connected as @{me.username}")
            print(f"Name: {me.first_name} {me.last_name or ''}")
            print(f"Premium: {getattr(me, 'premium', False)}")
            
            # Save working session
            session_string = client.session.save()
            with open('diplomatic_session.txt', 'w') as f:
                f.write(session_string)
            print(f"\nSession saved to diplomatic_session.txt")
            
            await client.disconnect()
            return True
        else:
            print("❌ Not authorized with this method")
            await client.disconnect()
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Method 2: Try phone auth
    print("\nSession data incompatible. You may need to:")
    print("1. Login fresh with phone number")
    print("2. Use a different session extraction method")
    
    return False

async def login_fresh():
    """Login with phone number"""
    
    client = TelegramClient('diplomatic_virtuoso_new', API_ID, API_HASH)
    
    await client.start(
        phone=lambda: input("Enter phone number (+33789541802): "),
        password=lambda: input("Enter 2FA password (if any): "),
        code_callback=lambda: input("Enter code received: ")
    )
    
    me = await client.get_me()
    print(f"\n✅ Logged in as @{me.username}")
    
    # Save string session
    session_string = StringSession.save(client.session)
    with open('diplomatic_session.txt', 'w') as f:
        f.write(session_string)
    
    print("Session saved to diplomatic_session.txt")
    await client.disconnect()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "login":
        # Fresh login
        asyncio.run(login_fresh())
    else:
        # Test existing session
        success = asyncio.run(test_connection())
        
        if not success:
            print("\nTo login fresh, run:")
            print("python3 test_telegram_connection.py login")