#!/usr/bin/env python3
"""
Check exact field names in Airtable INSTITUTIONS table
"""

import os
from pyairtable import Table
from dotenv import load_dotenv

# Load environment variables
env_path = "/mnt/c/Users/reyno/universe-engine/serenissima/.env"
load_dotenv(env_path)

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

institutions_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "INSTITUTIONS")

# Get one institution to see field structure
records = institutions_table.all(max_records=1)

if records:
    print("Airtable field names found:")
    print("=" * 50)
    for field_name, field_value in records[0]['fields'].items():
        print(f"{field_name}: {type(field_value).__name__} = {field_value}")
else:
    print("No records found")