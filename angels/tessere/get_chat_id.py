#!/usr/bin/env python3
"""
Get Telegram chat/channel IDs
For channels: Bot must be admin in the channel
"""

import requests
import json
from datetime import datetime

# Bot token
bot_token = '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA'

print("🔍 Fetching all chats/channels the bot has access to...")
print("For channels: Make sure the bot is added as admin!\n")

# Get updates with different types
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
response = requests.get(url)

# Also check for channel posts
if response.status_code == 200:
    data = response.json()
    
    # First, let's see ALL update types
    print("Update types found:")
    for update in data.get('result', [])[-20:]:
        print(f"- {list(update.keys())}")
    print()

if response.status_code == 200 and data['ok']:
        seen_chats = set()
        
        # Check all update types
        for update in data['result'][-50:]:  # Last 50 updates
            chat = None
            update_type = None
            
            # Check different update types
            if 'message' in update:
                chat = update['message']['chat']
                update_type = "message"
            elif 'channel_post' in update:
                chat = update['channel_post']['chat']
                update_type = "channel_post"
            elif 'edited_channel_post' in update:
                chat = update['edited_channel_post']['chat']
                update_type = "edited_channel_post"
            elif 'my_chat_member' in update:
                chat = update['my_chat_member']['chat']
                update_type = "my_chat_member"
                
            if chat and chat['id'] not in seen_chats:
                seen_chats.add(chat['id'])
                
                # Chat info
                chat_id = chat['id']
                chat_type = chat['type']
                title = chat.get('title', '')
                username = chat.get('username', '')
                first_name = chat.get('first_name', '')
                
                print(f"\n{'='*60}")
                print(f"Chat ID: {chat_id}")
                print(f"Type: {chat_type}")
                if title:
                    print(f"Title: {title}")
                if username:
                    print(f"Username: @{username}")
                if first_name:
                    print(f"Name: {first_name}")
                print(f"Update type: {update_type}")
                
        if not seen_chats:
            print("\n❌ No chats found!")
            print("\nFor channels:")
            print("1. Add the bot to your channel as admin")
            print("2. Post a message in the channel")
            print("3. Run this script again")
            
        print("\n\n📝 Channel IDs in Telegram:")
        print("- Private channels: Start with -100 (e.g., -1001234567890)")  
        print("- Public channels: Can also use @username format")
        print("- Groups: Negative numbers without -100 prefix")
else:
    print(f"❌ Error: {response.status_code}")