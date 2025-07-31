#!/usr/bin/env python3
"""
Extract Telegram Desktop session for diplomatic_virtuoso
For Windows 11
"""

import os
import shutil
from pathlib import Path

def find_telegram_data():
    """Find Telegram Desktop data on Windows"""
    # WSL path to Windows Telegram data
    tdata_path = Path("/mnt/c/Users/reyno/AppData/Roaming/Telegram Desktop/tdata")
    
    if tdata_path.exists():
        print(f"Found Telegram data at: {tdata_path}")
        return tdata_path
    else:
        print(f"Telegram data not found at: {tdata_path}")
        return None

def copy_session_files(tdata_path, output_dir="./telegram_session_export"):
    """Copy necessary session files"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    important_files = []
    
    # Key files to copy
    patterns = [
        "key_data",
        "settings*",
        "configs",
        "*.binlog",
        "usertag",
        "shortcuts-*"
    ]
    
    # Copy main files
    for item in tdata_path.iterdir():
        # Hex-named folders (session data)
        if item.is_dir() and len(item.name) == 16:
            try:
                int(item.name, 16)  # Check if valid hex
                shutil.copytree(item, output_path / item.name)
                important_files.append(item.name)
                print(f"Copied session folder: {item.name}")
            except ValueError:
                pass
        
        # Key files
        elif item.is_file():
            for pattern in patterns:
                if pattern.endswith("*"):
                    if item.name.startswith(pattern[:-1]):
                        shutil.copy2(item, output_path / item.name)
                        important_files.append(item.name)
                        print(f"Copied: {item.name}")
                elif item.name == pattern:
                    shutil.copy2(item, output_path / item.name)
                    important_files.append(item.name)
                    print(f"Copied: {item.name}")
    
    return output_path, important_files

def main():
    print("Telegram Desktop Session Extractor")
    print("==================================\n")
    
    # Find Telegram data
    tdata_path = find_telegram_data()
    
    if not tdata_path:
        print("\nTelegram Desktop data not found!")
        print("Please ensure Telegram Desktop is installed and you're logged in.")
        return
    
    # Copy files
    print(f"\nCopying session files from: {tdata_path}")
    output_path, files = copy_session_files(tdata_path)
    
    print(f"\n✅ Exported {len(files)} files to: {output_path}")
    print("\nNext steps:")
    print("1. Install opentele: pip install opentele")
    print("2. Run the session converter")
    print("3. Use the converted session with telethon")
    
    # Create converter script
    converter_script = '''#!/usr/bin/env python3
"""Convert Telegram Desktop session to Telethon"""

from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, CreateNewSession
import asyncio

async def convert_session():
    # Load TDesktop
    tdesk = TDesktop("./telegram_session_export")
    
    # Check if we can load it
    if not tdesk.isLoaded():
        print("Failed to load Telegram Desktop session")
        return
        
    print(f"Loaded session for: {tdesk.UserName() or 'Unknown'}")
    
    # Convert to Telethon
    client = await tdesk.ToTelethon(
        session="diplomatic_virtuoso.session",
        flag=CreateNewSession
    )
    
    # Test the session
    await client.connect()
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Session created for: @{me.username}")
        print(f"Name: {me.first_name} {me.last_name or ''}")
        print(f"ID: {me.id}")
    else:
        print("❌ Session not authorized")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(convert_session())
'''
    
    with open("convert_telegram_session.py", "w") as f:
        f.write(converter_script)
    
    print("\nCreated: convert_telegram_session.py")
    print("Run it after installing opentele")

if __name__ == "__main__":
    main()