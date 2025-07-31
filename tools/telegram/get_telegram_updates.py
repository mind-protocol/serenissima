#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime

def get_telegram_updates(bot_token=None, limit=100):
    """Get recent updates (messages) from Telegram
    
    Args:
        bot_token: Bot token to use (defaults to serenissima_ubc_bot)
        limit: Number of updates to fetch (max 100)
    """
    
    # Load credentials
    creds_path = os.path.join(os.path.dirname(__file__), 'telegram_credentials.json')
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    # Use provided token or default
    bot_token = bot_token or creds['default_bot']['token']
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    params = {
        "limit": limit,
        "allowed_updates": ["message", "channel_post"]
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get("ok"):
        updates = data.get("result", [])
        
        # Extract unique chats
        chats = {}
        for update in updates:
            message = update.get("message") or update.get("channel_post")
            if message and "chat" in message:
                chat = message["chat"]
                chat_id = chat["id"]
                
                if chat_id not in chats:
                    chats[chat_id] = {
                        "id": chat_id,
                        "type": chat["type"],
                        "title": chat.get("title", chat.get("username", "Private Chat")),
                        "username": chat.get("username"),
                        "last_message_date": message.get("date"),
                        "last_message_from": message.get("from", {}).get("username", "Unknown"),
                        "last_message_text": message.get("text", "")[:100] + "..." if len(message.get("text", "")) > 100 else message.get("text", "")
                    }
                else:
                    # Update if this message is newer
                    if message.get("date", 0) > chats[chat_id]["last_message_date"]:
                        chats[chat_id]["last_message_date"] = message.get("date")
                        chats[chat_id]["last_message_from"] = message.get("from", {}).get("username", "Unknown")
                        chats[chat_id]["last_message_text"] = message.get("text", "")[:100] + "..." if len(message.get("text", "")) > 100 else message.get("text", "")
        
        # Sort by last message date
        sorted_chats = sorted(chats.values(), key=lambda x: x["last_message_date"], reverse=True)
        
        print(f"\n🔍 Found {len(sorted_chats)} unique chats with recent messages:\n")
        
        for chat in sorted_chats:
            timestamp = datetime.fromtimestamp(chat["last_message_date"]).strftime("%Y-%m-%d %H:%M:%S")
            print(f"📱 Chat: {chat['title']}")
            print(f"   ID: {chat['id']}")
            print(f"   Type: {chat['type']}")
            if chat['username']:
                print(f"   Username: @{chat['username']}")
            print(f"   Last message: {timestamp}")
            print(f"   From: @{chat['last_message_from']}")
            print(f"   Preview: {chat['last_message_text']}")
            print("-" * 50)
    
    else:
        print(f"Error: {data.get('description', 'Unknown error')}")
    
    return data

def main():
    """CLI interface"""
    import sys
    
    bot_token = sys.argv[1] if len(sys.argv) > 1 else None
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    get_telegram_updates(bot_token, limit)

if __name__ == "__main__":
    main()