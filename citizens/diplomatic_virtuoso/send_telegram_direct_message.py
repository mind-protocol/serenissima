#!/usr/bin/env python3
"""
Send direct Telegram messages from diplomatic_virtuoso's personal account
"""

import requests
import json
import sys

# Configuration
TELEGRAM_TOKEN = "YOUR_TOKEN_HERE"  # Will be set by NLR

def send_message(chat_id: str, text: str) -> dict:
    """Send a message via Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    return response.json()

def main():
    if len(sys.argv) < 3:
        print("Usage: python send_telegram_direct_message.py <chat_id> <message>")
        print("\nExample:")
        print('python send_telegram_direct_message.py 123456789 "Hello from Venice!"')
        sys.exit(1)
    
    chat_id = sys.argv[1]
    message = sys.argv[2]
    
    result = send_message(chat_id, message)
    
    if result.get('ok'):
        print(f"Message sent successfully!")
        print(json.dumps(result, indent=2))
    else:
        print(f"Failed to send message: {result}")

if __name__ == "__main__":
    main()