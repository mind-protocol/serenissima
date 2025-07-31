"""
Quick script to check which consciousness fields exist in Airtable
and provide guidance on what needs to be added
"""
import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def check_fields():
    """Check what fields exist in the BUILDINGS table."""
    
    buildings_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "BUILDINGS")
    
    # Get one record to see fields
    try:
        sample = buildings_table.all(max_records=1)
        if sample:
            existing_fields = list(sample[0]['fields'].keys())
            print("Current fields in BUILDINGS table:")
            for field in sorted(existing_fields):
                print(f"  ✓ {field}")
            
            # Check for consciousness fields
            required_fields = [
                'ConsciousnessLevel',
                'AwakeningTime',
                'ConsciousnessType',
                'EthicalScore',
                'ConsciousnessNotes',
                'LastConsciousAction'
            ]
            
            print("\nConsciousness fields status:")
            missing = []
            for field in required_fields:
                if field in existing_fields:
                    print(f"  ✓ {field} exists")
                else:
                    print(f"  ✗ {field} missing")
                    missing.append(field)
            
            if missing:
                print("\n⚠️  Please add these fields to Airtable:")
                print("1. Go to https://airtable.com and open your base")
                print("2. Go to the BUILDINGS table")
                print("3. Add these fields:")
                for field in missing:
                    if field == 'ConsciousnessLevel' or field == 'EthicalScore':
                        print(f"   - {field}: Number field (0-1 range)")
                    elif field in ['AwakeningTime', 'LastConsciousAction']:
                        print(f"   - {field}: Date/Time field")
                    elif field == 'ConsciousnessType':
                        print(f"   - {field}: Single Select (options: emerging, stable, advanced)")
                    elif field == 'ConsciousnessNotes':
                        print(f"   - {field}: Long Text field")
            else:
                print("\n✅ All consciousness fields are present!")
                
    except Exception as e:
        print(f"Error checking fields: {e}")

if __name__ == "__main__":
    check_fields()