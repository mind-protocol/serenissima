#!/usr/bin/env python3
"""
Test Telegram session connection step by step
"""

import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Session file path
SESSION_FILE = 'diplomatic_virtuoso_session'

async def test_connection():
    """Test basic connection"""
    print("Step 1: Creating client...")
    
    # Create client with session name
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    
    print("Step 2: Connecting...")
    await client.connect()
    
    print("Step 3: Checking authorization...")
    if await client.is_user_authorized():
        print("✅ Already authorized!")
        
        me = await client.get_me()
        print(f"\n📱 Logged in as:")
        print(f"  Username: @{me.username}")
        print(f"  Name: {me.first_name} {me.last_name}")
        print(f"  ID: {me.id}")
        print(f"  Phone: {me.phone}")
        
        return True
    else:
        print("❌ Not authorized - need to login")
        print("\nTo login, you would need to:")
        print("1. Call client.start(phone='33789541802')")
        print("2. Enter the code sent to the phone")
        print("3. Save the session")
        
        return False
    
    await client.disconnect()

if __name__ == "__main__":
    # Check if session file exists
    if os.path.exists(f"{SESSION_FILE}.session"):
        print(f"✅ Found existing session file: {SESSION_FILE}.session")
    else:
        print(f"❌ No session file found at: {SESSION_FILE}.session")
        print("   Will need to create new session...")
    
    print("\nTesting connection...")
    asyncio.run(test_connection())