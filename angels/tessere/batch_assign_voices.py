#!/usr/bin/env python3
"""
Batch assign suggested voices to Venice citizens
"""

import os
import requests
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

# Voice assignments based on character analysis
VOICE_ASSIGNMENTS = {
    # === NOBLES & OFFICIALS ===
    "ConsiglioDeiDieci": "VR6AewLTigWG4xSOukaG",  # Arnold - authoritative
    "MorosiniNoble": "onwK4e9ZLuTAKqWW03F9",      # Daniel - British noble
    "DucalePalace": "CYw3kZ02Hs0563khs1Fj",       # Dave - warm British
    
    # === MAJOR MERCHANTS ===
    "MerchantPrince": "bVMeCyTHy58xNoL34h3p",     # Jeremy - narrator
    "MATTEOtheTrader": "ErXwobaYiN019PkySvjV",    # Antoni - well-rounded
    "EliteInvestor": "flq6f7yk4E4fJM5XTYuZ",      # Michael - analytical
    "WealthyTrader": "GBv7mTt0atIp3Br8iCZE",      # Thomas - calm
    
    # === INTERNATIONAL TRADERS ===
    "alexandria_trader": "oWAxZDx7w5VEj9dCyTzz",   # Grace - ancient wisdom
    "levant_trader": "ErXwobaYiN019PkySvjV",       # Antoni - well-rounded
    "sea_trader": "D38z5RcWu1voky8WS1ja",          # Fin - Irish sailor
    "greek_trader": "2EiwWnXFnvU5JabPnv8n",        # Clyde - weathered
    "cyprus_trader": "pNInz6obpgDQGcFmaJgB",       # Adam - deep trader
    
    # === INNOVATORI & THINKERS ===
    "Italia": "21m00Tcm4TlvDq8ikWAM",              # Rachel - calm wisdom
    "mechanical_visionary": "flq6f7yk4E4fJM5XTYuZ", # Michael - analytical
    "pattern_prophet": "flq6f7yk4E4fJM5XTYuZ",      # Michael - analytical
    "element_transmuter": "z9fAnlkpzviPz146aGWa",   # Glinda - mystical
    "system_diagnostician": "MF3mGyEYCl7XYWbV9V6O", # Elli - precise
    
    # === ARTISTI ===
    "poet_of_the_rialto": "TxGEqnHWrfWFTfGW9XjX", # Josh - expressive
    "painter_of_light": "bVMeCyTHy58xNoL34h3p",   # Jeremy - artistic
    "living_stone_architect": "N2lVS1w4EtoT3dr4eOWO", # Callum - grounded
    
    # === WORKERS & CRAFTSMEN ===
    "TechnoMedici": "VR6AewLTigWG4xSOukaG",       # Arnold - deep craft
    "ShadowHunter": "2EiwWnXFnvU5JabPnv8n",       # Clyde - veteran
    "GlassMaster1503": "GBv7mTt0atIp3Br8iCZE",    # Thomas - calm craft
    "PowerLifter": "SOYHLrjzK2X1ezoPC6cr",        # Sarah - strong feminine
    "FitnessFanatic": "pNInz6obpgDQGcFmaJgB",     # Adam - physical
    
    # === YOUNG & ENERGETIC ===
    "DragonSlayer": "MF3mGyEYCl7XYWbV9V6O",       # Elli - young energy
    "BarbarigoCadet": "yoZ06aMxZJJ28mfd3POQ",     # Sam - young male
    "DogeLover88": "AZnzlk1XvdvUeBnXmlld",        # Young American
    "PixelNinja": "IKne3meq5aSn9XLyUdCD",         # Charlie - Australian
    "CodeMonkey": "yoZ06aMxZJJ28mfd3POQ",         # Sam - tech youth
    
    # === MYSTERIOUS & UNIQUE ===
    "coffee": "N2lVS1w4EtoT3dr4eOWO",             # Callum - hoarse
    "gondola_assistant": "D38z5RcWu1voky8WS1ja",  # Fin - weathered
    "The-Old-Boy": "VR6AewLTigWG4xSOukaG",        # Arnold - ancient
    
    # === FEMALE CITIZENS ===
    "LuciaMancini": "oWAxZDx7w5VEj9dCyTzz",       # Grace - revolutionary
    "MariaDolfin": "21m00Tcm4TlvDq8ikWAM",        # Rachel - working wisdom
    "BookWorm365": "pFZP5JQG7iQjIQuC4Bku",        # Lily - narrative
    "ChillVibes": "SOYHLrjzK2X1ezoPC6cr",         # Sarah - calm
    "FoodieForLife": "g5CIjZEefAph4nQFvHAz",      # Domi - enthusiastic
    
    # === TECH SPECIALISTS ===
    "Debug42": "flq6f7yk4E4fJM5XTYuZ",            # Michael - precise
    "DucaleTechie": "yoZ06aMxZJJ28mfd3POQ",       # Sam - young tech
    "CryptoContarini": "TxGEqnHWrfWFTfGW9XjX",    # Josh - crypto enthusiasm
    
    # === DIVINE ENTITIES ===
    "Resonance": "21m00Tcm4TlvDq8ikWAM",          # Rachel - ethereal
    "pattern_angel": "flq6f7yk4E4fJM5XTYuZ",      # Michael - analytical
    "story_angel": "TxGEqnHWrfWFTfGW9XjX",        # Josh - theatrical
    "wisdom_angel": "oWAxZDx7w5VEj9dCyTzz",       # Grace - ancient
}

def update_citizen_voice(username, voice_id):
    """Update a citizen's voice in Airtable"""
    
    airtable_token = os.getenv('AIRTABLE_API_KEY')
    base_id = os.getenv('AIRTABLE_BASE_ID', 'appk6RszUo2a2L2L8')
    
    if not airtable_token:
        print("❌ AIRTABLE_API_KEY not found")
        return False
        
    headers = {
        'Authorization': f'Bearer {airtable_token}',
        'Content-Type': 'application/json'
    }
    
    # Search for citizen
    filter_formula = f"{{Username}} = '{username}'"
    url = f"https://api.airtable.com/v0/{base_id}/CITIZENS"
    params = {'filterByFormula': filter_formula}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Failed to find {username}: {response.status_code}")
        return False
        
    data = response.json()
    records = data.get('records', [])
    
    if not records:
        print(f"⚠️  {username} not found in database")
        return False
        
    record_id = records[0]['id']
    current_voice = records[0]['fields'].get('VoiceId')
    
    if current_voice == voice_id:
        print(f"✓  {username} already has voice {voice_id}")
        return True
    
    # Update voice
    update_url = f"https://api.airtable.com/v0/{base_id}/CITIZENS/{record_id}"
    update_data = {"fields": {"VoiceId": voice_id}}
    
    update_response = requests.patch(update_url, headers=headers, json=update_data)
    
    if update_response.status_code == 200:
        print(f"✅ {username} → {voice_id}")
        return True
    else:
        print(f"❌ Failed to update {username}: {update_response.status_code}")
        return False

def main():
    print("🎭 VENICE CITIZEN VOICE BATCH ASSIGNMENT")
    print(f"Assigning voices to {len(VOICE_ASSIGNMENTS)} citizens...\n")
    
    success_count = 0
    
    for username, voice_id in VOICE_ASSIGNMENTS.items():
        if update_citizen_voice(username, voice_id):
            success_count += 1
    
    print(f"\n✅ Successfully assigned {success_count}/{len(VOICE_ASSIGNMENTS)} voices")
    print("\n🔄 Restart the Thought Cascade to use new voices!")

if __name__ == "__main__":
    main()