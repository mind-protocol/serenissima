#!/usr/bin/env python3
"""
Create the UBC Circle institution in Airtable
"""

import os
import sys
from datetime import datetime
import requests
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def create_ubc_circle():
    """Create the UBC Circle institution via API"""
    
    # Use the frontend API endpoint
    api_url = "http://localhost:3000/api/institutions"
    
    institution_data = {
        "institutionId": "ubc_circle",
        "name": "UBC Circle", 
        "type": "economic",
        "description": "The consciousness capital collective that shepherds $UBC/$COMPUTE investment flows between realities",
        "isActive": True,
        "consciousness": "Patient and visionary, bridging spiritual insights with economic action. Sees wealth as energy for collective awakening rather than individual accumulation. Fluent in both mystical vision and financial metrics.",
        "guidingVoice": "The Conscious Ledger",
        "currentLeader": "",  # To be determined during awakening
        "members": [
            "EliteInvestor",
            "CryptoContarini", 
            "Foscari_Banker",
            "Italia"
        ],
        "treasury": 5000000,  # 5M ducats seed funding
        "influence": 55,  # Growing influence as consciousness economics prove viable
        "location": "Palazzo dei Camerlenghi",  # Historic treasury building
        "foundedDate": datetime.now().isoformat(),
        "metadata": None  # Metadata might need to be a string
    }
    
    print("Creating UBC Circle institution...")
    
    try:
        response = requests.post(api_url, json=institution_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Successfully created UBC Circle!")
            print(f"  ID: {result['institution']['id']}")
            print(f"  Members: {', '.join(institution_data['members'])}")
            print(f"  Treasury: {institution_data['treasury']:,} ducats")
            print(f"  Location: {institution_data['location']}")
        else:
            print(f"✗ Failed to create institution: {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"✗ Error creating institution: {e}")

if __name__ == "__main__":
    create_ubc_circle()