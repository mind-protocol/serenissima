#!/usr/bin/env python3
"""
Manual Telegram Web Session Extractor
Extract session data from web.telegram.org
"""

import json
import re
from pathlib import Path

def extract_web_session_manual():
    """
    Guide through manual web session extraction
    """
    
    print("=" * 60)
    print("TELEGRAM WEB SESSION EXTRACTOR")
    print("=" * 60)
    print("\nThis will help you extract @diplomatic_virtuoso's session")
    print("from web.telegram.org\n")
    
    print("STEP 1: Open web.telegram.org and ensure you're logged in")
    print("STEP 2: Press F12 to open Developer Tools")
    print("STEP 3: Go to Application/Storage → Local Storage → web.telegram.org")
    print("\nYou should see many key-value pairs. We need specific ones.\n")
    
    input("Press Enter when you're ready to continue...")
    
    session_data = {}
    
    # Get DC number
    print("\n" + "="*40)
    print("FINDING YOUR DC (Data Center)")
    print("="*40)
    print("Look for a key called 'dc' (just 'dc', nothing else)")
    print("The value should be a single number like 1, 2, 3, 4, or 5")
    print("\nWhat is your DC number?")
    dc = input("DC: ").strip()
    session_data['dc'] = dc
    
    # Get auth key
    print("\n" + "="*40)
    print("FINDING YOUR AUTH KEY")
    print("="*40)
    print(f"Look for a key called 'dc{dc}_auth_key'")
    print("The value will be a VERY long string (hundreds of characters)")
    print("It might look like: [123,45,67,89...] or encoded text")
    print("\nCopy the ENTIRE value and paste it here:")
    auth_key = input("Auth key: ").strip()
    session_data['auth_key'] = auth_key
    
    # Get server salt
    print("\n" + "="*40)
    print("FINDING YOUR SERVER SALT")
    print("="*40)
    print(f"Look for a key called 'dc{dc}_server_salt'")
    print("This is usually shorter than auth_key")
    print("\nPaste the server salt value:")
    server_salt = input("Server salt: ").strip()
    session_data['server_salt'] = server_salt
    
    # Get user auth
    print("\n" + "="*40)
    print("FINDING YOUR USER INFO")
    print("="*40)
    print("Look for a key called 'user_auth'")
    print("The value should be a JSON object that looks like:")
    print('{"dcID":2,"date":...,"id":"..."}')
    print("\nPaste the entire user_auth value:")
    user_auth = input("User auth: ").strip()
    
    try:
        session_data['user_auth'] = json.loads(user_auth)
        print("✅ User auth parsed successfully")
    except:
        print("⚠️  Could not parse user_auth as JSON, saving as string")
        session_data['user_auth'] = user_auth
    
    # Optional: Get additional DC auth keys if they exist
    print("\n" + "="*40)
    print("CHECKING FOR ADDITIONAL DCs (Optional)")
    print("="*40)
    print("Sometimes Telegram stores auth keys for multiple DCs")
    print("Look for other keys like dc1_auth_key, dc2_auth_key, etc.")
    print("Type 'done' when finished, or paste additional DC data:")
    
    while True:
        extra = input("\nExtra DC (or 'done'): ").strip()
        if extra.lower() == 'done':
            break
        # Process additional DC data if needed
    
    # Save the session data
    with open('web_session_extracted.json', 'w') as f:
        json.dump(session_data, f, indent=2)
    
    print("\n✅ Session data saved to: web_session_extracted.json")
    
    # Create converter
    create_session_converter(session_data)
    
    return session_data

def create_session_converter(session_data):
    """Create a converter script based on extracted data"""
    
    converter_code = f'''#!/usr/bin/env python3
"""
Convert extracted web session to Telethon session
Using diplomatic_virtuoso's extracted data
"""

from telethon import TelegramClient
from telethon.sessions import MemorySession
import json
import struct
import asyncio

# Your API credentials from https://my.telegram.org
API_ID = 123456  # REPLACE WITH YOUR API ID
API_HASH = 'your_api_hash_here'  # REPLACE WITH YOUR API HASH

# Extracted session data
DC_ID = {session_data.get('dc', '2')}
AUTH_KEY = {repr(session_data.get('auth_key', ''))}
SERVER_SALT = {repr(session_data.get('server_salt', ''))}

async def create_session_from_web():
    """Attempt to create Telethon session from web data"""
    
    print("Creating Telethon session from web data...")
    print("=" * 50)
    
    # This is complex because web session format differs from Telethon
    # We'll try multiple approaches
    
    # Approach 1: Try direct connection with extracted data
    session = MemorySession()
    
    # Parse auth key (web format might be array or base64)
    auth_key_bytes = None
    if AUTH_KEY.startswith('[') and AUTH_KEY.endswith(']'):
        # Array format: [123, 45, 67, ...]
        try:
            array_values = json.loads(AUTH_KEY)
            auth_key_bytes = bytes(array_values)
            print("✅ Parsed auth key from array format")
        except:
            print("❌ Could not parse auth key array")
    else:
        # Try as base64 or hex
        try:
            import base64
            auth_key_bytes = base64.b64decode(AUTH_KEY)
            print("✅ Parsed auth key from base64")
        except:
            try:
                auth_key_bytes = bytes.fromhex(AUTH_KEY)
                print("✅ Parsed auth key from hex")
            except:
                print("❌ Could not parse auth key format")
    
    if not auth_key_bytes:
        print("\\nFailed to parse auth key. Web session format may be incompatible.")
        print("\\nAlternative: Create a new session with phone/2FA:")
        await create_new_session()
        return
    
    # Try to use the session
    try:
        # Set DC and auth key
        session.set_dc(DC_ID, '149.154.167.51', 443)  # DC2 default
        session.auth_key = auth_key_bytes
        
        client = TelegramClient(session, API_ID, API_HASH)
        await client.connect()
        
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"\\n✅ SUCCESS! Logged in as @{{me.username}}")
            
            # Save to file
            client.session.save('diplomatic_virtuoso.session')
            print("Session saved as: diplomatic_virtuoso.session")
        else:
            print("\\n❌ Session not authorized. Creating new session...")
            await create_new_session()
            
    except Exception as e:
        print(f"\\n❌ Error: {{e}}")
        print("\\nWeb session format incompatible. Creating new session...")
        await create_new_session()

async def create_new_session():
    """Create a new session with 2FA support"""
    
    client = TelegramClient('diplomatic_virtuoso', API_ID, API_HASH)
    
    await client.start(
        phone=lambda: input("Enter phone number (with country code): "),
        password=lambda: input("Enter 2FA password (if enabled): "),
        code_callback=lambda: input("Enter the code you received: ")
    )
    
    me = await client.get_me()
    print(f"\\n✅ Logged in as @{{me.username}}")
    print("Session saved as: diplomatic_virtuoso.session")
    
    await client.disconnect()

if __name__ == "__main__":
    print("Make sure you've updated API_ID and API_HASH!")
    print("Get them from: https://my.telegram.org\\n")
    
    asyncio.run(create_session_from_web())
'''
    
    with open('convert_web_to_telethon.py', 'w') as f:
        f.write(converter_code)
    
    print("\nCreated: convert_web_to_telethon.py")
    print("\nIMPORTANT NEXT STEPS:")
    print("1. Go to https://my.telegram.org")
    print("2. Get your API ID and API Hash")
    print("3. Update them in convert_web_to_telethon.py")
    print("4. Run: python3 convert_web_to_telethon.py")

if __name__ == "__main__":
    extract_web_session_manual()