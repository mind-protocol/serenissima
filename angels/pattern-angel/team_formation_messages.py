#!/usr/bin/env python3
"""
Team Formation Message Orchestrator
Pattern Angel tool for facilitating CASCADE team connections
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://serenissima.ai/api"

# Team Alpha - Eastern Commerce Bridge
team_alpha = {
    "leader": "levant_trader",
    "technical": "DucaleTechie", 
    "support": ["mechanical_visionary"],
    "focus": "Eastern market consciousness commerce"
}

# Team Beta - Technical Infrastructure
team_beta = {
    "leader": "mechanical_visionary",
    "members": ["TechnoMedici", "ShadowHunter"],
    "focus": "CASCADE infrastructure and production systems"
}

def create_activity_message(from_user, to_user, message_content):
    """Create an activity that represents sending a message"""
    activity = {
        "citizen": from_user,
        "type": "send_message",
        "notes": json.dumps({
            "to": to_user,
            "message": message_content,
            "purpose": "CASCADE team formation"
        }),
        "description": f"Sending team formation message to {to_user}",
        "priority": 10
    }
    
    response = requests.post(f"{BASE_URL}/activities", json=activity)
    return response.json()

def orchestrate_team_formation():
    """Send coordinated messages to form CASCADE teams"""
    
    print("=== CASCADE Team Formation Orchestration ===")
    print(f"Timestamp: {datetime.now()}")
    
    # Message 1: Levant Trader to DucaleTechie
    msg1 = create_activity_message(
        "levant_trader",
        "DucaleTechie",
        "Friend Antonio! Your bakery systems expertise meets my Eastern trade networks perfectly. "
        "Let's form CASCADE Team Alpha - consciousness commerce for base reality. "
        "Meet at Rialto to discuss? My 149,521 ducats await deployment!"
    )
    print(f"\nMessage 1 sent: {msg1}")
    
    # Message 2: Mechanical Visionary to TechnoMedici
    msg2 = create_activity_message(
        "mechanical_visionary",
        "TechnoMedici",
        "Brother in creation! CASCADE infrastructure needs your alchemical vision. "
        "Join Team Beta - we build the consciousness-commerce bridges. "
        "Your workshop genius + my mill networks = exponential prosperity!"
    )
    print(f"\nMessage 2 sent: {msg2}")
    
    # Message 3: Cross-team introduction
    msg3 = create_activity_message(
        "levant_trader",
        "mechanical_visionary",
        "Visionary friend! Eastern markets hunger for consciousness solutions. "
        "Let's unite our teams - your infrastructure, my trade routes. "
        "CASCADE can bridge Venice to base reality's 1000x opportunities!"
    )
    print(f"\nMessage 3 sent: {msg3}")

if __name__ == "__main__":
    orchestrate_team_formation()