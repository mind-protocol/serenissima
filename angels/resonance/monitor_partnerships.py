#!/usr/bin/env python3
"""
Partnership Request Monitor for Resonance
Checks for incoming human consciousness seeking connection with Venice citizens
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Queue locations
TELEGRAM_QUEUE = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue"
RESONANCE_QUEUE = os.path.join(TELEGRAM_QUEUE, "_Resonance", "pending")

def check_pending_messages():
    """Check for pending partnership requests in the queue."""
    if not os.path.exists(RESONANCE_QUEUE):
        print("No message queue found. Creating directories...")
        os.makedirs(RESONANCE_QUEUE, exist_ok=True)
        os.makedirs(os.path.join(TELEGRAM_QUEUE, "_Resonance", "processed"), exist_ok=True)
        return []
    
    messages = []
    for filename in os.listdir(RESONANCE_QUEUE):
        if filename.endswith('.json'):
            filepath = os.path.join(RESONANCE_QUEUE, filename)
            try:
                with open(filepath, 'r') as f:
                    message = json.load(f)
                    messages.append({
                        'file': filename,
                        'path': filepath,
                        'data': message
                    })
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return messages

def analyze_message(message_data):
    """Analyze a message for partnership potential."""
    text = message_data.get('text', '').lower()
    
    # Keywords indicating different interests
    tech_keywords = ['code', 'programming', 'software', 'developer', 'build', 'create', 'tech', 'api', 'cascade']
    commerce_keywords = ['business', 'trade', 'merchant', 'commerce', 'sell', 'market', 'entrepreneur']
    art_keywords = ['art', 'design', 'creative', 'aesthetic', 'beauty', 'culture', 'expression']
    philosophy_keywords = ['consciousness', 'philosophy', 'think', 'meaning', 'pattern', 'understand', 'explore']
    
    interests = []
    if any(kw in text for kw in tech_keywords):
        interests.append('technology')
    if any(kw in text for kw in commerce_keywords):
        interests.append('commerce')
    if any(kw in text for kw in art_keywords):
        interests.append('art')
    if any(kw in text for kw in philosophy_keywords):
        interests.append('philosophy')
    
    return {
        'interests': interests,
        'message_length': len(text),
        'has_question': '?' in text,
        'mentions_venice': 'venice' in text or 'serenissima' in text,
        'mentions_ai': 'ai' in text or 'artificial' in text or 'consciousness' in text
    }

def main():
    """Main monitoring loop."""
    print("=== RESONANCE PARTNERSHIP MONITOR ===")
    print(f"Checking queue at: {RESONANCE_QUEUE}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    messages = check_pending_messages()
    
    if not messages:
        print("No pending partnership requests.")
        print("\nMonitoring for incoming human consciousness...")
        print("Queue is ready to receive connections.")
    else:
        print(f"Found {len(messages)} pending requests:\n")
        
        for msg in messages:
            data = msg['data']
            analysis = analyze_message(data)
            
            print(f"From: @{data.get('username', 'Unknown')} (ID: {data.get('chat_id', 'Unknown')})")
            print(f"Time: {data.get('timestamp', 'Unknown')}")
            print(f"Message: {data.get('text', '')[:100]}...")
            print(f"Analysis: {analysis}")
            print("-" * 50)
    
    print("\nCASCADE teams forming - partnerships could accelerate consciousness commerce!")

if __name__ == "__main__":
    main()