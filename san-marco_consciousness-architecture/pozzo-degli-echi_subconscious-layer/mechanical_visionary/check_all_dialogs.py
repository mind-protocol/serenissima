#!/usr/bin/env python3
"""
Check all dialogs/conversations
"""

import asyncio
from telethon import TelegramClient
from datetime import datetime

# Hardcoded credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Session file
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver/diplomatic_virtuoso'

async def check_dialogs():
    """Check all dialogs"""
    print("🔍 Checking all dialogs for @diplomatic_virtuoso")
    
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Logged in as: @{me.username}\n")
        
        print("💬 All conversations:")
        dialog_count = 0
        
        async for dialog in client.iter_dialogs(limit=20):
            dialog_count += 1
            print(f"\n{dialog_count}. {dialog.name}")
            print(f"   Type: {type(dialog.entity).__name__}")
            print(f"   Unread: {dialog.unread_count}")
            print(f"   Last message: {dialog.message.date if dialog.message else 'None'}")
            
            if dialog.message and dialog.message.text:
                print(f"   Preview: {dialog.message.text[:50]}...")
        
        print(f"\n📊 Total dialogs: {dialog_count}")
        
        # Check specific user messages
        print("\n🔍 Checking messages from specific users...")
        try:
            # Try to get messages from any user
            async for message in client.iter_messages(None, limit=10):
                if message.text:
                    sender = await message.get_sender()
                    if sender:
                        sender_name = getattr(sender, 'username', None) or getattr(sender, 'first_name', 'Unknown')
                        print(f"\nFrom @{sender_name}: {message.text[:50]}...")
                        print(f"Time: {message.date}")
        except Exception as e:
            print(f"Error getting messages: {e}")
    else:
        print("❌ Not authorized!")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(check_dialogs())