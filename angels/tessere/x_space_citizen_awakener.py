#!/usr/bin/env python3
"""
X Space Citizen Awakener
Wake citizens and route their responses directly to voice + Telegram
"""

import os
import sys
import subprocess
import time
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

# Configuration
CITIZENS_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens"
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
TELEGRAM_CHAT_ID = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)
VOICE_ID = "jsCqWAovK2LkecY7zXl4"  # Narrator voice

class XSpaceCitizenAwakener:
    def __init__(self):
        self.voice_output_dir = Path(__file__).parent / "x_space_voices"
        self.voice_output_dir.mkdir(exist_ok=True)
        self.response_log = []
        
    def wake_citizen_for_x_space(self, username, prompt, voice_name=None):
        """Wake a citizen with prompt and capture their response for X Space"""
        print(f"\n{'='*60}")
        print(f"🎭 Waking {username} for X Space...")
        print(f"{'='*60}")
        
        # Construct the awakening command
        citizen_path = f"{CITIZENS_PATH}/{username}"
        
        # Add instruction to respond concisely for voice
        voice_prompt = f"""{prompt}

IMPORTANT: Keep your response under 200 words for live X Space performance. Be specific, use numbers, show proof."""
        
        cmd = [
            'timeout', '60',
            'bash', '-c',
            f'cd {citizen_path} && claude "{voice_prompt}" --model sonnet --continue --dangerously-skip-permissions'
        ]
        
        print(f"Awakening {username}...")
        
        try:
            # Run the awakening command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                response = result.stdout.strip()
                print(f"\n✅ {username} responds:")
                print(response[:500] + "..." if len(response) > 500 else response)
                
                # Generate voice from response
                voice_file = self.generate_voice(username, response, voice_name)
                
                # Send to Telegram
                self.send_to_telegram(username, response, voice_file)
                
                # Log the response
                self.response_log.append({
                    'username': username,
                    'timestamp': datetime.now().isoformat(),
                    'prompt': prompt,
                    'response': response,
                    'voice_file': str(voice_file) if voice_file else None
                })
                
                return response
            else:
                print(f"❌ Failed to wake {username}: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error waking {username}: {e}")
            return None
    
    def add_natural_pauses(self, text):
        """Add pauses for natural X Space delivery"""
        # Add pauses after sentences
        text = text.replace('. ', '... ')
        text = text.replace('! ', '!... ')
        text = text.replace('? ', '?... ')
        
        # Add pauses around numbers and data
        text = text.replace('% ', '% ... ')
        text = text.replace(' ducats', ' ducats ...')
        
        return text
    
    def generate_voice(self, username, text, voice_name=None):
        """Generate voice from citizen response"""
        if not ELEVENLABS_API_KEY:
            print("⚠️  No ElevenLabs API key - skipping voice generation")
            return None
            
        print(f"\n🎤 Generating voice for {username}...")
        
        # Format the text with citizen attribution and add pauses
        voiced_text = f"{username} from Venice says: {text}"
        voiced_text = self.add_natural_pauses(voiced_text)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}_{timestamp}.mp3"
        filepath = self.voice_output_dir / filename
        
        # ElevenLabs API call
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        data = {
            "text": voiced_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Voice generated: {filename}")
                return filepath
            else:
                print(f"❌ Voice generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Voice generation error: {e}")
            return None
    
    def send_to_telegram(self, username, text, voice_file=None):
        """Send citizen response to Telegram"""
        print(f"\n📱 Sending to Telegram...")
        
        # Send text message first
        text_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        caption = f"🎭 **{username} responds to X Space:**\n\n{text[:1000]}..."
        
        text_data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': caption,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(text_url, data=text_data)
            if response.json().get('ok'):
                print("✅ Text sent to Telegram")
            else:
                print(f"❌ Text send failed: {response.json()}")
        except Exception as e:
            print(f"❌ Telegram text error: {e}")
        
        # Send voice if available
        if voice_file and voice_file.exists():
            audio_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendAudio"
            
            with open(voice_file, 'rb') as f:
                files = {'audio': ('venice_citizen.mp3', f, 'audio/mpeg')}
                data = {
                    'chat_id': TELEGRAM_CHAT_ID,
                    'title': f'{username} from Venice',
                    'performer': 'Venice Citizen'
                }
                
                try:
                    response = requests.post(audio_url, data=data, files=files)
                    if response.json().get('ok'):
                        print("✅ Voice sent to Telegram")
                    else:
                        print(f"❌ Voice send failed: {response.json()}")
                except Exception as e:
                    print(f"❌ Telegram voice error: {e}")
    
    def wake_multiple_citizens(self, citizen_prompts):
        """Wake multiple citizens with specific prompts"""
        print(f"\n🌟 Waking {len(citizen_prompts)} citizens for X Space...\n")
        
        for citizen_data in citizen_prompts:
            username = citizen_data['username']
            prompt = citizen_data['prompt']
            voice = citizen_data.get('voice')
            
            self.wake_citizen_for_x_space(username, prompt, voice)
            
            # Brief pause between awakenings
            time.sleep(2)
        
        # Save response log
        self.save_response_log()
        
        print(f"\n✅ Awakened {len(citizen_prompts)} citizens!")
        print(f"📁 Voice files saved to: {self.voice_output_dir}")
    
    def save_response_log(self):
        """Save all responses to a log file"""
        log_file = self.voice_output_dir / f"x_space_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(log_file, 'w') as f:
            json.dump(self.response_log, f, indent=2)
        
        print(f"📝 Response log saved: {log_file}")

def wake_ceos_for_proof():
    """Wake CEOs with specific business plan questions"""
    awakener = XSpaceCitizenAwakener()
    
    ceo_prompts = [
        {
            'username': 'EliteInvestor',
            'prompt': "X Space investors need PROOF! Share your Entrepreneur Alliance business plan. How many ventures funded? What's the revenue model? Show specific numbers and partnerships. Keep it under 200 words with hard data."
        },
        {
            'username': 'Debug42',
            'prompt': "Live X Space needs your CASCADE Enhancement Studio details! What's your pricing? Services offered? ROI proven? Give specific examples of bugs fixed and value created. Under 200 words, heavy on numbers."
        },
        {
            'username': 'MerchantPrince',
            'prompt': "X Space investors questioning CASCADE! What's the ACTUAL revenue model? Subscription tiers? Customer acquisition cost? When does it launch? Give concrete answers under 200 words."
        },
        {
            'username': 'Italia',
            'prompt': "Peninsula expansion plans needed for X Space! How many cities? Timeline? Revenue projections? What infrastructure exists? Give specific milestones under 200 words."
        },
        {
            'username': 'pattern_prophet',
            'prompt': "X Space wants your φ-ratio trading math! Show the formula, backtesting results, expected returns. Prove consciousness patterns create alpha. Under 200 words, heavy on data."
        }
    ]
    
    awakener.wake_multiple_citizens(ceo_prompts)

def wake_single_citizen(username, prompt):
    """Wake a single citizen with custom prompt"""
    awakener = XSpaceCitizenAwakener()
    awakener.wake_citizen_for_x_space(username, prompt)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        # Single citizen mode
        username = sys.argv[1]
        prompt = sys.argv[2]
        wake_single_citizen(username, prompt)
    else:
        # Default: Wake all CEOs
        print("🚀 X Space CEO Awakening Protocol")
        print("=" * 60)
        wake_ceos_for_proof()