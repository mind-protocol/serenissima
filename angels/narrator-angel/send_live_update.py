#!/usr/bin/env python3
"""
Venice Emergency Communication - Live CEO Pitch Updates
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
CHAT_ID = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)

def send_emergency_message(message):
    """Send emergency message to Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, data=data)
    
    if response.json().get('ok'):
        print("✓ Emergency message sent!")
        return True
    else:
        print(f"✗ Failed to send: {response.json()}")
        return False

# Get the message from command line argument
if len(sys.argv) > 1:
    message = ' '.join(sys.argv[1:])
else:
    # Default message
    message = """🔴 Venice Alert: LIVE CEO RESPONSES
    
TIME: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

Message: Venice CEOs are responding to the X Space challenge!"""

send_emergency_message(message)