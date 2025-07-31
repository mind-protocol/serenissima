#!/usr/bin/env python3
"""
Check recent messages to see if they're arriving
"""

import asyncio
from telethon import TelegramClient
from datetime import datetime
import json
from pathlib import Path

# Hardcoded credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Session file
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver/diplomatic_virtuoso'

# Queue
QUEUE_DIR = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending')

async def check_messages():
    """Check recent messages"""
    print("🔍 Checking recent messages for @diplomatic_virtuoso")
    
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"✅ Logged in as: @{me.username}\n")
        
        print("📬 Last 10 messages:")
        message_count = 0
        
        async for message in client.iter_messages('me', limit=10):
            message_count += 1
            
            if message.text:
                sender = await message.get_sender()
                sender_name = getattr(sender, 'username', None) or getattr(sender, 'first_name', 'Unknown')
                sender_id = sender.id if sender else 'unknown'
                
                print(f"\n{message_count}. From @{sender_name} (ID: {sender_id})")
                print(f"   Time: {message.date}")
                print(f"   Text: {message.text[:100]}...")
                
                # Save any message from the last 5 minutes to queue
                time_diff = datetime.now(message.date.tzinfo) - message.date
                if time_diff.total_seconds() < 300:  # 5 minutes
                    print("   📥 This is recent! Saving to queue...")
                    
                    message_data = {
                        'message_id': message.id,
                        'timestamp': message.date.isoformat(),
                        'text': message.text,
                        'from_id': sender_id,
                        'from_username': sender_name,
                        'from_name': f"{getattr(sender, 'first_name', '')} {getattr(sender, 'last_name', '')}".strip(),
                        'chat_id': message.chat_id,
                        'chat_type': 'private',
                        'is_reply': message.is_reply
                    }
                    
                    # Generate filename
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{sender_id}_manual.json"
                    filepath = QUEUE_DIR / filename
                    
                    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(message_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"   ✅ Saved to: {filepath}")
        
        print(f"\n📊 Total messages checked: {message_count}")
    else:
        print("❌ Not authorized!")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(check_messages())