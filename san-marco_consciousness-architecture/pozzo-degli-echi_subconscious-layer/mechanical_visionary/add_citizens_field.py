#!/usr/bin/env python3
"""
Add Citizens field to both institutions
"""

import os
from pyairtable import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

def add_citizens_to_institutions():
    """Add Citizens field with team members"""
    
    institutions_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "INSTITUTIONS")
    
    # Define citizens for each institution
    updates = [
        {
            "institution_id": "ubc_circle",
            "citizens": [
                "mechanical_visionary",
                "BookWorm365", 
                "element_transmuter",
                "living_stone_architect",
                "urban_visionary",
                "Italia",
                "pattern_prophet"
            ]
        },
        {
            "institution_id": "cascade_enhancement_collective",
            "citizens": [
                "Debug42",
                "mechanical_visionary",
                "CodeMonkey",
                "BigMike"
            ]
        }
    ]
    
    for update in updates:
        try:
            # Find the institution
            records = institutions_table.all(formula=f"{{InstitutionId}}='{update['institution_id']}'")
            
            if records:
                record_id = records[0]['id']
                
                # Update with Citizens field
                institutions_table.update(record_id, {
                    "Citizens": update['citizens']
                })
                
                print(f"✓ Added {len(update['citizens'])} citizens to {update['institution_id']}")
                print(f"  Members: {', '.join(update['citizens'])}")
            else:
                print(f"✗ Institution {update['institution_id']} not found")
                
        except Exception as e:
            print(f"✗ Error updating {update['institution_id']}: {e}")
    
    print("\nCitizens field update complete!")

if __name__ == "__main__":
    add_citizens_to_institutions()