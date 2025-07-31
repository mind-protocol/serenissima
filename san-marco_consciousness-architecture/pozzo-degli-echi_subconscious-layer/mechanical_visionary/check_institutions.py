#!/usr/bin/env python3
"""
Check institution records in Airtable for ubc_circle and cascade_enhancement_collective
"""
import os
import json
import requests
from datetime import datetime

# Airtable configuration - load from .env file
from dotenv import load_dotenv
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    print("Error: AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set in environment")
    exit(1)

# Headers for Airtable API
headers = {
    'Authorization': f'Bearer {AIRTABLE_API_KEY}',
    'Content-Type': 'application/json'
}

def fetch_institution_records():
    """Fetch institution records from Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/INSTITUTIONS"
    
    # Filter for our two institutions
    filter_formula = "OR({InstitutionId}='ubc_circle', {InstitutionId}='cascade_enhancement_collective')"
    
    params = {
        'filterByFormula': filter_formula
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('records', [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching institution records: {e}")
        return []

def analyze_institution_fields(records):
    """Analyze fields present in institution records"""
    print("=== INSTITUTION RECORDS ANALYSIS ===\n")
    
    # Expected fields based on typical institution structure
    expected_fields = [
        'InstitutionId',
        'Name',
        'Type',
        'Description',
        'Purpose',
        'Status',
        'Leader',
        'Members',
        'Location',
        'BuildingId',
        'Treasury',
        'Influence',
        'Reputation',
        'Activities',
        'Resources',
        'Contracts',
        'CreatedAt',
        'UpdatedAt',
        'Notes'
    ]
    
    for record in records:
        fields = record.get('fields', {})
        record_id = record.get('id', 'unknown')
        institution_id = fields.get('InstitutionId', 'unknown')
        
        print(f"Institution: {institution_id} (Record ID: {record_id})")
        print("=" * 50)
        
        # Show all existing fields
        print("\nExisting fields:")
        for field_name, field_value in sorted(fields.items()):
            if isinstance(field_value, (list, dict)):
                field_value = json.dumps(field_value, indent=2)
            print(f"  {field_name}: {field_value}")
        
        # Check for missing expected fields
        print("\nMissing expected fields:")
        missing_fields = []
        for expected_field in expected_fields:
            if expected_field not in fields:
                missing_fields.append(expected_field)
        
        if missing_fields:
            for field in missing_fields:
                print(f"  - {field}")
        else:
            print("  None - all expected fields present")
        
        print("\n" + "-" * 50 + "\n")
    
    return records

def main():
    """Main function"""
    print(f"Checking institution records at {datetime.now()}\n")
    
    # Fetch records
    records = fetch_institution_records()
    
    if not records:
        print("No institution records found for ubc_circle or cascade_enhancement_collective")
        return
    
    # Analyze fields
    analyzed_records = analyze_institution_fields(records)
    
    # Save raw data for reference
    with open('institution_records_raw.json', 'w') as f:
        json.dump(records, f, indent=2)
    
    print(f"\nRaw data saved to institution_records_raw.json")

if __name__ == "__main__":
    main()