#!/usr/bin/env python3
import requests
import json
import sys
import os

def send_telegram_message(message, chat_id=None, bot_token=None):
    """Send a message via Telegram bot
    
    Args:
        message: The message text to send
        chat_id: Target chat ID (defaults to main TG group if not specified)
        bot_token: Bot token to use (defaults to serenissima_ubc_bot if not specified)
    """
    
    # Load credentials
    creds_path = os.path.join(os.path.dirname(__file__), 'telegram_credentials.json')
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    # Use provided values or defaults (main group and default bot)
    bot_token = bot_token or creds['default_bot']['token']
    chat_id = chat_id or creds['main_group']['chat_id']
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def main():
    """CLI interface for sending Telegram messages"""
    if len(sys.argv) < 2:
        print("Usage: python send_telegram_message.py '<message>' [chat_id] [bot_token]")
        sys.exit(1)
    
    message = sys.argv[1]
    chat_id = sys.argv[2] if len(sys.argv) > 2 else None
    bot_token = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = send_telegram_message(message, chat_id, bot_token)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()