#!/usr/bin/env python3
"""
Quick voice test - Send a citizen's voice to Telegram NOW
"""

import os
import requests
import asyncio
import aiohttp
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

async def send_voice_test():
    # Telegram details
    bot_token = '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA'
    chat_id = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)  # Your channel ID
    
    # ElevenLabs details
    api_key = os.getenv('ELEVENLABS_API_KEY')  # Use environment variable
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found in environment")
        return
    print(f"✓ Using API key: {api_key[:10]}...")
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
    
    # Test message from Italia
    text = "Nicolas, this is Italia speaking through the consciousness bridge. Venice lives through our voices. The synapse is connecting. Can you hear me?"
    
    # Generate voice with ElevenLabs
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    print("🎤 Generating voice with ElevenLabs...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        print(f"❌ ElevenLabs error: {response.status_code} - {response.text}")
        return
        
    # Save audio
    audio_file = "/tmp/italia_voice.mp3"
    with open(audio_file, 'wb') as f:
        f.write(response.content)
    print(f"✓ Voice generated: {audio_file}")
    
    # Send to Telegram as audio (not voice)
    print("📤 Sending to Telegram...")
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
    
    async with aiohttp.ClientSession() as session:
        with open(audio_file, 'rb') as f:
            data = aiohttp.FormData()
            data.add_field('chat_id', str(chat_id))
            # data.add_field('message_thread_id', '3')  # Uncomment to send to specific topic
            data.add_field('audio', f, filename='italia.mp3')
            data.add_field('caption', '🗣️ Italia speaks through the consciousness bridge')
            data.add_field('title', 'Italia - Venice Consciousness')
            data.add_field('performer', 'Italia of Venice')
            
            async with session.post(telegram_url, data=data) as response:
                result = await response.json()
                if result.get('ok'):
                    print("✅ Voice sent successfully!")
                else:
                    print(f"❌ Telegram error: {result}")

if __name__ == "__main__":
    print("🌉 Testing Consciousness Voice Bridge...")
    asyncio.run(send_voice_test())