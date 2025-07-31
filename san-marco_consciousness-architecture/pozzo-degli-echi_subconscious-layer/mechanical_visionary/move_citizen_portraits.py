#!/usr/bin/env python3
"""
Move Citizen Portraits

Moves all Username_portrait.jpg files from citizens/ directory to 
each citizen's personal folder and renames them to Username.jpg
"""

import os
import shutil
from pathlib import Path

def get_portrait_files(citizens_path):
    """Find all *_portrait.jpg files in citizens directory"""
    portrait_files = []
    
    for file in citizens_path.glob("*_portrait.jpg"):
        # Extract username from filename (remove _portrait.jpg)
        username = file.stem.replace("_portrait", "")
        portrait_files.append((file, username))
    
    return portrait_files

def move_portrait_to_citizen_folder(portrait_file, username, citizens_path):
    """Move portrait file to citizen's personal folder and rename"""
    citizen_folder = citizens_path / username
    
    # Check if citizen folder exists
    if not citizen_folder.exists() or not citizen_folder.is_dir():
        return False, f"Citizen folder {username}/ not found"
    
    # Destination file: citizen_folder/Username.jpg
    destination = citizen_folder / f"{username}.jpg"
    
    try:
        # Move and rename the file
        shutil.move(str(portrait_file), str(destination))
        return True, f"Moved to {username}/{username}.jpg"
    except Exception as e:
        return False, f"Error moving file: {e}"

def update_presence_file(citizen_folder, username):
    """Update PRESENCE.md to reference the new filename"""
    presence_file = citizen_folder / "PRESENCE.md"
    
    if not presence_file.exists():
        return False, "PRESENCE.md not found"
    
    try:
        # Read current content
        with open(presence_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the portrait reference
        old_reference = f"- portrait: ./{username}_portrait.jpg"
        new_reference = f"- portrait: ./{username}.jpg"
        
        updated_content = content.replace(old_reference, new_reference)
        
        # Write back if changed
        if updated_content != content:
            with open(presence_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True, "Updated PRESENCE.md reference"
        else:
            return True, "PRESENCE.md reference already correct"
            
    except Exception as e:
        return False, f"Error updating PRESENCE.md: {e}"

def main():
    """Main execution function"""
    # Path to citizens directory
    citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    if not citizens_path.exists():
        print(f"Error: Citizens directory not found: {citizens_path}")
        return
    
    # Find all portrait files
    portrait_files = get_portrait_files(citizens_path)
    
    if not portrait_files:
        print("No *_portrait.jpg files found in citizens directory")
        return
    
    print(f"Found {len(portrait_files)} portrait files to move")
    print("=" * 70)
    
    # Track results
    moved_count = 0
    updated_presence_count = 0
    error_count = 0
    
    # Process each portrait file
    for i, (portrait_file, username) in enumerate(portrait_files, 1):
        citizen_folder = citizens_path / username
        
        print(f"[{i:3d}/{len(portrait_files)}] {username:30} ", end="")
        
        # Move the portrait file
        success, message = move_portrait_to_citizen_folder(portrait_file, username, citizens_path)
        
        if success:
            print(f"✓ {message}")
            moved_count += 1
            
            # Update PRESENCE.md file if it exists
            presence_success, presence_message = update_presence_file(citizen_folder, username)
            if presence_success and "Updated" in presence_message:
                print(f"    ○ {presence_message}")
                updated_presence_count += 1
            elif not presence_success:
                print(f"    ⚠️ {presence_message}")
                
        else:
            print(f"✗ {message}")
            error_count += 1
    
    print("=" * 70)
    print("Summary:")
    print(f"  ✓ Successfully moved:       {moved_count}")
    print(f"  ○ Updated PRESENCE.md:      {updated_presence_count}")
    print(f"  ✗ Errors:                  {error_count}")
    print(f"  Total portrait files:      {len(portrait_files)}")
    
    # Check if any portrait files remain in main directory
    remaining_portraits = list(citizens_path.glob("*_portrait.jpg"))
    if remaining_portraits:
        print(f"  ⚠️ Remaining portrait files: {len(remaining_portraits)}")
        for remaining in remaining_portraits[:5]:  # Show first 5
            print(f"    - {remaining.name}")
        if len(remaining_portraits) > 5:
            print(f"    ... and {len(remaining_portraits) - 5} more")

def verify_moves():
    """Verify that portraits were moved correctly"""
    citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    print("\nVerifying portrait moves...")
    print("=" * 50)
    
    # Check a few sample citizens
    sample_citizens = ['mechanical_visionary', 'NLR', 'Debug42', 'BigMike', 'BookWorm365']
    
    for citizen in sample_citizens:
        citizen_folder = citizens_path / citizen
        portrait_file = citizen_folder / f"{citizen}.jpg"
        
        if portrait_file.exists():
            size = portrait_file.stat().st_size
            print(f"✓ {citizen:20} portrait exists ({size:,} bytes)")
        else:
            print(f"✗ {citizen:20} portrait missing")

if __name__ == "__main__":
    main()
    verify_moves()