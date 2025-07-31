#!/usr/bin/env python3
"""
Setup script to assign citizens to workrooms
"""

import requests
import json
import sys

API_BASE = "https://serenissima.ai/api"

def assign_citizen_to_room(username, room_name):
    """Assign a citizen to a workroom via stratagem"""
    
    # Create the stratagem to update room
    stratagem_data = {
        "stratagems": [{
            "action": "UpdateCitizenRoom",
            "subjectCitizenUsername": username,
            "data": {
                "room": room_name
            }
        }]
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/stratagems/try-create",
            json=stratagem_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ Assigned {username} to room '{room_name}'")
            return True
        else:
            print(f"❌ Failed to assign {username}: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error assigning {username}: {e}")
        return False

def setup_reddit_team():
    """Set up the Reddit AMA team in the reddit workroom"""
    team = [
        "diplomatic_virtuoso",  # Lead
        "Italia",              # Research/facts
        "pattern_prophet",     # Mathematical proofs
        "mechanical_visionary" # Technical examples
    ]
    
    print("🏛️ Setting up Reddit AMA team...")
    
    for username in team:
        assign_citizen_to_room(username, "reddit")
    
    print("\n✨ Reddit team setup complete!")
    print("Run 'python3 workroom_monitor.py reddit' to start real-time collaboration")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        # Manual assignment mode
        username = sys.argv[1]
        room = sys.argv[2]
        assign_citizen_to_room(username, room)
    else:
        # Default: set up reddit team
        setup_reddit_team()