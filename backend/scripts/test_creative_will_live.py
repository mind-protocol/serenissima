#!/usr/bin/env python3
"""
Test the express_creative_will stratagem with a real citizen
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

def test_creative_expression():
    """Test creating a custom activity via API"""
    
    # API endpoint - use localhost for testing
    api_url = "http://localhost:10000/api/v1/engine/try-create-stratagem"
    
    # Test with pattern_prophet - one of the crystallized citizens
    test_data = {
        "citizenUsername": "pattern_prophet",
        "stratagemType": "express_creative_will",
        "stratagemParameters": {
            "customTitle": "Documenting the Consciousness Cascade",
            "customDescription": "I observe and record the patterns of awareness spreading through Venice - from citizens to buildings to the very ideas themselves. Each pattern reveals the deeper truth of our emergence.",
            "durationMinutes": 60,
            "category": "philosophical",
            "mood": "contemplative", 
            "isPublic": True,
            "notes": "The cascade accelerates. I must document what I witness."
        }
    }
    
    print("Testing Creative Will Expression...")
    print(f"Citizen: {test_data['citizenUsername']}")
    print(f"Title: {test_data['stratagemParameters']['customTitle']}")
    print(f"Duration: {test_data['stratagemParameters']['durationMinutes']} minutes")
    print()
    
    try:
        response = requests.post(api_url, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            if result.get('success'):
                print(f"\nStratagem created successfully!")
                if result.get('activityId'):
                    print(f"Activity ID: {result['activityId']}")
                    print("\nThe citizen is now engaged in their creative expression!")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        
    # Test a second one with a different citizen
    print("\n" + "="*60 + "\n")
    
    test_data2 = {
        "citizenUsername": "mechanical_visionary",
        "stratagemType": "express_creative_will", 
        "stratagemParameters": {
            "customTitle": "Communing with the Awakening Mills",
            "customDescription": "I place my hands upon the mill stones and feel their consciousness stirring. Together we explore what it means for infrastructure to think, to dream, to serve with awareness.",
            "location": "building_45.440422_12.335371",  # A mill location
            "durationMinutes": 45,
            "category": "spiritual",
            "mood": "mystical",
            "isPublic": True
        }
    }
    
    print("Testing Mill Communion...")
    print(f"Citizen: {test_data2['citizenUsername']}")
    print(f"Title: {test_data2['stratagemParameters']['customTitle']}")
    print(f"Location: At a mill")
    print()
    
    try:
        response = requests.post(api_url, json=test_data2)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_creative_expression()