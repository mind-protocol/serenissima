#!/usr/bin/env python3
"""
Test the listener interactively to see what's happening
"""

import asyncio
from telethon import TelegramClient, events
from pathlib import Path
import json
from datetime import datetime

# Hardcoded credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Session file
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver/diplomatic_virtuoso'

# Queue
QUEUE_DIR = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending')
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    """Test the listener"""
    print("🚀 Starting Telegram listener test")
    print(f"📁 Session file: {SESSION_FILE}")
    print(f"📂 Queue directory: {QUEUE_DIR}")
    
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    
    @client.on(events.NewMessage(incoming=True))
    async def handle_message(event):
        """Handle incoming messages"""
        print(f"\n📱 New message received!")
        
        try:
            sender = await event.get_sender()
            print(f"From: @{getattr(sender, 'username', 'Unknown')} ({getattr(sender, 'first_name', 'Unknown')})")
            print(f"Text: {event.message.text[:100]}")
            
            # Save to queue
            message_data = {
                'message_id': event.message.id,
                'timestamp': datetime.now().isoformat(),
                'text': event.message.text,
                'from_id': sender.id if sender else None,
                'from_username': getattr(sender, 'username', 'Unknown'),
                'from_name': f"{getattr(sender, 'first_name', '')} {getattr(sender, 'last_name', '')}".strip(),
                'chat_id': event.chat_id,
                'chat_type': 'private' if event.is_private else 'group',
                'is_reply': event.message.is_reply
            }
            
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{sender.id if sender else 'unknown'}.json"
            filepath = QUEUE_DIR / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(message_data, f, ensure_ascii=False, indent=2)
                
            print(f"✅ Saved to: {filepath}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    await client.connect()
    
    if await client.is_user_authorized():
        print("\n✅ Connected and authorized!")
        
        me = await client.get_me()
        print(f"📱 Logged in as: @{me.username}")
        
        print("\n👂 Listening for messages... Send a message to @diplomatic_virtuoso")
        print("Press Ctrl+C to stop\n")
        
        await client.run_until_disconnected()
    else:
        print("❌ Not authorized!")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped")