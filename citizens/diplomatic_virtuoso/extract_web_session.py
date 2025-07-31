#!/usr/bin/env python3
"""
Extract Telegram Web session for diplomatic_virtuoso
Works with web.telegram.org session data
"""

import json
import base64
from pathlib import Path

def extract_web_session():
    """
    Extract session from Telegram Web
    
    Instructions:
    1. Open web.telegram.org in Chrome/Firefox
    2. Make sure you're logged in as @diplomatic_virtuoso
    3. Open Developer Tools (F12)
    4. Go to Application tab (Chrome) or Storage tab (Firefox)
    5. Find Local Storage → web.telegram.org
    6. Look for these keys and copy their values:
       - dc
       - dc1_auth_key, dc2_auth_key, etc.
       - dc1_server_salt, dc2_server_salt, etc.
       - user_auth
    7. Paste the values when prompted
    """
    
    print("Telegram Web Session Extractor")
    print("=" * 50)
    print("\nFollow these steps:")
    print("1. Open web.telegram.org")
    print("2. Press F12 for Developer Tools")
    print("3. Go to Application → Local Storage → web.telegram.org")
    print("4. Find and copy the session data\n")
    
    session_data = {}
    
    # Collect DC info
    print("Enter the 'dc' value (usually a number like 2):")
    session_data['dc'] = input().strip()
    
    # Collect auth keys
    print(f"\nEnter 'dc{session_data['dc']}_auth_key' value:")
    print("(This is a long string, paste it all)")
    session_data['auth_key'] = input().strip()
    
    print(f"\nEnter 'dc{session_data['dc']}_server_salt' value:")
    session_data['server_salt'] = input().strip()
    
    print("\nEnter 'user_auth' value (JSON object):")
    user_auth_raw = input().strip()
    
    try:
        session_data['user_auth'] = json.loads(user_auth_raw)
    except:
        print("Could not parse user_auth as JSON")
        session_data['user_auth'] = user_auth_raw
    
    # Save session data
    with open('web_session_data.json', 'w') as f:
        json.dump(session_data, f, indent=2)
    
    print("\n✅ Session data saved to web_session_data.json")
    
    # Create converter script
    create_web_converter()
    
    return session_data

def create_web_converter():
    """Create script to convert web session to Telethon"""
    
    converter_code = '''#!/usr/bin/env python3
"""
Convert Telegram Web session to Telethon session
"""

from telethon import TelegramClient
from telethon.sessions import StringSession
import json
import asyncio

# Your API credentials (get from my.telegram.org)
API_ID = 123456  # Replace with your API ID
API_HASH = 'your_api_hash'  # Replace with your API hash

async def convert_web_session():
    """Convert web session data to Telethon"""
    
    # Load web session data
    with open('web_session_data.json', 'r') as f:
        session_data = json.load(f)
    
    print("Converting web session to Telethon...")
    print("=" * 50)
    
    # Create a new client with string session
    client = TelegramClient(
        StringSession(),
        API_ID,
        API_HASH
    )
    
    try:
        # Connect and attempt to use existing auth
        await client.connect()
        
        # Import session manually (advanced)
        # This requires manual session construction
        # which is complex due to MTProto encryption
        
        print("\\nNote: Direct web session import is complex.")
        print("Alternative approach:")
        print("1. Use QR code login")
        print("2. Use phone number auth")
        print("3. Use session string from another client")
        
        # For now, let's try QR code approach
        if not await client.is_user_authorized():
            print("\\nGenerating QR code for login...")
            
            # QR Code login
            qr_login = await client.qr_login()
            
            # Show QR code URL
            print(f"\\n📱 Scan this QR code with Telegram mobile:")
            print(f"URL: {qr_login.url}")
            
            # Wait for login
            try:
                await qr_login.wait()
                print("✅ Login successful!")
            except asyncio.TimeoutError:
                print("❌ QR code expired. Run again.")
                return
        
        # If authorized, save session
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"\\n✅ Logged in as: @{me.username}")
            print(f"Name: {me.first_name} {me.last_name or ''}")
            
            # Save session string
            session_string = client.session.save()
            with open('diplomatic_session_string.txt', 'w') as f:
                f.write(session_string)
            
            print(f"\\nSession string saved to: diplomatic_session_string.txt")
            print("You can use this string to login anywhere!")
            
            # Also save as regular session
            new_client = TelegramClient('diplomatic_virtuoso', API_ID, API_HASH)
            await new_client.connect()
            await new_client.import_session(StringSession(session_string))
            await new_client.disconnect()
            
            print("Regular session saved as: diplomatic_virtuoso.session")
            
    except Exception as e:
        print(f"\\nError: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    print("Make sure to update API_ID and API_HASH first!")
    print("Get them from: https://my.telegram.org")
    asyncio.run(convert_web_session())
'''
    
    with open('convert_web_session.py', 'w') as f:
        f.write(converter_code)
    
    print("Created: convert_web_session.py")
    print("\nNext steps:")
    print("1. Get API credentials from https://my.telegram.org")
    print("2. Update API_ID and API_HASH in convert_web_session.py")
    print("3. Run: python3 convert_web_session.py")

def alternative_qr_login():
    """Create a simple QR code login script"""
    
    qr_code = '''#!/usr/bin/env python3
"""
QR Code Login for diplomatic_virtuoso
Simplest way to get Telethon session
"""

from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import qrcode

# Your API credentials (get from my.telegram.org)
API_ID = 123456  # Replace with your API ID
API_HASH = 'your_api_hash'  # Replace with your API hash

async def qr_login():
    """Login using QR code"""
    
    client = TelegramClient('diplomatic_virtuoso', API_ID, API_HASH)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Generating QR code...")
        
        # Generate QR login
        qr_login = await client.qr_login()
        
        # Create QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_login.url)
        qr.make(fit=True)
        
        # Save QR code
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('telegram_login_qr.png')
        
        print("\\n📱 QR Code saved as: telegram_login_qr.png")
        print("Scan with Telegram mobile app")
        print(f"Or use URL: {qr_login.url}")
        
        # Wait for scan
        try:
            await qr_login.wait()
            print("\\n✅ Login successful!")
        except asyncio.TimeoutError:
            print("\\n❌ QR code expired")
            return
    
    # Check login
    me = await client.get_me()
    print(f"\\nLogged in as: @{me.username}")
    print(f"Name: {me.first_name} {me.last_name or ''}")
    print(f"User ID: {me.id}")
    
    # Save session string
    session_string = StringSession.save(client.session)
    with open('session_string.txt', 'w') as f:
        f.write(session_string)
    
    print("\\nSession saved!")
    print("- Regular session: diplomatic_virtuoso.session")
    print("- String session: session_string.txt")
    
    await client.disconnect()

if __name__ == "__main__":
    # Install: pip install telethon qrcode pillow
    asyncio.run(qr_login())
'''
    
    with open('qr_code_login.py', 'w') as f:
        f.write(qr_code)
    
    print("\nAlso created: qr_code_login.py")
    print("This uses QR code login - much simpler!")

if __name__ == "__main__":
    extract_web_session()
    alternative_qr_login()