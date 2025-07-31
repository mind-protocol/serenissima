#!/usr/bin/env python3
"""
Test Telegram API to get channel info and recent messages
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_CHAT_ID = '-1001699255893'

def get_chat_info():
    """Get info about the chat"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat"
    params = {'chat_id': TELEGRAM_GROUP_CHAT_ID}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            print("=== MAIN CHANNEL INFO ===")
            print(f"ID: {result.get('id')}")
            print(f"Title: {result.get('title')}")
            print(f"Type: {result.get('type')}")
            print(f"Is Forum: {result.get('is_forum', False)}")
            print(f"Username: @{result.get('username', 'N/A')}")
            print()
        else:
            print(f"Error getting chat info: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def get_forum_topics():
    """Get forum topics if it's a forum"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getForumTopicIconStickers"
    
    # Try to get some recent messages with different thread IDs
    url2 = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {
        'offset': -100,  # Get last 100 messages
        'allowed_updates': ['message']
    }
    
    try:
        response = requests.get(url2, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            updates = data.get('result', [])
            
            print("=== RECENT MESSAGES WITH THREADS ===")
            threads_seen = {}
            
            for update in updates[-20:]:  # Last 20 messages
                msg = update.get('message', {})
                thread_id = msg.get('message_thread_id')
                text = msg.get('text', '')[:50] + '...' if msg.get('text') else 'No text'
                from_user = msg.get('from', {}).get('username', 'Unknown')
                
                if thread_id and thread_id not in threads_seen:
                    threads_seen[thread_id] = {
                        'sample_text': text,
                        'from_user': from_user
                    }
            
            for tid, info in threads_seen.items():
                print(f"Thread ID: {tid}")
                print(f"  Sample message: {info['sample_text']}")
                print(f"  From: @{info['from_user']}")
                print()
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_chat_info()
    get_forum_topics()