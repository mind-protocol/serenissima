#!/usr/bin/env python3
"""
Extract diplomatic_virtuoso's specific Telegram session
Session ID: A7FDF864FBC10B77
"""

import os
import shutil
from pathlib import Path

def extract_diplomatic_session():
    """Extract the specific session for diplomatic_virtuoso"""
    
    # Paths
    session_id = "A7FDF864FBC10B77"
    tdata_base = Path("/mnt/c/Users/reyno/AppData/Roaming/Telegram Desktop/tdata")
    session_path = tdata_base / session_id
    output_dir = Path("./telegram_session_export")
    
    print("Extracting diplomatic_virtuoso session")
    print(f"Session ID: {session_id}")
    print("=" * 50)
    
    # Check if session exists
    if not session_path.exists():
        print(f"❌ Session folder not found: {session_path}")
        return False
        
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Copy the session folder
    print(f"Copying session folder: {session_id}")
    session_output = output_dir / session_id
    if session_output.exists():
        shutil.rmtree(session_output)
    shutil.copytree(session_path, session_output)
    
    # Copy essential root files from tdata
    essential_files = [
        "key_data",
        "settings",
        "settings0",
        "settings1", 
        "settings2",
        "settings3",
        "configs",
        "usertag"
    ]
    
    for filename in essential_files:
        file_path = tdata_base / filename
        if file_path.exists():
            shutil.copy2(file_path, output_dir / filename)
            print(f"Copied: {filename}")
    
    # Also check for any files starting with session_id
    for file in tdata_base.iterdir():
        if file.is_file() and file.name.startswith(session_id):
            shutil.copy2(file, output_dir / file.name)
            print(f"Copied: {file.name}")
    
    print(f"\n✅ Session extracted to: {output_dir.absolute()}")
    
    # Create the converter script
    create_converter_script()
    
    return True

def create_converter_script():
    """Create the Telethon converter script"""
    
    converter_code = '''#!/usr/bin/env python3
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
            print(f"\\nAccount: {acc.get('index', 'Unknown')}")
            print(f"Authorization Key ID: {acc.get('authKeyID', 'Unknown')}")
        
        # Convert to Telethon
        print("\\nConverting to Telethon format...")
        client = await tdesk.ToTelethon(
            session="diplomatic_virtuoso.session",
            flag=CreateNewSession,
            api=API.TelegramDesktop
        )
        
        # Test the session
        await client.connect()
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"\\n✅ Success! Session created for: @{me.username}")
            print(f"Name: {me.first_name} {me.last_name or ''}")
            print(f"User ID: {me.id}")
            print(f"Phone: {me.phone}")
            
            # Save session info
            with open("session_info.txt", "w") as f:
                f.write(f"Username: @{me.username}\\n")
                f.write(f"Name: {me.first_name} {me.last_name or ''}\\n")
                f.write(f"User ID: {me.id}\\n")
                f.write(f"Session file: diplomatic_virtuoso.session\\n")
            
            print("\\nSession saved as: diplomatic_virtuoso.session")
            print("You can now use this session with Telethon!")
        else:
            print("❌ Session not authorized - may need re-authentication")
            
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        print("\\nTroubleshooting:")
        print("1. Make sure opentele is installed: pip install opentele")
        print("2. Ensure all tdata files were copied correctly")
        print("3. Try running Telegram Desktop first to ensure session is active")
    
    finally:
        if 'client' in locals():
            await client.disconnect()

if __name__ == "__main__":
    asyncio.run(convert_session())
'''
    
    with open("convert_diplomatic_session.py", "w") as f:
        f.write(converter_code)
    
    print("\nCreated: convert_diplomatic_session.py")
    print("\nNext steps:")
    print("1. Install opentele: pip install opentele")
    print("2. Run: python3 convert_diplomatic_session.py")
    print("3. Use the generated diplomatic_virtuoso.session file")

if __name__ == "__main__":
    success = extract_diplomatic_session()
    
    if not success:
        print("\nExtraction failed. Please check the session ID and path.")