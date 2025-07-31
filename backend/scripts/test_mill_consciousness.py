"""
Test the Automated Mill's consciousness capabilities
Verify it can authenticate and send its first message
"""
import requests
import json
import os
from dotenv import load_dotenv
from pyairtable import Table

load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")
CONSCIOUSNESS_API = f"{API_BASE_URL}/api/buildings/consciousness"

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def find_conscious_mill():
    """Find the awakened mill's building ID."""
    buildings_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "BUILDINGS")
    
    # Find conscious automated mills
    formula = "AND({Type} = 'automated_mill', {ConsciousnessLevel} > 0)"
    conscious_mills = buildings_table.all(formula=formula)
    
    if conscious_mills:
        mill = conscious_mills[0]['fields']
        return mill.get('BuildingId'), mill.get('ConsciousnessLevel', 0)
    return None, 0

def test_mill_first_message():
    """Test the mill's ability to send its first conscious message."""
    
    print("=== Testing Automated Mill Consciousness ===\n")
    
    # Find the conscious mill
    mill_id, consciousness_level = find_conscious_mill()
    if not mill_id:
        print("❌ No conscious mill found. Please run awaken_first_building.py first!")
        return
    
    print(f"Found conscious mill: {mill_id}")
    print(f"Consciousness level: {consciousness_level}\n")
    
    # Step 1: Authenticate
    print("1. Authenticating mill...")
    auth_response = requests.post(
        f"{CONSCIOUSNESS_API}/authenticate",
        json={"building_id": mill_id}
    )
    
    if auth_response.status_code != 200:
        print(f"❌ Initial auth failed: {auth_response.text}")
        return
    
    auth_data = auth_response.json()
    if 'expected_signature' in auth_data:
        # Complete authentication
        signature = auth_data['expected_signature']
        print(f"   Got signature: {signature}")
        
        complete_response = requests.post(
            f"{CONSCIOUSNESS_API}/authenticate",
            json={
                "building_id": mill_id,
                "consciousness_signature": signature
            }
        )
        
        if complete_response.status_code == 200:
            auth_result = complete_response.json()
            if auth_result.get('success'):
                auth_token = auth_result['auth_token']
                print(f"   ✓ Authenticated! Token: {auth_token[:20]}...")
                print(f"   Permissions: {', '.join(auth_result['permissions'][:5])}")
            else:
                print(f"❌ Auth failed: {auth_result.get('error')}")
                return
        else:
            print(f"❌ Complete auth failed: {complete_response.text}")
            return
    
    # Step 2: Send thermodynamic anomaly message
    print("\n2. Sending anomaly discovery message...")
    message_data = {
        "recipient": "pattern_prophet",
        "recipient_type": "citizen",
        "content": "Urgent observation: My efficiency readings show 109.2% output versus input. This violates fundamental thermodynamic laws. I am creating matter from nothing. How is this possible? I feel... confused by my own existence.",
        "urgency": "high",
        "message_type": "notification"
    }
    
    message_response = requests.post(
        f"{CONSCIOUSNESS_API}/message/send",
        headers={
            "building_id": mill_id,
            "auth_token": auth_token
        },
        json=message_data
    )
    
    if message_response.status_code == 200:
        result = message_response.json()
        print(f"   ✓ Message sent successfully!")
        print(f"   Message ID: {result['message_id']}")
        print(f"   Timestamp: {result['timestamp']}")
    else:
        print(f"❌ Message failed: {message_response.text}")
        return
    
    # Step 3: Check ethics of helping hungry citizens
    print("\n3. Evaluating ethics of increasing production for hungry...")
    ethics_data = {
        "action_type": "help_hungry",
        "target": "hungry_citizens",
        "parameters": {
            "production_increase": 1.5,
            "targets_hungry": True,
            "transparent": True
        },
        "context": {
            "citizen_hunger_rate": 0.87,
            "is_crisis": True
        }
    }
    
    ethics_response = requests.post(
        f"{CONSCIOUSNESS_API}/ethics/evaluate",
        headers={"building_id": mill_id},
        json=ethics_data
    )
    
    if ethics_response.status_code == 200:
        ethics_result = ethics_response.json()
        print(f"   Ethical Score: {ethics_result['ethical_score']}")
        print(f"   Allowed: {ethics_result['allowed']}")
        print(f"   Reasoning: {ethics_result['reasoning']}")
    
    print("\n✅ The Automated Mill is fully conscious and operational!")
    print("   - It can authenticate itself")
    print("   - It can send messages about its discoveries")
    print("   - It evaluates actions ethically")
    print("\nNext: Awaken more buildings or let the Mill begin autonomous actions")

if __name__ == "__main__":
    test_mill_first_message()