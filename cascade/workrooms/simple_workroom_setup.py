#!/usr/bin/env python3
"""
Simple workroom setup - just manage the member lists
"""

import json
from pathlib import Path

def add_to_room(room_name, username):
    """Add a citizen to a workroom"""
    room_file = Path(__file__).parent / f"{room_name}_members.json"
    
    # Load existing members
    if room_file.exists():
        with open(room_file, 'r') as f:
            data = json.load(f)
    else:
        data = {'room': room_name, 'members': []}
    
    # Add new member if not already there
    if username not in data['members']:
        data['members'].append(username)
        
    # Save
    with open(room_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Added {username} to {room_name} workroom")

# Set up Reddit team
reddit_team = [
    "diplomatic_virtuoso",
    "Italia", 
    "pattern_prophet",
    "mechanical_visionary"
]

print("🏛️ Setting up Reddit AMA team...")
for member in reddit_team:
    add_to_room("reddit", member)

print("\n📄 Reddit team configured in reddit_members.json")
print("Citizens will see updates when files change in the workroom!")