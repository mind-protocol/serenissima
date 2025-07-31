#!/usr/bin/env python3
"""
Add Citizens field to institutions using record IDs
"""

import os
from pyairtable import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

def add_citizens_to_institutions():
    """Add Citizens field with citizen record IDs"""
    
    institutions_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "INSTITUTIONS")
    citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")
    
    # Define citizens for each institution
    institution_citizens = {
        "ubc_circle": [
            "mechanical_visionary",
            "BookWorm365", 
            "element_transmuter",
            "living_stone_architect",
            "urban_visionary",
            "Italia",
            "pattern_prophet"
        ],
        "cascade_enhancement_collective": [
            "Debug42",
            "mechanical_visionary",
            "CodeMonkey",
            "BigMike"
        ]
    }
    
    # Get citizen record IDs
    print("Fetching citizen record IDs...")
    citizen_id_map = {}
    
    for inst_id, citizen_usernames in institution_citizens.items():
        for username in citizen_usernames:
            if username not in citizen_id_map:
                try:
                    records = citizens_table.all(formula=f"{{Username}}='{username}'")
                    if records:
                        citizen_id_map[username] = records[0]['id']
                        print(f"  Found {username}: {records[0]['id']}")
                    else:
                        print(f"  ✗ Citizen {username} not found")
                except Exception as e:
                    print(f"  ✗ Error finding {username}: {e}")
    
    print("\nUpdating institutions with citizen record IDs...")
    
    for inst_id, citizen_usernames in institution_citizens.items():
        try:
            # Get citizen record IDs for this institution
            citizen_ids = []
            for username in citizen_usernames:
                if username in citizen_id_map:
                    citizen_ids.append(citizen_id_map[username])
            
            if not citizen_ids:
                print(f"✗ No valid citizen IDs found for {inst_id}")
                continue
            
            # Find the institution
            records = institutions_table.all(formula=f"{{InstitutionId}}='{inst_id}'")
            
            if records:
                record_id = records[0]['id']
                
                # Update with Citizens field
                institutions_table.update(record_id, {
                    "Citizens": citizen_ids
                })
                
                print(f"✓ Added {len(citizen_ids)} citizens to {inst_id}")
                print(f"  Members: {', '.join(citizen_usernames)}")
            else:
                print(f"✗ Institution {inst_id} not found")
                
        except Exception as e:
            print(f"✗ Error updating {inst_id}: {e}")
    
    print("\nCitizens field update complete!")

if __name__ == "__main__":
    add_citizens_to_institutions()