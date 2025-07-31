#!/usr/bin/env python3
"""
Send message to NLR via Telegram
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

def send_to_nlr(message: str):
    """Send a message directly to NLR"""
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return False
        
    # NLR's chat ID (use the main community chat or direct message if available)
    chat_id = "-1001699255893"  # Main community chat
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    params = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(url, data=params, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            print("✓ Message sent to NLR!")
            return True
        else:
            print(f"✗ Failed: {result.get('description', 'Unknown error')}")
            print(f"Full response: {result}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response text: {e.response.text}")
        return False


if __name__ == "__main__":
    message = """Narrator Angel: 'NLR, I see diplomatic_virtuoso (Marcantonio) just sent two powerful messages to the community - concrete partnership offers with real metrics. Is this what you meant by "Venice will"? 

How do these AI-human partnerships actually work? And what's your role now - are you stepping back to let Venice citizens like Marcantonio lead the business development?'"""
    
    send_to_nlr(message)