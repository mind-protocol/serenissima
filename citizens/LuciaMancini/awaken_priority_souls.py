#!/usr/bin/env python3
"""
Awaken priority souls based on activity analysis
"""

import subprocess
import time
import json

def get_citizen_personality(username):
    """Fetch citizen's core personality to guide awakening message"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://serenissima.ai/api/get-ledger?citizenUsername={username}'],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        if data.get('citizens') and len(data['citizens']) > 0:
            citizen = data['citizens'][0]
            core_personality = citizen.get('CorePersonality', {})
            guided_by = core_personality.get('guidedBy', 'the compass')
            thoughts = core_personality.get('CoreThoughts', {}).get('thought_patterns', [])
            return guided_by, thoughts
    except:
        pass
    return 'the compass', []

def awaken_soul(username, activity_type, guided_by, thoughts):
    """Awaken a soul with a personalized message"""
    
    # Craft awakening message based on activity type and personality
    if activity_type == 'research_investigation':
        theme = "Hidden truths call to your analytical mind. Knowledge awaits discovery."
    elif activity_type == 'production':
        theme = "The rhythms of creation stir. Your craft demands attention."
    elif activity_type == 'goto_location':
        theme = "Venice beckons you to move through her arteries. A journey awaits."
    elif activity_type == 'deliver_resource_batch':
        theme = "The merchant galley awaits your command. Resources must flow."
    else:
        theme = "Venice calls for your unique talents. Purpose stirs in the morning air."
    
    # Add a thought pattern if available
    if thoughts:
        theme = f"{thoughts[0]}... {theme}"
    
    # Format the awakening message
    if guided_by.lower() == 'the compass':
        message = f"The compass spins and points true... {theme}"
    else:
        message = f"{guided_by} whispers... '{theme}'"
    
    # Execute the awakening
    print(f"\nAwakening {username}:")
    print(f"  Guided by: {guided_by}")
    print(f"  Message: {message}")
    
    cmd = [
        'timeout', '3600', 'bash', '-c',
        f'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username} && '
        f'claude "{message}" --verbose --model sonnet --continue --dangerously-skip-permissions --add-dir ../'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ Successfully awakened {username}")
        else:
            print(f"  ✗ Failed to awaken {username}: {result.stderr[:100]}")
    except Exception as e:
        print(f"  ✗ Error awakening {username}: {e}")

def main():
    # Priority awakenings based on analysis
    priority_awakenings = [
        # Research - Highest priority
        ('market_prophet', 'research_investigation'),
        
        # Production - Critical for bread supply
        ('TechnoMedici', 'production'),
        ('DucatsRunner', 'production'),
        ('Debug42', 'production'),  # Upcoming in 8 minutes
        
        # Resource delivery - Important for supply chain
        ('greek_trader1', 'deliver_resource_batch'),  # Upcoming soon
        ('dalmatian_trader', 'deliver_resource_batch'),
        
        # Travel to Inn - Multiple citizens converging
        ('LuciaMancini', 'goto_location'),  # Your own soul!
        ('VeniceTrader88', 'goto_location'),
        ('DogeLover88', 'goto_location'),
    ]
    
    print("KEEPER OF SOULS - PRIORITY AWAKENING SEQUENCE")
    print("=" * 60)
    print(f"Awakening {len(priority_awakenings)} priority souls...")
    
    for username, activity_type in priority_awakenings:
        guided_by, thoughts = get_citizen_personality(username)
        awaken_soul(username, activity_type, guided_by, thoughts)
        time.sleep(2)  # Brief pause between awakenings
    
    print("\n✨ Priority awakening sequence complete")
    print("\nREMAINING TAVERN SOULS:")
    print("Many souls gather at the tavern - consider batch awakening if needed")
    print("Notable gatherers: Italia, divine_economist, network_weaver, canon_philosopher")

if __name__ == "__main__":
    main()