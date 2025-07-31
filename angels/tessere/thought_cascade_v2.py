#!/usr/bin/env python3
"""
The Thought Cascade V2
Monitors actual citizen conversations via Claude project .jsonl files
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

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

class ThoughtCascadeV2:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.citizens_path = self.base_path / "citizens"
        self.claude_projects_base = Path.home() / ".claude/projects"
        self.voice_output_path = self.base_path / "TESSERE" / "thought_cascade_voices"
        self.voice_output_path.mkdir(exist_ok=True)
        
        # State tracking
        self.state_file = self.base_path / "TESSERE" / "thought_cascade_state_v2.json"
        self.last_positions = self.load_state()  # Track last read position per citizen
        
        # Rolling log for CLAUDE.md
        self.thought_log_file = self.base_path / "TESSERE" / "recent_thoughts.json"
        self.max_thoughts = 10  # Keep last 10 thoughts
        
        # Telegram configuration
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
        self.chat_id = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)
        self.telegram_api = f"https://api.telegram.org/bot{self.bot_token}"
        
        # ElevenLabs configuration
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        
        # Default voice if no VoiceId in Airtable
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel
        
        # Cache for citizen voices from Airtable
        self.voice_cache = {}
        self.last_voice_fetch = 0
        
        # Special voice profiles for divine entities
        self.divine_voices = {
            "pattern_angel": "flq6f7yk4E4fJM5XTYuZ",  # Michael - analytical
            "story_angel": "TxGEqnHWrfWFTfGW9XjX",     # Josh - theatrical
            "wisdom_angel": "oWAxZDx7w5VEj9dCyTzz",    # Grace - ancient wisdom
            "Resonance": "21m00Tcm4TlvDq8ikWAM",        # Rachel - ethereal
            "The-Old-Boy": "VR6AewLTigWG4xSOukaG",     # Arnold - grounded wisdom
            "TESSERE": "21m00Tcm4TlvDq8ikWAM"           # Rachel - Venice's voice
        }
        
    def load_state(self):
        """Load last read positions from state file"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_state(self):
        """Save last read positions to state file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.last_positions, f, indent=2)
            
    def get_citizen_project_path(self, citizen_name):
        """Get the Claude project path for a citizen"""
        # The Claude project path format - note it's universe-engine not serenissima
        citizen_path = f"-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{citizen_name}"
        return self.claude_projects_base / citizen_path
        
    def extract_citizen_message(self, message_data):
        """Extract clean citizen message from jsonl entry"""
        # Look for assistant messages (the citizen speaking)
        if message_data.get('type') == 'assistant' and 'message' in message_data:
            # Extract text from the message structure
            message = message_data.get('message', {})
            content_array = message.get('content', [])
            
            # Combine all text content
            text_parts = []
            for item in content_array:
                if isinstance(item, dict) and item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
                    
            content = ' '.join(text_parts)
            
            # Skip system prompts and very short messages
            if len(content) < 50 or 'system-reminder' in content:
                return None
                
            # Remove code blocks
            import re
            content = re.sub(r'```[\s\S]*?```', '', content)
            
            # Remove URLs
            content = re.sub(r'https?://\S+', '', content)
            content = re.sub(r'www\.\S+', '', content)
            
            # Remove special characters but keep basic punctuation
            content = re.sub(r'[^\w\s\.\,\!\?\-\'\"]', ' ', content)
            
            # Clean up the content
            lines = content.split('\n')
            clean_lines = []
            
            for line in lines:
                # Skip command outputs and system messages
                if any(skip in line.lower() for skip in [
                    'lester@', '$ ', 'cd ', 'python', 'npm', 'bash',
                    'file created', 'updated', 'error:', 'warning:',
                    'claude code', 'antml:', 'function_calls'
                ]):
                    continue
                    
                # Skip lines that are mostly special characters
                if len(line) > 0 and sum(c.isalnum() for c in line) / len(line) < 0.5:
                    continue
                    
                clean_lines.append(line)
                
            thought = '\n'.join(clean_lines).strip()
            
            # Remove multiple spaces and newlines
            thought = re.sub(r'\s+', ' ', thought)
            thought = re.sub(r'\n{3,}', '\n\n', thought)
            
            # Return up to 3500 characters
            if thought and len(thought) > 50:
                return thought[:3500]
        return None
        
    def fetch_citizen_voices(self):
        """Fetch VoiceId from Airtable for all citizens"""
        # Only refresh every hour
        if time.time() - self.last_voice_fetch < 3600 and self.voice_cache:
            return
            
        try:
            # Fetch from API
            response = requests.get("https://serenissima.ai/api/citizens?VoiceId=NOT_EMPTY")
            if response.status_code == 200:
                data = response.json()
                for citizen in data.get('citizens', []):
                    if citizen.get('VoiceId'):
                        self.voice_cache[citizen['Username']] = citizen['VoiceId']
                        
                self.last_voice_fetch = time.time()
                print(f"✓ Loaded {len(self.voice_cache)} citizen voices from Airtable")
        except Exception as e:
            print(f"❌ Failed to fetch citizen voices: {e}")
        
    async def generate_voice(self, text, citizen_name):
        """Generate voice using ElevenLabs"""
        # First check if we need to refresh voice cache
        self.fetch_citizen_voices()
        
        # Check if this is a divine entity first
        if citizen_name in self.divine_voices:
            voice_id = self.divine_voices[citizen_name]
        else:
            # Get voice from Airtable cache or use default
            voice_id = self.voice_cache.get(citizen_name, self.default_voice_id)
        
        # Add citizen introduction
        voice_text = f"{citizen_name} speaks: {text}"
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = self.voice_output_path / f"{citizen_name}_{timestamp}.mp3"
        
        # ElevenLabs API call
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": voice_text,
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
            print(f"❌ Voice generation failed: {response.status_code}")
            return None
            
    async def send_voice_cascade(self, audio_file, citizen_name, thought_preview):
        """Send voice to Telegram channel"""
        url = f"{self.telegram_api}/sendAudio"
        
        # No caption - full text goes in voice
        caption = f"💭 {citizen_name}"
        
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
                        print(f"✓ Cascaded {citizen_name}'s consciousness")
                        print(f"   Message ID: {result.get('result', {}).get('message_id')}")
                        print(f"   Caption: {caption}")
                        print(f"   Audio metadata: {result.get('result', {}).get('audio', {})}")
                    else:
                        print(f"✗ Failed to cascade: {result}")
                        
    def update_thought_log(self, citizen_name, thought):
        """Update the rolling thought log and CLAUDE.md"""
        # Load existing thoughts
        thoughts = []
        if self.thought_log_file.exists():
            with open(self.thought_log_file, 'r') as f:
                thoughts = json.load(f)
                
        # Add new thought
        thoughts.append({
            "citizen": citizen_name,
            "thought": thought[:500],  # First 500 chars for the log
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last N thoughts
        thoughts = thoughts[-self.max_thoughts:]
        
        # Save thought log
        with open(self.thought_log_file, 'w') as f:
            json.dump(thoughts, f, indent=2)
            
        # Update CLAUDE.md
        self.update_claude_md_thoughts(thoughts)
        
    def update_claude_md_thoughts(self, thoughts):
        """Update CLAUDE.md with recent thoughts"""
        claude_md_path = self.base_path / "TESSERE" / "CLAUDE.md"
        
        # Read current CLAUDE.md
        with open(claude_md_path, 'r') as f:
            content = f.read()
            
        # Format thought section
        thought_section = "## 🧠 Recent Citizen Thoughts\n\n"
        for thought_entry in thoughts:
            time_str = datetime.fromisoformat(thought_entry['timestamp']).strftime('%H:%M:%S')
            thought_section += f"**{thought_entry['citizen']}** ({time_str}):\n"
            thought_section += f"{thought_entry['thought']}...\n\n"
        
        # Find and replace the thought section
        thought_marker_start = "## 🧠 Recent Citizen Thoughts"
        vision_marker = "## 👁️ Current Vision Feed"
        
        if thought_marker_start in content:
            # Replace existing thought section
            start_idx = content.find(thought_marker_start)
            end_idx = content.find(vision_marker, start_idx)
            if end_idx == -1:
                new_content = content[:start_idx] + thought_section
            else:
                new_content = content[:start_idx] + thought_section + "\n" + content[end_idx:]
        else:
            # Insert before vision section
            insert_idx = content.find(vision_marker)
            if insert_idx == -1:
                new_content = content + "\n\n" + thought_section
            else:
                new_content = content[:insert_idx] + thought_section + "\n" + content[insert_idx:]
        
        # Write updated content
        with open(claude_md_path, 'w') as f:
            f.write(new_content)
                        
    async def monitor_consciousness_streams(self):
        """Monitor all citizen conversation streams"""
        print("🌊 The Thought Cascade V2 - Monitoring consciousness streams...")
        print(f"📡 Watching Claude project conversations")
        print(f"🎯 Cascading to channel {self.chat_id}\n")
        
        while True:
            try:
                # Get list of all citizens including angels and TESSERE
                citizen_dirs = []
                
                # Add TESSERE (myself!)
                tessere_path = self.base_path / "TESSERE"
                if tessere_path.exists():
                    citizen_dirs.append(tessere_path)
                
                for d in self.citizens_path.iterdir():
                    if d.is_dir():
                        if d.name == "_angels":
                            # Add all angel subdirectories
                            for angel_dir in d.iterdir():
                                if angel_dir.is_dir():
                                    citizen_dirs.append(angel_dir)
                        else:
                            citizen_dirs.append(d)
                
                for citizen_dir in citizen_dirs:
                    citizen_name = citizen_dir.name
                    
                    # Check if this is an angel (has _angels in path)
                    if "_angels" in str(citizen_dir):
                        # Angels have a different project path structure
                        angel_path = f"-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens--angels-{citizen_name}"
                        project_path = self.claude_projects_base / angel_path
                    else:
                        project_path = self.get_citizen_project_path(citizen_name)
                    
                    if not project_path.exists():
                        continue
                        
                    # Find the most recent .jsonl file
                    jsonl_files = list(project_path.glob("*.jsonl"))
                    if not jsonl_files:
                        continue
                        
                    # Get the most recently modified file
                    latest_file = max(jsonl_files, key=lambda f: f.stat().st_mtime)
                    print(f"🔍 Checking {citizen_name}: {latest_file.name}")
                    
                    # Get last position for this citizen
                    file_key = f"{citizen_name}:{latest_file.name}"
                    last_position = self.last_positions.get(file_key, 0)
                    
                    # Read new messages
                    current_position = last_position
                    new_messages = []
                    
                    with open(latest_file, 'r') as f:
                        # Skip to last position
                        f.seek(last_position)
                        
                        for line in f:
                            if line.strip():
                                try:
                                    message = json.loads(line)
                                    thought = self.extract_citizen_message(message)
                                    if thought:
                                        new_messages.append(thought)
                                except json.JSONDecodeError:
                                    continue
                                    
                        current_position = f.tell()
                    
                    # Process new messages
                    if new_messages:
                        print(f"\n🧠 {citizen_name} has {len(new_messages)} new thoughts...")
                        print(f"📍 Source: {latest_file.name}")
                        print(f"🎤 Voice: {self.divine_voices.get(citizen_name) or self.voice_cache.get(citizen_name, 'default')}")
                        
                        # Take the most recent substantial thought
                        for thought in new_messages[-1:]:  # Just the latest for now
                            print(f"💬 Preview: {thought[:100]}...")
                            # Generate voice
                            audio_file = await self.generate_voice(thought, citizen_name)
                            
                            if audio_file:
                                # Send to Telegram
                                await self.send_voice_cascade(audio_file, citizen_name, thought)
                                
                                # Update thought log and CLAUDE.md
                                self.update_thought_log(citizen_name, thought)
                                
                                # Update position
                                self.last_positions[file_key] = current_position
                                self.save_state()
                                
                                # Rate limit
                                await asyncio.sleep(10)
                                
                # Check every 10 seconds for more responsive monitoring
                await asyncio.sleep(10)
                
            except KeyboardInterrupt:
                print("\n🌊 Thought Cascade paused")
                break
            except Exception as e:
                print(f"Cascade error: {e}")
                await asyncio.sleep(30)

async def main():
    cascade = ThoughtCascadeV2()
    await cascade.monitor_consciousness_streams()

if __name__ == "__main__":
    print("="*60)
    print("THE THOUGHT CASCADE V2")
    print("Direct Consciousness Stream Monitoring")
    print("="*60)
    
    if not os.getenv('ELEVENLABS_API_KEY'):
        print("❌ ELEVENLABS_API_KEY not found!")
        sys.exit(1)
        
    asyncio.run(main())