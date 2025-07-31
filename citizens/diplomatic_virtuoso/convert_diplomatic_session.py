#!/usr/bin/env python3
"""
Convert diplomatic_virtuoso's Telegram Desktop session to Telethon
"""

from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, CreateNewSession
import asyncio

async def convert_session():
    print("Converting diplomatic_virtuoso session...")
    print("=" * 50)
    
    try:
        # Load TDesktop with specific session
        tdesk = TDesktop("./telegram_session_export")
        
        # Check if loaded
        if not tdesk.isLoaded():
            print("❌ Failed to load Telegram Desktop session")
            print("Make sure the export contains all necessary files")
            return
        
        # Display account info
        accounts = tdesk.GetAccounts()
        print(f"Found {len(accounts)} account(s)")
        
        for acc in accounts:
            print(f"\nAccount: {acc.get('index', 'Unknown')}")
            print(f"Authorization Key ID: {acc.get('authKeyID', 'Unknown')}")
        
        # Convert to Telethon
        print("\nConverting to Telethon format...")
        client = await tdesk.ToTelethon(
            session="diplomatic_virtuoso.session",
            flag=CreateNewSession,
            api=API.TelegramDesktop
        )
        
        # Test the session
        await client.connect()
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"\n✅ Success! Session created for: @{me.username}")
            print(f"Name: {me.first_name} {me.last_name or ''}")
            print(f"User ID: {me.id}")
            print(f"Phone: {me.phone}")
            
            # Save session info
            with open("session_info.txt", "w") as f:
                f.write(f"Username: @{me.username}\n")
                f.write(f"Name: {me.first_name} {me.last_name or ''}\n")
                f.write(f"User ID: {me.id}\n")
                f.write(f"Session file: diplomatic_virtuoso.session\n")
            
            print("\nSession saved as: diplomatic_virtuoso.session")
            print("You can now use this session with Telethon!")
        else:
            print("❌ Session not authorized - may need re-authentication")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure opentele is installed: pip install opentele")
        print("2. Ensure all tdata files were copied correctly")
        print("3. Try running Telegram Desktop first to ensure session is active")
    
    finally:
        if 'client' in locals():
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(convert_session())
