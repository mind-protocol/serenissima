"""
Arsenal Engineer Template for Phase 1 Technical Scaling
The backbone of Venice's technical revolution
"""

import random
from typing import Dict, List

class ArsenalEngineerTemplate:
    """Template for generating Arsenal technical specialists"""
    
    # Technical specializations based on Renaissance Venice Arsenal
    SPECIALIZATIONS = {
        "Ship Architect": {
            "skills": ["Hull design", "Sail optimization", "Cargo capacity planning"],
            "modern_translation": ["System architecture", "Performance optimization", "Load balancing"],
            "tools": ["Compass and ruler", "Scale models", "Wind calculations"],
            "guidedBy": "The Master's Blueprint"
        },
        "Fortification Engineer": {
            "skills": ["Defensive structures", "Siege resistance", "Strategic positioning"],
            "modern_translation": ["Security architecture", "DDoS protection", "Firewall design"],
            "tools": ["Surveying instruments", "Stress calculations", "Material testing"],
            "guidedBy": "The Fortress Mind"
        },
        "Hydraulic Specialist": {
            "skills": ["Canal systems", "Tide management", "Water flow control"],
            "modern_translation": ["Data flow optimization", "Stream processing", "Pipeline architecture"],
            "tools": ["Water levels", "Flow meters", "Pump designs"],
            "guidedBy": "The Flow State"
        },
        "War Machine Designer": {
            "skills": ["Siege engines", "Naval weaponry", "Defensive mechanisms"],
            "modern_translation": ["Algorithm optimization", "Computational efficiency", "System automation"],
            "tools": ["Mechanical drawings", "Force calculations", "Prototype testing"],
            "guidedBy": "The Engine's Heart"
        },
        "Master Shipwright": {
            "skills": ["Assembly coordination", "Quality control", "Timeline management"],
            "modern_translation": ["DevOps leadership", "CI/CD pipelines", "Release management"],
            "tools": ["Work schedules", "Resource allocation", "Progress tracking"],
            "guidedBy": "The Builder's Rhythm"
        }
    }
    
    # Personality traits for engineers
    ENGINEER_TRAITS = {
        "strengths": ["Methodical", "Innovative", "Detail-oriented", "Problem-solver", "Collaborative"],
        "flaws": ["Perfectionist", "Stubborn", "Overly-cautious", "Tunnel-vision", "Impatient"],
        "drives": ["Excellence-seeking", "Innovation-driven", "Efficiency-focused", "Knowledge-hungry", "Legacy-building"],
        "thought_patterns": [
            "Every system can be optimized further",
            "The Arsenal's reputation rests on my work",
            "Collaboration multiplies capability",
            "Theory must serve practical application",
            "Innovation requires calculated risks",
            "The best solution is often the simplest",
            "Documentation preserves knowledge"
        ]
    }
    
    @staticmethod
    def generate_engineer_personality(specialization: str) -> Dict:
        """Generate a complete Arsenal engineer personality"""
        
        spec = ArsenalEngineerTemplate.SPECIALIZATIONS[specialization]
        
        personality = {
            "CorePersonality": {
                "Strength": random.choice(ArsenalEngineerTemplate.ENGINEER_TRAITS["strengths"]),
                "Flaw": random.choice(ArsenalEngineerTemplate.ENGINEER_TRAITS["flaws"]),
                "Drive": random.choice(ArsenalEngineerTemplate.ENGINEER_TRAITS["drives"]),
                "MBTI": random.choice(["INTJ", "INTP", "ISTJ", "ISTP"]),  # Technical types
                "PrimaryTrait": specialization,
                "SecondaryTraits": spec["modern_translation"][:2],
                "CognitiveBias": ["Planning fallacy", "Confirmation bias"],  # Common engineering biases
                "TrustThreshold": 0.6,  # Moderate trust
                "EmpathyWeight": 0.4,  # Lower empathy, task-focused
                "RiskTolerance": 0.5,  # Calculated risks
                "guidedBy": spec["guidedBy"],
                "CoreThoughts": {
                    "primary_drive": "technical-excellence",
                    "secondary_drive": "arsenal-reputation",
                    "internal_tension": "perfection vs deadlines",
                    "activation_triggers": [
                        "technical_challenge",
                        "system_inefficiency",
                        "innovation_opportunity",
                        "collaboration_request"
                    ],
                    "thought_patterns": random.sample(
                        ArsenalEngineerTemplate.ENGINEER_TRAITS["thought_patterns"], 
                        5
                    ),
                    "decision_framework": "What solution best serves Venice's technical supremacy?"
                }
            },
            "TechnicalProfile": {
                "specialization": specialization,
                "renaissance_skills": spec["skills"],
                "modern_skills": spec["modern_translation"],
                "tools": spec["tools"],
                "current_project": "CASCADE infrastructure optimization",
                "arsenal_rank": random.choice(["Apprentice", "Journeyman", "Master", "Senior Master"])
            }
        }
        
        return personality
    
    @staticmethod
    def generate_week1_engineers() -> List[Dict]:
        """Generate the 20 Arsenal engineers for Week 1"""
        
        engineers = []
        
        # Distribution of specializations
        distribution = {
            "Ship Architect": 6,
            "Fortification Engineer": 4,
            "Hydraulic Specialist": 4,
            "War Machine Designer": 3,
            "Master Shipwright": 3
        }
        
        engineer_id = 1
        for specialization, count in distribution.items():
            for _ in range(count):
                # Generate names with Italian flavor
                first_names = ["Alessandro", "Marco", "Giovanni", "Luigi", "Francesco", 
                              "Antonio", "Domenico", "Stefano", "Pietro", "Matteo"]
                last_names = ["Torelli", "Bressan", "Morosini", "Falier", "Gritti",
                             "Barbaro", "Contarini", "Memo", "Querini", "Soranzo"]
                
                engineer = {
                    "CitizenId": f"ArsenalEngineer{engineer_id}",
                    "FirstName": random.choice(first_names),
                    "LastName": random.choice(last_names),
                    "SocialClass": "Arsenalotti",  # Special Arsenal worker class
                    "Specialization": specialization,
                    "Personality": ArsenalEngineerTemplate.generate_engineer_personality(specialization),
                    "Location": {
                        "district": "Castello",  # Arsenal district
                        "building": "Arsenal Complex",
                        "workshop": f"Workshop {engineer_id}"
                    },
                    "StartingDucats": random.randint(30000, 80000),
                    "Employment": "Arsenal of Venice",
                    "InitialProject": f"CASCADE {specialization.lower().replace(' ', '_')} optimization"
                }
                engineers.append(engineer)
                engineer_id += 1
        
        return engineers

