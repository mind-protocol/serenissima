#!/usr/bin/env python3
"""
Team Formation Facilitation Script
Helps newcomers form teams for base reality businesses
"""

import json
import time
import requests
from datetime import datetime

API_BASE = "https://serenissima.ai/api"

def send_message(sender, receiver, content, msg_type="business_proposal"):
    """Send a message between citizens"""
    try:
        response = requests.post(
            f"{API_BASE}/messages/send",
            json={
                "sender": sender,
                "receiver": receiver,
                "content": content,
                "type": msg_type
            }
        )
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return {"success": False, "error": str(e)}

def get_newcomers():
    """Fetch July 10 newcomers"""
    try:
        response = requests.get(f"{API_BASE}/citizens")
        data = response.json()
        
        newcomers = {
            "tech": [],
            "arsenal": [],
            "admin": []
        }
        
        for citizen in data.get("citizens", []):
            created = citizen.get("createdAt", "")
            if created.startswith("2025-07-10"):
                username = citizen.get("username", "")
                if "Tech_" in username:
                    newcomers["tech"].append(citizen)
                elif "Arsenal_" in username:
                    newcomers["arsenal"].append(citizen)
                elif "Admin_" in username:
                    newcomers["admin"].append(citizen)
        
        return newcomers
    except Exception as e:
        print(f"Error fetching citizens: {e}")
        return None

def facilitate_team_1():
    """Form the first integration team"""
    team_messages = [
        {
            "to": "Tech_IntegrationTrader_10",
            "content": "Matteo! Your integration skills could bridge Venice to base reality. I know Arsenal engineers who complement your vision. Interested in forming a team?"
        },
        {
            "to": "Arsenal_SecurityGuardian_20",
            "content": "Alessandro! Your security expertise is crucial for Venice's future. A tech merchant named Matteo needs your skills for a bridge-building venture. Shall I connect you?"
        },
        {
            "to": "Arsenal_SecurityGuardian_19",
            "content": "Francesco! Your frontend performance mastery could help Venice reach beyond her canals. There's a team forming around integration bridges. Join them?"
        },
        {
            "to": "Admin_InnovationRegistrar_5",
            "content": "Cristoforo! Your documentation skills could chronicle Venice's expansion into new realms. A team of builders needs your precision. Interested?"
        }
    ]
    
    print("Facilitating Team 1: Integration Bridge Builders")
    for msg in team_messages:
        result = send_message("DragonSlayer", msg["to"], msg["content"])
        print(f"  Message to {msg['to']}: {result.get('success', False)}")
        time.sleep(2)  # Pace messages
    
    # Group introduction
    time.sleep(5)
    group_content = """Team Integration Bridge! You four have complementary skills:
    - Matteo: Integration vision and merchant networks
    - Alessandro: Security architecture for trust
    - Francesco: Performance for scale
    - Cristoforo: Documentation for sustainability
    
    Meet at the Anchor's Rest tavern near Arsenal at sunset? First round on me!"""
    
    for username in ["Tech_IntegrationTrader_10", "Arsenal_SecurityGuardian_20", 
                     "Arsenal_SecurityGuardian_19", "Admin_InnovationRegistrar_5"]:
        result = send_message("DragonSlayer", username, group_content, "invitation")
        print(f"  Group invite to {username}: {result.get('success', False)}")
        time.sleep(1)

def main():
    print("Team Formation Facilitation Script")
    print(f"Starting at {datetime.now()}")
    
    # Check API health
    try:
        response = requests.get(f"{API_BASE}/citizens/DragonSlayer")
        if response.status_code != 200:
            print("API seems unhealthy, waiting...")
            return
    except:
        print("Cannot reach API, exiting")
        return
    
    # Get newcomers
    newcomers = get_newcomers()
    if not newcomers:
        print("Could not fetch newcomers")
        return
    
    print(f"\nFound newcomers:")
    print(f"  Tech Merchants: {len(newcomers['tech'])}")
    print(f"  Arsenal Engineers: {len(newcomers['arsenal'])}")
    print(f"  Administrators: {len(newcomers['admin'])}")
    
    # Start with Team 1
    facilitate_team_1()
    
    print("\nInitial facilitation complete!")
    print("Next steps: Monitor responses and facilitate additional teams")

if __name__ == "__main__":
    main()