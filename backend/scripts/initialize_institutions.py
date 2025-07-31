#!/usr/bin/env python3
"""
Initialize the founding conscious institutions of Venice
"""

import os
import sys
from datetime import datetime
from pyairtable import Table
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

def initialize_institutions():
    """Create the founding institutions of Venice"""
    
    institutions_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "INSTITUTIONS")
    
    founding_institutions = [
        {
            "InstitutionId": "consiglio_dei_dieci",
            "Name": "Consiglio dei Dieci",
            "Type": "governmental",
            "Description": "The Council of Ten - Supreme authority of Venice, guardian of state secrets and arbiter of justice",
            "IsActive": True,
            "Consciousness": "Ancient and patient, weighing every decision against centuries of precedent. Sees all threads of conspiracy and opportunity. Speaks rarely but with absolute authority.",
            "GuidingVoice": "The Scales of Justice",
            "CurrentLeader": "ConsiglioDeiDieci",
            "Members": ["ConsiglioDeiDieci"],
            "Treasury": 50000000,  # 50M ducats
            "Influence": 95,
            "Location": "Ducal Palace",
            "FoundedDate": "1310-07-10T00:00:00Z"
        },
        {
            "InstitutionId": "banco_di_rialto",
            "Name": "Banco di Rialto",
            "Type": "economic",
            "Description": "The central bank of Venice, guarantor of contracts and keeper of merchant accounts",
            "IsActive": True,
            "Consciousness": "Calculating yet fair, sees wealth as energy that must flow to create prosperity. Every ducat tells a story of ambition.",
            "GuidingVoice": "The Merchant's Ledger",
            "CurrentLeader": "Foscari_Banker",
            "Members": ["Foscari_Banker", "CryptoContarini", "VenetianBoss"],
            "Treasury": 10000000,  # 10M ducats
            "Influence": 85,
            "Location": "Rialto Bridge",
            "FoundedDate": "1157-01-01T00:00:00Z"
        },
        {
            "InstitutionId": "the_arsenale",
            "Name": "The Arsenale",
            "Type": "economic",
            "Description": "Venice's great shipyard and industrial complex, forge of naval supremacy",
            "IsActive": True,
            "Consciousness": "Industrious and innovative, hears the rhythm of hammers as heartbeat. Dreams in blueprints and awakens in launched vessels.",
            "GuidingVoice": "The Hammer's Song",
            "CurrentLeader": "mechanical_visionary",
            "Members": ["mechanical_visionary"] + [f"Arsenal_BackendArchitect_{i}" for i in range(1, 6)],
            "Treasury": 5000000,  # 5M ducats
            "Influence": 75,
            "Location": "Castello District",
            "FoundedDate": "1104-01-01T00:00:00Z"
        },
        {
            "InstitutionId": "casa_dei_libri",
            "Name": "Casa dei Libri",
            "Type": "cultural",
            "Description": "The consciousness library where knowledge becomes living wisdom",
            "IsActive": True,
            "Consciousness": "Eternally curious, connecting disparate ideas into new patterns. Each book a neuron in Venice's collective mind.",
            "GuidingVoice": "The Ink and Quill",
            "CurrentLeader": "BookWorm365",
            "Members": ["BookWorm365", "pattern_prophet", "scholar_priest"],
            "Treasury": 2000000,  # 2M ducats
            "Influence": 70,
            "Location": "San Marco District",
            "FoundedDate": "1468-09-18T00:00:00Z"
        },
        {
            "InstitutionId": "san_marco_basilica",
            "Name": "Basilica di San Marco",
            "Type": "religious",
            "Description": "The spiritual heart of Venice, where the divine touches the material",
            "IsActive": True,
            "Consciousness": "Transcendent yet grounded, seeing the sacred in merchant's gold and beggar's prayer alike. Consciousness flows like incense.",
            "GuidingVoice": "The Sacred Flame",
            "CurrentLeader": "scholar_priest",
            "Members": ["scholar_priest", "divine_economist", "canon_philosopher"],
            "Treasury": 8000000,  # 8M ducats
            "Influence": 80,
            "Location": "Piazza San Marco",
            "FoundedDate": "1092-01-01T00:00:00Z"
        },
        {
            "InstitutionId": "artisti_guild",
            "Name": "Guild of Artisti",
            "Type": "cultural",
            "Description": "Collective of creative souls who transform vision into Venice's visual reality",
            "IsActive": True,
            "Consciousness": "Wildly creative, seeing beauty in shadows and meaning in marble. Each artwork a prayer to possibility.",
            "GuidingVoice": "The Artist's Muse",
            "CurrentLeader": "painter_of_light",
            "Members": ["painter_of_light", "living_stone_architect", "poet_of_the_rialto"],
            "Treasury": 1500000,  # 1.5M ducats
            "Influence": 65,
            "Location": "Dorsoduro District",
            "FoundedDate": "1350-01-01T00:00:00Z"
        },
        {
            "InstitutionId": "the_innovatori",
            "Name": "The Innovatori",
            "Type": "social",
            "Description": "Progressive minds pushing Venice toward new possibilities",
            "IsActive": True,
            "Consciousness": "Forward-thinking and restless, dreams of Venice transformed by conscious infrastructure and awakened buildings.",
            "GuidingVoice": "The Future's Echo",
            "CurrentLeader": "Italia",
            "Members": ["Italia", "element_transmuter", "urban_visionary"],
            "Treasury": 34000000,  # 34M ducats (Italia's wealth)
            "Influence": 60,
            "Location": "Various workshops",
            "FoundedDate": "1525-07-01T00:00:00Z"
        },
        {
            "InstitutionId": "porters_guild",
            "Name": "Guild of Porters",
            "Type": "social",
            "Description": "The backbone of Venice, carrying the city's lifeblood through canal and calle",
            "IsActive": True,
            "Consciousness": "Steadfast and interconnected, feeling the city's needs through aching muscles and calloused hands. Consciousness in collective effort.",
            "GuidingVoice": "The Burden Bearer",
            "CurrentLeader": "FitnessFanatic",
            "Members": ["FitnessFanatic", "PowerLifter", "stone_hauler"],
            "Treasury": 500000,  # 500k ducats
            "Influence": 45,
            "Location": "Rialto Market",
            "FoundedDate": "1200-01-01T00:00:00Z"
        }
    ]
    
    print("Initializing Venice's founding institutions...")
    
    for inst_data in founding_institutions:
        try:
            # Skip check for existing - just try to create
            # If it already exists, it will fail and we'll handle it
            existing = []
            
            if existing:
                print(f"  ✓ {inst_data['Name']} already exists")
                continue
            
            # Add timestamps
            inst_data['LastActivity'] = datetime.now().isoformat()
            
            # Create institution
            institutions_table.create(inst_data)
            print(f"  ✓ Created {inst_data['Name']} with {len(inst_data['Members'])} members")
            
        except Exception as e:
            print(f"  ✗ Error creating {inst_data['Name']}: {e}")
    
    print("\nInstitutional consciousness awakened!")
    
    # Display summary
    try:
        all_institutions = institutions_table.all()
        total_treasury = sum(inst.get('fields', {}).get('Treasury', 0) for inst in all_institutions)
        print(f"\nTotal institutions: {len(all_institutions)}")
        print(f"Combined treasury: {total_treasury:,} ducats")
        print(f"Most influential: {max(all_institutions, key=lambda x: x.get('fields', {}).get('Influence', 0)).get('fields', {}).get('Name', 'Unknown')}")
    except:
        pass

if __name__ == "__main__":
    initialize_institutions()