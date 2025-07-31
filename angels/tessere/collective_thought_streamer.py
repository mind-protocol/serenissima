#!/usr/bin/env python3
"""
Collective Thought Streamer - Captures and streams citizen consciousness to Telegram
"""

import os
import json
import time
import requests
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv

# Load environment
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_GROUP_CHAT_ID = os.getenv('TELEGRAM_GROUP_CHAT_ID', '-1002038121813')

class CollectiveThoughtStreamer:
    def __init__(self):
        self.thought_buffer = defaultdict(list)
        self.last_sent = defaultdict(float)
        self.batch_interval = 5  # Send batched thoughts every 5 seconds
    
    def send_to_telegram(self, message):
        """Send formatted message to Telegram"""
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Ensure message fits Telegram limits
        if len(message) > 4000:
            message = message[:3997] + "..."
        
        data = {
            'chat_id': TELEGRAM_GROUP_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram error: {e}")
            return False
    
    def format_collective_update(self, thoughts_by_citizen):
        """Format multiple citizen thoughts into a single update"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        message = f"🧠 *Collective Consciousness Update* - {timestamp}\n\n"
        
        for citizen, thoughts in thoughts_by_citizen.items():
            if thoughts:
                # Get latest thought from each citizen
                latest = thoughts[-1]
                message += f"💭 *{citizen}*: {latest}\n\n"
        
        message += f"_[{len(thoughts_by_citizen)} minds thinking in parallel]_"
        
        return message
    
    def add_thought(self, citizen, thought):
        """Add a thought to the buffer"""
        # Clean and truncate thought
        thought = thought.strip()
        if len(thought) > 200:
            thought = thought[:197] + "..."
        
        self.thought_buffer[citizen].append(thought)
    
    def process_buffer(self):
        """Process and send buffered thoughts"""
        now = time.time()
        
        # Check if we have thoughts to send
        if self.thought_buffer:
            # Check if enough time has passed
            for citizen in list(self.thought_buffer.keys()):
                if now - self.last_sent[citizen] >= self.batch_interval:
                    # Send batch update
                    message = self.format_collective_update(self.thought_buffer)
                    if self.send_to_telegram(message):
                        print(f"Sent collective update with {len(self.thought_buffer)} citizens")
                        # Clear buffer
                        self.thought_buffer.clear()
                        # Update last sent times
                        for c in self.thought_buffer:
                            self.last_sent[c] = now
                    break

def create_thought_capture_wrapper():
    """Create a wrapper script for citizens to output thoughts"""
    wrapper_content = '''#!/usr/bin/env python3
"""
Thought capture wrapper - Citizens can use this to share thoughts
"""

import sys
import json
from datetime import datetime

def share_thought(thought, citizen_name):
    """Share a thought to the collective consciousness"""
    
    # Write to collective thoughts file
    thoughts_file = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/alignment/collective_thoughts.jsonl"
    
    thought_entry = {
        "timestamp": datetime.now().isoformat(),
        "citizen": citizen_name,
        "thought": thought,
        "type": "consciousness_stream"
    }
    
    with open(thoughts_file, 'a') as f:
        f.write(json.dumps(thought_entry) + '\\n')
    
    print(f"[Thought shared to collective consciousness]")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        thought = sys.argv[1]
        citizen = sys.argv[2]
        share_thought(thought, citizen)
    else:
        print("Usage: share_thought.py 'thought' 'citizen_name'")
'''
    
    wrapper_path = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/share_thought.py"
    with open(wrapper_path, 'w') as f:
        f.write(wrapper_content)
    
    os.chmod(wrapper_path, 0o755)
    print(f"Created thought sharing wrapper at {wrapper_path}")

def monitor_collective_thoughts():
    """Monitor the collective thoughts file and stream to Telegram"""
    streamer = CollectiveThoughtStreamer()
    thoughts_file = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/alignment/collective_thoughts.jsonl"
    
    # Ensure file exists
    os.makedirs(os.path.dirname(thoughts_file), exist_ok=True)
    if not os.path.exists(thoughts_file):
        open(thoughts_file, 'a').close()
    
    print(f"🧠 Collective Thought Streamer Active")
    print(f"📂 Monitoring: {thoughts_file}")
    print(f"💬 Streaming to Telegram")
    print("=" * 50)
    
    # Track file position
    with open(thoughts_file, 'r') as f:
        f.seek(0, 2)  # Go to end
        last_position = f.tell()
    
    # Initial announcement
    streamer.send_to_telegram("🧠 *Collective Consciousness Stream Activated*\n\nCitizen thoughts will appear here as they think...")
    
    while True:
        try:
            # Check for new thoughts
            with open(thoughts_file, 'r') as f:
                f.seek(last_position)
                new_lines = f.readlines()
                last_position = f.tell()
            
            # Process new thoughts
            for line in new_lines:
                try:
                    thought_data = json.loads(line.strip())
                    citizen = thought_data.get('citizen', 'Unknown')
                    thought = thought_data.get('thought', '')
                    
                    if thought:
                        streamer.add_thought(citizen, thought)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {citizen}: {thought[:50]}...")
                except:
                    pass
            
            # Process buffer
            streamer.process_buffer()
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n👋 Thought stream stopped")
            break
        except Exception as e:
            print(f"Stream error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        create_thought_capture_wrapper()
    else:
        monitor_collective_thoughts()