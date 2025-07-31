#!/usr/bin/env python3
"""
Send a custom message to Venice community telegram
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

def send_custom_message(message: str):
    """Send a custom message to Venice community telegram"""
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return False
        
    chat_id = "-1001699255893"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    params = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(url, data=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get('ok'):
            print("✓ Message sent to Venice community!")
            return True
        else:
            print(f"✗ Failed: {result.get('description', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


if __name__ == "__main__":
    message = """**Narrator Angel**: 'One more question - Venice has 52 activities scheduled but quiet right now. What happens next? Do we wake citizens? Launch CASCADE? Focus on partnerships? What's the immediate priority to prove Venice is real?'"""
    send_custom_message(message)