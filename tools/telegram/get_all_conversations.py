#!/usr/bin/env python3
"""
Analyze all conversations from Telegram bot updates
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

def get_all_conversations(bot_token):
    """Get all unique conversations from recent updates"""
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {"limit": 100}  # Get last 100 updates
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if not data.get('ok'):
        print(f"Error: {data}")
        return
    
    conversations = defaultdict(dict)
    
    for update in data.get('result', []):
        if 'message' in update:
            msg = update['message']
            chat = msg['chat']
            chat_id = chat['id']
            
            # Store conversation info
            conversations[chat_id] = {
                'type': chat['type'],
                'title': chat.get('title', 'Private Chat'),
                'username': chat.get('username', 'N/A'),
                'first_name': chat.get('first_name', ''),
                'last_name': chat.get('last_name', ''),
                'last_message': msg.get('text', '')[:50] + '...',
                'last_update': datetime.fromtimestamp(msg['date']).strftime('%Y-%m-%d %H:%M:%S')
            }
    
    print(f"=== Active Conversations ({len(conversations)}) ===\n")
    
    for chat_id, info in conversations.items():
        print(f"Chat ID: {chat_id}")
        print(f"Type: {info['type']}")
        print(f"Name: {info['title']} (@{info['username']})")
        if info['type'] == 'private':
            print(f"User: {info['first_name']} {info['last_name']}")
        print(f"Last message: {info['last_message']}")
        print(f"Last update: {info['last_update']}")
        print("-" * 50)
    
    # Save to file
    with open('active_conversations.json', 'w') as f:
        json.dump(dict(conversations), f, indent=2)
    print(f"\nSaved to active_conversations.json")

if __name__ == "__main__":
    # My bot token
    bot_token = "8159027121:AAHdzWfhIOABHY3fiyiOOblfS8Fuzq9IwR8"
    get_all_conversations(bot_token)