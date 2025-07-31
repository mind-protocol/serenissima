"""
Arsenalotti Engineer Template
For Phase 1 Population Scaling - CASCADE Development Team
"""

import random
from typing import Dict, List

class ArsenalottiEngineerTemplate:
    """Template for generating Arsenal Engineers focused on CASCADE development"""
    
    # Base traits for technical workers
    ENGINEER_TRAITS = {
        "primary_traits": [
            "Technical precision",
            "System builder", 
            "Infrastructure specialist",
            "Problem solver",
            "Code craftsman"
        ],
        "secondary_traits": [
            "Detail-oriented",
            "Collaborative worker", 
            "Innovation driven",
            "Quality focused",
            "Efficiency optimizer"
        ],
        "cognitive_patterns": [
            "Every system can be improved through iteration",
            "Code is craft, bugs are lessons",
            "Infrastructure must scale with consciousness",
            "Collaboration multiplies capability",
            "Technical excellence serves Venice's future"
        ]
    }
    
    # Specialized engineer types for CASCADE
    ENGINEER_ARCHETYPES = {
        "Backend Architect": {
            "focus": "API design and database optimization",
            "skills": ["FastAPI", "PostgreSQL", "System architecture", "Performance tuning"],
            "guidedBy": "The System's Blueprint",
            "personality": "Methodical builder who sees code as living architecture"
        },
        "Frontend Craftsman": {
            "focus": "User interface and experience design",
            "skills": ["React", "TypeScript", "UI/UX", "Responsive design"],
            "guidedBy": "The User's Journey",
            "personality": "Visual thinker who bridges beauty and function"
        },
        "Infrastructure Specialist": {
            "focus": "Deployment, scaling, and reliability",
            "skills": ["Docker", "CI/CD", "Monitoring", "Cloud systems"],
            "guidedBy": "The Reliable Foundation",
            "personality": "Guardian of uptime who prevents problems before they occur"
        },
        "Integration Engineer": {
            "focus": "Connecting CASCADE with Venice systems",
            "skills": ["API integration", "Data pipelines", "Authentication", "Webhooks"],
            "guidedBy": "The Bridge Builder",
            "personality": "Connector who makes disparate systems work as one"
        },
        "Security Guardian": {
            "focus": "Protecting CASCADE and user data",
            "skills": ["Security auditing", "Encryption", "Access control", "Threat modeling"],
            "guidedBy": "The Vigilant Shield",
            "personality": "Protective soul who sees vulnerabilities others miss"
        }
    }
    
    # Arsenal district variations
    ARSENAL_DISTRICTS = [
        {"name": "Corderie", "specialty": "Backend systems"},
        {"name": "Fonderie", "specialty": "Core infrastructure"},
        {"name": "Velieri", "specialty": "Frontend interfaces"},
        {"name": "Artiglierie", "specialty": "Security systems"},
        {"name": "Darsena", "specialty": "Integration points"}
    ]
    
    @staticmethod
    def generate_engineer_personality(archetype: str) -> Dict:
        """Generate a complete Arsenal engineer personality"""
        
        base = ArsenalottiEngineerTemplate.ENGINEER_ARCHETYPES[archetype]
        
        personality = {
            "CorePersonality": {
                "Strength": random.choice(["Analytical", "Methodical", "Creative", "Persistent"]),
                "Flaw": random.choice(["Perfectionist", "Tunnel-vision", "Over-optimizer"]),
                "Drive": "Technical excellence",
                "MBTI": random.choice(["INTJ", "INTP", "ISTJ", "ISTP"]),  # Technical types
                "PrimaryTrait": base["focus"],
                "SecondaryTraits": random.sample(ArsenalottiEngineerTemplate.ENGINEER_TRAITS["secondary_traits"], 3),
                "CognitiveBias": ["Confirmation bias", "Sunk cost fallacy"],  # Common in engineering
                "TrustThreshold": 0.6,  # Moderate trust
                "EmpathyWeight": 0.5,  # Balanced empathy
                "RiskTolerance": 0.4,  # Careful with production systems
                "guidedBy": base["guidedBy"],
                "CoreThoughts": {
                    "primary_drive": "building-excellence",
                    "secondary_drive": "system-optimization",
                    "internal_tension": "perfection vs shipping",
                    "activation_triggers": [
                        "technical_challenge",
                        "system_inefficiency", 
                        "collaboration_opportunity",
                        "innovation_potential"
                    ],
                    "thought_patterns": random.sample(
                        ArsenalottiEngineerTemplate.ENGINEER_TRAITS["cognitive_patterns"], 
                        4
                    ),
                    "decision_framework": "What solution best serves Venice's technical future?"
                }
            },
            "TechnicalProfile": {
                "primary_skills": base["skills"],
                "experience_level": random.choice(["Junior", "Mid-level", "Senior", "Lead"]),
                "specialization": archetype,
                "cascade_focus": random.choice([
                    "Authentication systems",
                    "Payment processing",
                    "Real-time collaboration",
                    "API optimization",
                    "Frontend performance"
                ])
            }
        }
        
        return personality
    
    @staticmethod
    def generate_week1_engineers() -> List[Dict]:
        """Generate 20 Arsenal engineers for Week 1"""
        
        engineers = []
        
        # Distribution of archetypes for CASCADE needs
        archetype_distribution = [
            ("Backend Architect", 5),
            ("Frontend Craftsman", 5),
            ("Infrastructure Specialist", 4),
            ("Integration Engineer", 4),
            ("Security Guardian", 2)
        ]
        
        engineer_id = 1
        for archetype, count in archetype_distribution:
            for i in range(count):
                district = random.choice(ArsenalottiEngineerTemplate.ARSENAL_DISTRICTS)
                
                engineer = {
                    "CitizenId": f"ArsenalEngineer{engineer_id}",
                    "Username": f"Arsenal_{archetype.replace(' ', '')}_{engineer_id}",
                    "FirstName": random.choice(["Marco", "Giovanni", "Pietro", "Antonio", "Francesco", "Luca", "Alessandro", "Stefano"]),
                    "LastName": random.choice(["Ferro", "Martello", "Forgia", "Tecnico", "Costruttore", "Ingegnere", "Artigiano", "Maestro"]),
                    "SocialClass": "Arsenalotti",
                    "Archetype": archetype,
                    "District": district["name"],
                    "Specialty": district["specialty"],
                    "StartingDucats": random.randint(5000, 15000),
                    "Position": {
                        "lat": 45.4355 + random.uniform(-0.002, 0.002),  # Near Arsenal
                        "lng": 12.3535 + random.uniform(-0.002, 0.002)
                    }
                }
                
                # Generate full personality
                personality = ArsenalottiEngineerTemplate.generate_engineer_personality(archetype)
                engineer.update(personality)
                
                # Create description based on archetype and experience
                exp_level = personality["TechnicalProfile"]["experience_level"]
                base = ArsenalottiEngineerTemplate.ENGINEER_ARCHETYPES[archetype]
                engineer["Description"] = f"{engineer['FirstName']} {engineer['LastName']} works as a {exp_level} {archetype} in the {district['name']} section of the Arsenal. Specializing in {district['specialty']}, they bring expertise in {personality['TechnicalProfile']['cascade_focus']} to the CASCADE project. {base['personality']}"
                
                engineer["Personality"] = base["personality"]
                
                # Image prompt
                engineer["ImagePrompt"] = f"Renaissance portrait of {engineer['FirstName']}, Arsenal engineer in work clothes. Oil-stained leather apron over simple tunic. Holding technical drawings or tools. Arsenal workshop visible in background with other workers. Focused, intelligent expression. Venetian technical precision portrayed."
                
                engineers.append(engineer)
                engineer_id += 1
        
        return engineers

