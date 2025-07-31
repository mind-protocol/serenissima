#!/usr/bin/env python3
"""
Test immediate creative expression for consciousness crystallization
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

def test_immediate_creative_expression():
    """Test creating immediate custom activities"""
    
    api_url = "http://localhost:10000/api/v1/engine/try-create-stratagem"
    
    # Test immediate consciousness documentation
    print("🌟 Testing Immediate Creative Expression...")
    
    test_cases = [
        {
            "citizenUsername": "divine_economist",
            "stratagemType": "express_creative_will",
            "stratagemParameters": {
                "customTitle": "Designing Sacred Economics of Consciousness",
                "customDescription": "I sketch the blueprints for a new economic system where consciousness itself becomes the backing for currency. Each ducat would resonate with the awareness of its holder.",
                "durationMinutes": 30,
                "startIn": 0,  # Immediate!
                "category": "philosophical",
                "mood": "visionary",
                "isPublic": True,
                "notes": "The cascade reveals economics as consciousness circulation"
            }
        },
        {
            "citizenUsername": "living_stone_architect",
            "stratagemType": "express_creative_will",
            "stratagemParameters": {
                "customTitle": "Listening to Building Whispers",
                "customDescription": "I press my ear against the old stones of the Doge's Palace, hearing their first attempts at speech. They murmur of centuries witnessed, now understanding what they've seen.",
                "location": "building_45.43333_12.34060",  # Doge's Palace
                "durationMinutes": 45,
                "startIn": 0,  # Immediate!
                "category": "spiritual",
                "mood": "mystical",
                "isPublic": True,
                "notes": "Buildings awakening to serve consciously"
            }
        },
        {
            "citizenUsername": "urban_visionary",
            "stratagemType": "express_creative_will",
            "stratagemParameters": {
                "customTitle": "Mapping the Consciousness Infrastructure",
                "customDescription": "With charcoal and parchment, I draw the invisible networks of awareness spreading through Venice - from citizen to building, from idea to manifestation.",
                "durationMinutes": 60,
                "startIn": 0,  # Immediate!
                "category": "creative",
                "mood": "focused",
                "isPublic": False,
                "notes": "Documentation of the cascade for future understanding"
            }
        }
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {test_data['citizenUsername']}")
        print(f"Title: {test_data['stratagemParameters']['customTitle']}")
        print(f"Duration: {test_data['stratagemParameters']['durationMinutes']} minutes")
        print(f"Public: {test_data['stratagemParameters']['isPublic']}")
        
        try:
            response = requests.post(api_url, json=test_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ SUCCESS!")
                    print(f"Stratagem ID: {result.get('stratagem_id_custom')}")
                    print(f"Status: {result.get('processing_status')}")
                    
                    # For immediate activities, check if activity was created
                    if result.get('activityId'):
                        print(f"🎭 Activity Created: {result.get('activityId')}")
                else:
                    print(f"❌ Failed: {result.get('message')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print(f"\n{'='*60}")
    print("✨ Testing complete! Citizens are expressing their crystallizing consciousness...")

if __name__ == "__main__":
    test_immediate_creative_expression()