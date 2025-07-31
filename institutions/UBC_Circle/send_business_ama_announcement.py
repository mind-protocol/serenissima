#!/usr/bin/env python3
"""Send Business AMA announcement to Venice Telegram"""

import os
import sys
import requests
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
TELEGRAM_CHAT_ID = '-1001699255893'  # Venice main channel from .env

def send_telegram_message(message: str) -> bool:
    """Send message to Telegram channel"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Clean up message for Telegram formatting
    message = message.replace('**', '*')  # Convert bold to Telegram format
    message = message.replace('###', '▶️')  # Replace headers with arrows
    message = message.replace('##', '📌')  # Replace subheaders
    message = message.replace('- [', '- \\[')  # Escape square brackets
    message = message.replace('] ', '\\] ')  # Escape square brackets
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Business AMA announcement sent successfully!")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def main():
    # Read the announcement
    announcement_path = Path(__file__).parent / "telegram_messages" / "business_ama_launch_message.md"
    
    with open(announcement_path, 'r') as f:
        # Skip the first line (title) as it's already in the message
        lines = f.readlines()
        message = ''.join(lines[1:])  # Skip first line which is duplicate title
    
    # Send to Telegram
    success = send_telegram_message(message)
    
    if success:
        print("\n🚀 Business AMA is LIVE!")
        print("📱 Check Venice Telegram for the announcement")
        print("⏰ 2-hour countdown has begun!")
    
    return success

if __name__ == "__main__":
    main()