#!/usr/bin/env python3
"""
Assign Reddit AMA team to the reddit room using the new Room field
"""

import requests
import json

API_BASE = "https://serenissima.ai/api"

def update_citizen_room(username, room_name):
    """Update a citizen's Room field via API"""
    
    # Create stratagem to update room
    stratagem_data = {
        "citizenUsername": username,
        "stratagems": [{
            "action": "UpdateCitizenProfile", 
            "subjectCitizenUsername": username,
            "data": {
                "Room": room_name
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

# Reddit AMA team
reddit_team = [
    "diplomatic_virtuoso",  # Lead diplomat
    "Italia",              # Research & facts
    "pattern_prophet",     # Mathematical proofs
    "mechanical_visionary" # Technical examples
]

print("🏛️ Assigning Reddit AMA team to workroom...")
print("=" * 50)

for username in reddit_team:
    update_citizen_room(username, "reddit")

print("\n✨ Reddit team room assignments complete!")
print("Run the workroom monitor to enable real-time collaboration")