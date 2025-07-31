#!/usr/bin/env python3
"""
Periodic checker for new Telegram messages
Runs every 30 seconds to fetch new messages
"""

import asyncio
import json
import time
from pathlib import Path
from telethon import TelegramClient
from datetime import datetime, timezone

# API credentials
API_ID = 25575567
API_HASH = 'cfd7b9972213410976adab046c07c5d4'

# Session file
SESSION_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver/diplomatic_virtuoso'

# Queue
QUEUE_DIR = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending')
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

# State file to track last check
STATE_FILE = Path('telegram_checker_state.json')

def load_state():
    """Load last check timestamp"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'last_check': datetime.now(timezone.utc).isoformat()}

def save_state(state):
    """Save state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

async def check_new_messages():
    """Check for new messages since last check"""
    state = load_state()
    last_check = datetime.fromisoformat(state['last_check'])
    
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Not authorized!")
        return
    
    new_messages = 0
    
    # Check all dialogs for new messages
    async for dialog in client.iter_dialogs(limit=20):
        if dialog.unread_count > 0 or (dialog.message and dialog.message.date > last_check):
            # Get messages from this dialog
            async for message in client.iter_messages(dialog, limit=10):
                if message.date > last_check and message.text and not message.out:
                    # New incoming message!
                    sender = await message.get_sender()
                    
                    if sender:
                        print(f"📱 New message from @{getattr(sender, 'username', 'Unknown')}: {message.text[:50]}...")
                        
                        # Save to queue
                        message_data = {
                            'message_id': message.id,
                            'timestamp': message.date.isoformat(),
                            'text': message.text,
                            'from_id': sender.id,
                            'from_username': getattr(sender, 'username', 'Unknown'),
                            'from_name': f"{getattr(sender, 'first_name', '')} {getattr(sender, 'last_name', '')}".strip(),
                            'chat_id': dialog.id,
                            'chat_type': 'private' if dialog.is_user else 'group',
                            'is_reply': message.is_reply
                        }
                        
                        # Generate filename
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{sender.id}_{new_messages}.json"
                        filepath = QUEUE_DIR / filename
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(message_data, f, ensure_ascii=False, indent=2)
                        
                        new_messages += 1
    
    # Update state
    state['last_check'] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    
    await client.disconnect()
    
    return new_messages

async def main():
    """Main loop"""
    print("🔄 Starting Telegram Periodic Checker")
    print("📱 Checking every 30 seconds for new messages...")
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            # Check for new messages
            count = await check_new_messages()
            
            if count > 0:
                print(f"✅ Saved {count} new message(s) to queue")
            else:
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - No new messages")
            
            # Wait 30 seconds
            await asyncio.sleep(30)
            
        except KeyboardInterrupt:
            print("\n👋 Stopping checker...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())