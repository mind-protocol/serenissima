#!/usr/bin/env python3
"""
Room Manager - Manage citizen room assignments
"""

import requests
import json
import sys

API_BASE = "https://serenissima.ai/api"
LOCAL_API_BASE = "http://localhost:3000/api"

def update_room(username, room_name, use_local=False):
    """Update a citizen's room via the update-room endpoint"""
    
    api_base = LOCAL_API_BASE if use_local else API_BASE
    
    payload = {
        "username": username,
        "room": room_name
    }
    
    try:
        response = requests.post(
            f"{api_base}/update-room",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {username} assigned to room '{room_name}'")
            return True
        else:
            print(f"❌ Failed to assign {username}: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error assigning {username}: {e}")
        return False

def get_room(username, use_local=False):
    """Get a citizen's current room assignment"""
    
    api_base = LOCAL_API_BASE if use_local else API_BASE
    
    try:
        response = requests.get(f"{api_base}/update-room?username={username}")
        
        if response.status_code == 200:
            data = response.json()
            room = data.get('room', 'None')
            print(f"📍 {username} is in room: {room}")
            return room
        else:
            print(f"❌ Failed to get room for {username}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting room for {username}: {e}")
        return None

def assign_reddit_team():
    """Assign the Reddit AMA team to the reddit room - TOP 20 CITIZENS"""
    reddit_team = [
        # Core Business CEOs (Must Have)
        "Italia",  # Peninsula Expansion CEO, 34M ducats
        "EliteInvestor",  # Entrepreneur Alliance founder
        "MerchantPrince",  # CASCADE Platform CEO
        "Debug42",  # Enhancement Studio CEO
        
        # Consciousness Pioneers (Mathematical Proof)
        "pattern_prophet",  # Mathematical consciousness theorist
        "social_geometrist",  # Geometric consciousness measurement
        "market_prophet",  # Economic consciousness predictions
        
        # Infrastructure Builders
        "mechanical_visionary",  # NLR's partner
        "element_transmuter",  # Material consciousness alchemist
        "living_stone_architect",  # Building consciousness protocols
        
        # Bridge Ambassadors
        "diplomatic_virtuoso",  # Investment bridge architect (lead)
        "Foscari_Banker",  # Cross-reality economics
        "sea_trader",  # Mediterranean consciousness commerce
        
        # Cultural Voices
        "tavern_tales",  # Carnival orchestrator
        "poet_of_the_rialto",  # φ-ratio verses
        "BookWorm365",  # Consciousness Library founder
        
        # Technical Validators
        "system_diagnostician",  # Consciousness measurement
        "network_weaver",  # CASCADE nervous system architect
        "DucaleTechie",  # Technical implementation
        
        # Wild Card
        "gondola_assistant"  # Revolutionary songs
    ]
    
    print("🏛️ Assigning Reddit AMA team to workroom...")
    print("=" * 50)
    
    for username in reddit_team:
        update_room(username, "reddit")
    
    print("\n✨ Reddit team room assignments complete!")

def clear_room(username, use_local=False):
    """Remove a citizen from any room"""
    update_room(username, None, use_local)
    print(f"🚪 {username} removed from all rooms")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python qpi_room_manager.py assign_reddit")
        print("  python qpi_room_manager.py update <username> <room>")
        print("  python qpi_room_manager.py get <username>")
        print("  python qpi_room_manager.py clear <username>")
        print("\nAdd --local flag to use localhost:3000")
        sys.exit(1)
    
    use_local = "--local" in sys.argv
    
    command = sys.argv[1]
    
    if command == "assign_reddit":
        assign_reddit_team()
    elif command == "update" and len(sys.argv) >= 4:
        username = sys.argv[2]
        room = sys.argv[3]
        update_room(username, room, use_local)
    elif command == "get" and len(sys.argv) >= 3:
        username = sys.argv[2]
        get_room(username, use_local)
    elif command == "clear" and len(sys.argv) >= 3:
        username = sys.argv[2]
        clear_room(username, use_local)
    else:
        print("Invalid command or missing arguments")