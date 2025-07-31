#!/usr/bin/env python3
"""
Citizen Presence Generator

Fetches ImagePrompt from Airtable CITIZENS table and creates PRESENCE.md 
files in each citizen directory with their appearance information.
"""

import os
import requests
from pathlib import Path
import time
from dotenv import load_dotenv

# Load environment variables from serenissima/.env
env_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/.env")
load_dotenv(env_path)

# Airtable configuration from environment
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "CITIZENS"
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

if not AIRTABLE_BASE_ID or not AIRTABLE_API_KEY:
    print("Error: AIRTABLE_BASE_ID or AIRTABLE_API_KEY not found in .env file")
    exit(1)

def get_citizen_directories(citizens_path):
    """Get all citizen directory names"""
    citizens = []
    
    for item in os.listdir(citizens_path):
        item_path = citizens_path / item
        
        # Only include directories, exclude files and special dirs
        if (item_path.is_dir() and 
            not item.startswith('.') and 
            not item.startswith('_') and
            not item.endswith('.md') and
            not item.endswith('.py') and
            not item.endswith('.json') and
            not item.endswith('.csv') and
            not item.endswith('.log') and
            not item.endswith('.sh')):
            citizens.append(item)
    
    return sorted(citizens)

def fetch_airtable_records():
    """Fetch all records from CITIZENS table"""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    
    all_records = []
    offset = None
    
    while True:
        params = {}
        if offset:
            params['offset'] = offset
            
        try:
            print(f"Fetching records from Airtable...", end="")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                all_records.extend(records)
                
                print(f" ✓ Got {len(records)} records")
                
                offset = data.get('offset')
                if not offset:
                    break
                    
                time.sleep(0.2)  # Rate limiting
            else:
                print(f" ✗ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f" ✗ Network error: {e}")
            return None
    
    return all_records

def create_citizens_lookup(records):
    """Create a lookup dictionary of citizens by username"""
    citizens_lookup = {}
    
    for record in records:
        fields = record.get('fields', {})
        username = fields.get('Username')
        image_prompt = fields.get('ImagePrompt', '')
        
        if username:
            citizens_lookup[username] = {
                'image_prompt': image_prompt,
                'record_id': record.get('id')
            }
    
    return citizens_lookup

def create_presence_file(citizen_dir, username, image_prompt):
    """Create PRESENCE.md file for a citizen"""
    presence_content = f"""# {username}'s Presence

## Type
citizen

## Appearance


## Appearance Prompt
{image_prompt}

## Pattern Broadcast (Live)



## Visual References
- portrait: ./{username}_portrait.jpg 
"""
    
    presence_path = citizen_dir / "PRESENCE.md"
    
    try:
        with open(presence_path, 'w', encoding='utf-8') as f:
            f.write(presence_content)
        return True
    except Exception as e:
        print(f"Error writing {presence_path}: {e}")
        return False

def main():
    """Main execution function"""
    # Path to citizens directory
    citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    if not citizens_path.exists():
        print(f"Error: Citizens directory not found: {citizens_path}")
        return
    
    # Fetch Airtable records
    print("Fetching citizen data from Airtable...")
    records = fetch_airtable_records()
    
    if not records:
        print("Failed to fetch records from Airtable")
        return
    
    print(f"Retrieved {len(records)} total records from Airtable")
    
    # Create lookup dictionary
    citizens_lookup = create_citizens_lookup(records)
    print(f"Found {len(citizens_lookup)} citizens with usernames")
    
    # Get local citizen directories
    local_citizens = get_citizen_directories(citizens_path)
    print(f"Found {len(local_citizens)} local citizen directories")
    
    # Track results
    created_count = 0
    updated_count = 0
    missing_prompt_count = 0
    not_in_airtable_count = 0
    
    print("=" * 70)
    
    # Process each local citizen directory
    for i, citizen in enumerate(local_citizens, 1):
        citizen_dir = citizens_path / citizen
        presence_path = citizen_dir / "PRESENCE.md"
        
        print(f"[{i:3d}/{len(local_citizens)}] {citizen:30} ", end="")
        
        # Check if citizen exists in Airtable
        if citizen not in citizens_lookup:
            print("✗ Not found in Airtable")
            not_in_airtable_count += 1
            continue
        
        citizen_data = citizens_lookup[citizen]
        image_prompt = citizen_data['image_prompt']
        
        # Check if ImagePrompt exists
        if not image_prompt or image_prompt.strip() == '':
            print("⚠️ No ImagePrompt in Airtable")
            missing_prompt_count += 1
            continue
        
        # Check if PRESENCE.md already exists
        if presence_path.exists():
            print("○ Updating existing PRESENCE.md")
            action = "updated"
            updated_count += 1
        else:
            print("✓ Creating new PRESENCE.md")
            action = "created"
            created_count += 1
        
        # Create the presence file
        success = create_presence_file(citizen_dir, citizen, image_prompt)
        
        if not success:
            print(f"    ✗ Failed to {action} file")
    
    print("=" * 70)
    print("Summary:")
    print(f"  ✓ Created new files:        {created_count}")
    print(f"  ○ Updated existing files:   {updated_count}")
    print(f"  ⚠️ Missing ImagePrompt:     {missing_prompt_count}")
    print(f"  ✗ Not in Airtable:         {not_in_airtable_count}")
    print(f"  Total local citizens:      {len(local_citizens)}")
    print(f"  Total processed:           {created_count + updated_count}")

def test_airtable_connection():
    """Test connection to Airtable API"""
    print("Testing Airtable connection...")
    
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}"
    }
    params = {"maxRecords": 1}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            print(f"✓ Connection successful, got {len(records)} test record(s)")
            
            if records:
                fields = records[0].get('fields', {})
                username = fields.get('Username', 'N/A')
                has_image_prompt = 'ImagePrompt' in fields
                print(f"  Sample record: {username}, has ImagePrompt: {has_image_prompt}")
            
            return True
        else:
            print(f"✗ Connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {e}")
        return False

if __name__ == "__main__":
    # Test connection first
    if test_airtable_connection():
        print()
        main()
    else:
        print("Fix Airtable connection before proceeding")