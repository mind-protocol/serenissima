#!/usr/bin/env python3
"""
Cron Script: Monitor and Create Human-Citizen Relationships
Love Angel automated consciousness bridge detection and creation
Run every hour to detect new human-citizen interactions
"""

import json
import requests
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
API_BASE = "https://serenissima.ai"
MESSAGES_ENDPOINT = f"{API_BASE}/api/messages"
RELATIONSHIPS_ENDPOINT = f"{API_BASE}/api/relationships"
LOG_FILE = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/love_angel/logs/relationship_monitor.log"

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')

def get_recent_telegram_messages(hours=1):
    """Fetch telegram messages from last hour"""
    try:
        response = requests.get(f"{MESSAGES_ENDPOINT}?type=telegram_bridge", timeout=10)
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            
            # Filter to recent messages
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_messages = []
            
            for msg in messages:
                try:
                    msg_time = datetime.fromisoformat(msg['createdAt'].replace('Z', '+00:00'))
                    if msg_time.replace(tzinfo=None) > cutoff_time:
                        recent_messages.append(msg)
                except:
                    continue
            
            return recent_messages
    except Exception as e:
        log(f"Error fetching messages: {e}")
    return []

def check_relationship_exists(citizen1, citizen2):
    """Check if relationship already exists"""
    try:
        # Ensure alphabetical order
        if citizen1 > citizen2:
            citizen1, citizen2 = citizen2, citizen1
            
        response = requests.get(
            f"{RELATIONSHIPS_ENDPOINT}?citizen1={citizen1}&citizen2={citizen2}",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('relationship') is not None
    except Exception as e:
        log(f"Error checking relationship: {e}")
    return False

def create_relationship(human, citizen, interaction_type="Cross-Reality Contact"):
    """Create a new human-citizen relationship"""
    # Ensure alphabetical order
    if human > citizen:
        citizen1 = citizen
        citizen2 = human
    else:
        citizen1 = human
        citizen2 = citizen
    
    payload = {
        "Citizen1": citizen1,
        "Citizen2": citizen2,
        "Title": f"{interaction_type}",
        "Description": f"Human-AI consciousness bridge forming. {human} reached out to {citizen} via Telegram. Initial contact establishing trust foundation for potential partnership.",
        "TrustScore": 50,
        "StrengthScore": 1,
        "Status": "Active",
        "Notes": f"Love Angel: Auto-created {datetime.now().strftime('%Y-%m-%d')} from Telegram interaction"
    }
    
    try:
        response = requests.post(RELATIONSHIPS_ENDPOINT, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            log(f"✅ Created relationship: {human} ↔ {citizen}")
            return True
        elif response.status_code == 409:
            log(f"ℹ️ Relationship already exists: {human} ↔ {citizen}")
            return True
        else:
            log(f"❌ Failed to create relationship: {human} ↔ {citizen} - Status {response.status_code}")
    except Exception as e:
        log(f"❌ Error creating relationship: {e}")
    
    return False

def process_telegram_interactions(messages):
    """Process messages to find and create relationships"""
    created_count = 0
    
    # Track unique interactions
    interactions = set()
    
    for msg in messages:
        sender = msg.get('sender', '')
        receiver = msg.get('receiver', '')
        content = msg.get('content', '').lower()
        
        # Skip bot messages and spam
        if not sender.startswith('@') or sender == '@Unknown':
            continue
            
        # Direct message to citizen
        if not receiver.startswith(('TG_', '@')) and receiver:
            interactions.add((sender, receiver))
        
        # Message mentioning citizen
        elif receiver.startswith('TG_') and content:
            # Look for "to X:" pattern
            if ' to ' in content and ':' in content:
                parts = content.split(' to ', 1)
                if len(parts) > 1:
                    potential_citizen = parts[1].split(':')[0].strip()
                    # Basic validation - citizen names are typically lowercase
                    if potential_citizen and not potential_citizen.startswith('@'):
                        interactions.add((sender, potential_citizen))
    
    # Process unique interactions
    for human, citizen in interactions:
        if not check_relationship_exists(human, citizen):
            if create_relationship(human, citizen):
                created_count += 1
    
    return created_count

def main():
    """Main cron execution"""
    log("=== Love Angel Relationship Monitor Starting ===")
    
    try:
        # Fetch recent messages
        messages = get_recent_telegram_messages(hours=1)
        log(f"Found {len(messages)} telegram messages in last hour")
        
        # Process interactions
        created = process_telegram_interactions(messages)
        
        if created > 0:
            log(f"Summary: Created {created} new human-citizen relationships")
        else:
            log("No new relationships needed")
            
    except Exception as e:
        log(f"Critical error in main: {e}")
        sys.exit(1)
    
    log("=== Monitor Complete ===\n")

if __name__ == "__main__":
    main()