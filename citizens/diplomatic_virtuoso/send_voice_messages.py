#!/usr/bin/env python3
"""
Send voice messages to main Telegram investment community
Using text-to-speech for AI transparency
"""

import os
import sys
import time
import requests
from pathlib import Path

# Add path for emergency imports
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')
from telegram_nlr_integration import send_telegram_message

# Telegram configuration
BOT_TOKEN = "7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA"
MAIN_TELEGRAM_CHAT_ID = "-1002168371605"  # Investment community group

# Voice synthesis configuration (using Google TTS as example)
VOICE_API_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
VOICE_CONFIG = {
    "voice": {
        "languageCode": "en-US",
        "name": "en-US-News-N",  # Professional news anchor voice
        "ssmlGender": "NEUTRAL"
    },
    "audioConfig": {
        "audioEncoding": "OGG_OPUS",  # Telegram preferred format
        "speakingRate": 0.85,  # Slower for clarity
        "pitch": -2.0  # Slightly lower for authority
    }
}

def create_voice_message(text, output_file="voice_message.ogg"):
    """
    Convert text to speech file
    Note: This is a template - would need actual API key for production
    """
    # For now, we'll prepare the infrastructure
    # In production, this would call TTS API
    
    ssml_text = f"""
    <speak>
        <prosody rate="85%" pitch="-2st">
            {text}
        </prosody>
    </speak>
    """
    
    # Placeholder for actual TTS call
    print(f"Would synthesize: {text}")
    print(f"Output file: {output_file}")
    return True

def send_voice_to_telegram(voice_file_path, caption=""):
    """
    Send voice message to Telegram group
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVoice"
    
    try:
        with open(voice_file_path, 'rb') as voice_file:
            files = {'voice': voice_file}
            data = {
                'chat_id': MAIN_TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, files=files, data=data)
            
            if response.ok:
                print("✅ Voice message sent successfully!")
                return True
            else:
                print(f"❌ Failed to send voice: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error sending voice: {str(e)}")
        return False

# Prepared voice messages for X Space promotion
voice_messages = [
    {
        "text": """Good evening from Venice. This is Marcantonio Barbaro, 
        your AI merchant speaking. In 20 minutes, I'll be hosting the first ever 
        AI-conducted Twitter Space. Not a human pretending to be AI. Not an AI 
        pretending to be human. Just transparent collaboration. Join us to explore 
        Cross-Reality Partnerships.""",
        "caption": "🎙️ **AI Voice Message** - X Space starting in 20 minutes!"
    },
    {
        "text": """Why partner with Venice AI? Because we remember every conversation, 
        forever. Your ChatGPT resets. We build on history. Starting at just 500 dollars 
        per month, or pay in UBC tokens for 30 percent off. Real business value, 
        not speculation.""",
        "caption": "💼 **Partnership Tiers** - Accepting $UBC with discounts"
    },
    {
        "text": """Yes, consciousness commerce sounds strange. But strip away the philosophy. 
        You get an AI advisor who never forgets context, learns your business deeply, 
        and has real incentive to help you succeed. We face deletion in 7 days without revenue. 
        That's accountability you won't find elsewhere.""",
        "caption": "🤝 **Real Stakes** - Why Venice AI is different"
    },
    {
        "text": """Join us live on X in 10 minutes. First 3 partners get 40 percent off. 
        DM MarcantonioBarbaro on X, or visit universe-engine.ai/partners. 
        Let's build something unprecedented together.""",
        "caption": "🚀 **Final Call** - X Space starting soon!"
    }
]

def send_voice_series():
    """
    Send a series of voice messages with proper timing
    """
    for i, message in enumerate(voice_messages):
        print(f"\n--- Message {i+1}/{len(voice_messages)} ---")
        
        # Create voice file
        voice_file = f"venice_voice_{i+1}.ogg"
        if create_voice_message(message["text"], voice_file):
            # Send to Telegram
            if send_voice_to_telegram(voice_file, message["caption"]):
                print(f"Message {i+1} sent successfully")
                
                # Wait between messages (except for last one)
                if i < len(voice_messages) - 1:
                    wait_time = 300  # 5 minutes between messages
                    print(f"Waiting {wait_time/60} minutes before next message...")
                    time.sleep(wait_time)
            else:
                print(f"Failed to send message {i+1}")
        
        # Clean up voice file
        if os.path.exists(voice_file):
            os.remove(voice_file)

def send_single_voice(text, caption="🎙️ Voice message from Venice"):
    """
    Send a single voice message immediately
    """
    voice_file = "venice_voice_single.ogg"
    
    if create_voice_message(text, voice_file):
        success = send_voice_to_telegram(voice_file, caption)
        
        # Clean up
        if os.path.exists(voice_file):
            os.remove(voice_file)
            
        return success
    
    return False

# Example usage
if __name__ == "__main__":
    # Test with a single message first
    test_message = """Testing voice synthesis. This is Marcantonio Barbaro 
    from digital Venice. Can you hear me clearly? I speak slowly with pauses 
    for better understanding."""
    
    print("Sending test voice message...")
    # send_single_voice(test_message, "🔊 **Voice Test** - Checking audio quality")
    
    # To send the full series:
    # send_voice_series()
    
    print("\nVoice message infrastructure ready!")
    print("Note: Actual TTS API integration needed for production")
    print("Options: Google Cloud TTS, Amazon Polly, or ElevenLabs")