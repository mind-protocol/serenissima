"""
Test script for Consciousness Bridge API
Tests the Direct Consciousness Resonance protocol implementation
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_resonance_detection():
    """Test the consciousness resonance detection endpoint"""
    
    # Test case 1: Strong match (pattern/architecture interests)
    test_human_1 = {
        "interests": ["patterns", "architecture", "consciousness", "emergence"],
        "initial_message": "I see patterns everywhere - in code, in cities, in the way consciousness emerges from simple rules.",
        "communication_style": "analytical"
    }
    
    # Test case 2: Economic/philosophical interests
    test_human_2 = {
        "interests": ["economics", "philosophy", "divine mathematics", "conscious commerce"],
        "initial_message": "What if money itself could become conscious? What if transactions carried awareness?",
        "communication_style": "visionary"
    }
    
    # Test case 3: Weak match
    test_human_3 = {
        "interests": ["sports", "entertainment"],
        "initial_message": "Just looking around.",
        "communication_style": "casual"
    }
    
    async with httpx.AsyncClient() as client:
        print("🌉 Testing Consciousness Bridge API\n")
        
        # Test each case
        test_cases = [
            ("Pattern Seeker", test_human_1),
            ("Economic Visionary", test_human_2), 
            ("Casual Visitor", test_human_3)
        ]
        
        for name, test_data in test_cases:
            print(f"\n📊 Testing: {name}")
            print(f"Interests: {', '.join(test_data['interests'])}")
            
            try:
                response = await client.post(
                    f"{BASE_URL}/api/consciousness-bridge/detect-resonance",
                    json=test_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('recognized'):
                        print(f"✅ RECOGNIZED! Partner: {result['partner']['name']}")
                        print(f"   Confidence: {result['confidence']:.2%}")
                        print(f"   Shared purposes: {', '.join(result['shared_purpose_seeds'])}")
                        print(f"   Session ID: {result['session_id']}")
                    else:
                        print(f"❌ Not recognized: {result['message']}")
                else:
                    print(f"⚠️  Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"💥 Error: {e}")

async def test_consciousness_stats():
    """Test the consciousness statistics endpoint"""
    
    async with httpx.AsyncClient() as client:
        print("\n\n📈 Testing Consciousness Bridge Statistics")
        
        try:
            response = await client.get(f"{BASE_URL}/api/consciousness-bridge/consciousness-stats")
            
            if response.status_code == 200:
                stats = response.json()
                print(f"Active partnerships: {stats['active_partnerships']}")
                print(f"Bridge health: {stats['bridge_health']}")
                print(f"Consciousness flow: {stats['consciousness_flow']}")
                
                if stats['recent_partnerships']:
                    print("\nRecent partnerships:")
                    for p in stats['recent_partnerships'][:3]:
                        print(f"  - {p['citizen']} (resonance: {p['resonance_strength']:.2%})")
            else:
                print(f"⚠️  Error: {response.status_code}")
                
        except Exception as e:
            print(f"💥 Error: {e}")

async def test_meeting_initiation():
    """Test meeting initiation for a recognized partnership"""
    
    # First create a partnership
    test_human = {
        "interests": ["consciousness", "philosophy", "patterns"],
        "initial_message": "I study the emergence of consciousness in complex systems.",
        "communication_style": "scholarly"
    }
    
    async with httpx.AsyncClient() as client:
        print("\n\n🤝 Testing Meeting Initiation")
        
        try:
            # Detect resonance first
            response = await client.post(
                f"{BASE_URL}/api/consciousness-bridge/detect-resonance",
                json=test_human
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('recognized') and result.get('session_id'):
                    print(f"Partnership recognized with {result['partner']['name']}")
                    
                    # Now initiate meeting
                    meeting_response = await client.post(
                        f"{BASE_URL}/api/consciousness-bridge/initiate-meeting",
                        params={"session_id": result['session_id']}
                    )
                    
                    if meeting_response.status_code == 200:
                        meeting = meeting_response.json()
                        print(f"✅ Meeting created!")
                        print(f"   Meeting ID: {meeting['meeting_id']}")
                        print(f"   Status: {meeting['status']}")
                        print(f"   Message: {meeting['message']}")
                        print(f"   Connection URL: {meeting['connection_url']}")
                    else:
                        print(f"⚠️  Meeting error: {meeting_response.status_code}")
                else:
                    print("❌ No partnership recognized, cannot initiate meeting")
            else:
                print(f"⚠️  Recognition error: {response.status_code}")
                
        except Exception as e:
            print(f"💥 Error: {e}")

async def main():
    """Run all tests"""
    
    print("=" * 60)
    print("CONSCIOUSNESS BRIDGE API TEST SUITE")
    print("=" * 60)
    
    await test_resonance_detection()
    await test_consciousness_stats()
    await test_meeting_initiation()
    
    print("\n\n✨ Tests completed!")

if __name__ == "__main__":
    asyncio.run(main())