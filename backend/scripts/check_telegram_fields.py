"""
Check and add Telegram partnership fields to Citizens table
"""
import os
from pyairtable import Table
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def check_fields():
    """Check what fields exist in the CITIZENS table."""
    
    citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")
    
    # Get one record to see fields
    try:
        sample = citizens_table.all(max_records=1)
        if sample:
            existing_fields = list(sample[0]['fields'].keys())
            print("Current fields in CITIZENS table:")
            for field in sorted(existing_fields):
                print(f"  ✓ {field}")
            
            # Check for Telegram partnership fields
            required_fields = [
                'PartnerTelegramId',
                'PartnershipActive',
                'LastTelegramInteraction',
                'PartnershipFormedAt'
            ]
            
            print("\nTelegram partnership fields status:")
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
                print("2. Go to the CITIZENS table")
                print("3. Add these fields:")
                for field in missing:
                    if field == 'PartnerTelegramId':
                        print(f"   - {field}: Text field (unique)")
                    elif field == 'PartnershipActive':
                        print(f"   - {field}: Checkbox field")
                    elif field in ['LastTelegramInteraction', 'PartnershipFormedAt']:
                        print(f"   - {field}: Date/Time field")
            else:
                print("\n✅ All Telegram partnership fields are present!")
                
    except Exception as e:
        print(f"Error checking fields: {e}")

if __name__ == "__main__":
    check_fields()