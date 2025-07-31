#!/usr/bin/env python3
"""
Send narration to Telegram investment community
"""

import os
import sys
import json
import asyncio
import httpx
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
INVESTMENT_GROUP_ID = -1001699255893  # Investment community group

async def send_text_message(text: str):
    """Send a text message to the investment group"""
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not configured")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Split long messages if needed
    messages = []
    if len(text) > 4000:
        # Simple split at 4000 chars
        for i in range(0, len(text), 4000):
            messages.append(text[i:i+4000])
    else:
        messages = [text]
    
    for message in messages:
        data = {
            'chat_id': INVESTMENT_GROUP_ID,
            'text': message
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                result = response.json()
                
                if not result.get('ok'):
                    print(f"Telegram API error: {result}")
                    return False
                else:
                    print(f"Message sent successfully")
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
        
        # Small delay between chunks
        if len(messages) > 1:
            await asyncio.sleep(0.5)
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python send_narration.py 'Your message here'")
        sys.exit(1)
    
    message = sys.argv[1]
    
    # For now, send as text message
    # TODO: Add ElevenLabs voice generation later
    success = asyncio.run(send_text_message(message))
    
    if success:
        print("Narration sent successfully")
    else:
        print("Failed to send narration")
        sys.exit(1)

if __name__ == "__main__":
    main()