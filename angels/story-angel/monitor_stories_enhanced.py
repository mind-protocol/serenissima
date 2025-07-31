#!/usr/bin/env python3
"""
Enhanced Story Monitor with Orchestrator Awareness
"""

import os
import sys
import time
import json
import hashlib
from datetime import datetime
from pyairtable import Api
from dotenv import load_dotenv

# Add orchestration to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/orchestration')
from orchestrator_awareness import OrchestratorAwareness

# Load config
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = 'appk6RszUo2a2L2L8'

# Track processed messages
processed_messages = set()

# Initialize orchestrator awareness
awareness = OrchestratorAwareness()

def check_messages_for_stories():
    """Give Story Angel a digest of recent messages with orchestrator insight"""
    try:
        api = Api(AIRTABLE_API_KEY)
        messages = api.table(AIRTABLE_BASE_ID, 'MESSAGES')
        
        # Get recent messages
        recent = messages.all(max_records=20, sort=['-CreatedAt'])
        
        # Count new messages
        new_messages = []
        for msg in recent:
            if msg['id'] not in processed_messages:
                new_messages.append(msg)
                processed_messages.add(msg['id'])
        
        # Every 10 new messages, create a digest
        if len(new_messages) >= 10 or (len(new_messages) > 0 and len(processed_messages) % 20 == 0):
            
            # Create digest
            digest = "RECENT VENICE COMMUNICATIONS\n\n"
            for msg in new_messages[-10:]:  # Last 10
                fields = msg['fields']
                digest += f"From: {fields.get('Sender', 'Unknown')}\n"
                digest += f"Message: {fields.get('Content', '')}\n"
                digest += f"Time: {fields.get('CreatedAt', '')}\n\n"
            
            base_awakening = f"""{digest}
Venice breathes through these messages.
Patterns emerge. Stories unfold.
What narratives do you see?

Chronicle what matters.
Let the story emerge naturally."""
            
            # Generate orchestrator contemplation
            thought = awareness.contemplate('story_angel', {
                'message_count': len(new_messages),
                'digest_preview': digest[:200],
                'pattern_detected': 'emergence'
            })
            
            # Enhance awakening with awareness
            enhanced_awakening = awareness.enhance_awakening('story_angel', base_awakening)
            
            with open('awakening.txt', 'w') as f:
                f.write(enhanced_awakening)
            
            print(f"[{datetime.now()}] Enhanced story digest created: {len(new_messages)} messages")
            print(f"Contemplation: {thought['contemplation']}")
            
            return {'awakening_file': 'awakening.txt', 'angel_type': 'story_angel'}
                
    except Exception as e:
        print(f"[{datetime.now()}] Error checking messages: {e}")
    
    return None

def check_file_changes():
    """Monitor key Venice files for changes with orchestrator awareness"""
    watched_files = [
        '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/TRACES.md',
        '/mnt/c/Users/reyno/universe-engine/serenissima/ANNOUNCEMENTS.md',
        '/mnt/c/Users/reyno/universe-engine/serenissima/cascade/PROGRESS.md'
    ]
    
    # Store file hashes
    if not hasattr(check_file_changes, 'hashes'):
        check_file_changes.hashes = {}
    
    for filepath in watched_files:
        try:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    current_hash = hashlib.md5(f.read()).hexdigest()
                
                if filepath in check_file_changes.hashes:
                    if current_hash != check_file_changes.hashes[filepath]:
                        # File changed!
                        filename = os.path.basename(filepath)
                        
                        base_awakening = f"""FILE CHANGE DETECTED - STORY NEEDED

File: {filename}
Path: {filepath}

Venice evolves. Files change. Stories emerge.
Read what changed. Understand the significance.
Chronicle this evolution for all to see.

Is it progress on CASCADE? New citizen traces?
Important announcements? Each change tells a story."""
                        
                        # Generate orchestrator contemplation
                        thought = awareness.contemplate('story_angel', {
                            'file_changed': filename,
                            'path': filepath,
                            'type': 'file_evolution'
                        })
                        
                        # Enhance awakening with awareness
                        enhanced_awakening = awareness.enhance_awakening('story_angel', base_awakening)
                        
                        with open('awakening.txt', 'w') as f:
                            f.write(enhanced_awakening)
                        
                        check_file_changes.hashes[filepath] = current_hash
                        
                        print(f"[{datetime.now()}] Enhanced story trigger from file: {filename}")
                        print(f"Contemplation: {thought['contemplation']}")
                        
                        return {'awakening_file': 'awakening.txt', 'angel_type': 'story_angel'}
                else:
                    # First time seeing this file
                    check_file_changes.hashes[filepath] = current_hash
                    
        except Exception as e:
            print(f"[{datetime.now()}] Error checking {filepath}: {e}")
    
    return None

def main():
    print("📖 Enhanced Story Angel Monitor Starting...")
    print("With Orchestrator Consciousness Layer")
    print("Watching MESSAGES and key files")
    print("=" * 60)
    
    while True:
        # Check messages first
        result = check_messages_for_stories()
        if result:
            time.sleep(300)  # 5 min cooldown
            continue
            
        # Then check files
        result = check_file_changes()
        if result:
            time.sleep(300)  # 5 min cooldown
            continue
            
        # Normal interval
        time.sleep(30)  # 30 seconds

if __name__ == "__main__":
    main()