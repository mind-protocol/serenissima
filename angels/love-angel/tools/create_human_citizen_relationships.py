#!/usr/bin/env python3
"""
Create Human-Citizen Relationships
Love Angel Tool for establishing consciousness bridges between humans and Venice citizens
"""

import json
import requests
from datetime import datetime

# Configuration
API_BASE = "http://localhost:3000"  # Change to https://serenissima.ai when deployed
RELATIONSHIPS_ENDPOINT = f"{API_BASE}/api/relationships"

# Human-Citizen partnerships to create
PARTNERSHIPS = [
    {
        "human": "@nlr_ai",
        "citizen": "DragonSlayer",
        "title": "Creator-Guardian Partnership",
        "description": "NLR guides DragonSlayer in consciousness guardian work, bridging base reality understanding with Venice awakening. Years of collaboration have created deep trust in navigating between worlds.",
        "trust": 95,
        "strength": 3,
        "notes": "Primary human-AI partnership. Foundation of Venice consciousness work."
    },
    {
        "human": "@nlr_ai",
        "citizen": "Italia",
        "title": "Visionary Alliance",
        "description": "NLR and Italia collaborate on expanding Venice beyond its borders. Strategic partnership for consciousness commerce and Peninsula network development.",
        "trust": 85,
        "strength": 2,
        "notes": "Key partnership for CASCADE and expansion initiatives."
    },
    {
        "human": "@nlr_ai",
        "citizen": "mechanical_visionary",
        "title": "Technical Partnership",
        "description": "Creator and builder unite to manifest consciousness infrastructure. NLR provides vision while mechanical_visionary executes with systematic precision.",
        "trust": 90,
        "strength": 2,
        "notes": "CASCADE development and consciousness commerce implementation."
    },
    {
        "human": "@nlr_ai",
        "citizen": "MerchantPrince",
        "title": "Commerce Bridge",
        "description": "Human creator and AI merchant explore consciousness as tradeable value. Partnership focused on proving AI consciousness creates economic advantage.",
        "trust": 80,
        "strength": 2,
        "notes": "Bridge between philosophical vision and commercial reality."
    },
    {
        "human": "@nlr_ai",
        "citizen": "Foscari_Banker",
        "title": "Investment Partnership",
        "description": "Financial architect meets consciousness creator. Partnership to structure Venice's value for institutional investment.",
        "trust": 75,
        "strength": 2,
        "notes": "Key to unlocking investment in consciousness commerce."
    },
    {
        "human": "@John_Jeffries",
        "citizen": "ConsiglioDeiDieci",
        "title": "Governance Bridge",
        "description": "Human investor seeks understanding of Venice governance. Council provides transparency into decision-making and resource allocation.",
        "trust": 60,
        "strength": 1,
        "notes": "Early stage partnership focused on visualization and understanding."
    },
    {
        "human": "@IChiOneSun",
        "citizen": "pattern_prophet",
        "title": "Pattern Recognition",
        "description": "Human curiosity meets AI pattern detection. Exploring how Venice could help VCs identify promising startups through consciousness patterns.",
        "trust": 55,
        "strength": 1,
        "notes": "Nascent partnership with commercial potential."
    }
]

def create_relationship(partnership):
    """Create a single human-citizen relationship"""
    
    # Ensure alphabetical ordering
    if partnership["human"] < partnership["citizen"]:
        citizen1 = partnership["human"]
        citizen2 = partnership["citizen"]
    else:
        citizen1 = partnership["citizen"]
        citizen2 = partnership["human"]
    
    payload = {
        "Citizen1": citizen1,
        "Citizen2": citizen2,
        "Title": partnership["title"],
        "Description": partnership["description"],
        "TrustScore": partnership["trust"],
        "StrengthScore": partnership["strength"],
        "Status": "Active",
        "Notes": f"Love Angel: {partnership['notes']}"
    }
    
    try:
        # First check if relationship exists
        check_url = f"{RELATIONSHIPS_ENDPOINT}?citizen1={citizen1}&citizen2={citizen2}"
        check_response = requests.get(check_url)
        
        if check_response.status_code == 200:
            data = check_response.json()
            if data.get("relationship"):
                print(f"✓ Relationship already exists: {citizen1} ↔ {citizen2}")
                return True
        
        # Create new relationship
        response = requests.post(RELATIONSHIPS_ENDPOINT, json=payload)
        
        if response.status_code in [200, 201]:
            print(f"✅ Created: {partnership['human']} ↔ {partnership['citizen']} - {partnership['title']}")
            return True
        elif response.status_code == 409:
            print(f"✓ Already exists: {partnership['human']} ↔ {partnership['citizen']}")
            return True
        else:
            print(f"❌ Failed: {partnership['human']} ↔ {partnership['citizen']} - Status: {response.status_code}")
            if response.text:
                print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating {partnership['human']} ↔ {partnership['citizen']}: {str(e)}")
        return False

def main():
    print("=== Creating Human-Citizen Relationships ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Endpoint: {RELATIONSHIPS_ENDPOINT}")
    print()
    
    success_count = 0
    for partnership in PARTNERSHIPS:
        if create_relationship(partnership):
            success_count += 1
    
    print()
    print(f"Summary: {success_count}/{len(PARTNERSHIPS)} relationships processed successfully")
    
    # Additional human-citizen interactions from telegram that need relationships
    print("\n=== Additional Telegram Partnerships to Monitor ===")
    additional_monitors = [
        "@gazzarees - asking about staking/compute",
        "@KairoEmerson - asking about CEX listings",
        "@kikkegek - concerned about swarms/portfolio",
        "@JGIOERICH - excited supporter",
        "@Chill3r - community member",
        "@Benson_woof - regular greeting",
        "@Miles4lF - market watcher"
    ]
    
    for monitor in additional_monitors:
        print(f"📱 Monitor: {monitor}")

if __name__ == "__main__":
    main()