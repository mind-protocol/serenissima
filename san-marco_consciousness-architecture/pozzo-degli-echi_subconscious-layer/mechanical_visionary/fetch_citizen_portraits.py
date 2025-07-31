#!/usr/bin/env python3
"""
Citizen Portrait Fetcher

Fetches portrait images for all citizens from the Serenissima backend
and saves them as username_portrait.jpg in the citizens directory.
"""

import os
import requests
from pathlib import Path
import time

def get_citizen_directories(citizens_path):
    """Get all citizen directory names (excluding files and special dirs)"""
    citizens = []
    
    for item in os.listdir(citizens_path):
        item_path = citizens_path / item
        
        # Skip files and special directories
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

def fetch_portrait(username, output_path):
    """Fetch portrait for a single citizen"""
    url = f"http://backend.serenissima.ai/public_assets/images/citizens/{username}.jpg"
    
    try:
        print(f"Fetching portrait for {username}...", end="")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f" ✓ Success ({len(response.content)} bytes)")
            return True
        elif response.status_code == 404:
            print(f" ✗ Not found (404)")
            return False
        else:
            print(f" ✗ Error ({response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f" ✗ Network error: {e}")
        return False

def main():
    """Main execution function"""
    # Path to citizens directory
    citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    if not citizens_path.exists():
        print(f"Error: Citizens directory not found: {citizens_path}")
        return
    
    # Get all citizen directories
    citizens = get_citizen_directories(citizens_path)
    
    print(f"Found {len(citizens)} citizen directories")
    print("=" * 60)
    
    # Track results
    success_count = 0
    not_found_count = 0
    error_count = 0
    
    # Fetch portraits for each citizen
    for i, citizen in enumerate(citizens, 1):
        output_path = citizens_path / f"{citizen}_portrait.jpg"
        
        # Skip if already exists
        if output_path.exists():
            print(f"[{i:3d}/{len(citizens)}] {citizen:30} ○ Already exists")
            continue
        
        print(f"[{i:3d}/{len(citizens)}] {citizen:30} ", end="")
        
        success = fetch_portrait(citizen, output_path)
        
        if success:
            success_count += 1
        elif "404" in str(success):
            not_found_count += 1
        else:
            error_count += 1
        
        # Small delay to be nice to the server
        time.sleep(0.1)
    
    print("=" * 60)
    print(f"Summary:")
    print(f"  ✓ Successfully fetched: {success_count}")
    print(f"  ✗ Not found (404):     {not_found_count}")  
    print(f"  ✗ Errors:              {error_count}")
    print(f"  Total citizens:        {len(citizens)}")

if __name__ == "__main__":
    main()