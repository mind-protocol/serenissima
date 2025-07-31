#!/usr/bin/env python3
"""
Send diplomatic_virtuoso's responses back to Telegram
"""

import asyncio
import json
from pathlib import Path
from telethon import TelegramClient
from datetime import datetime

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Session file
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver/diplomatic_virtuoso'

# Response directory
RESPONSE_DIR = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_responses/diplomatic_virtuoso')
SENT_DIR = RESPONSE_DIR / 'sent'

async def send_responses():
    """Check for responses and send them"""
    print("📤 Telegram Response Sender for diplomatic_virtuoso")
    
    # Create directories
    RESPONSE_DIR.mkdir(parents=True, exist_ok=True)
    SENT_DIR.mkdir(parents=True, exist_ok=True)
    
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized!")
        return
    
    print("✅ Connected to Telegram")
    
    # Check for response files
    responses = list(RESPONSE_DIR.glob("*.json"))
    
    if not responses:
        print("📭 No responses to send")
        return
    
    print(f"📬 Found {len(responses)} response(s) to send")
    
    for response_file in responses:
        try:
            with open(response_file, 'r') as f:
                data = json.load(f)
            
            recipient = data.get('recipient_username') or data.get('recipient_id')
            message = data.get('message', '')
            
            if not recipient or not message:
                print(f"❌ Invalid response format in {response_file.name}")
                continue
            
            print(f"\n📱 Sending to @{recipient}: {message[:50]}...")
            
            # Send message
            await client.send_message(recipient, message)
            print("   ✅ Sent!")
            
            # Move to sent folder
            sent_path = SENT_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{response_file.name}"
            response_file.rename(sent_path)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    await client.disconnect()
    print("\n✅ Response sending complete")

if __name__ == "__main__":
    asyncio.run(send_responses())