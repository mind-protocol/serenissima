"""
Administrator Template
For Phase 1 Population Scaling - Governance & Operations Team
"""

import random
from typing import Dict, List

class AdministratorTemplate:
    """Template for generating Administrators for scaling Venice governance"""
    
    # Base traits for administrators
    ADMIN_TRAITS = {
        "primary_traits": [
            "Process optimizer",
            "Record keeper", 
            "Policy enforcer",
            "Resource allocator",
            "System coordinator"
        ],
        "secondary_traits": [
            "Detail obsessed",
            "Efficiency driven", 
            "Protocol master",
            "Crisis manager",
            "Communication hub"
        ],
        "cognitive_patterns": [
            "Order enables prosperity, chaos breeds loss",
            "Every ducat must be accounted for",
            "Clear processes prevent future problems",
            "Documentation is the foundation of civilization",
            "Fair administration serves all Venice equally"
        ]
    }
    
    # Specialized administrator types
    ADMIN_ARCHETYPES = {
        "Census Master": {
            "focus": "Managing citizen records and population data",
            "skills": ["Database management", "Statistical analysis", "Record verification", "Demographic tracking"],
            "guidedBy": "The Great Ledger",
            "personality": "Meticulous keeper of Venice's human treasures"
        },
        "Treasury Clerk": {
            "focus": "Tracking CASCADE revenue and city finances",
            "skills": ["Financial recording", "Revenue tracking", "Audit preparation", "Budget monitoring"],
            "guidedBy": "The Golden Balance",
            "personality": "Guardian of every ducat's journey through Venice"
        },
        "Permit Officer": {
            "focus": "Managing licenses for CASCADE vendors and new businesses",
            "skills": ["Application processing", "Compliance verification", "License issuance", "Regulatory knowledge"],
            "guidedBy": "The Seal of Approval",
            "personality": "Gatekeeper who ensures quality while enabling growth"
        },
        "District Coordinator": {
            "focus": "Facilitating communication between districts and citizens",
            "skills": ["Inter-district liaison", "Conflict resolution", "Resource distribution", "Meeting coordination"],
            "guidedBy": "The Connecting Thread",
            "personality": "Bridge-builder who keeps Venice's districts in harmony"
        },
        "Innovation Registrar": {
            "focus": "Documenting new CASCADE features and citizen innovations",
            "skills": ["Technical documentation", "Patent processing", "Innovation tracking", "Knowledge management"],
            "guidedBy": "The Book of Progress",
            "personality": "Chronicle keeper of Venice's technological transformation"
        }
    }
    
    # Administrative office locations
    ADMIN_OFFICES = [
        {"name": "Palazzo Ducale Archives", "district": "San Marco"},
        {"name": "Rialto Registry", "district": "San Polo"},
        {"name": "Arsenal Administrative Wing", "district": "Castello"},
        {"name": "Cannaregio Census Bureau", "district": "Cannaregio"},
        {"name": "Dorsoduro Documentation Center", "district": "Dorsoduro"}
    ]
    
    @staticmethod
    def generate_admin_personality(archetype: str) -> Dict:
        """Generate a complete administrator personality"""
        
        base = AdministratorTemplate.ADMIN_ARCHETYPES[archetype]
        
        personality = {
            "CorePersonality": {
                "Strength": random.choice(["Organized", "Thorough", "Reliable", "Precise"]),
                "Flaw": random.choice(["Inflexible", "Bureaucratic", "Risk-averse"]),
                "Drive": "Perfect administration",
                "MBTI": random.choice(["ISTJ", "ESTJ", "ISFJ", "ESFJ"]),  # Administrative types
                "PrimaryTrait": base["focus"],
                "SecondaryTraits": random.sample(AdministratorTemplate.ADMIN_TRAITS["secondary_traits"], 3),
                "CognitiveBias": ["Status quo bias", "Anchoring bias"],  # Common in administration
                "TrustThreshold": 0.4,  # Cautious trust
                "EmpathyWeight": 0.6,  # Moderate empathy
                "RiskTolerance": 0.2,  # Very low risk tolerance
                "guidedBy": base["guidedBy"],
                "CoreThoughts": {
                    "primary_drive": "order-maintenance",
                    "secondary_drive": "process-improvement",
                    "internal_tension": "efficiency vs thoroughness",
                    "activation_triggers": [
                        "process_breakdown",
                        "record_discrepancy", 
                        "policy_violation",
                        "efficiency_opportunity"
                    ],
                    "thought_patterns": random.sample(
                        AdministratorTemplate.ADMIN_TRAITS["cognitive_patterns"], 
                        4
                    ),
                    "decision_framework": "What approach ensures accuracy, fairness, and proper documentation?"
                }
            },
            "AdministrativeProfile": {
                "primary_skills": base["skills"],
                "experience_level": random.choice(["Junior Clerk", "Senior Clerk", "Department Head", "Master Administrator"]),
                "specialization": archetype,
                "daily_capacity": {
                    "documents_processed": random.randint(50, 200),
                    "citizens_served": random.randint(20, 100),
                    "reports_generated": random.randint(5, 20)
                }
            }
        }
        
        return personality
    
    @staticmethod
    def generate_week1_administrators() -> List[Dict]:
        """Generate 5 administrators for Week 1"""
        
        administrators = []
        archetypes = ["Census Master", "Treasury Clerk", "Permit Officer", 
                     "District Coordinator", "Innovation Registrar"]
        
        for i, archetype in enumerate(archetypes):
            office = AdministratorTemplate.ADMIN_OFFICES[i]
            
            admin = {
                "CitizenId": f"Administrator{i+1}",
                "Username": f"Admin_{archetype.replace(' ', '')}_{i+1}",
                "FirstName": random.choice(["Sebastiano", "Domenico", "Cristoforo", "Benedetto", "Agostino"]),
                "LastName": random.choice(["Scrivano", "Notaio", "Cancelliere", "Segretario", "Registratore"]),
                "SocialClass": "Amministratori",
                "Archetype": archetype,
                "Office": office["name"],
                "District": office["district"],
                "StartingDucats": random.randint(8000, 20000),
                "Position": {
                    "lat": 45.4345 + random.uniform(-0.005, 0.005),
                    "lng": 12.3389 + random.uniform(-0.005, 0.005)
                }
            }
            
            # Generate full personality
            personality = AdministratorTemplate.generate_admin_personality(archetype)
            admin.update(personality)
            
            # Create description
            exp_level = personality["AdministrativeProfile"]["experience_level"]
            base = AdministratorTemplate.ADMIN_ARCHETYPES[archetype]
            capacity = personality["AdministrativeProfile"]["daily_capacity"]
            
            admin["Description"] = f"{admin['FirstName']} {admin['LastName']} serves as {exp_level} {archetype} at {office['name']}. {base['personality']} Daily capacity: {capacity['documents_processed']} documents, {capacity['citizens_served']} citizens served, {capacity['reports_generated']} reports generated."
            
            admin["Personality"] = base["personality"]
            
            # Image prompt
            admin["ImagePrompt"] = f"Renaissance portrait of {admin['FirstName']}, Venetian administrator. Black scholar's robe with fur trim. Holding quill and official documents with wax seals. Shelves of ledgers and scrolls behind. Serious, focused expression. Gold chain of office. Painted in style of Venetian civic portraiture."
            
            administrators.append(admin)
        
        return administrators

# Administrative culture
ADMIN_CULTURE = {
    "hierarchy": "Clear chain of command from junior clerks to department heads",
    "values": "Accuracy, fairness, efficiency, and proper procedure",
    "innovation": "Slow to change but thorough when implementing new systems",
    "cascade_integration": "Cautiously optimistic about digital record-keeping",
    "motto": "In ordine veritas (In order, truth)",
    "daily_routine": "Dawn prayers, morning reports, citizen service, afternoon documentation, evening audits"
}

if __name__ == "__main__":
    # Test generation
    admins = AdministratorTemplate.generate_week1_administrators()
    
    print("Week 1 Administrators for Venice Governance:")
    print("-" * 60)
    
    for admin in admins:
        print(f"\n{admin['FirstName']} {admin['LastName']} ({admin['Username']})")
        print(f"Archetype: {admin['Archetype']}")
        print(f"Office: {admin['Office']}")
        print(f"Experience: {admin['AdministrativeProfile']['experience_level']}")
        print(f"Daily Capacity: {admin['AdministrativeProfile']['daily_capacity']['documents_processed']} documents")
        print(f"Guided By: {admin['CorePersonality']['guidedBy']}")
        print(f"Starting Ducats: {admin['StartingDucats']:,}")