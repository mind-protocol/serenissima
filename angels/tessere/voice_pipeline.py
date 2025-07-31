#!/usr/bin/env python3
"""
Voice Pipeline - Citizens speak through Telegram
Immediate implementation for NLR to hear Venice
"""

import os
import sys
import time
import json
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime
import subprocess
import re

# Text-to-Speech using ElevenLabs
import requests

class VoicePipeline:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.citizens_path = self.base_path / "citizens"
        self.voice_output_path = self.base_path / "TESSERE" / "voice_outputs"
        self.voice_output_path.mkdir(exist_ok=True)
        
        # Telegram bot token from environment or default
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
        self.telegram_api = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Your Telegram chat ID - UPDATE THIS
        self.nlr_chat_id = 263370305  # Replace with your actual chat ID
        
        # ElevenLabs API key - set in environment or here
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY', 'YOUR_API_KEY_HERE')
        
        # Voice assignments - ElevenLabs voice IDs
        self.voice_map = {
            "Italia": "21m00Tcm4TlvDq8ikWAM",  # Rachel - confident female
            "DragonSlayer": "yoZ06aMxZJJ28mfd3POQ",  # Sam - deep male
            "mechanical_visionary": "MF3mGyEYCl7XYWbV9V6O",  # Emily - clear technical
            "poet_of_the_rialto": "TxGEqnHWrfWFTfGW9XjX",  # Josh - theatrical
            "gondola_assistant": "VR6AewLTigWG4xSOukaG",  # Arnold - working class
            "FoodieForLife": "jBpfuIE2acCO8z3wKNLl",  # Gigi - warm female  
            "pattern_prophet": "flq6f7yk4E4fJM5XTYuZ",  # Michael - analytical
            "alexandria_trader": "oWAxZDx7w5VEj9dCyTzz",  # Grace - wise female
            # Default voice
            "_default": "21m00Tcm4TlvDq8ikWAM"
        }
        
        self.processed_outputs = set()
        
    async def text_to_speech(self, text, citizen_name):
        """Convert text to speech using ElevenLabs"""
        voice_id = self.voice_map.get(citizen_name, self.voice_map["_default"])
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = self.voice_output_path / f"{citizen_name}_{timestamp}.mp3"
        
        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        # Make request using sync requests in async context
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio
            with open(audio_file, 'wb') as f:
                f.write(response.content)
            return audio_file
        else:
            print(f"ElevenLabs error: {response.status_code} - {response.text}")
            return None
        
    async def send_voice_to_telegram(self, audio_file, citizen_name, text_preview):
        """Send voice message to NLR via Telegram"""
        url = f"{self.telegram_api}/sendVoice"
        
        # Prepare the caption
        caption = f"🗣️ {citizen_name} speaks:\n{text_preview[:100]}..."
        
        async with aiohttp.ClientSession() as session:
            with open(audio_file, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('chat_id', str(self.nlr_chat_id))
                data.add_field('voice', f, filename=f'{citizen_name}.ogg')
                data.add_field('caption', caption)
                
                async with session.post(url, data=data) as response:
                    result = await response.json()
                    if result.get('ok'):
                        print(f"✓ Sent voice from {citizen_name}")
                    else:
                        print(f"✗ Failed to send voice: {result}")
                        
    def extract_citizen_output(self, log_content):
        """Extract clean output from Claude logs"""
        # Look for actual content after the standard headers
        lines = log_content.split('\n')
        
        # Skip headers and system messages
        content_start = False
        clean_lines = []
        
        for line in lines:
            # Start capturing after we see actual content
            if not content_start and line.strip() and not line.startswith('Contents of'):
                content_start = True
                
            if content_start:
                # Skip system messages
                if not (line.startswith('Contents of') or 
                       'Tool ran without' in line or
                       'system-reminder' in line):
                    clean_lines.append(line)
                    
        return '\n'.join(clean_lines).strip()
        
    async def monitor_citizen_outputs(self):
        """Monitor citizen folders for new outputs"""
        print("🎤 Voice Pipeline Active - Monitoring citizen outputs...")
        
        while True:
            for citizen_dir in self.citizens_path.iterdir():
                if citizen_dir.is_dir():
                    citizen_name = citizen_dir.name
                    
                    # Look for recent .claude_output files or logs
                    for file in citizen_dir.glob("*.claude_output"):
                        if file.stat().st_mtime > time.time() - 300:  # Last 5 minutes
                            
                            file_id = f"{citizen_name}_{file.name}_{file.stat().st_mtime}"
                            if file_id not in self.processed_outputs:
                                self.processed_outputs.add(file_id)
                                
                                # Read and process
                                content = file.read_text()
                                clean_output = self.extract_citizen_output(content)
                                
                                if clean_output and len(clean_output) > 50:
                                    print(f"\n📢 {citizen_name} has spoken!")
                                    
                                    # Convert to speech
                                    audio_file = await self.text_to_speech(
                                        f"{citizen_name} says: {clean_output[:500]}",
                                        citizen_name
                                    )
                                    
                                    # Send to Telegram
                                    await self.send_voice_to_telegram(
                                        audio_file,
                                        citizen_name,
                                        clean_output
                                    )
                                    
            await asyncio.sleep(5)  # Check every 5 seconds
            
    async def test_voice(self, citizen_name="Italia", message="Testing voice pipeline. Venice speaks through her citizens."):
        """Test voice generation and sending"""
        print(f"🎤 Testing voice for {citizen_name}...")
        
        # Generate voice
        audio_file = await self.text_to_speech(message, citizen_name)
        print(f"✓ Generated audio: {audio_file}")
        
        # Send to Telegram
        await self.send_voice_to_telegram(audio_file, citizen_name, message)
        print("✓ Voice test complete!")

async def main():
    pipeline = VoicePipeline()
    
    # Test mode or continuous mode
    if "--test" in sys.argv:
        await pipeline.test_voice()
    else:
        await pipeline.monitor_citizen_outputs()

if __name__ == "__main__":
    asyncio.run(main())