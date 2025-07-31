#!/usr/bin/env python3
"""
Create UBC Circle directly in Airtable
"""

import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

def create_ubc_direct():
    """Create UBC Circle directly via Airtable API"""
    
    institutions_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "INSTITUTIONS")
    
    # Only use fields that exist in current institutions
    institution_data = {
        "Name": "UBC Circle",
        "Type": "Economic",
        "GuidingVoice": "The Conscious Ledger",
        "Treasury": 5000000,
        "FoundedDate": "2025-07-14"
    }
    
    print("Creating UBC Circle directly in Airtable...")
    
    try:
        result = institutions_table.create(institution_data)
        print(f"✓ Successfully created UBC Circle!")
        print(f"  Record ID: {result['id']}")
        print(f"  Name: {result['fields']['Name']}")
        print(f"  Treasury: {result['fields']['Treasury']:,} ducats")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    create_ubc_direct()