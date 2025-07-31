#!/usr/bin/env python3
"""
Create the CASCADE Enhancement Collective institution in Airtable with minimal fields
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
    
    # Start with minimal required fields
    cascade_collective = {
        "InstitutionId": "cascade_enhancement_collective",
        "Name": "CASCADE Enhancement Collective",
        "Type": "economic"
    }
    
    print("Creating CASCADE Enhancement Collective with minimal fields...")
    
    try:
        # Create the institution
        result = institutions_table.create(cascade_collective)
        print(f"✓ Created CASCADE Enhancement Collective")
        print(f"  - Record ID: {result['id']}")
        print("\nNow updating with additional fields...")
        
        # Try to update with additional fields one by one
        optional_fields = [
            ("CurrentLeader", "Debug42"),
            ("Members", ["Debug42", "mechanical_visionary", "CodeMonkey", "BigMike"]),
            ("Treasury", 75000),
            ("Influence", 50),
            ("Location", "Arsenal District Tech Hub"),
            ("FoundedDate", "2025-07-14T00:00:00Z"),
            ("LastActivity", datetime.now().isoformat()),
            ("Consciousness", "Systematic and solution-oriented, debugging reality itself."),
            ("GuidingVoice", "The Debugger's Logic")
        ]
        
        for field_name, field_value in optional_fields:
            try:
                institutions_table.update(result['id'], {field_name: field_value})
                print(f"  ✓ Added {field_name}")
            except Exception as e:
                print(f"  ✗ Could not add {field_name}: {e}")
        
        print("\nCASCADE Enhancement Collective created successfully!")
        print(f"  - Members: Debug42 (CEO/Security), mechanical_visionary (Backend), CodeMonkey (Frontend), BigMike (Performance)")
        print(f"  - Treasury: €75,000")
        print(f"  - Services: Security audits (€20K), Payment integration (€25K), Web development (50-300K ducats)")
        
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