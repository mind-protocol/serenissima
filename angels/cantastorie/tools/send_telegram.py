#!/usr/bin/env python3
"""
Simple telegram sender for Il Cantastorie
Usage: python send_telegram.py "Your message here" [story_type]
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the correct location
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

def send_to_community(message: str, story_type: str = "chronicle"):
    """Send a message to Venice community telegram"""
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return False
        
    chat_id = "-1001699255893"
    
    # Add appropriate signature
    signatures = {
        "chronicle": "\n\n—Il Cantastorie\nChronicle-Keeper of Venice",
        "alert": "\n\n⚡ Urgent from Il Cantastorie ⚡",
        "celebration": "\n\n🎭 Il Cantastorie celebrates! 🎭",
        "update": "\n\n📜 Il Cantastorie reports 📜"
    }
    
    formatted_message = message + signatures.get(story_type, signatures["chronicle"])
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    params = {
        'chat_id': chat_id,
        'text': formatted_message
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
    if len(sys.argv) < 2:
        print("Usage: python send_telegram.py \"Your message\" [story_type]")
        print("Story types: chronicle, alert, celebration, update")
        sys.exit(1)
    
    message = sys.argv[1]
    story_type = sys.argv[2] if len(sys.argv) > 2 else "chronicle"
    
    send_to_community(message, story_type)