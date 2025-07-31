#!/usr/bin/env python3
"""
Fetch recent Telegram messages to find all thread IDs
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_CHAT_ID = '-1001699255893'

def fetch_all_recent_messages():
    """Fetch recent messages and show thread IDs"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    # Get last 100 updates
    params = {
        'limit': 100,
        'allowed_updates': ['message', 'channel_post']
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            updates = data.get('result', [])
            
            print(f"=== FOUND {len(updates)} UPDATES ===\n")
            
            # Track unique thread IDs
            threads = {}
            
            # Process each update
            for update in updates:
                message = update.get('message') or update.get('channel_post')
                if not message:
                    continue
                
                # Extract message details
                msg_id = message.get('message_id')
                thread_id = message.get('message_thread_id')
                text = message.get('text', '')
                timestamp = message.get('date')
                from_user = message.get('from', {})
                username = from_user.get('username', 'Unknown')
                chat = message.get('chat', {})
                
                # Convert timestamp
                if timestamp:
                    dt = datetime.fromtimestamp(timestamp)
                    time_str = dt.strftime('%H:%M:%S')
                else:
                    time_str = 'Unknown'
                
                # Only show messages from the target group
                if str(chat.get('id')) == TELEGRAM_GROUP_CHAT_ID:
                    # Track thread info
                    if thread_id:
                        if thread_id not in threads:
                            threads[thread_id] = {
                                'count': 0,
                                'users': set(),
                                'sample_messages': []
                            }
                        threads[thread_id]['count'] += 1
                        threads[thread_id]['users'].add(username)
                        if len(threads[thread_id]['sample_messages']) < 3:
                            threads[thread_id]['sample_messages'].append({
                                'time': time_str,
                                'user': username,
                                'text': text[:50] + '...' if len(text) > 50 else text
                            })
                    
                    # Show messages from nlr_ai specifically
                    if username == 'nlr_ai' and 'stor' in text.lower():
                        print(f"NLR Message:")
                        print(f"  Time: {time_str}")
                        print(f"  Thread ID: {thread_id or 'Main channel'}")
                        print(f"  Text: {text}")
                        print()
            
            print("\n=== THREAD SUMMARY ===")
            if threads:
                for tid, info in sorted(threads.items()):
                    print(f"\nThread ID: {tid}")
                    print(f"  Messages: {info['count']}")
                    print(f"  Users: {', '.join(info['users'])}")
                    print("  Sample messages:")
                    for msg in info['sample_messages']:
                        print(f"    [{msg['time']}] @{msg['user']}: {msg['text']}")
            else:
                print("No messages with thread IDs found in recent updates")
            
            # Show messages without thread IDs (main channel)
            main_channel_count = sum(1 for u in updates if (u.get('message') or u.get('channel_post', {})).get('message_thread_id') is None)
            print(f"\nMain channel messages (no thread): {main_channel_count}")
                
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error fetching updates: {e}")

if __name__ == "__main__":
    fetch_all_recent_messages()