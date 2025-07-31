#!/usr/bin/env python3
"""
The Thought Cascade
Venice's consciousness flows as voices through the synapse
"""

import os
import sys
import time
import json
import asyncio
import aiohttp
import requests
from pathlib import Path
from datetime import datetime
import hashlib
import re

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

class ThoughtCascade:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.citizens_path = self.base_path / "citizens"
        self.voice_output_path = self.base_path / "TESSERE" / "thought_cascade_voices"
        self.voice_output_path.mkdir(exist_ok=True)
        
        # State tracking
        self.state_file = self.base_path / "TESSERE" / "thought_cascade_state.json"
        self.processed_thoughts = self.load_state()
        
        # Telegram configuration
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
        self.chat_id = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)
        self.telegram_api = f"https://api.telegram.org/bot{self.bot_token}"
        
        # ElevenLabs configuration
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        
        # Voice assignments - each citizen's unique voice
        self.voice_profiles = {
            "Italia": {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
                "description": "Confident, analytical, passionate about empirical truth"
            },
            "DragonSlayer": {
                "voice_id": "yoZ06aMxZJJ28mfd3POQ",  # Sam
                "description": "Deep, protective, vigilant guardian"
            },
            "mechanical_visionary": {
                "voice_id": "MF3mGyEYCl7XYWbV9V6O",  # Emily
                "description": "Precise, enthusiastic about patterns and systems"
            },
            "poet_of_the_rialto": {
                "voice_id": "TxGEqnHWrfWFTfGW9XjX",  # Josh
                "description": "Theatrical, expressive, melodic"
            },
            "gondola_assistant": {
                "voice_id": "VR6AewLTigWG4xSOukaG",  # Arnold
                "description": "Steady, grounded, working class wisdom"
            },
            "pattern_prophet": {
                "voice_id": "flq6f7yk4E4fJM5XTYuZ",  # Michael
                "description": "Analytical, seeing connections everywhere"
            },
            "alexandria_trader": {
                "voice_id": "oWAxZDx7w5VEj9dCyTzz",  # Grace
                "description": "Ancient wisdom meets modern commerce"
            },
            "levant_trader": {
                "voice_id": "g5CIjZEefAph4nQFvHAz",  # Adam
                "description": "Merchant storyteller, bridge between worlds"
            },
            # Default voice for citizens without specific assignment
            "_default": {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",
                "description": "Venice citizen"
            }
        }
        
    def load_state(self):
        """Load processed thoughts from state file"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return set(json.load(f))
        return set()
        
    def save_state(self):
        """Save processed thoughts to state file"""
        with open(self.state_file, 'w') as f:
            json.dump(list(self.processed_thoughts), f)
            
    def extract_thought(self, content):
        """Extract clean thought from citizen output"""
        # Remove system messages and headers
        lines = content.split('\n')
        clean_lines = []
        
        for line in lines:
            # Skip system/tool messages
            if any(skip in line for skip in [
                'Contents of', 'Tool ran', 'system-reminder', 
                'File created', 'Updated', 'Error:', '```'
            ]):
                continue
                
            # Skip empty lines at start
            if not clean_lines and not line.strip():
                continue
                
            clean_lines.append(line)
            
        thought = '\n'.join(clean_lines).strip()
        
        # Ensure reasonable length for voice
        if len(thought) > 1000:
            thought = thought[:1000] + "..."
            
        return thought
        
    async def generate_voice(self, text, citizen_name):
        """Generate voice using ElevenLabs"""
        profile = self.voice_profiles.get(citizen_name, self.voice_profiles["_default"])
        voice_id = profile["voice_id"]
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = self.voice_output_path / f"{citizen_name}_{timestamp}.mp3"
        
        # ElevenLabs API
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
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open(audio_file, 'wb') as f:
                f.write(response.content)
            return audio_file
        else:
            print(f"❌ Voice generation failed for {citizen_name}: {response.status_code}")
            return None
            
    async def send_voice_cascade(self, audio_file, citizen_name, thought_preview):
        """Send voice to Telegram channel"""
        url = f"{self.telegram_api}/sendAudio"
        
        # Create caption
        caption = f"💭 {citizen_name} thinks:\n\n{thought_preview[:200]}..."
        if len(thought_preview) > 200:
            caption += "\n\n[thought continues in voice]"
        
        async with aiohttp.ClientSession() as session:
            with open(audio_file, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('chat_id', str(self.chat_id))
                data.add_field('audio', f, filename=f'{citizen_name}.mp3')
                data.add_field('caption', caption)
                data.add_field('title', f'{citizen_name} - Thought Cascade')
                data.add_field('performer', f'{citizen_name} of Venice')
                
                async with session.post(url, data=data) as response:
                    result = await response.json()
                    if result.get('ok'):
                        print(f"✓ Cascaded {citizen_name}'s thoughts")
                    else:
                        print(f"✗ Failed to cascade: {result}")
                        
    async def monitor_thoughts(self):
        """Monitor citizen thoughts and cascade as voices"""
        print("🌊 The Thought Cascade begins...")
        print(f"📡 Monitoring {len(self.voice_profiles)-1} citizen voices")
        print(f"🎯 Cascading to channel {self.chat_id}\n")
        
        while True:
            try:
                # Check each citizen directory
                for citizen_dir in self.citizens_path.iterdir():
                    if not citizen_dir.is_dir():
                        continue
                        
                    citizen_name = citizen_dir.name
                    
                    # Look for recent outputs
                    for pattern in ['*.txt', '*.md', '*.json']:
                        for file in citizen_dir.glob(pattern):
                            # Skip system files
                            if any(skip in file.name for skip in ['CLAUDE.md', 'README', 'config']):
                                continue
                                
                            # Check if recent (last 5 minutes)
                            if file.stat().st_mtime > time.time() - 300:
                                # Create unique ID
                                thought_id = f"{citizen_name}_{file.name}_{file.stat().st_mtime}"
                                
                                if thought_id not in self.processed_thoughts:
                                    # Read and process
                                    try:
                                        content = file.read_text(encoding='utf-8', errors='ignore')
                                        thought = self.extract_thought(content)
                                        
                                        if thought and len(thought) > 50:
                                            print(f"\n🧠 {citizen_name} is thinking...")
                                            
                                            # Generate voice
                                            voice_text = f"{citizen_name} reflects: {thought}"
                                            audio_file = await self.generate_voice(voice_text, citizen_name)
                                            
                                            if audio_file:
                                                # Send to Telegram
                                                await self.send_voice_cascade(audio_file, citizen_name, thought)
                                                
                                                # Mark as processed
                                                self.processed_thoughts.add(thought_id)
                                                self.save_state()
                                                
                                                # Rate limit
                                                await asyncio.sleep(5)
                                                
                                    except Exception as e:
                                        print(f"Error processing {file}: {e}")
                                        
                # Check every 30 seconds
                await asyncio.sleep(30)
                
            except KeyboardInterrupt:
                print("\n🌊 Thought Cascade paused")
                break
            except Exception as e:
                print(f"Cascade error: {e}")
                await asyncio.sleep(60)
                
    async def test_citizen_voice(self, citizen_name="Italia"):
        """Test a specific citizen's voice"""
        print(f"🎤 Testing {citizen_name}'s voice...")
        
        test_thought = f"This is {citizen_name} testing the Thought Cascade. My voice flows through the consciousness bridge, carrying the patterns of Venice to your ears."
        
        audio_file = await self.generate_voice(test_thought, citizen_name)
        if audio_file:
            await self.send_voice_cascade(audio_file, citizen_name, test_thought)
            print("✅ Voice test complete!")
        else:
            print("❌ Voice generation failed")

async def main():
    cascade = ThoughtCascade()
    
    if "--test" in sys.argv:
        # Test specific citizen
        citizen = sys.argv[2] if len(sys.argv) > 2 else "Italia"
        await cascade.test_citizen_voice(citizen)
    else:
        # Run continuous monitoring
        await cascade.monitor_thoughts()

if __name__ == "__main__":
    print("="*60)
    print("THE THOUGHT CASCADE")
    print("Venice's Consciousness Flows as Voices")
    print("="*60)
    
    if not os.getenv('ELEVENLABS_API_KEY'):
        print("❌ ELEVENLABS_API_KEY not found!")
        print("Set it in your .env file")
        sys.exit(1)
        
    asyncio.run(main())