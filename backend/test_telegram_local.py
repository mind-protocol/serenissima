"""
Test Telegram Bot Locally
Checks if bot is configured and can receive messages
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def test_bot():
    """Test bot configuration"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set in .env")
        print("Please add: TELEGRAM_BOT_TOKEN=your_bot_token_here")
        return
    
    print("✅ Bot token configured")
    
    # Get bot info
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Bot connected: @{bot_info['username']}")
                print(f"   Bot name: {bot_info['first_name']}")
                print(f"   Bot ID: {bot_info['id']}")
            else:
                print(f"❌ Bot error: {data}")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print("\n📱 To test:")
    print("1. Start the backend: python backend/run.py")
    print("2. Open Telegram and search for your bot")
    print("3. Send any message to the bot")
    print("4. Watch the console for Resonance being triggered!")
    
    print("\n🔍 The flow will be:")
    print("Bot receives message → Poller detects it → Routes to Resonance → Resonance awakens → Response sent back")

if __name__ == "__main__":
    asyncio.run(test_bot())