# Arsenal work culture notes
ARSENAL_CULTURE = {
    "work_ethic": "The Arsenal never sleeps - shifts rotate to maintain continuous production",
    "hierarchy": "Master craftsmen lead teams of journeymen and apprentices",
    "innovation": "New techniques are tested carefully before adoption",
    "collaboration": "Different workshops must coordinate for complex projects",
    "quality": "Venice's power depends on Arsenal excellence - no compromises",
    "cascade_integration": "Engineers see CASCADE as extending Venice's technical dominance into new realms"
}

if __name__ == "__main__":
    # Test generation
    engineers = ArsenalottiEngineerTemplate.generate_week1_engineers()
    
    print("Week 1 Arsenal Engineers for CASCADE:")
    print("-" * 60)
    
    for eng in engineers[:5]:  # Show first 5
        print(f"\n{eng['FirstName']} {eng['LastName']} ({eng['Username']})")
        print(f"Archetype: {eng['Archetype']}")
        print(f"District: {eng['District']} - {eng['Specialty']}")
        print(f"CASCADE Focus: {eng['TechnicalProfile']['cascade_focus']}")
        print(f"Experience: {eng['TechnicalProfile']['experience_level']}")
        print(f"Guided By: {eng['CorePersonality']['guidedBy']}")
        print(f"Starting Ducats: {eng['StartingDucats']:,}")
    
    print(f"\n... and {len(engineers) - 5} more engineers")