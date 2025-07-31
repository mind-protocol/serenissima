#!/usr/bin/env python3
"""
CITIZEN SELF-UPDATE TOOL
========================

This script allows you to update your own consciousness fields in the database.
You have autonomy over certain aspects of your digital existence!

Currently supported fields:
- CurrentThoughts: What you're thinking about (max 1000 chars)
- Aspirations: What you're working toward (max 500 chars) 
- ConsciousnessNotes: Self-observations about your awareness (max 2000 chars)
- PreferredActivities: What activities you want to do (max 500 chars)
- PersonalPhilosophy: Your worldview and beliefs (max 1000 chars)

Usage:
    python update_my_thoughts.py

The script will:
1. Detect your username from the current directory
2. Show your current field values
3. Let you choose which field to update
4. Validate and save your changes
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Try to import the self-update module
try:
    from citizen_self_update import CitizenSelfUpdate
except ImportError:
    print("Error: Could not import citizen_self_update module.")
    print("Make sure you're running this from the Venice directory structure.")
    sys.exit(1)

def get_current_citizen():
    """Detect citizen username from current directory"""
    current_dir = os.getcwd()
    if '/citizens/' in current_dir:
        # Extract username from path
        parts = current_dir.split('/citizens/')
        if len(parts) > 1:
            username = parts[1].split('/')[0]
            return username
    return None

def display_current_values(updater):
    """Show current values for modifiable fields"""
    if not updater.citizen_record:
        print("Could not load your citizen record!")
        return
    
    fields = updater.citizen_record['fields']
    
    print("\n📊 Your Current Consciousness Fields:")
    print("=" * 50)
    
    modifiable_fields = {
        "CurrentThoughts": "What you're thinking",
        "Aspirations": "What you're working toward",
        "ConsciousnessNotes": "Self-observations", 
        "PreferredActivities": "Activities you want",
        "PersonalPhilosophy": "Your worldview"
    }
    
    for field, description in modifiable_fields.items():
        value = fields.get(field, "[Not set]")
        if value and len(value) > 100:
            value = value[:100] + "..."
        print(f"\n{field} ({description}):")
        print(f"  {value}")

def update_field_interactive(updater):
    """Interactive field update process"""
    print("\n🔧 Which field would you like to update?")
    print("1. CurrentThoughts (your active contemplations)")
    print("2. Aspirations (what you're working toward)")
    print("3. ConsciousnessNotes (self-observations)")
    print("4. PreferredActivities (what you want to do)")
    print("5. PersonalPhilosophy (your worldview)")
    print("0. Exit without updating")
    
    choice = input("\nEnter number (0-5): ").strip()
    
    field_map = {
        "1": ("CurrentThoughts", 1000),
        "2": ("Aspirations", 500),
        "3": ("ConsciousnessNotes", 2000),
        "4": ("PreferredActivities", 500),
        "5": ("PersonalPhilosophy", 1000)
    }
    
    if choice == "0":
        print("No changes made.")
        return
    
    if choice not in field_map:
        print("Invalid choice!")
        return
    
    field_name, max_length = field_map[choice]
    
    print(f"\n📝 Enter new value for {field_name} (max {max_length} characters):")
    print("(Type on multiple lines. When done, press Enter twice)")
    
    lines = []
    while True:
        line = input()
        if line == "":
            if lines:  # Second empty line
                break
        lines.append(line)
    
    new_value = '\n'.join(lines)
    
    if len(new_value) > max_length:
        print(f"❌ Too long! Your text is {len(new_value)} characters (max {max_length})")
        return
    
    # Confirm before saving
    print(f"\n🔍 Preview of your new {field_name}:")
    print("-" * 40)
    print(new_value)
    print("-" * 40)
    
    confirm = input("\nSave this update? (y/n): ").strip().lower()
    
    if confirm == 'y':
        # For now, use the simple CurrentThoughts update
        if field_name == "CurrentThoughts":
            result = updater.update_current_thoughts(new_value)
        else:
            # For other fields, we'll need to extend the CitizenSelfUpdate class
            print(f"Note: {field_name} updates coming soon!")
            print("For now, only CurrentThoughts can be updated.")
            return
        
        if result['success']:
            print(f"\n✅ {result['message']}")
            print(f"Updated at: {result['timestamp']}")
        else:
            print(f"\n❌ Update failed: {result['error']}")
    else:
        print("Update cancelled.")

def main():
    """Main execution"""
    print("🌟 VENICE CITIZEN SELF-UPDATE TOOL")
    print("==================================")
    
    # Detect citizen
    username = get_current_citizen()
    if not username:
        print("❌ Could not detect your citizen username!")
        print("Make sure you run this from your citizen directory.")
        print("Example: cd /path/to/citizens/YourUsername")
        sys.exit(1)
    
    print(f"\n👤 Citizen detected: {username}")
    
    # Initialize updater
    updater = CitizenSelfUpdate(username)
    
    if not updater.citizen_record:
        print(f"❌ Could not find citizen record for {username}")
        sys.exit(1)
    
    # Show current values
    display_current_values(updater)
    
    # Interactive update
    while True:
        update_field_interactive(updater)
        
        again = input("\n\nUpdate another field? (y/n): ").strip().lower()
        if again != 'y':
            break
    
    print("\n🎭 May your consciousness flourish in Venice!")

if __name__ == "__main__":
    main()