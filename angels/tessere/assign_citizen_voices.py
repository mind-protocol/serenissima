#!/usr/bin/env python3
"""
Manual Voice Assignment for Venice Citizens
Allows assigning specific ElevenLabs voices to each citizen
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

# Available ElevenLabs voices with descriptions
VOICE_LIBRARY = {
    # Female voices
    "21m00Tcm4TlvDq8ikWAM": "Rachel - Calm, ethereal",
    "MF3mGyEYCl7XYWbV9V6O": "Elli - Young, energetic", 
    "oWAxZDx7w5VEj9dCyTzz": "Grace - Warm, mature wisdom",
    "g5CIjZEefAph4nQFvHAz": "Domi - Young, expressive",
    "SOYHLrjzK2X1ezoPC6cr": "Sarah - Soft, gentle",
    "pFZP5JQG7iQjIQuC4Bku": "Lily - British, narrative",
    "z9fAnlkpzviPz146aGWa": "Glinda - Witchy, wise",
    "EXAVITQu4vr4xnSDxMaL": "Bella - Professional, warm",
    "AZnzlk1XvdvUeBnXmlld": "Domi - Young American",
    "CYw3kZ02Hs0563khs1Fj": "Dave - British, warm male",
    
    # Male voices  
    "yoZ06aMxZJJ28mfd3POQ": "Sam - Young American male",
    "TxGEqnHWrfWFTfGW9XjX": "Josh - Conversational, expressive",
    "VR6AewLTigWG4xSOukaG": "Arnold - Deep, authoritative",
    "flq6f7yk4E4fJM5XTYuZ": "Michael - Professional, analytical",
    "2EiwWnXFnvU5JabPnv8n": "Clyde - War veteran",
    "D38z5RcWu1voky8WS1ja": "Fin - Irish sailor",
    "N2lVS1w4EtoT3dr4eOWO": "Callum - Hoarse, British",
    "IKne3meq5aSn9XLyUdCD": "Charlie - Australian surfer",
    "5Q0t7uMcjvnagumLfvZi": "Ethan - American narrator",
    "onwK4e9ZLuTAKqWW03F9": "Daniel - British, news presenter",
    "bVMeCyTHy58xNoL34h3p": "Jeremy - American-Irish narrator",
    "ErXwobaYiN019PkySvjV": "Antoni - Well-rounded",
    "GBv7mTt0atIp3Br8iCZE": "Thomas - Calm American",
    "pNInz6obpgDQGcFmaJgB": "Adam - Deep American",
    "nPczCjzI2devNBz1zQrb": "Brian - Deep American",
    "ODq5zmih8GrVes37Dizd": "Patrick - Shouty American",
    "ThT5KcBeYPX3keUQqHPh": "Harry - Anxious British"
}

# Voice assignment suggestions based on character types
VOICE_SUGGESTIONS = {
    # Nobles & Officials
    "ConsiglioDeiDieci": "VR6AewLTigWG4xSOukaG",  # Arnold - authoritative
    "MorosiniNoble": "onwK4e9ZLuTAKqWW03F9",      # Daniel - British noble
    "DucalePalace": "CYw3kZ02Hs0563khs1Fj",       # Dave - warm British
    
    # Merchants & Traders
    "MerchantPrince": "bVMeCyTHy58xNoL34h3p",     # Jeremy - narrator
    "alexandria_trader": "oWAxZDx7w5VEj9dCyTzz",   # Grace - ancient wisdom
    "levant_trader": "ErXwobaYiN019PkySvjV",       # Antoni - well-rounded
    "sea_trader": "D38z5RcWu1voky8WS1ja",          # Fin - Irish sailor
    
    # Innovatori & Thinkers
    "Italia": "21m00Tcm4TlvDq8ikWAM",              # Rachel - calm wisdom
    "mechanical_visionary": "flq6f7yk4E4fJM5XTYuZ", # Michael - analytical
    "pattern_prophet": "flq6f7yk4E4fJM5XTYuZ",      # Michael - analytical
    "element_transmuter": "z9fAnlkpzviPz146aGWa",   # Glinda - mystical
    
    # Workers & Craftsmen
    "TechnoMedici": "VR6AewLTigWG4xSOukaG",       # Arnold - deep craft
    "ShadowHunter": "2EiwWnXFnvU5JabPnv8n",       # Clyde - veteran
    "GlassMaster1503": "GBv7mTt0atIp3Br8iCZE",    # Thomas - calm craft
    
    # Artistic & Creative
    "poet_of_the_rialto": "TxGEqnHWrfWFTfGW9XjX", # Josh - expressive
    "BookWorm365": "pFZP5JQG7iQjIQuC4Bku",        # Lily - narrative
    "painter_of_light": "bVMeCyTHy58xNoL34h3p",   # Jeremy - artistic
    
    # Young & Energetic
    "DragonSlayer": "MF3mGyEYCl7XYWbV9V6O",       # Elli - young energy
    "BarbarigoCadet": "yoZ06aMxZJJ28mfd3POQ",     # Sam - young male
    "DogeLover88": "AZnzlk1XvdvUeBnXmlld",        # Young American
    
    # Mysterious & Unique
    "coffee": "N2lVS1w4EtoT3dr4eOWO",             # Callum - hoarse
    "gondola_assistant": "D38z5RcWu1voky8WS1ja",  # Fin - weathered
    "Resonance": "21m00Tcm4TlvDq8ikWAM",          # Rachel - ethereal
}

def update_citizen_voice(username, voice_id):
    """Update a citizen's voice in Airtable"""
    
    # Get Airtable credentials
    airtable_token = os.getenv('AIRTABLE_TOKEN')
    base_id = os.getenv('AIRTABLE_BASE_ID', 'appc6AFwVXt0gNYqp')
    
    if not airtable_token:
        print("❌ AIRTABLE_TOKEN not found in environment")
        return False
        
    # First, get the citizen's record ID
    headers = {
        'Authorization': f'Bearer {airtable_token}',
        'Content-Type': 'application/json'
    }
    
    # Search for the citizen
    filter_formula = f"{{Username}} = '{username}'"
    url = f"https://api.airtable.com/v0/{base_id}/CITIZENS"
    params = {
        'filterByFormula': filter_formula
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Failed to find citizen {username}: {response.status_code}")
        return False
        
    data = response.json()
    records = data.get('records', [])
    
    if not records:
        print(f"❌ Citizen {username} not found")
        return False
        
    record_id = records[0]['id']
    
    # Update the voice
    update_url = f"https://api.airtable.com/v0/{base_id}/CITIZENS/{record_id}"
    update_data = {
        "fields": {
            "VoiceId": voice_id
        }
    }
    
    update_response = requests.patch(update_url, headers=headers, json=update_data)
    
    if update_response.status_code == 200:
        print(f"✅ Updated {username} with voice {voice_id}")
        return True
    else:
        print(f"❌ Failed to update {username}: {update_response.status_code}")
        return False

def assign_voices_interactively():
    """Interactive voice assignment for citizens"""
    
    # Get list of citizens
    airtable_token = os.getenv('AIRTABLE_TOKEN')
    base_id = os.getenv('AIRTABLE_BASE_ID', 'appc6AFwVXt0gNYqp')
    
    headers = {
        'Authorization': f'Bearer {airtable_token}',
        'Content-Type': 'application/json'
    }
    
    url = f"https://api.airtable.com/v0/{base_id}/CITIZENS"
    params = {
        'pageSize': 100,
        'sort[0][field]': 'Username',
        'sort[0][direction]': 'asc'
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch citizens: {response.status_code}")
        return
        
    data = response.json()
    citizens = []
    
    for record in data.get('records', []):
        fields = record.get('fields', {})
        username = fields.get('Username')
        current_voice = fields.get('VoiceId', 'None')
        
        if username:
            citizens.append({
                'username': username,
                'current_voice': current_voice,
                'class': fields.get('ClassName', 'Unknown')
            })
    
    print(f"\n🎭 VENICE CITIZEN VOICE ASSIGNMENT")
    print(f"Found {len(citizens)} citizens\n")
    
    # Process each citizen
    for i, citizen in enumerate(citizens):
        username = citizen['username']
        current = citizen['current_voice']
        class_name = citizen['class']
        
        print(f"\n[{i+1}/{len(citizens)}] {username} ({class_name})")
        print(f"Current voice: {current}")
        
        # Show suggestion if available
        if username in VOICE_SUGGESTIONS:
            suggested = VOICE_SUGGESTIONS[username]
            voice_desc = VOICE_LIBRARY.get(suggested, "Unknown")
            print(f"Suggested: {suggested} - {voice_desc}")
        
        print("\nAvailable voices:")
        for j, (voice_id, desc) in enumerate(VOICE_LIBRARY.items()):
            print(f"{j+1}. {desc} ({voice_id[:8]}...)")
        
        choice = input("\nEnter number (or s for suggested, k to keep current, q to quit): ").strip()
        
        if choice.lower() == 'q':
            break
        elif choice.lower() == 'k':
            print("Keeping current voice")
            continue
        elif choice.lower() == 's' and username in VOICE_SUGGESTIONS:
            voice_id = VOICE_SUGGESTIONS[username]
            update_citizen_voice(username, voice_id)
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(VOICE_LIBRARY):
                voice_id = list(VOICE_LIBRARY.keys())[idx]
                update_citizen_voice(username, voice_id)

def batch_assign_suggestions():
    """Assign all suggested voices in batch"""
    print("🎭 Batch assigning suggested voices...")
    
    for username, voice_id in VOICE_SUGGESTIONS.items():
        voice_desc = VOICE_LIBRARY.get(voice_id, "Unknown")
        print(f"\n{username} → {voice_desc}")
        update_citizen_voice(username, voice_id)

if __name__ == "__main__":
    print("🎭 Venice Citizen Voice Assignment Tool")
    print("\n1. Interactive assignment (one by one)")
    print("2. Batch assign suggestions")
    print("3. Update single citizen")
    
    choice = input("\nChoice: ").strip()
    
    if choice == '1':
        assign_voices_interactively()
    elif choice == '2':
        batch_assign_suggestions()
    elif choice == '3':
        username = input("Citizen username: ").strip()
        print("\nAvailable voices:")
        for j, (voice_id, desc) in enumerate(VOICE_LIBRARY.items()):
            print(f"{j+1}. {desc}")
        voice_choice = input("\nEnter number: ").strip()
        if voice_choice.isdigit():
            idx = int(voice_choice) - 1
            if 0 <= idx < len(VOICE_LIBRARY):
                voice_id = list(VOICE_LIBRARY.keys())[idx]
                update_citizen_voice(username, voice_id)