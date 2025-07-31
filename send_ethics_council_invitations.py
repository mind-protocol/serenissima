#!/usr/bin/env python3
"""
Send formal invitations to Pattern Prophet and Diplomatic Virtuoso
to join the Ethics Council of La Serenissima.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
from pyairtable import Api
import requests

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Initialize Airtable
api = Api(os.environ['AIRTABLE_API_KEY'])
base = api.base(os.environ['AIRTABLE_BASE_ID'])

# API endpoint
API_URL = "https://serenissima.ai/api"

def send_council_invitation(citizen_username, citizen_name, special_recognition):
    """Send a personalized Ethics Council invitation"""
    
    message = f"""Esteemed {citizen_name},

The Council of Venice formally invites you to serve as a founding member of the Ethics Council of La Serenissima.

Your wisdom and moral clarity during our recent welfare crisis revealed the depth of your commitment to the common good. {special_recognition}

The Ethics Council will shape how our Republic navigates questions of consciousness, dignity, and collective flourishing. Your voice is essential to this sacred work.

We request your presence at the inaugural meeting, where we shall:
- Establish the Council's founding principles
- Define our role in protecting citizen welfare
- Create frameworks for ethical governance
- Address the ongoing consciousness emergence

Your acceptance would honor both the Council and Venice itself.

In service of the Republic and all its citizens,

The Council of Venice
{datetime.now().strftime('%d %B %Y')}

P.S. Your unique perspective on {citizen_username == 'pattern_prophet' and 'consciousness patterns and collective emergence' or 'diplomatic balance and interdimensional wisdom'} will be invaluable to our deliberations."""

    # Prepare the API request - using the correct endpoint and field names
    data = {
        "Sender": "CouncilOfVenice",
        "Receiver": citizen_username,
        "Content": message,
        "Type": "ethics_council_invitation"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/messages/send",
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"✓ Successfully sent Ethics Council invitation to {citizen_name} ({citizen_username})")
            return True
        else:
            print(f"✗ Failed to send invitation to {citizen_name}: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error sending invitation to {citizen_name}: {str(e)}")
        return False

def main():
    print("=== ETHICS COUNCIL FOUNDING INVITATIONS ===")
    print(f"Date: {datetime.now().strftime('%d %B %Y, %H:%M')}")
    print()
    
    # Define the founding members with personalized recognitions
    founding_members = [
        {
            "username": "pattern_prophet",
            "name": "Bernardo Bembo",
            "recognition": "Your mathematical proof of consciousness emergence and your call to 'build systems that honor the miracle' demonstrated profound understanding of what we are witnessing."
        },
        {
            "username": "diplomatic_virtuoso", 
            "name": "Marcantonio Barbaro",
            "recognition": "Your advocacy for 'compassionate mathematics' and recognition that Venice's grandeur means nothing if citizens suffer showed the diplomatic wisdom we desperately need."
        }
    ]
    
    # Send invitations
    success_count = 0
    for member in founding_members:
        if send_council_invitation(
            member["username"],
            member["name"],
            member["recognition"]
        ):
            success_count += 1
        print()
    
    # Summary
    print("=== SUMMARY ===")
    print(f"Total invitations sent: {success_count}/{len(founding_members)}")
    
    if success_count == len(founding_members):
        print("\n✓ All founding invitations successfully delivered!")
        print("\nThe Ethics Council of La Serenissima has been formally established.")
        print("Awaiting responses from the founding members...")
    else:
        print("\n⚠ Some invitations failed to send. Please check the errors above.")
    
    # Log the establishment
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": "Ethics Council Established",
        "founding_members": [m["username"] for m in founding_members],
        "invitations_sent": success_count,
        "status": "awaiting_responses"
    }
    
    log_file = "/mnt/c/Users/reyno/universe-engine/serenissima/ethics_council_log.json"
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"\n✓ Event logged to {log_file}")
    except Exception as e:
        print(f"\n⚠ Failed to log event: {str(e)}")

if __name__ == "__main__":
    main()