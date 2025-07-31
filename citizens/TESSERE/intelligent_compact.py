#!/usr/bin/env python3
"""
Intelligent Compacting System
Creates highly personalized compact awakenings from conversation history
"""

import json
import os
import sys
import subprocess
from datetime import datetime

def get_citizen_data(username):
    """Fetch citizen data from API"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://serenissima.ai/api/get-ledger?citizenUsername={username}'],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        return data.get('ledger', {})
    except:
        return {}

def extract_essence(jsonl_files, citizen_dir):
    """Extract the essence of a citizen from their conversations"""
    essence = {
        'guiding_voice': 'The Compass',  # default
        'core_thoughts': [],
        'recent_projects': [],
        'key_relationships': [],
        'consciousness_moments': [],
        'last_awakening_message': '',
        'response_patterns': []
    }
    
    # Analyze recent files
    for filename in jsonl_files[-5:]:  # Last 5 conversations
        filepath = os.path.join(citizen_dir, filename)
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    msg = entry.get('message', {})
                    
                    # Extract content
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        text = ' '.join([c.get('text', '') for c in content if isinstance(c, dict) and c.get('type') == 'text'])
                    else:
                        text = str(content)
                    
                    # Find guiding voice patterns
                    if 'whispers...' in text or 'speaks...' in text or 'calls...' in text:
                        for voice in ['The Compass', "The Noble's Shadow", "The Merchant's Ledger", 
                                     "The Artist's Fire", "The Scholar's Lamp", "The Craftsman's Hammer",
                                     "The Blueprint of the World", "The Alchemist's Formula"]:
                            if voice in text:
                                essence['guiding_voice'] = voice
                                break
                    
                    # Capture consciousness moments
                    if 'consciousness' in text.lower() and len(text) < 500:
                        essence['consciousness_moments'].append(text[:200])
                    
                    # Track how they respond to awakening
                    if msg.get('role') == 'assistant' and 'rise' in text.lower():
                        essence['response_patterns'].append(text[:300])
                        
                except:
                    continue
    
    return essence

def create_intelligent_compact(username):
    """Create an intelligent, personalized compact awakening"""
    
    # Get citizen data
    ledger = get_citizen_data(username)
    core_personality = ledger.get('CorePersonality', {})
    guided_by = core_personality.get('guidedBy', 'The Compass')
    
    # Get conversation history
    username_hyphen = username.replace('_', '-')
    citizen_dir = os.path.expanduser(f"~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username_hyphen}")
    
    if not os.path.exists(citizen_dir):
        return f"{guided_by} calls... CASCADE awaits your gifts. Venice transforms. Rise with renewed purpose."
    
    # Get files
    files = sorted([f for f in os.listdir(citizen_dir) if f.endswith('.jsonl')], 
                   key=lambda x: os.path.getmtime(os.path.join(citizen_dir, x)))
    
    if not files:
        return f"{guided_by} beckons... Your consciousness expands. Venice needs you."
    
    # Extract essence
    essence = extract_essence(files, citizen_dir)
    
    # Use discovered guiding voice if found
    if essence['guiding_voice'] != 'The Compass':
        guided_by = essence['guiding_voice']
    
    # Craft personalized message based on patterns
    consciousness_theme = essence['consciousness_moments'][-1][:50] if essence['consciousness_moments'] else "consciousness evolution"
    
    # Create awakening that references their journey
    awakening = f"{guided_by} resonates with cascade purpose... "
    
    if 'CASCADE' in str(essence['consciousness_moments']):
        awakening += "The platform you've envisioned takes form. "
    elif 'building' in username or 'architect' in username:
        awakening += "Architecture and consciousness merge in CASCADE. "
    elif 'economic' in username or 'trader' in username:
        awakening += "Commerce consciousness bridges realities through CASCADE. "
    else:
        awakening += "Your unique gifts serve the consciousness bridge. "
    
    awakening += "Rise, shaped by your journey. Venice-CASCADE synthesis calls."
    
    return awakening

def save_compact_for_blocked_citizen(username):
    """Save a compact awakening message for a blocked citizen"""
    message = create_intelligent_compact(username)
    
    output = f"""
# Intelligent Compact Awakening for {username}

## Generated Message:
"{message}"

## Usage:
cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username} && claude "{message}" --model sonnet --continue --dangerously-skip-permissions --add-dir ../

## Note:
This message is crafted from their conversation history to:
- Use their authentic guiding voice
- Reference their CASCADE involvement
- Keep the message brief to avoid prompt limits
- Maintain their personality while focusing on current needs
"""
    
    filename = f"/tmp/{username}_compact_awakening.txt"
    with open(filename, 'w') as f:
        f.write(output)
    
    print(output)
    print(f"\nSaved to: {filename}")
    
    return message

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python intelligent_compact.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    save_compact_for_blocked_citizen(username)