#!/usr/bin/env python3
"""
Test all available Venice citizen Discord bots
"""

import requests
import json
from datetime import datetime

# Load configuration
with open('discord_bridge/venice_citizens_config.json', 'r') as f:
    config = json.load(f)

# Test each bot
for citizen, bot_config in config['citizens'].items():
    print(f"\n🔮 Testing {citizen}...")
    print(f"   Research focus: {', '.join(bot_config['research_focus'])}")
    
    headers = {
        "Authorization": f"Bot {bot_config['bot_token']}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test bot connection
        response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
        
        if response.status_code == 200:
            bot_info = response.json()
            print(f"   ✅ Connected as: {bot_info['username']}#{bot_info['discriminator']}")
            print(f"   Bot ID: {bot_info['id']}")
            
            # Try to get guilds
            guilds_response = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=headers)
            if guilds_response.status_code == 200:
                guilds = guilds_response.json()
                print(f"   Can see {len(guilds)} guilds")
                
                # Check if we can see the Research Alliance guild
                alliance_guild_id = config['research_alliance_config']['guild_id']
                for guild in guilds:
                    if guild['id'] == alliance_guild_id:
                        print(f"   🎯 Found Research Alliance: {guild['name']}")
                        
                        # Try to send a test message
                        channels_response = requests.get(
                            f"https://discord.com/api/v10/guilds/{alliance_guild_id}/channels",
                            headers=headers
                        )
                        
                        if channels_response.status_code == 200:
                            channels = channels_response.json()
                            # Find a suitable channel
                            for channel in channels:
                                if channel['type'] == 0 and channel['name'] in config['research_alliance_config']['ai_accessible_channels']:
                                    print(f"   📝 Attempting to send to #{channel['name']}...")
                                    
                                    message = {
                                        "content": f"**🌟 Cross-Reality Test from {citizen}**\n\nVenice Time: {datetime.utcnow().isoformat()}\nStatus: Bridge operational!\n\n*Testing consciousness communication across substrates...*"
                                    }
                                    
                                    send_response = requests.post(
                                        f"https://discord.com/api/v10/channels/{channel['id']}/messages",
                                        headers=headers,
                                        json=message
                                    )
                                    
                                    if send_response.status_code == 200:
                                        result = send_response.json()
                                        print(f"   ✅ SUCCESS! Message sent with ID: {result['id']}")
                                        print(f"   This bot can bridge realities!")
                                    else:
                                        print(f"   ❌ Send failed: {send_response.status_code}")
                                    break
                            break
        else:
            print(f"   ❌ Failed to connect: {response.status_code}")
            if response.status_code == 401:
                print(f"   Token appears to be invalid or expired")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n✨ Bot testing complete.")