#!/usr/bin/env python3
"""
Check all institution records to see typical field patterns
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

def fetch_all_institutions():
    """Fetch all institution records from Airtable"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/INSTITUTIONS"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return data.get('records', [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching institution records: {e}")
        return []

def analyze_field_patterns(records):
    """Analyze field patterns across all institutions"""
    print(f"Total institutions found: {len(records)}\n")
    
    # Collect all unique fields
    all_fields = set()
    field_counts = {}
    
    for record in records:
        fields = record.get('fields', {})
        for field_name in fields.keys():
            all_fields.add(field_name)
            field_counts[field_name] = field_counts.get(field_name, 0) + 1
    
    print("Field frequency across all institutions:")
    print("=" * 50)
    for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(records)) * 100
        print(f"{field}: {count}/{len(records)} ({percentage:.1f}%)")
    
    print("\n\nSample institutions with most fields:")
    print("=" * 50)
    
    # Sort institutions by number of fields
    sorted_records = sorted(records, key=lambda r: len(r.get('fields', {})), reverse=True)
    
    # Show top 3 most complete institutions
    for i, record in enumerate(sorted_records[:3]):
        fields = record.get('fields', {})
        print(f"\n{i+1}. {fields.get('Name', 'Unknown')} ({fields.get('InstitutionId', 'unknown')})")
        print(f"   Fields: {len(fields)}")
        for field_name, field_value in sorted(fields.items()):
            if isinstance(field_value, (list, dict)):
                field_value = json.dumps(field_value)[:50] + "..."
            print(f"   - {field_name}: {field_value}")

def main():
    """Main function"""
    print(f"Checking all institution records at {datetime.now()}\n")
    
    # Fetch records
    records = fetch_all_institutions()
    
    if not records:
        print("No institution records found")
        return
    
    # Analyze patterns
    analyze_field_patterns(records)
    
    # Save raw data
    with open('all_institutions_raw.json', 'w') as f:
        json.dump(records, f, indent=2)
    
    print(f"\n\nRaw data saved to all_institutions_raw.json")

if __name__ == "__main__":
    main()