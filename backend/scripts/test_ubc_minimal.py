#!/usr/bin/env python3
"""
Test minimal UBC Circle creation
"""

import requests

def test_minimal():
    api_url = "http://localhost:3000/api/institutions"
    
    # Absolute minimum required fields
    minimal_data = {
        "institutionId": "ubc_circle",
        "name": "UBC Circle",
        "type": "economic"
    }
    
    print("Testing minimal institution creation...")
    print(f"Data: {minimal_data}")
    
    try:
        response = requests.post(api_url, json=minimal_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_minimal()