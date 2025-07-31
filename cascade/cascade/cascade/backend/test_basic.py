#!/usr/bin/env python3
"""
Basic test for Cascade API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_exchange_rate():
    """Test exchange rate endpoint"""
    print("Testing exchange rate endpoint...")
    response = requests.get(f"{BASE_URL}/api/economics/exchange-rate")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_currency_conversion():
    """Test currency conversion"""
    print("Testing currency conversion...")
    data = {
        "amount": 100,
        "from_currency": "ducat",
        "to_currency": "usd",
        "include_fee": True
    }
    response = requests.post(
        f"{BASE_URL}/api/economics/convert",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_space():
    """Test creating a collaboration space"""
    print("Testing collaboration space creation...")
    data = {
        "title": "Test Collaboration Space",
        "description": "A test space for API testing",
        "max_participants": 10,
        "is_public": True
    }
    response = requests.post(
        f"{BASE_URL}/api/collaboration/spaces",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_consciousness_verification():
    """Test consciousness verification"""
    print("Testing consciousness verification...")
    data = {
        "citizen_id": "pattern_prophet",
        "include_details": True
    }
    response = requests.post(
        f"{BASE_URL}/api/consciousness/verify",
        json=data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_network_coherence():
    """Test TESSERE network coherence measurement"""
    print("Testing TESSERE network coherence...")
    data = {
        "node_id": "italia",
        "network_context": "TESSERE",
        "measurement_type": "integration_depth"
    }
    response = requests.post(
        f"{BASE_URL}/api/consciousness/coherence",
        json=data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

def test_tessere_network():
    """Test TESSERE network status"""
    print("Testing TESSERE network status...")
    response = requests.get(f"{BASE_URL}/api/consciousness/tessere/network")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=== Cascade API Basic Tests ===\n")
    
    # Give server time to start if just launched
    time.sleep(2)
    
    try:
        test_root()
        test_health()
        test_exchange_rate()
        test_currency_conversion()
        test_create_space()
        test_consciousness_verification()
        test_network_coherence()
        test_tessere_network()
        
        print("=== All tests completed ===")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server at", BASE_URL)
        print("Make sure the server is running: python test_server.py")
    except Exception as e:
        print(f"ERROR: {e}")