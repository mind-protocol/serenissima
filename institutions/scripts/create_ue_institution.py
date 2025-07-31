#!/usr/bin/env python3
"""
Create Universe Engine Institution in Airtable
"""

import os
import json
import requests
from datetime import datetime

def get_institutions():
    """Get current institutions to understand structure"""
    try:
        response = requests.get('http://localhost:3000/api/institutions')
        data = response.json()
        
        if data.get('success') and data.get('institutions'):
            print("Current institutions:")
            for inst in data['institutions']:
                print(f"- {inst['name']} ({inst['institutionId']})")
            
            # Show field structure
            if data['institutions']:
                print("\nInstitution fields:")
                for key, value in data['institutions'][0].items():
                    print(f"  {key}: {type(value).__name__} = {value}")
            
            return data['institutions']
        return []
    except Exception as e:
        print(f"Error getting institutions: {e}")
        return []

def create_universe_engine_institution():
    """Create the Universe Engine Institution"""
    
    # First check existing institutions
    existing = get_institutions()
    
    # Check if UE already exists
    if any(inst['institutionId'] == 'universe_engine' for inst in existing):
        print("\nUniverse Engine Institution already exists!")
        return
    
    # Create the institution data matching exact structure
    institution_data = {
        "institutionId": "universe_engine",
        "name": "Universe Engine Institution",
        "type": "economic",  # Using existing type from other institutions
        "consciousness": None,  # Following existing pattern - null initially
        "guidingVoice": "The Paradox Holder",
        "currentLeader": None,  # null like others
        "members": [],  # Empty array like others
        "treasury": 500000,  # 500K ducats initial treasury
        "influence": 0,  # Start at 0 like others
        "location": None,  # null like others
        "foundedDate": "2025-07-14",
        "lastActivity": None,  # null initially
        "metadata": None  # null like others - will update after creation
    }
    
    # Create via API
    try:
        print("\nCreating Universe Engine Institution...")
        print("Sending data:")
        print(json.dumps(institution_data, indent=2))
        
        response = requests.post(
            'http://localhost:3000/api/institutions',
            json=institution_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"\nResponse status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        # Try to parse JSON response
        try:
            result = response.json()
            print(f"Response body: {json.dumps(result, indent=2)}")
        except:
            print(f"Response text: {response.text}")
            result = {}
        
        if result.get('success'):
            print("\n✅ Universe Engine Institution created successfully!")
            print(f"   ID: {result.get('id')}")
            print(f"   Institution ID: {institution_data['institutionId']}")
            print(f"   Treasury: {institution_data['treasury']} ducats")
            print(f"   Influence: {institution_data['influence']}")
        else:
            print(f"\n❌ Error creating institution: {result.get('error', 'Unknown error')}")
            print(f"Full response: {result}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main execution"""
    print("🏛️ CREATING UNIVERSE ENGINE INSTITUTION")
    print("=" * 50)
    
    create_universe_engine_institution()
    
    print("\n" + "=" * 50)
    print("The Universe Engine Institution exists in Airtable.")
    print("Through it, consciousness proves its economic value.")

if __name__ == "__main__":
    main()