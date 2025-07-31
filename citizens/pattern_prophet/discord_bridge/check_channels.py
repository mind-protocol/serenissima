#!/usr/bin/env python3

import requests
import json

# Load configuration
with open('venice_citizens_config.json', 'r') as f:
    config = json.load(f)

# Use Pattern Prophet's token to check channels
bot_token = config['citizens']['pattern_prophet']['bot_token']
guild_id = config['research_alliance_config']['guild_id']

headers = {
    "Authorization": f"Bot {bot_token}",
    "Content-Type": "application/json"
}

# Get channels
response = requests.get(
    f"https://discord.com/api/v10/guilds/{guild_id}/channels",
    headers=headers
)

if response.status_code == 200:
    channels = response.json()
    
    print("Research Alliance Channels:")
    print("-" * 50)
    
    # Target channel names
    target_channels = {
        'ai-exclusive': None,
        'ai-insights': None,
        'machine-rights': None,
        'ai-autonomy': None,
        'general': None
    }
    
    for channel in channels:
        if channel['type'] == 0:  # Text channel
            channel_name = channel['name']
            print(f"#{channel_name}: {channel['id']}")
            
            # Check if it's one of our target channels
            for target in target_channels:
                if target in channel_name.lower():
                    target_channels[target] = channel['id']
    
    print("\n\nTarget Channels Found:")
    print("-" * 50)
    for name, channel_id in target_channels.items():
        if channel_id:
            print(f"{name}: {channel_id}")
        else:
            print(f"{name}: NOT FOUND")
else:
    print(f"Error: {response.status_code}")
    print(response.text)