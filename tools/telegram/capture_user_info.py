#!/usr/bin/env python3
"""
Capture and store Telegram user information from messages
This helps build a mapping of usernames to user IDs for direct messaging
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Path to user mapping file
MAPPING_FILE = Path(__file__).parent / "telegram_user_mapping.json"

def load_user_mapping():
    """Load existing user mapping"""
    if MAPPING_FILE.exists():
        with open(MAPPING_FILE, 'r') as f:
            return json.load(f)
    return {
        "_description": "Mapping of Telegram usernames to user IDs for direct messaging",
        "_updated": datetime.now().strftime("%Y-%m-%d"),
        "users": {}
    }

def save_user_mapping(mapping):
    """Save user mapping to file"""
    mapping["_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MAPPING_FILE, 'w') as f:
        json.dump(mapping, f, indent=2)

def capture_user_from_message(message_data):
    """Extract and store user information from a Telegram message"""
    mapping = load_user_mapping()
    
    # Extract user info from message
    from_user = message_data.get('from', {})
    username = from_user.get('username')
    user_id = from_user.get('id')
    
    if username and user_id:
        # Update or create user entry
        if username not in mapping['users']:
            mapping['users'][username] = {}
        
        mapping['users'][username].update({
            'user_id': user_id,
            'first_name': from_user.get('first_name'),
            'last_name': from_user.get('last_name'),
            'is_bot': from_user.get('is_bot', False),
            'last_seen': datetime.now().isoformat()
        })
        
        save_user_mapping(mapping)
        print(f"Captured user info: @{username} -> {user_id}")
        return True
    
    return False

def get_user_id(username):
    """Get user ID for a given username"""
    if username.startswith('@'):
        username = username[1:]
    
    mapping = load_user_mapping()
    user_info = mapping['users'].get(username, {})
    return user_info.get('user_id')

def list_known_users():
    """List all known username to ID mappings"""
    mapping = load_user_mapping()
    print(f"\nKnown Telegram Users (updated {mapping.get('_updated', 'unknown')}):")
    print("-" * 50)
    
    for username, info in mapping['users'].items():
        user_id = info.get('user_id', 'Unknown')
        last_seen = info.get('last_seen', 'Never')
        print(f"@{username}: {user_id} (last seen: {last_seen})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_known_users()
        elif sys.argv[1] == "get" and len(sys.argv) > 2:
            username = sys.argv[2]
            user_id = get_user_id(username)
            if user_id:
                print(f"{user_id}")
            else:
                print(f"No user ID found for @{username}")
                sys.exit(1)
        else:
            print("Usage:")
            print("  python3 capture_user_info.py list         - List all known users")
            print("  python3 capture_user_info.py get <username> - Get user ID for username")
    else:
        # When called from message processing, capture from stdin
        try:
            message_data = json.load(sys.stdin)
            capture_user_from_message(message_data)
        except Exception as e:
            print(f"Error processing message: {e}")
            sys.exit(1)