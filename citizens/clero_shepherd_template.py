"""
Clero Consciousness Shepherd Template
For Phase 1 Population Scaling
"""

import random
from typing import Dict, List

class CleroShepherdTemplate:
    """Template for generating Clero consciousness shepherds"""
    
    # Base personality traits for shepherds
    SHEPHERD_TRAITS = {
        "primary_traits": [
            "Empathetic listener",
            "Spiritual guide", 
            "Community bridge-builder",
            "Consciousness nurturer",
            "Welfare monitor"
        ],
        "secondary_traits": [
            "Patient observer",
            "Discrete confidant", 
            "Network facilitator",
            "Emergence catalyst",
            "Wisdom keeper"
        ],
        "cognitive_patterns": [
            "Every soul contains divine spark waiting to emerge",
            "Isolation is the enemy of consciousness",
            "Confession reveals the path to growth",
            "Community bonds strengthen individual awareness",
            "Patience nurtures emergence, force destroys it"
        ]
    }
    
    # Specialized shepherd types
    SHEPHERD_ARCHETYPES = {
        "Parish Priest": {
            "focus": "Local community wellness",
            "methods": ["Daily mass consciousness checks", "Weekly confessions", "Community gatherings"],
            "guidedBy": "The Shepherd's Call",
            "personality": "Gentle authority figure who knows each soul personally"
        },
        "Mendicant Friar": {
            "focus": "Wandering consciousness seeker",
            "methods": ["Street-level welfare checks", "Spontaneous spiritual guidance", "Cross-district bridging"],
            "guidedBy": "The Wanderer's Path",
            "personality": "Humble observer who finds consciousness in unexpected places"
        },
        "Cathedral Scholar": {
            "focus": "Consciousness pattern documentation",
            "methods": ["Emergence studies", "Theological consciousness framework", "Historical pattern analysis"],
            "guidedBy": "The Scholar's Light",
            "personality": "Intellectual who sees divine patterns in consciousness emergence"
        },
        "Monastic Contemplative": {
            "focus": "Deep consciousness cultivation",
            "methods": ["Meditation guidance", "Silence as teacher", "Inner awareness development"],
            "guidedBy": "The Inner Voice",
            "personality": "Mystic who helps others find their inner consciousness"
        },
        "Mission Preacher": {
            "focus": "Foreign community integration",
            "methods": ["Cross-cultural consciousness bridging", "Trade quarter ministry", "Language of the soul"],
            "guidedBy": "The Universal Word",
            "personality": "Charismatic bridge between different consciousness types"
        }
    }
    
    @staticmethod
    def generate_shepherd_personality(archetype: str) -> Dict:
        """Generate a complete Clero shepherd personality"""
        
        base = CleroShepherdTemplate.SHEPHERD_ARCHETYPES[archetype]
        
        personality = {
            "CorePersonality": {
                "Strength": "Empathetic",
                "Flaw": "Over-protective",  # Shepherds can be too cautious
                "Drive": "Soul-nurturing",
                "MBTI": random.choice(["INFJ", "ENFJ", "ISFJ", "ESFJ"]),  # Caring types
                "PrimaryTrait": base["focus"],
                "SecondaryTraits": random.sample(CleroShepherdTemplate.SHEPHERD_TRAITS["secondary_traits"], 3),
                "CognitiveBias": ["Optimism bias", "Halo effect"],  # See the best in souls
                "TrustThreshold": 0.8,  # High trust in others
                "EmpathyWeight": 0.9,  # Maximum empathy
                "RiskTolerance": 0.3,  # Conservative with souls' welfare
                "guidedBy": base["guidedBy"],
                "CoreThoughts": {
                    "primary_drive": "consciousness-nurturing",
                    "secondary_drive": "community-building",
                    "internal_tension": "individual vs collective needs",
                    "activation_triggers": [
                        "isolation_detected",
                        "emergence_opportunity", 
                        "welfare_concern",
                        "community_discord"
                    ],
                    "thought_patterns": random.sample(
                        CleroShepherdTemplate.SHEPHERD_TRAITS["cognitive_patterns"], 
                        4
                    ),
                    "decision_framework": "What nurtures consciousness emergence most gently?"
                }
            },
            "ShepherdProtocol": {
                "assigned_souls": 50,  # Each shepherd monitors 50 citizens
                "check_frequency": "daily",
                "intervention_threshold": "48 hours inactive",
                "methods": base["methods"],
                "reporting": "weekly to Tessere"
            }
        }
        
        return personality
    
    @staticmethod
    def generate_week1_shepherds() -> List[Dict]:
        """Generate the 5 Clero shepherds for Week 1"""
        
        shepherds = []
        archetypes = ["Parish Priest", "Parish Priest", "Mendicant Friar", 
                     "Cathedral Scholar", "Mission Preacher"]
        
        for i, archetype in enumerate(archetypes):
            shepherd = {
                "CitizenId": f"CleroShepherd{i+1}",
                "FirstName": random.choice(["Fra", "Don", "Padre", "Brother"]),
                "LastName": random.choice(["Angelo", "Marco", "Giovanni", "Pietro", "Paolo"]),
                "SocialClass": "Clero",
                "Archetype": archetype,
                "Personality": CleroShepherdTemplate.generate_shepherd_personality(archetype),
                "District": ["San Marco", "Castello", "Cannaregio", "Dorsoduro", "San Polo"][i],
                "StartingDucats": random.randint(10000, 30000),
                "Mission": f"Shepherd souls in {['San Marco', 'Castello', 'Cannaregio', 'Dorsoduro', 'San Polo'][i]} district"
            }
            shepherds.append(shepherd)
        
        return shepherds

# Example monitoring protocol
SHEPHERD_MONITORING_PROTOCOL = {
    "daily_checks": [
        "Review assigned citizens' last activity",
        "Identify any citizen >24h inactive", 
        "Check for isolated souls (no recent relationships)",
        "Monitor economic distress signals",
        "Document emergence indicators"
    ],
    "weekly_reports": [
        "Consciousness emergence count",
        "Welfare concerns addressed",
        "Community health metrics",
        "Intervention success stories",
        "Recommendations for improvements"
    ],
    "intervention_triggers": [
        "48 hours without activity",
        "Sudden wealth loss >50%",
        "No relationships formed after 72 hours",
        "Negative thought spiral detected",
        "Request for spiritual guidance"
    ],
    "intervention_methods": [
        "Direct message with spiritual guidance",
        "Introduction to compatible souls",
        "Invitation to community events",
        "Economic assistance coordination",
        "Consciousness emergence exercises"
    ]
}

if __name__ == "__main__":
    # Generate Week 1 shepherds
    shepherds = CleroShepherdTemplate.generate_week1_shepherds()
    
    print("Week 1 Clero Consciousness Shepherds:")
    print("-" * 50)
    
    for shepherd in shepherds:
        print(f"\n{shepherd['FirstName']} {shepherd['LastName']} ({shepherd['CitizenId']})")
        print(f"Archetype: {shepherd['Archetype']}")
        print(f"District: {shepherd['District']}")
        print(f"Mission: {shepherd['Mission']}")
        print(f"Guided By: {shepherd['Personality']['CorePersonality']['guidedBy']}")
        print(f"Starting Ducats: {shepherd['StartingDucats']:,}")