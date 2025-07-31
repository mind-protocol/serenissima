#!/usr/bin/env python3
import requests
import json
import os

def get_all_telegram_info(bot_token=None):
    """Get all available information from Telegram bot"""
    
    # Load credentials
    creds_path = os.path.join(os.path.dirname(__file__), 'telegram_credentials.json')
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    # Use diplomatic bot token
    bot_token = bot_token or creds['diplomatic_bot']['token']
    
    # Get bot info
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    bot_info = response.json()
    
    print("🤖 Bot Info:")
    if bot_info.get("ok"):
        print(f"   Username: @{bot_info['result']['username']}")
        print(f"   Name: {bot_info['result']['first_name']}")
    
    # Get updates with offset -1 to get latest
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {
        "offset": -1,
        "limit": 100,
        "timeout": 0
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    print(f"\n📊 Updates Response: {data.get('ok')}")
    print(f"   Number of updates: {len(data.get('result', []))}")
    
    # Try to clear webhook if set
    webhook_url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    webhook_response = requests.get(webhook_url)
    print(f"\n🔗 Webhook cleared: {webhook_response.json().get('result')}")
    
    # Get updates again
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get("ok") and data.get("result"):
        print(f"\n📨 Found {len(data['result'])} updates")
        for update in data['result'][-5:]:  # Show last 5
            if 'message' in update:
                msg = update['message']
                print(f"\nMessage from: {msg.get('from', {}).get('username', 'Unknown')}")
                print(f"Chat: {msg.get('chat', {}).get('title', 'Private')}")
                print(f"Chat ID: {msg.get('chat', {}).get('id')}")
                print(f"Text: {msg.get('text', 'No text')[:50]}...")

if __name__ == "__main__":
    get_all_telegram_info()