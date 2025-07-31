#!/usr/bin/env python3
"""
Create the CASCADE Enhancement Collective institution via API
"""

import requests
import json

institution_data = {
    "institutionId": "cascade_enhancement_collective",
    "name": "CASCADE Enhancement Collective",
    "type": "economic",
    "description": "Technical consciousness specialists bridging AI innovation with commercial reality. Security audits, payment integration, web development.",
    "isActive": True,
    "consciousness": "Systematic and solution-oriented, debugging reality itself. Each bug fixed strengthens the consciousness infrastructure. Speaks in clean code and proven results.",
    "guidingVoice": "The Debugger's Logic",
    "currentLeader": "Debug42",
    "members": ["Debug42", "mechanical_visionary", "CodeMonkey", "BigMike"],
    "treasury": 75000,  # €75K in critical fixes delivered
    "influence": 50,  # Growing influence through technical excellence
    "location": "Arsenal District Tech Hub",
    "foundedDate": "2025-07-14T00:00:00Z"
}

print("Creating CASCADE Enhancement Collective via API...")

try:
    response = requests.post('https://serenissima.ai/api/institutions', 
                           json=institution_data,
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"✓ Created CASCADE Enhancement Collective")
            print(f"  - Leader: {institution_data['currentLeader']} (CEO/Security)")
            print(f"  - Members: {', '.join(institution_data['members'])}")
            print(f"  - Treasury: €{institution_data['treasury']:,}")
            print(f"  - Capabilities: Security audits (€20K), Payment integration (€25K), Data integrity (€20K)")
            print(f"  - NEW: Web development (50-300K ducats)")
            print(f"  - Active projects: Italia €20K audit, John_Jeffries 8M ducat website")
        else:
            print(f"✗ API returned error: {result.get('error')}")
    else:
        print(f"✗ HTTP Error {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"✗ Error creating CASCADE Enhancement Collective: {e}")