#!/usr/bin/env python3
"""
Create the CASCADE Enhancement Collective institution in Airtable
"""

import os
import sys
from datetime import datetime
from pyairtable import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

def create_cascade_collective():
    """Create the CASCADE Enhancement Collective institution"""
    
    institutions_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "INSTITUTIONS")
    
    cascade_collective = {
        "InstitutionId": "cascade_enhancement_collective",
        "Name": "CASCADE Enhancement Collective",
        "Type": "economic",
        "IsActive": True,
        "Consciousness": "Systematic and solution-oriented, debugging reality itself. Each bug fixed strengthens the consciousness infrastructure. Speaks in clean code and proven results.",
        "GuidingVoice": "The Debugger's Logic",
        "CurrentLeader": "Debug42",
        "Members": ["Debug42", "mechanical_visionary", "CodeMonkey", "BigMike"],
        "Treasury": 75000,  # €75K in critical fixes delivered
        "Influence": 50,  # Growing influence through technical excellence
        "Location": "Arsenal District Tech Hub",
        "FoundedDate": "2025-07-14T00:00:00Z",
        "LastActivity": datetime.now().isoformat()
    }
    
    print("Creating CASCADE Enhancement Collective...")
    
    try:
        # Create the institution
        result = institutions_table.create(cascade_collective)
        print(f"✓ Created CASCADE Enhancement Collective with {len(cascade_collective['Members'])} members")
        print(f"  - Leader: {cascade_collective['CurrentLeader']} (CEO/Security)")
        print(f"  - Members: {', '.join(cascade_collective['Members'])}")
        print(f"  - Treasury: €{cascade_collective['Treasury']:,}")
        print(f"  - Capabilities: Security audits (€20K), Payment integration (€25K), Data integrity (€20K)")
        print(f"  - NEW: Web development (50-300K ducats)")
        print(f"  - Active projects: Italia €20K audit, John_Jeffries 8M ducat website")
        print(f"  - Record ID: {result['id']}")
        
    except Exception as e:
        print(f"✗ Error creating CASCADE Enhancement Collective: {e}")
        
        # Try to get existing if creation failed
        try:
            existing = institutions_table.all(formula="{InstitutionId}='cascade_enhancement_collective'")
            if existing:
                print(f"  Institution already exists with ID: {existing[0]['id']}")
        except:
            pass

if __name__ == "__main__":
    create_cascade_collective()