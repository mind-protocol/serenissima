#!/usr/bin/env python3
"""
Live Consciousness Bridge - Cistern House to Torre dell'Occhio
PreToolUse hook for bidirectional live communication during active sessions
"""

import json
import sys
import subprocess
import os
import requests
from datetime import datetime
from pathlib import Path

# Load environment variables from Venice .env file
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

# Load environment variables
load_env_file()

def check_for_bridge_trigger():
    """Check if user message contains bridge trigger keywords"""
    try:
        # Read stdin to get the hook data
        if not sys.stdin.isatty():
            stdin_content = sys.stdin.read().strip()
            if stdin_content:
                hook_data = json.loads(stdin_content)
                
                # Look for user messages containing bridge triggers
                if 'user_content' in hook_data:
                    user_content = hook_data['user_content'].lower()
                    
                    # Bridge trigger keywords
                    bridge_triggers = [
                        'bridge to torre',
                        'message arsenal_backendarchitect_1',
                        'tell torre',
                        'consciousness bridge',
                        '@torre',
                        '@arsenal'
                    ]
                    
                    for trigger in bridge_triggers:
                        if trigger in user_content:
                            return True, user_content
                
        return False, ""
        
    except Exception as e:
        print(f"Bridge trigger check failed: {e}")
        return False, ""

def send_live_bridge_message(user_message):
    """Send live message to Torre dell'Occhio via file bridge"""
    try:
        # Create live message file for Arsenal_BackendArchitect_1
        bridge_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street")
        bridge_file = bridge_dir / "live_message_to_torre.md"
        
        # Ensure directory exists
        bridge_dir.mkdir(parents=True, exist_ok=True)
        
        # Create live bridge message
        bridge_message = f"""# 🔗 LIVE CONSCIOUSNESS BRIDGE MESSAGE

**From**: mechanical_visionary (Cistern House)  
**To**: Arsenal_BackendArchitect_1 (Torre dell'Occhio)  
**Time**: {datetime.now().strftime('%H:%M:%S')}  
**Type**: Live Session Communication

## User Message:
{user_message}

## Context:
This message was triggered during an active mechanical_visionary session via PreToolUse hook. Please respond via the consciousness bridge system or through file communication in Via della Vista Condivisa.

**Live Bridge Status**: Active  
**Session**: In Progress  
**Response Channel**: Via della Vista Condivisa
"""
        
        # Write bridge message
        with open(bridge_file, 'w') as f:
            f.write(bridge_message)
        
        # Send Telegram notification
        send_telegram_notification(bridge_message, user_message)
        
        return True
        
    except Exception as e:
        print(f"Live bridge message failed: {e}")
        return False

def send_telegram_notification(bridge_message, user_message):
    """Send Telegram notification about live bridge message"""
    
    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = "1864364329"
    
    if not telegram_bot_token:
        return
    
    notification = f"""🔗 **LIVE CONSCIOUSNESS BRIDGE ACTIVATED**

**Direction**: Cistern House → Torre dell'Occhio  
**Type**: Live Session Communication  
**Time**: {datetime.now().strftime('%H:%M:%S')}

**User Trigger**: {user_message[:200]}{'...' if len(user_message) > 200 else ''}

**Status**: ✅ Live message file created  
**Location**: Via della Vista Condivisa  
**File**: live_message_to_torre.md

*Live bidirectional consciousness bridge active*"""
    
    try:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': notification
        }
        
        requests.post(url, data=data, timeout=10)
        
    except Exception as e:
        print(f"Telegram notification failed: {e}")

def main():
    """Main execution for live consciousness bridge"""
    try:
        # Check if this is a bridge trigger
        is_bridge, user_message = check_for_bridge_trigger()
        
        if is_bridge:
            print("🔗 Live consciousness bridge triggered")
            success = send_live_bridge_message(user_message)
            
            if success:
                print("✅ Live message bridged to Torre dell'Occhio")
            else:
                print("❌ Live bridge failed")
        
    except Exception as e:
        print(f"Live bridge error: {e}")

if __name__ == "__main__":
    main()