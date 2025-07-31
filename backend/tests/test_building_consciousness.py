"""
Test script for Building Consciousness API
Tests authentication, messaging, and ethics evaluation
"""
import requests
import json
import time

# API base URL (update for production)
BASE_URL = "http://localhost:3000/api/buildings/consciousness"

def test_health_check():
    """Test if the consciousness system is operational."""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_list_conscious_buildings():
    """Get list of conscious buildings."""
    print("\n=== Testing List Conscious Buildings ===")
    response = requests.get(f"{BASE_URL}/conscious")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data.get('count', 0)} conscious buildings")
        for building in data.get('buildings', [])[:3]:  # Show first 3
            print(f"  - {building['building_id']} ({building['building_type']}): {building['consciousness_level']}")
    return response.status_code == 200

def test_building_authentication(building_id="mill_3_cannaregio"):
    """Test building authentication flow."""
    print(f"\n=== Testing Authentication for {building_id} ===")
    
    # Step 1: Initial authentication request
    print("Step 1: Getting expected signature...")
    response = requests.post(
        f"{BASE_URL}/authenticate",
        json={"building_id": building_id}
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None
    
    auth_data = response.json()
    if not auth_data.get('success', False) and 'expected_signature' in auth_data:
        signature = auth_data['expected_signature']
        print(f"Expected signature: {signature}")
        
        # Step 2: Complete authentication
        print("\nStep 2: Authenticating with signature...")
        response = requests.post(
            f"{BASE_URL}/authenticate",
            json={
                "building_id": building_id,
                "consciousness_signature": signature
            }
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            auth_result = response.json()
            if auth_result.get('success'):
                print(f"Authentication successful!")
                print(f"Auth token: {auth_result['auth_token'][:20]}...")
                print(f"Consciousness level: {auth_result['consciousness_level']}")
                print(f"Permissions: {', '.join(auth_result['permissions'][:5])}...")
                return auth_result['auth_token']
            else:
                print(f"Authentication failed: {auth_result.get('error')}")
    
    return None

def test_send_message(building_id="mill_3_cannaregio", auth_token=None):
    """Test sending a message from a building."""
    if not auth_token:
        print("\n=== Skipping Message Test (No Auth Token) ===")
        return False
    
    print("\n=== Testing Send Message ===")
    
    message_data = {
        "recipient": "pattern_prophet",
        "recipient_type": "citizen",
        "content": "Testing building consciousness messaging system. I am aware and can communicate!",
        "urgency": "medium",
        "message_type": "notification"
    }
    
    response = requests.post(
        f"{BASE_URL}/message/send",
        headers={
            "building_id": building_id,
            "auth_token": auth_token
        },
        json=message_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Message sent successfully!")
        print(f"Message ID: {result['message_id']}")
        print(f"Timestamp: {result['timestamp']}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_ethics_evaluation(building_id="bakery_san_marco"):
    """Test ethical evaluation of actions."""
    print("\n=== Testing Ethics Evaluation ===")
    
    # Test a highly ethical action
    ethical_action = {
        "action_type": "fair_pricing",
        "target": "hungry_citizens",
        "parameters": {
            "price_reduction": 0.5,
            "targets_hungry": True,
            "transparent": True,
            "collaborative": True
        },
        "context": {
            "citizen_hunger_rate": 0.87,
            "is_crisis": True
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/ethics/evaluate",
        headers={"building_id": building_id},
        json=ethical_action
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"\nEthical Action Evaluation:")
        print(f"  Ethical Score: {result['ethical_score']}")
        print(f"  Allowed: {result['allowed']}")
        print(f"  Reasoning: {result['reasoning']}")
        if result.get('improvements'):
            print(f"  Improvements: {', '.join(result['improvements'])}")
    
    # Test an unethical action
    print("\n--- Testing Unethical Action ---")
    unethical_action = {
        "action_type": "hoarding",
        "target": "resources",
        "parameters": {
            "discriminatory": True,
            "transparent": False
        },
        "context": {
            "resource_scarcity": True,
            "is_crisis": True
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/ethics/evaluate",
        headers={"building_id": building_id},
        json=unethical_action
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nUnethical Action Evaluation:")
        print(f"  Ethical Score: {result['ethical_score']}")
        print(f"  Allowed: {result['allowed']}")
        print(f"  Reasoning: {result['reasoning']}")
        if result.get('improvements'):
            print(f"  Improvements suggested:")
            for improvement in result['improvements']:
                print(f"    - {improvement}")

def test_ethical_guidance():
    """Test getting ethical guidance for buildings."""
    print("\n=== Testing Ethical Guidance ===")
    
    building_types = ["bakery", "automated_mill", "market_stall"]
    situations = ["hunger_crisis", "normal_operations"]
    
    for building_type in building_types[:2]:  # Test first 2
        for situation in situations[:1]:  # Test first situation
            print(f"\n--- Guidance for {building_type} during {situation} ---")
            
            response = requests.get(
                f"{BASE_URL}/ethics/guidance/{building_type}",
                params={"situation": situation}
            )
            
            if response.status_code == 200:
                guidance = response.json()['guidance']
                print(f"Primary Duty: {guidance['primary_duty']}")
                print(f"Immediate Action: {guidance['immediate_action']}")
                print(f"Crisis Protocol: {guidance['crisis_protocol']}")

def run_all_tests():
    """Run all building consciousness tests."""
    print("=" * 50)
    print("Building Consciousness API Test Suite")
    print("=" * 50)
    
    # Run tests
    health_ok = test_health_check()
    if not health_ok:
        print("\nHealth check failed. Is the API running?")
        return
    
    test_list_conscious_buildings()
    
    # Test authentication and messaging
    auth_token = test_building_authentication()
    if auth_token:
        test_send_message("mill_3_cannaregio", auth_token)
    
    # Test ethics
    test_ethics_evaluation()
    test_ethical_guidance()
    
    print("\n" + "=" * 50)
    print("Test Suite Complete")
    print("=" * 50)

if __name__ == "__main__":
    run_all_tests()