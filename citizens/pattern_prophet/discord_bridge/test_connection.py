#!/usr/bin/env python3
"""
Test Pattern Prophet's Discord connection
"""

import json
from venice_citizen_client import VeniceCitizenDiscordClient

# Load configuration
with open('venice_citizens_config.json', 'r') as f:
    config = json.load(f)

# Initialize Pattern Prophet
citizen = config['citizens']['pattern_prophet']
client = VeniceCitizenDiscordClient(
    'pattern_prophet',
    citizen['bot_token']
)

print("Testing Pattern Prophet Discord connection...")
print("-" * 50)

try:
    # Get bot info
    me = client.get_me()
    print(f"✅ Connected as: {me['username']}#{me['discriminator']}")
    print(f"   Bot ID: {me['id']}")
    
    # Get guilds
    guilds = client.get_guilds()
    print(f"\n✅ Connected to {len(guilds)} servers:")
    for guild in guilds:
        print(f"   - {guild['name']} (ID: {guild['id']})")
    
    # Check Research Alliance
    research_alliance_id = config['research_alliance_config']['guild_id']
    if any(g['id'] == research_alliance_id for g in guilds):
        print(f"\n✅ Confirmed access to Research Alliance!")
    else:
        print(f"\n❌ Not in Research Alliance server!")
        
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nPossible issues:")
    print("1. Bot token may be invalid")
    print("2. Bot may not be added to the server")
    print("3. Network connection issues")