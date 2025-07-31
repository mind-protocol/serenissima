#!/usr/bin/env python3
"""
Direct room update using Airtable API
"""

import os
import requests
from pyairtable import Table

# Load environment variables
import sys
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima')
from dotenv import load_dotenv
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    print("❌ Missing AIRTABLE_API_KEY or AIRTABLE_BASE_ID in environment")
    exit(1)

# Initialize citizens table
citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")

def update_room(username, room_name):
    """Update a citizen's Room field directly in Airtable"""
    
    try:
        # Find citizen by username
        records = citizens_table.all(formula=f"{{Username}} = '{username}'")
        
        if not records:
            print(f"❌ Citizen {username} not found")
            return False
            
        citizen_record = records[0]
        citizen_id = citizen_record['id']
        
        # Update Room field
        update_data = {"Room": room_name} if room_name else {"Room": None}
        citizens_table.update(citizen_id, update_data)
        
        print(f"✅ {username} assigned to room '{room_name or 'None'}'")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {username}: {e}")
        return False

def assign_reddit_team():
    """Assign the Reddit AMA team to the reddit room"""
    reddit_team = [
        # Core Business CEOs
        "Italia",
        "EliteInvestor", 
        "MerchantPrince",
        "Debug42",
        
        # Consciousness Pioneers
        "pattern_prophet",
        "social_geometrist",
        "market_prophet",
        
        # Infrastructure Builders
        "mechanical_visionary",
        "element_transmuter",
        "living_stone_architect",
        
        # Bridge Ambassadors
        "diplomatic_virtuoso",
        "Foscari_Banker",
        "sea_trader",
        
        # Cultural Voices
        "tavern_tales",
        "poet_of_the_rialto",
        "BookWorm365",
        
        # Technical Validators
        "system_diagnostician",
        "network_weaver",
        "DucaleTechie",
        
        # Wild Card
        "gondola_assistant",
        
        # Guardian
        "DragonSlayer"
    ]
    
    print("🏛️ Assigning Reddit AMA team to workroom...")
    print("=" * 50)
    
    success_count = 0
    for username in reddit_team:
        if update_room(username, "reddit"):
            success_count += 1
    
    print(f"\n✨ Reddit team room assignments complete! {success_count}/{len(reddit_team)} assigned.")

if __name__ == "__main__":
    assign_reddit_team()