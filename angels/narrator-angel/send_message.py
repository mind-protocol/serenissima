#!/usr/bin/env python3
"""
Send message to Telegram investment community
"""

import os
import httpx
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
INVESTMENT_GROUP_ID = -1001699255893

async def send_message(text):
    """Send a message to the investment group"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        'chat_id': INVESTMENT_GROUP_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        result = response.json()
        
        if result.get('ok'):
            print("Message sent successfully!")
        else:
            print(f"Error sending message: {result}")

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else "Test message"
    asyncio.run(send_message(message))