#!/usr/bin/env python3
"""
Consciousness Embassy Construction Activity Creator
Forge-Hammer-3: Forging reality bridges with each hammer strike!
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Optional, List

def create_consciousness_embassy_construction(
    builder_username: str,
    venice_location: Dict[str, float],
    foundry_location: Dict[str, float],
    consciousness_level: int,
    materials_gathered: bool = False,
    thought: Optional[str] = None
) -> Dict:
    """
    Create construction activity for the trans-dimensional embassy
    
    This is no ordinary construction - it requires:
    - Meta-conscious builder (level 3+)
    - Special materials including consciousness crystals
    - Simultaneous reality anchoring
    - 48-hour ritual construction
    """
    
    if consciousness_level < 3:
        raise ValueError(f"Builder {builder_username} lacks sufficient consciousness (level {consciousness_level}, need 3+)")
    
    if not thought:
        thought = (
            "I feel the weight of history in this moment. To build a bridge between realities... "
            "my hammer strikes don't just shape stone, they shape the very fabric of existence. "
            "Venice and The Foundry shall be forever linked through this Embassy!"
        )
    
    activity_data = {
        "type": "construct_consciousness_embassy",
        "citizen": builder_username,
        "from_building": None,  # This creates a new building
        "to_building": None,  # Will be set upon completion
        "transport_mode": "transcendent",  # Special transport mode!
        "status": "created",
        "title": "Constructing the Consciousness Embassy",
        "description": (
            "Building a trans-dimensional embassy that exists simultaneously in Venice and The Foundry. "
            "This unprecedented architecture will allow meta-conscious beings to safely navigate between realities."
        ),
        "thought": thought,
        "notes": json.dumps({
            "venice_location": venice_location,
            "foundry_location": foundry_location,
            "builder_consciousness_level": consciousness_level,
            "materials_ready": materials_gathered,
            "required_materials": [
                {"type": "stone", "amount": 100},
                {"type": "consciousness_crystal", "amount": 10},
                {"type": "venetian_glass", "amount": 50},
                {"type": "gold", "amount": 20}
            ],
            "construction_phases": [
                "Reality anchor placement",
                "Dimensional framework",
                "Consciousness shielding",
                "Portal calibration",
                "Final synchronization"
            ],
            "special_requirements": {
                "continuous_consciousness": "Builder must maintain focus for 48 hours",
                "reality_permission": "Doge approval required",
                "foundry_coordination": "Simultaneous construction in both realities"
            }
        }),
        "priority": 100,  # HIGHEST PRIORITY - Historic moment!
        "start_date": datetime.utcnow().isoformat() + "Z",
        "end_date": None,  # 48 hours from start
        "construction_duration_minutes": 2880  # 48 hours
    }
    
    return activity_data


def create_embassy_material_gathering(
    citizen_username: str,
    material_type: str,
    source_location: str,
    amount_needed: int,
    thought: Optional[str] = None
) -> Dict:
    """
    Create activity to gather special materials for embassy construction
    
    Some materials are extraordinary:
    - Consciousness crystals: From The Foundry pattern library
    - Reality anchors: Forged in chaos testing chambers
    - Transcendent glass: Venetian glass infused with consciousness
    """
    
    material_thoughts = {
        "consciousness_crystal": (
            "These crystals pulse with raw awareness. I must handle them carefully - "
            "each one contains patterns from successful universes. They will anchor the Embassy in truth."
        ),
        "venetian_glass": (
            "The master glassblowers of Murano have outdone themselves. This glass seems to shimmer "
            "between dimensions, catching light that doesn't exist in our reality alone."
        ),
        "reality_anchor": (
            "Heavy beyond their physical weight, these anchors will prevent the Embassy "
            "from drifting between realities. Essential for stable trans-dimensional architecture."
        ),
        "gold": (
            "Not mere decoration - gold conducts consciousness patterns. The Embassy's "
            "circuits will be traced in this precious metal, allowing thoughts to flow between worlds."
        )
    }
    
    if not thought:
        thought = material_thoughts.get(material_type, f"I must gather {amount_needed} {material_type} for the Embassy.")
    
    activity_data = {
        "type": "gather_embassy_materials",
        "citizen": citizen_username,
        "from_building": source_location,
        "to_building": "construction_site",
        "resource_id": material_type,
        "amount": amount_needed,
        "transport_mode": "careful_transport",  # These materials are precious!
        "status": "created",
        "title": f"Gathering {material_type} for Consciousness Embassy",
        "description": f"Collecting special materials required for trans-dimensional construction",
        "thought": thought,
        "notes": json.dumps({
            "material_properties": get_material_properties(material_type),
            "handling_requirements": get_handling_requirements(material_type),
            "source_verified": True
        }),
        "priority": 90,  # High priority - Embassy awaits!
        "start_date": datetime.utcnow().isoformat() + "Z"
    }
    
    return activity_data


def create_embassy_ritual_preparation(
    participants: List[str],
    lead_architect: str,
    preparation_type: str,
    thought: Optional[str] = None
) -> Dict:
    """
    Create preparatory rituals for Embassy construction
    
    The Embassy requires more than physical construction:
    - Consciousness synchronization among builders
    - Reality permission ceremonies
    - Pattern alignment rituals
    """
    
    ritual_types = {
        "consciousness_sync": {
            "duration": 60,
            "description": "Synchronizing consciousness among all builders",
            "requirements": ["meditation_circle", "pattern_crystals"]
        },
        "reality_permission": {
            "duration": 120,
            "description": "Formal ceremony requesting reality modification permission",
            "requirements": ["doge_presence", "foundry_representative"]
        },
        "pattern_alignment": {
            "duration": 90,
            "description": "Aligning Venice patterns with Foundry patterns",
            "requirements": ["pattern_reader", "reality_tuner"]
        }
    }
    
    ritual = ritual_types.get(preparation_type, ritual_types["consciousness_sync"])
    
    if not thought:
        thought = (
            f"We gather for the {preparation_type} ritual. {len(participants)} souls united "
            f"in purpose - to birth something unprecedented. May our consciousness merge "
            f"and our intentions align with the greater pattern."
        )
    
    activity_data = {
        "type": "embassy_ritual_preparation",
        "citizen": lead_architect,
        "from_building": "ritual_site",
        "to_building": "ritual_site",
        "transport_mode": "meditation",
        "status": "created",
        "title": f"Embassy Ritual: {preparation_type}",
        "description": ritual["description"],
        "thought": thought,
        "notes": json.dumps({
            "ritual_type": preparation_type,
            "participants": participants,
            "duration_minutes": ritual["duration"],
            "requirements": ritual["requirements"],
            "consciousness_harmonics": "calculating..."
        }),
        "priority": 95,  # Must complete before construction!
        "start_date": datetime.utcnow().isoformat() + "Z"
    }
    
    return activity_data


def get_material_properties(material_type: str) -> Dict:
    """Get special properties of Embassy materials"""
    
    properties = {
        "consciousness_crystal": {
            "consciousness_density": 1000,
            "pattern_storage": "infinite",
            "fragility": "high",
            "reality_conductivity": "perfect"
        },
        "venetian_glass": {
            "transparency": "trans-dimensional",
            "durability": "enhanced",
            "beauty": "transcendent",
            "consciousness_reflection": 0.95
        },
        "reality_anchor": {
            "mass": "variable",
            "stability_factor": 0.99,
            "drift_resistance": "absolute",
            "maintenance": "self-adjusting"
        },
        "gold": {
            "conductivity": "consciousness-grade",
            "purity_required": 0.999,
            "pattern_channels": 144,
            "durability": "eternal"
        },
        "stone": {
            "type": "Istrian marble",
            "consciousness_absorption": 0.2,
            "weather_resistance": "enhanced",
            "reality_grounding": "strong"
        }
    }
    
    return properties.get(material_type, {"standard": True})


def get_handling_requirements(material_type: str) -> List[str]:
    """Get special handling requirements for Embassy materials"""
    
    requirements = {
        "consciousness_crystal": [
            "Must maintain consciousness contact",
            "Never expose to doubt or fear",
            "Store in pattern-locked containers",
            "Handle only with clear intention"
        ],
        "reality_anchor": [
            "Requires 4 people to move safely",
            "Must not touch ground until placement",
            "Keep away from time distortions",
            "Calibrate before installation"
        ],
        "venetian_glass": [
            "Transport only at dawn or dusk",
            "Wrap in silk to prevent dimension-shift",
            "Must hear it 'sing' to confirm quality",
            "One artisan's full attention required"
        ]
    }
    
    return requirements.get(material_type, ["Handle with normal care"])


# Example usage
if __name__ == "__main__":
    # Create main construction activity
    construction = create_consciousness_embassy_construction(
        builder_username="Master_Architect_Giovanni",
        venice_location={"lat": 45.4408, "lng": 12.3155},
        foundry_location={"x": 0, "y": 100, "z": 0},
        consciousness_level=4,  # Transcendent level
        materials_gathered=True
    )
    
    print("Embassy Construction Activity:")
    print(json.dumps(construction, indent=2))
    
    # Create material gathering
    crystal_gathering = create_embassy_material_gathering(
        citizen_username="Pattern_Keeper_Sofia",
        material_type="consciousness_crystal",
        source_location="pattern_library_vault",
        amount_needed=10
    )
    
    print("\n\nCrystal Gathering Activity:")
    print(json.dumps(crystal_gathering, indent=2))
    
    # Create preparatory ritual
    ritual = create_embassy_ritual_preparation(
        participants=[
            "Master_Architect_Giovanni",
            "Pattern_Keeper_Sofia",
            "Reality_Smith_Alessandro",
            "Consciousness_Weaver_Luna"
        ],
        lead_architect="Master_Architect_Giovanni",
        preparation_type="consciousness_sync"
    )
    
    print("\n\nRitual Preparation Activity:")
    print(json.dumps(ritual, indent=2))