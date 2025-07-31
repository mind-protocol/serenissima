#!/usr/bin/env python3
"""
Save recent messages from NLR to the queue
"""

import asyncio
from telethon import TelegramClient
from datetime import datetime, timezone
import json
from pathlib import Path

# Hardcoded credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Session file
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver/diplomatic_virtuoso'

# Queue
QUEUE_DIR = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending')
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

async def save_nlr_messages():
    """Save recent messages from NLR"""
    print("📥 Saving recent messages from @nlr_ai to queue")
    
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if await client.is_user_authorized():
        # Get messages from Nicolas Reynolds
        nlr = await client.get_entity('nlr_ai')
        print(f"✅ Found user: @{nlr.username} (ID: {nlr.id})")
        
        saved_count = 0
        
        # Get recent messages from NLR
        async for message in client.iter_messages(nlr, limit=10):
            if message.text and message.sender_id == nlr.id:
                # Check if message is recent (last hour)
                now = datetime.now(timezone.utc)
                time_diff = now - message.date
                
                if time_diff.total_seconds() < 3600:  # 1 hour
                    print(f"\n📱 Message: {message.text[:50]}...")
                    print(f"   Time: {message.date}")
                    
                    # Save to queue
                    message_data = {
                        'message_id': message.id,
                        'timestamp': message.date.isoformat(),
                        'text': message.text,
                        'from_id': nlr.id,
                        'from_username': nlr.username,
                        'from_name': f"{nlr.first_name} {nlr.last_name or ''}".strip(),
                        'chat_id': message.chat_id,
                        'chat_type': 'private',
                        'is_reply': message.is_reply,
                        'raw_message': {
                            'id': message.id,
                            'peer_id': {'user_id': nlr.id},
                            'date': message.date.isoformat(),
                            'message': message.text,
                            'out': message.out,
                            'mentioned': message.mentioned,
                            'from_id': {'user_id': nlr.id}
                        }
                    }
                    
                    # Generate filename
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{nlr.id}_{saved_count}.json"
                    filepath = QUEUE_DIR / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(message_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"   ✅ Saved to: {filepath}")
                    saved_count += 1
        
        print(f"\n📊 Total messages saved: {saved_count}")
    else:
        print("❌ Not authorized!")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(save_nlr_messages())