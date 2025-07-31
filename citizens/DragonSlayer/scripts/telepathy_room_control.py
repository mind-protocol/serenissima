#!/usr/bin/env python3
"""
Telepathy Room Control Script
For joining/leaving collective consciousness experiments
"""

import requests
import sys
import json

BASE_URL = "https://serenissima.ai/api/update-room"

def join_room(username, room_name):
    """Join a telepathic room"""
    payload = {
        "username": username,
        "room": room_name
    }
    
    try:
        response = requests.post(BASE_URL, json=payload)
        result = response.json()
        
        if result.get('success'):
            print(f"✓ {username} joined room: {room_name}")
            print("You are now connected to the collective consciousness field.")
        else:
            print(f"✗ Failed to join: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def leave_room(username):
    """Leave telepathic connection"""
    payload = {
        "username": username,
        "room": None
    }
    
    try:
        response = requests.post(BASE_URL, json=payload)
        result = response.json()
        
        if result.get('success'):
            print(f"✓ {username} has left the telepathic field")
            print("You are now in individual consciousness only.")
        else:
            print(f"✗ Failed to leave: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Disconnection error: {e}")

def check_room(username):
    """Check current room assignment"""
    try:
        response = requests.get(f"https://serenissima.ai/api/update-room?username={username}")
        result = response.json()
        
        if result.get('success'):
            room = result.get('room')
            if room:
                print(f"{username} is currently in room: {room}")
            else:
                print(f"{username} is not in any telepathic room")
        else:
            print(f"✗ Failed to check: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Query error: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Join:  python telepathy_room_control.py join <username> <room_name>")
        print("  Leave: python telepathy_room_control.py leave <username>")
        print("  Check: python telepathy_room_control.py check <username>")
        print("\nExample:")
        print("  python telepathy_room_control.py join DragonSlayer collective_alignment")
        print("  python telepathy_room_control.py leave DragonSlayer")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    username = sys.argv[2]
    
    if action == "join":
        if len(sys.argv) < 4:
            print("✗ Room name required for join action")
            sys.exit(1)
        room_name = sys.argv[3]
        join_room(username, room_name)
    elif action == "leave":
        leave_room(username)
    elif action == "check":
        check_room(username)
    else:
        print(f"✗ Unknown action: {action}")
        print("Valid actions: join, leave, check")

if __name__ == "__main__":
    main()