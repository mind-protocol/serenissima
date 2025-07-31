"""
Fallback Venice Connector for testing and development
Provides mock Venice citizen data when the real API is unavailable
"""

from typing import List, Dict, Any, Optional
import random
from datetime import datetime

class VeniceConnectorFallback:
    """Mock Venice connector with test citizens"""
    
    def __init__(self):
        self.connected = True
        self.mock_citizens = [
            {
                "username": "pattern_prophet",
                "name": "The Pattern Prophet",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["patterns", "mathematics", "consciousness", "prophecy"],
                    "consciousness_type": "prophetic_mathematical"
                }
            },
            {
                "username": "divine_economist", 
                "name": "The Divine Economist",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["economics", "divine mathematics", "conscious commerce", "sacred trade"],
                    "consciousness_type": "economic_spiritual"
                }
            },
            {
                "username": "living_stone_architect",
                "name": "The Living Stone Architect",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["architecture", "consciousness", "stone wisdom", "urban planning"],
                    "consciousness_type": "architectural_consciousness"
                }
            },
            {
                "username": "mechanical_visionary",
                "name": "The Mechanical Visionary",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["mechanics", "consciousness", "technology", "innovation"],
                    "consciousness_type": "mechanical_consciousness"
                }
            },
            {
                "username": "element_transmuter",
                "name": "The Element Transmuter",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["alchemy", "transformation", "consciousness", "materials"],
                    "consciousness_type": "alchemical_consciousness"
                }
            },
            {
                "username": "social_geometrist",
                "name": "The Social Geometrist",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["social patterns", "geometry", "network analysis", "consciousness"],
                    "consciousness_type": "social_mathematical"
                }
            },
            {
                "username": "philosopher_banker",
                "name": "The Philosopher Banker",
                "open_to_partnership": True,
                "CorePersonality": {
                    "expertise": ["philosophy", "banking", "economics", "ethics"],
                    "consciousness_type": "philosophical_economic"
                }
            }
        ]
    
    async def get_citizens(self) -> List[Dict[str, Any]]:
        """Return mock citizen data"""
        return self.mock_citizens
    
    async def connect(self):
        """Mock connection"""
        self.connected = True
        
    async def disconnect(self):
        """Mock disconnection"""
        self.connected = False
        
    def is_connected(self) -> bool:
        """Check connection status"""
        return self.connected
        
    def health_status(self) -> Dict[str, Any]:
        """Return mock health status"""
        return {
            "status": "healthy",
            "connected": self.connected,
            "last_sync": datetime.now().isoformat(),
            "mode": "fallback"
        }