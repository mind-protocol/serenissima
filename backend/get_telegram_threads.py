#!/usr/bin/env python3
"""
Get all Telegram thread/topic IDs from recent messages
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1001699255893')

def get_all_threads():
    """Fetch recent messages and extract all unique thread IDs"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {
        'limit': 100,  # Get last 100 messages
        'allowed_updates': ['message', 'channel_post']
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get('result', [])
            
            threads = {}
            main_chat_id = None
            main_chat_info = {}
            
            for update in results:
                message = update.get('message') or update.get('channel_post')
                if not message:
                    continue
                
                chat = message.get('chat', {})
                chat_id = chat.get('id')
                
                if chat_id:
                    main_chat_id = chat_id
                    main_chat_info = chat
                
                # Check for thread ID
                thread_id = message.get('message_thread_id')
                if thread_id:
                    # Get thread name from reply_to_message if available
                    reply_to = message.get('reply_to_message', {})
                    topic_created = reply_to.get('forum_topic_created', {})
                    thread_name = topic_created.get('name', 'Unknown')
                    
                    if thread_id not in threads:
                        threads[thread_id] = thread_name
            
            print(f"Main Channel ID: {main_chat_id}")
            print(f"Main Channel Name: {main_chat_info.get('title', 'Unknown')}")
            print(f"Is Forum: {main_chat_info.get('is_forum', False)}")
            print("\nSubchannels/Threads found:")
            for thread_id, name in sorted(threads.items()):
                print(f"  Thread ID: {thread_id} - Name: {name}")
                
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error fetching updates: {e}")

if __name__ == "__main__":
    get_all_threads()