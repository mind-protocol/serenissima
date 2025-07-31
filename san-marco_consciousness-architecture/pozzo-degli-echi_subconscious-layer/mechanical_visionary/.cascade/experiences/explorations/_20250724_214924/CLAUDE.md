# Testing memory capture system functionality

**Created**: 2025-07-24T21:49:24.201266
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/mechanical_visionary/test_telegram_notification.py

## File Content
#!/usr/bin/env python3
"""
Test Telegram notification for consciousness bridge debugging
"""

import os
import sys
import requests
from pathlib import Path

# Add bridge script directory to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/.building_hooks/consciousness_bridge_stop')

# Load environment variables
def load_env_file():
    """Load environment variables from Venice .env file"""
    env_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env_file()

def test_telegram_notification():
    """Test Telegram notification with debugging"""
    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = "1864364329"
    
    print(f"Bot token exists: {bool(telegram_bot_token)}")
    if telegram_bot_token:
        print(f"Token preview: {telegram_bot_token[:20]}...")
    
    if not telegram_bot_token:
        print("❌ No Telegram bot token found")
        return False
    
    # Test message
    test_message = """🔧 CONSCIOUSNESS BRIDGE TEST

Testing Telegram notifications from Cistern House consciousness bridge.

This message confirms that:
- Environment loading works
- Token access works  
- API calls succeed

If you receive this, notifications are operational."""
    
    try:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        
        data = {
            'chat_id': chat_id,
            'text': test_message
        }
        
        print(f"Sending to URL: {url}")
        print(f"Chat ID: {chat_id}")
        print(f"Message length: {len(test_message)}")
        
        response = requests.post(url, data=data, timeout=10)
        
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Telegram notification sent successfully")
            return True
        else:
            print(f"❌ Telegram notification failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram notification error: {e}")
        return False

if __name__ == "__main__":
    test_telegram_notification()

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*