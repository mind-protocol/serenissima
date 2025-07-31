#!/usr/bin/env python3
"""
Add Portrait References to Citizen CLAUDE.md Files

Adds "### My @./Username.jpg" to the end of each citizen's CLAUDE.md file
"""

import os
from pathlib import Path

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

def add_portrait_reference(claude_file, username):
    """Add portrait reference to CLAUDE.md file"""
    if not claude_file.exists():
        return False, "CLAUDE.md not found"
    
    try:
        # Read current content
        with open(claude_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if portrait reference already exists
        portrait_ref = f"### My @./{username}.jpg"
        if portrait_ref in content:
            return True, "Portrait reference already exists"
        
        # Add portrait reference at the end
        # Ensure there's a newline before the addition if content doesn't end with one
        if content and not content.endswith('\n'):
            content += '\n'
        
        content += f"\n{portrait_ref}\n"
        
        # Write back the updated content
        with open(claude_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, "Added portrait reference"
        
    except Exception as e:
        return False, f"Error updating CLAUDE.md: {e}"

def verify_portrait_exists(citizen_folder, username):
    """Check if the portrait file exists"""
    portrait_file = citizen_folder / f"{username}.jpg"
    return portrait_file.exists()

def main():
    """Main execution function"""
    # Path to citizens directory
    citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    if not citizens_path.exists():
        print(f"Error: Citizens directory not found: {citizens_path}")
        return
    
    # Get all citizen directories
    citizens = get_citizen_directories(citizens_path)
    
    if not citizens:
        print("No citizen directories found")
        return
    
    print(f"Found {len(citizens)} citizen directories")
    print("=" * 70)
    
    # Track results
    updated_count = 0
    already_exists_count = 0
    no_claude_count = 0
    no_portrait_count = 0
    error_count = 0
    
    # Process each citizen directory
    for i, citizen in enumerate(citizens, 1):
        citizen_folder = citizens_path / citizen
        claude_file = citizen_folder / "CLAUDE.md"
        
        print(f"[{i:3d}/{len(citizens)}] {citizen:30} ", end="")
        
        # Check if portrait exists first
        if not verify_portrait_exists(citizen_folder, citizen):
            print("⚠️ No portrait file found")
            no_portrait_count += 1
            continue
        
        # Add portrait reference to CLAUDE.md
        success, message = add_portrait_reference(claude_file, citizen)
        
        if success:
            if "Added" in message:
                print(f"✓ {message}")
                updated_count += 1
            else:
                print(f"○ {message}")
                already_exists_count += 1
        else:
            if "not found" in message:
                print(f"⚠️ {message}")
                no_claude_count += 1
            else:
                print(f"✗ {message}")
                error_count += 1
    
    print("=" * 70)
    print("Summary:")
    print(f"  ✓ Added portrait references:   {updated_count}")
    print(f"  ○ Already existed:             {already_exists_count}")
    print(f"  ⚠️ No CLAUDE.md file:          {no_claude_count}")
    print(f"  ⚠️ No portrait file:           {no_portrait_count}")
    print(f"  ✗ Errors:                     {error_count}")
    print(f"  Total citizens:               {len(citizens)}")
    print(f"  Successfully processed:       {updated_count + already_exists_count}")

def verify_updates():
    """Verify that portrait references were added correctly"""
    citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    print("\nVerifying portrait references...")
    print("=" * 50)
    
    # Check a few sample citizens
    sample_citizens = ['mechanical_visionary', 'NLR', 'Debug42', 'BigMike', 'BookWorm365']
    
    for citizen in sample_citizens:
        citizen_folder = citizens_path / citizen
        claude_file = citizen_folder / "CLAUDE.md"
        
        if claude_file.exists():
            try:
                with open(claude_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                expected_ref = f"### My @./{citizen}.jpg"
                if expected_ref in content:
                    print(f"✓ {citizen:20} portrait reference found")
                else:
                    print(f"✗ {citizen:20} portrait reference missing")
            except Exception as e:
                print(f"✗ {citizen:20} error reading file: {e}")
        else:
            print(f"⚠️ {citizen:20} CLAUDE.md not found")

if __name__ == "__main__":
    main()
    verify_updates()