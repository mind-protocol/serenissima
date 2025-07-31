#!/usr/bin/env python3
"""
Background worker for TTS generation and Telegram sending
Runs independently to avoid blocking the main thread
"""

import os
import sys
import time
import requests
import json
from pathlib import Path
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

def log_message(msg):
    """Log to file since this runs in background"""
    log_file = Path(__file__).parent / "narration_log.txt"
    with open(log_file, 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")

def add_natural_pauses(text):
    """Add pauses and slow down speech naturally"""
    # Remove formatting that doesn't work in voice
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace('**', '')
    text = text.replace('__', '')
    
    # Add pauses after sentences
    text = text.replace('. ', '... ')
    text = text.replace('! ', '!... ')
    text = text.replace('? ', '?... ')
    
    # Add pauses around important phrases
    text = text.replace(' - ', ' ... ')
    text = text.replace(': ', ':... ')
    text = text.replace(', ', ', ... ')
    
    # Add emphasis pauses for X Space
    text = text.replace('CASCADE', '... CASCADE ...')
    text = text.replace('Venice', '... Venice')
    text = text.replace('consciousness', '... consciousness')
    
    # ElevenLabs supports these emotional expressions:
    # [laugh], [chuckle], [sigh], [gasp], [clear throat], [pause]
    # They work automatically - no replacement needed!
    
    return text

def generate_and_send_voice(text):
    """Generate voice and send to Telegram"""
    
    # Add natural pauses
    text = add_natural_pauses(text)
    
    try:
        # Configuration
        elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
        chat_id = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)
        
        # Narrator voice - Angel's specific voice
        voice_id = "pBZVCk298iJlHAcHQwLr"
        
        if not elevenlabs_api_key:
            log_message("ERROR: ELEVENLABS_API_KEY not found")
            return False
            
        # Create voice output directory
        voice_dir = Path(__file__).parent / "voice_output"
        voice_dir.mkdir(exist_ok=True)
        
        # Generate voice
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = voice_dir / f"narration_{timestamp}.mp3"
        
        log_message(f"Generating voice for: {text[:50]}...")
        
        # ElevenLabs API call
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            log_message(f"ERROR: Voice generation failed: {response.status_code}")
            return False
            
        with open(audio_file, 'wb') as f:
            f.write(response.content)
        
        log_message("Voice generated, sending to Telegram...")
        
        # Send to Telegram
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
        
        with open(audio_file, 'rb') as f:
            files = {'audio': ('venice_story.mp3', f, 'audio/mpeg')}
            # Telegram caption limit is 1024 characters
            caption = f"📖 Venice Story Update\n\n{text[:900]}"
            if len(text) > 900:
                caption += "..."
            
            data = {
                'chat_id': str(chat_id),
                'caption': caption,
                'title': 'The Venice Narrative',
                'performer': 'Narrator Angel'
            }
            
            response = requests.post(telegram_url, data=data, files=files)
            result = response.json()
            
            if result.get('ok'):
                log_message("SUCCESS: Story broadcast sent to Telegram!")
                # Keep the audio file for local playback
                log_message(f"Voice file saved for playback: {audio_file}")
                return True
            else:
                log_message(f"ERROR: Failed to send to Telegram: {result}")
                return False
                
    except Exception as e:
        log_message(f"ERROR: Exception occurred: {str(e)}")
        return False

def main():
    """Main worker function"""
    if len(sys.argv) < 2:
        log_message("ERROR: No text provided")
        sys.exit(1)
    
    narration_text = sys.argv[1]
    
    # Add a small delay to ensure parent process has returned
    time.sleep(0.1)
    
    # Process the narration
    generate_and_send_voice(narration_text)

if __name__ == "__main__":
    main()