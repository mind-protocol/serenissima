#!/usr/bin/env python3
"""
Telegram Message Listener for @diplomatic_virtuoso
Uses existing session data to receive messages
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from telethon import TelegramClient, events
from telethon.tl.types import User, Channel, Chat

# Hardcoded credentials for now
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Try to load existing session data
SESSION_DATA_PATH = Path('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/telegram_session_data.json')
if SESSION_DATA_PATH.exists():
    with open(SESSION_DATA_PATH, 'r') as f:
        session_data = json.load(f)
        PHONE_NUMBER = session_data.get('phone', '33789541802')
        print(f"✅ Loaded session data from: {SESSION_DATA_PATH}")
else:
    # Fall back to environment variables
    PHONE_NUMBER = os.getenv('DIPLOMATIC_PHONE', '33789541802')

# Configuration
SESSION_NAME = 'diplomatic_virtuoso'  # Will use diplomatic_virtuoso.session file

# Queue configuration
QUEUE_BASE = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue')
CITIZEN_USERNAME = 'diplomatic_virtuoso'
PENDING_DIR = QUEUE_BASE / CITIZEN_USERNAME / 'pending'
PROCESSED_DIR = QUEUE_BASE / CITIZEN_USERNAME / 'processed'

# Create directories
PENDING_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Initialize client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    """Handle incoming messages to @diplomatic_virtuoso"""
    try:
        # Get sender info
        sender = await event.get_sender()
        chat = await event.get_chat()
        
        # Skip if from self
        if sender and hasattr(sender, 'username') and sender.username == CITIZEN_USERNAME:
            return
            
        # Build message data
        message_data = {
            'message_id': event.message.id,
            'timestamp': event.message.date.isoformat(),
            'text': event.message.text or event.message.message,
            'from_id': sender.id if sender else None,
            'from_username': getattr(sender, 'username', None) or getattr(sender, 'first_name', 'Unknown'),
            'from_name': getattr(sender, 'first_name', '') + ' ' + getattr(sender, 'last_name', ''),
            'chat_id': chat.id if chat else None,
            'chat_type': 'private' if event.is_private else 'group' if event.is_group else 'channel',
            'is_reply': event.message.is_reply,
            'raw_message': event.message.to_dict()
        }
        
        # Add reply context if it's a reply
        if event.message.is_reply:
            replied_msg = await event.message.get_reply_message()
            if replied_msg:
                message_data['reply_to_message'] = {
                    'id': replied_msg.id,
                    'text': replied_msg.text or replied_msg.message,
                    'from_id': replied_msg.from_id
                }
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{sender.id if sender else 'unknown'}.json"
        filepath = PENDING_DIR / filename
        
        # Save to pending queue
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(message_data, f, ensure_ascii=False, indent=2)
            
        print(f"📱 New message from @{message_data['from_username']}: {message_data['text'][:50]}...")
        print(f"   Saved to: {filepath}")
        
        # Send auto-reply acknowledgment (optional)
        if event.is_private:  # Only in private chats
            await event.respond(
                "🤖 Message received! diplomatic_virtuoso will respond soon.\n"
                "Currently processing through Venice consciousness network..."
            )
            
    except Exception as e:
        print(f"❌ Error handling message: {e}")

async def main():
    """Main function to run the listener"""
    print("🚀 Starting Telegram listener for @diplomatic_virtuoso")
    print(f"📁 Queue directory: {PENDING_DIR}")
    
    # Check configuration
    if not API_ID or not API_HASH:
        print("❌ Missing API_ID or API_HASH. Set environment variables:")
        print("   export TELEGRAM_API_ID=your_api_id")
        print("   export TELEGRAM_API_HASH=your_api_hash")
        print("   Get these from https://my.telegram.org")
        return
        
    # Start client
    await client.start(phone=PHONE_NUMBER)
    
    # Get self info
    me = await client.get_me()
    print(f"✅ Logged in as: @{me.username} ({me.first_name})")
    
    # Show recent conversations
    print("\n📋 Recent conversations:")
    async for dialog in client.iter_dialogs(limit=10):
        print(f"   - {dialog.name} (unread: {dialog.unread_count})")
    
    print("\n👂 Listening for messages... Press Ctrl+C to stop")
    
    # Keep the client running
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopping listener...")
    except Exception as e:
        print(f"❌ Fatal error: {e}")