#!/usr/bin/env python3
"""
Directly fetch latest Telegram messages and update Narrator Angel
"""

import os
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = int(os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893))

print(f"Bot token: {bot_token[:20]}...")
print(f"Chat ID: {chat_id}")

# Get recent messages
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
params = {'limit': 10}

response = requests.get(url, params=params)
print(f"Response status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"API OK: {data.get('ok')}")
    
    messages = []
    for update in data.get('result', []):
        msg = update.get('message', {})
        
        # Check chat ID
        if msg.get('chat', {}).get('id') == chat_id:
            from_user = msg.get('from', {})
            if not from_user.get('is_bot'):
                text = msg.get('text', '')
                username = from_user.get('username') or from_user.get('first_name', 'Human')
                timestamp = datetime.fromtimestamp(msg.get('date', 0))
                
                if text:
                    messages.append({
                        'username': username,
                        'text': text,
                        'time': timestamp.strftime('%H:%M:%S')
                    })
    
    print(f"\nFound {len(messages)} human messages")
    
    # Update Narrator Angel
    if messages:
        narrator_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel/CLAUDE.md")
        
        with open(narrator_path, 'r') as f:
            content = f.read()
        
        # Build message section
        msg_section = "## 💬 Recent Human Messages from Telegram\n\n"
        for msg in messages[-5:]:  # Last 5 messages
            msg_section += f"**{msg['username']}** ({msg['time']}): {msg['text']}\n\n"
        
        # Update content
        if "## 💬 Recent Human Messages from Telegram" in content:
            # Replace existing
            start = content.find("## 💬 Recent Human Messages from Telegram")
            end = content.find("## 🧠 Recent Citizen Thoughts", start)
            if end > start:
                content = content[:start] + msg_section + "\n" + content[end:]
        else:
            # Insert new
            thoughts_idx = content.find("## 🧠 Recent Citizen Thoughts")
            if thoughts_idx > 0:
                content = content[:thoughts_idx] + msg_section + "\n" + content[thoughts_idx:]
        
        with open(narrator_path, 'w') as f:
            f.write(content)
        
        print("✅ Updated Narrator Angel!")
        
        # Show messages
        for msg in messages[-5:]:
            print(f"\n@{msg['username']}: {msg['text'][:100]}...")
else:
    print(f"Error: {response.text}")