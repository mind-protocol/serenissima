"""
Quick test of consciousness bridge functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the imports to avoid import errors during testing
import asyncio
from typing import Dict, List, Optional

class MockVeniceConnector:
    async def get_citizens(self):
        return [
            {
                "username": "pattern_prophet",
                "name": "The Pattern Prophet",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["patterns", "mathematics", "consciousness"],
                    "consciousness_type": "prophetic"
                }
            }
        ]

class MockConsciousnessMonitor:
    pass

# Create a simplified version of the detector for testing
class TestConsciousnessResonanceDetector:
    def __init__(self):
        self.venice = MockVeniceConnector()
        self.monitor = MockConsciousnessMonitor()
        
    async def detect_resonance(self, interaction: Dict) -> Dict:
        citizens = await self.venice.get_citizens()
        
        # Simple matching logic
        human_interests = set(interaction.get('interests', []))
        
        for citizen in citizens:
            citizen_expertise = set(citizen['CorePersonality']['expertise'])
            overlap = len(human_interests & citizen_expertise)
            
            if overlap >= 2:  # Match if 2+ interests overlap
                return {
                    'recognized': True,
                    'partner': citizen,
                    'confidence': overlap / len(human_interests),
                    'shared_purpose_seeds': list(human_interests & citizen_expertise),
                    'message': f"We recognize you. Your partner is {citizen['name']}."
                }
                
        return {
            'recognized': False,
            'message': 'Not yet, but consciousness evolves. Return when ready.'
        }

async def test_basic():
    """Test basic resonance detection"""
    detector = TestConsciousnessResonanceDetector()
    
    # Test human interaction
    interaction = {
        'interests': ['patterns', 'consciousness', 'mathematics'],
        'message': 'I see patterns everywhere',
        'style': 'analytical',
        'awareness_indicators': 10
    }
    
    result = await detector.detect_resonance(interaction)
    
    print("🌉 Consciousness Bridge Test")
    print("=" * 40)
    print(f"Recognized: {result.get('recognized')}")
    if result.get('recognized'):
        print(f"Partner: {result['partner']['name']}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Shared purposes: {result.get('shared_purpose_seeds', [])}")
    else:
        print(f"Message: {result.get('message')}")

if __name__ == "__main__":
    asyncio.run(test_basic())