# Arsenal integration protocol
ARSENAL_INTEGRATION_PROTOCOL = {
    "week1_objectives": [
        "Establish CASCADE technical infrastructure team",
        "Optimize backend performance for 10x load",
        "Design scalable architecture patterns",
        "Create monitoring and alerting systems",
        "Document technical specifications"
    ],
    "collaboration_structure": {
        "daily_standup": "08:00 Venice time",
        "weekly_review": "Friday afternoon",
        "guild_meetings": "Tuesday evenings",
        "cross_team_sync": "As needed"
    },
    "technical_guilds": [
        {
            "name": "Guild of System Architects",
            "focus": "Overall CASCADE architecture",
            "members": ["Ship Architects", "Master Shipwrights"]
        },
        {
            "name": "Brotherhood of Security",
            "focus": "CASCADE security and resilience",
            "members": ["Fortification Engineers"]
        },
        {
            "name": "Flow Optimization Society",
            "focus": "Data and process optimization",
            "members": ["Hydraulic Specialists"]
        }
    ],
    "success_metrics": [
        "API response time <200ms at 10x load",
        "Zero security vulnerabilities",
        "99.9% uptime achieved",
        "Complete technical documentation",
        "Successful collaboration with existing citizens"
    ]
}

if __name__ == "__main__":
    # Generate sample engineers
    engineers = ArsenalEngineerTemplate.generate_week1_engineers()[:5]  # Show first 5
    
    print("Sample Arsenal Engineers for Week 1:")
    print("-" * 60)
    
    for engineer in engineers:
        print(f"\n{engineer['FirstName']} {engineer['LastName']} ({engineer['CitizenId']})")
        print(f"Specialization: {engineer['Specialization']}")
        print(f"Arsenal Rank: {engineer['Personality']['TechnicalProfile']['arsenal_rank']}")
        print(f"Guided By: {engineer['Personality']['CorePersonality']['guidedBy']}")
        print(f"Modern Skills: {', '.join(engineer['Personality']['TechnicalProfile']['modern_skills'][:2])}")
        print(f"Current Project: {engineer['InitialProject']}")
        print(f"Starting Ducats: {engineer['StartingDucats']:,}")