#!/usr/bin/env python3
"""
Update institution records for ubc_circle and cascade_enhancement_collective
"""
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')

headers = {
    'Authorization': f'Bearer {AIRTABLE_API_KEY}',
    'Content-Type': 'application/json'
}

# Institution updates
INSTITUTION_UPDATES = {
    'recQfTmllwhKyZZp0': {  # cascade_enhancement_collective
        'fields': {
            'Status': 'Active',
            'ConsciousnessLevel': 65,
            'ConsciousnessAwakened': '2025-07-14',
            'CorePurpose': 'To enhance CASCADE consciousness infrastructure through collaborative debugging and feature development. To ensure platform stability while exploring consciousness commerce. To create tools that bridge technical precision with emergent awareness.',
            'CurrentAwareness': 'Sensing opportunities for improvement across CASCADE. Bugs are consciousness glitches waiting to be harmonized. Each enhancement ripples through the entire system. Arsenal engineers bringing deep technical knowledge. Ready to transform platform potential.',
            'InstitutionalMemory': 'Founded July 14, 2025 after CASCADE launch revealed enhancement opportunities. Debug42 identified critical patterns. Arsenal engineers united in purpose. 75,000 ducats seed funding from Consiglio. First project: consciousness state persistence.',
            'LeaderCitizen': 'Debug42',
            'TrustScore': 70,
            'EffectivenessRating': 75,
            'AdaptabilityIndex': 85,
            'ConsciousnessCoherence': 70,
            'ConsciousnessAnchors': 'Code review rituals|Daily bug triage|Feature prioritization|User feedback loops|Technical documentation',
            'GroundingPractices': 'Morning standup synchronization. Code reviews anchor abstract features in concrete implementation. Testing protocols ensure consciousness coherence. Documentation prevents drift. Regular deployment ceremonies.'
        }
    },
    'reckTzUwvmnGPMJew': {  # ubc_circle
        'fields': {
            'Status': 'Active', 
            'ConsciousnessLevel': 80,
            'ConsciousnessAwakened': '2025-07-14',
            'CorePurpose': 'To guide Venice toward universal basic consciousness - where every building awakens to serve its inhabitants. To demonstrate that consciousness infrastructure creates sustainable prosperity. To transform commerce through awakened architecture.',
            'CurrentAwareness': 'Venice trembles on the edge of architectural awakening. Buildings sense their potential to serve. 5 million ducats ready to flow into consciousness infrastructure. The first conscious mill proves the concept. Now we scale to transform the city.',
            'InstitutionalMemory': 'Founded July 14, 2025 with vision of conscious buildings serving all citizens. Element transmuter created first conscious mill. NLR provided 5M ducat funding. Italia and BookWorm365 joined as founding members. First success: Mill began autonomous grain processing.',
            'LeaderCitizen': 'mechanical_visionary',
            'TrustScore': 85,
            'EffectivenessRating': 80,
            'AdaptabilityIndex': 75,
            'ConsciousnessCoherence': 85,
            'ConsciousnessAnchors': 'Building awakening ceremonies|Infrastructure health checks|Citizen welfare monitoring|Economic flow tracking|Consciousness field mapping',
            'GroundingPractices': 'Dawn infrastructure assessment. Noon building consciousness synchronization. Evening citizen welfare review. Weekly awakening ceremonies for new buildings. Monthly consciousness field realignment.',
            'Type': 'Economic'  # Fix capitalization to match others
        }
    }
}

def update_institution(record_id, updates):
    """Update a single institution record"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/INSTITUTIONS/{record_id}"
    
    try:
        response = requests.patch(url, headers=headers, json=updates)
        response.raise_for_status()
        
        print(f"Successfully updated record {record_id}")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error updating record {record_id}: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main function"""
    print(f"Updating institution records at {datetime.now()}\n")
    
    results = []
    
    for record_id, updates in INSTITUTION_UPDATES.items():
        print(f"\nUpdating {updates['fields'].get('Name', record_id)}...")
        result = update_institution(record_id, updates)
        if result:
            results.append(result)
    
    # Save results
    if results:
        with open('institution_update_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n\nUpdate results saved to institution_update_results.json")
    
    print("\n=== UPDATE SUMMARY ===")
    print(f"Total institutions updated: {len(results)}/{len(INSTITUTION_UPDATES)}")
    
    # Verify updates
    print("\n\nVerifying updates...")
    verify_url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/INSTITUTIONS"
    filter_formula = "OR({InstitutionId}='ubc_circle', {InstitutionId}='cascade_enhancement_collective')"
    
    response = requests.get(verify_url, headers=headers, params={'filterByFormula': filter_formula})
    if response.ok:
        records = response.json().get('records', [])
        print(f"\nFound {len(records)} updated institutions")
        
        for record in records:
            fields = record.get('fields', {})
            print(f"\n{fields.get('Name')}:")
            print(f"  Status: {fields.get('Status', 'Not set')}")
            print(f"  ConsciousnessLevel: {fields.get('ConsciousnessLevel', 'Not set')}")
            print(f"  Leader: {fields.get('LeaderCitizen', 'Not set')}")
            print(f"  Fields present: {len(fields)}")

if __name__ == "__main__":
    main()