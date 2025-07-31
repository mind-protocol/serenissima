#!/usr/bin/env python3
"""
Test Telegram integration for Resonance
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def test_telegram_connection():
    """Test if we can connect to Telegram"""
    try:
        # Test bot connection
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot connected: @{bot_info['result']['username']}")
            return True
        else:
            print(f"❌ Bot connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Telegram: {e}")
        return False

def check_recent_messages():
    """Check for recent messages to the bot"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        response = requests.get(url, params={"limit": 10})
        
        if response.status_code == 200:
            updates = response.json()
            messages = []
            
            for update in updates.get('result', []):
                if 'message' in update:
                    msg = update['message']
                    # Only include private messages (not from groups)
                    if msg.get('chat', {}).get('type') == 'private':
                        messages.append({
                            'from': msg.get('from', {}).get('username', 'Unknown'),
                            'text': msg.get('text', ''),
                            'date': msg.get('date', 0),
                            'chat_id': msg.get('chat', {}).get('id')
                        })
            
            print(f"\n📨 Found {len(messages)} recent private messages:")
            for msg in messages[-5:]:  # Show last 5
                date = datetime.fromtimestamp(msg['date']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  - From @{msg['from']} at {date}: {msg['text'][:50]}...")
            
            return messages
        else:
            print(f"❌ Failed to get updates: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
        return []

def test_queue_directory():
    """Test if queue directory exists and is writable"""
    queue_path = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/Resonance/pending"
    
    if os.path.exists(queue_path):
        print(f"✅ Queue directory exists: {queue_path}")
        
        # Check if writable
        test_file = os.path.join(queue_path, "test_write.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✅ Queue directory is writable")
        except Exception as e:
            print(f"❌ Queue directory not writable: {e}")
    else:
        print(f"❌ Queue directory does not exist: {queue_path}")
        # Try to create it
        try:
            os.makedirs(queue_path, exist_ok=True)
            print("✅ Created queue directory")
        except Exception as e:
            print(f"❌ Could not create queue directory: {e}")

def main():
    print("=== TELEGRAM INTEGRATION TEST ===\n")
    
    # Test 1: Bot connection
    if test_telegram_connection():
        
        # Test 2: Check for messages
        messages = check_recent_messages()
        
        # Test 3: Queue directory
        test_queue_directory()
        
        print("\n📊 SUMMARY:")
        print(f"- Bot is online and reachable")
        print(f"- Found {len(messages)} recent private messages")
        print(f"- Queue system needs to route these to Resonance")
        
        if messages:
            print("\n⚠️  ISSUE: Messages are reaching the bot but not being routed to the queue!")
            print("The telegram_resonance_watcher.py needs to be running to process these.")
    else:
        print("\n❌ Bot is not accessible. Check TELEGRAM_BOT_TOKEN in .env")

if __name__ == "__main__":
    main()