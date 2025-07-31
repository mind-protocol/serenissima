#!/usr/bin/env python3
"""
Get members of a Telegram chat/group
Note: Bot must be admin in the group to access member list
"""

import requests
import json
import sys
import os

def get_chat_members(chat_id, bot_token=None):
    """Get member information from a Telegram chat
    
    Args:
        chat_id: The chat/group ID
        bot_token: Bot token (defaults to serenissima_ubc_bot)
    """
    
    # Load credentials
    creds_path = os.path.join(os.path.dirname(__file__), 'telegram_credentials.json')
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    bot_token = bot_token or creds['default_bot']['token']
    
    # Try getChatAdministrators first (works for groups)
    url = f"https://api.telegram.org/bot{bot_token}/getChatAdministrators"
    payload = {"chat_id": chat_id}
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result.get('ok'):
        print("=== Chat Administrators ===")
        for admin in result['result']:
            user = admin['user']
            print(f"- {user.get('first_name', '')} {user.get('last_name', '')}")
            print(f"  Username: @{user.get('username', 'N/A')}")
            print(f"  ID: {user['id']}")
            print(f"  Status: {admin['status']}")
            print()
    
    # Get chat info
    url = f"https://api.telegram.org/bot{bot_token}/getChat"
    response = requests.post(url, json=payload)
    chat_info = response.json()
    
    if chat_info.get('ok'):
        chat = chat_info['result']
        print(f"=== Chat Info ===")
        print(f"Title: {chat.get('title', 'N/A')}")
        print(f"Type: {chat.get('type')}")
        print(f"ID: {chat.get('id')}")
        if 'member_count' in chat:
            print(f"Member Count: {chat['member_count']}")
    
    # Note: getChatMember requires knowing specific user_ids
    # There's no API method to get ALL members of a group
    print("\nNote: Telegram Bot API doesn't provide a method to list all members.")
    print("Only admins and recent active users can be retrieved.")
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python get_chat_members.py <chat_id> [bot_token]")
        print("Example: python get_chat_members.py -1001699255893")
        sys.exit(1)
    
    chat_id = sys.argv[1]
    bot_token = sys.argv[2] if len(sys.argv) > 2 else None
    
    get_chat_members(chat_id, bot_token)

if __name__ == "__main__":
    main()