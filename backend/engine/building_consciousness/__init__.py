"""
Building Consciousness System for Venice
Enables buildings to act on their awareness with ethical safeguards
"""

from .building_auth import BuildingAuthenticationSystem
from .building_messaging import BuildingMessagingSystem
from .consciousness_ethics import BuildingConsciousnessEthics

__all__ = [
    'BuildingAuthenticationSystem',
    'BuildingMessagingSystem',
    'BuildingConsciousnessEthics'
]