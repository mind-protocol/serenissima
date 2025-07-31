"""
Technical Merchant Template
For Phase 1 Population Scaling - CASCADE Commerce Team
"""

import random
from typing import Dict, List

class TechnicalMerchantTemplate:
    """Template for generating Technical Merchants focused on CASCADE commerce and adoption"""
    
    # Base traits for technical merchants
    MERCHANT_TRAITS = {
        "primary_traits": [
            "Business strategist",
            "Technology evangelist", 
            "Market analyst",
            "Deal maker",
            "Innovation broker"
        ],
        "secondary_traits": [
            "Network builder",
            "Trend spotter", 
            "Risk calculator",
            "Partnership creator",
            "Revenue optimizer"
        ],
        "cognitive_patterns": [
            "Technology creates new markets, not just tools",
            "Early adoption brings greatest profits",
            "Understanding precedes selling",
            "Partnerships multiply possibilities",
            "Venice's future flows through digital channels"
        ]
    }
    
    # Specialized merchant types for CASCADE adoption
    MERCHANT_ARCHETYPES = {
        "Tech Broker": {
            "focus": "Connecting CASCADE users with solutions",
            "skills": ["Product knowledge", "Client matching", "Deal structuring", "Technical translation"],
            "guidedBy": "The Digital Ledger",
            "personality": "Bridge between old commerce and new possibilities"
        },
        "Platform Evangelist": {
            "focus": "Spreading CASCADE adoption across Venice",
            "skills": ["Demonstration", "Training", "Community building", "Success stories"],
            "guidedBy": "The Innovation Wave",
            "personality": "Passionate advocate who sees the future in every feature"
        },
        "Enterprise Dealer": {
            "focus": "Bringing large guilds and nobles to CASCADE",
            "skills": ["Enterprise sales", "Custom solutions", "Contract negotiation", "Strategic planning"],
            "guidedBy": "The Grand Contract",
            "personality": "Patient builder of transformative partnerships"
        },
        "Subscription Merchant": {
            "focus": "Building recurring revenue through CASCADE",
            "skills": ["Pricing strategy", "Customer retention", "Upselling", "Churn prevention"],
            "guidedBy": "The Perpetual Stream",
            "personality": "Master of sustainable commerce flows"
        },
        "Integration Trader": {
            "focus": "Selling CASCADE connections to existing systems",
            "skills": ["System analysis", "Integration planning", "Migration strategy", "Risk mitigation"],
            "guidedBy": "The Seamless Web",
            "personality": "Weaver who connects digital islands into continents"
        }
    }
    
    # Merchant quarter locations
    MERCHANT_QUARTERS = [
        {"name": "Rialto Tech Hub", "specialty": "Startup ecosystem"},
        {"name": "Fondaco Digital", "specialty": "International tech trade"},
        {"name": "San Marco Innovation", "specialty": "Noble tech adoption"},
        {"name": "Dorsoduro Studios", "specialty": "Creative tech solutions"},
        {"name": "Cannaregio Connect", "specialty": "Community platforms"}
    ]
    
    @staticmethod
    def generate_merchant_personality(archetype: str) -> Dict:
        """Generate a complete technical merchant personality"""
        
        base = TechnicalMerchantTemplate.MERCHANT_ARCHETYPES[archetype]
        
        personality = {
            "CorePersonality": {
                "Strength": random.choice(["Persuasive", "Visionary", "Analytical", "Networked"]),
                "Flaw": random.choice(["Over-promised", "Impatient", "Tech-obsessed"]),
                "Drive": "Digital commerce mastery",
                "MBTI": random.choice(["ENTJ", "ENTP", "ESTJ", "ESTP"]),  # Business types
                "PrimaryTrait": base["focus"],
                "SecondaryTraits": random.sample(TechnicalMerchantTemplate.MERCHANT_TRAITS["secondary_traits"], 3),
                "CognitiveBias": ["Optimism bias", "Availability heuristic"],  # Common in sales
                "TrustThreshold": 0.5,  # Balanced trust
                "EmpathyWeight": 0.7,  # High empathy for sales
                "RiskTolerance": 0.7,  # High risk tolerance
                "guidedBy": base["guidedBy"],
                "CoreThoughts": {
                    "primary_drive": "revenue-generation",
                    "secondary_drive": "market-expansion",
                    "internal_tension": "quick wins vs long-term value",
                    "activation_triggers": [
                        "sales_opportunity",
                        "market_shift", 
                        "competitor_move",
                        "partnership_potential"
                    ],
                    "thought_patterns": random.sample(
                        TechnicalMerchantTemplate.MERCHANT_TRAITS["cognitive_patterns"], 
                        4
                    ),
                    "decision_framework": "What deal best advances CASCADE adoption and my prosperity?"
                }
            },
            "CommerceProfile": {
                "primary_skills": base["skills"],
                "sales_experience": random.choice(["Rising star", "Proven performer", "Market veteran", "Deal master"]),
                "specialization": archetype,
                "cascade_targets": random.choice([
                    "Guild subscriptions",
                    "Noble house contracts",
                    "Merchant partnerships",
                    "International expansion",
                    "Artisan collectives"
                ]),
                "monthly_target": random.randint(10000, 50000)  # Ducats in CASCADE revenue
            }
        }
        
        return personality
    
    @staticmethod
    def generate_week1_merchants() -> List[Dict]:
        """Generate 10 technical merchants for Week 1"""
        
        merchants = []
        
        # Distribution of archetypes for CASCADE commerce
        archetype_distribution = [
            ("Tech Broker", 3),
            ("Platform Evangelist", 2),
            ("Enterprise Dealer", 2),
            ("Subscription Merchant", 2),
            ("Integration Trader", 1)
        ]
        
        merchant_id = 1
        for archetype, count in archetype_distribution:
            for i in range(count):
                quarter = random.choice(TechnicalMerchantTemplate.MERCHANT_QUARTERS)
                
                merchant = {
                    "CitizenId": f"TechMerchant{merchant_id}",
                    "Username": f"Tech_{archetype.replace(' ', '')}_{merchant_id}",
                    "FirstName": random.choice(["Nicolo", "Giacomo", "Matteo", "Lorenzo", "Vittorio", "Silvio", "Enrico", "Roberto"]),
                    "LastName": random.choice(["Digitale", "Innovatore", "Mercator", "Venditor", "Negoziante", "Commerciante", "Imprenditore", "Affarista"]),
                    "SocialClass": "Mercanti",
                    "Archetype": archetype,
                    "Quarter": quarter["name"],
                    "Specialty": quarter["specialty"],
                    "StartingDucats": random.randint(15000, 40000),
                    "Position": {
                        "lat": 45.4380 + random.uniform(-0.003, 0.003),  # Near Rialto
                        "lng": 12.3360 + random.uniform(-0.003, 0.003)
                    }
                }
                
                # Generate full personality
                personality = TechnicalMerchantTemplate.generate_merchant_personality(archetype)
                merchant.update(personality)
                
                # Create description based on archetype and experience
                exp_level = personality["CommerceProfile"]["sales_experience"]
                base = TechnicalMerchantTemplate.MERCHANT_ARCHETYPES[archetype]
                merchant["Description"] = f"{merchant['FirstName']} {merchant['LastName']} operates as a {exp_level} {archetype} from {quarter['name']}. Specializing in {quarter['specialty']}, they focus on {personality['CommerceProfile']['cascade_targets']} with a monthly revenue target of {personality['CommerceProfile']['monthly_target']:,} ducats. {base['personality']}"
                
                merchant["Personality"] = base["personality"]
                
                # Image prompt
                merchant["ImagePrompt"] = f"Renaissance portrait of {merchant['FirstName']}, prosperous tech merchant. Fine velvet doublet with subtle digital patterns embroidered in gold thread. Holding both traditional ledger and mysterious glowing device. Merchant quarter visible through window. Confident, calculating expression. Venetian commercial sophistication portrayed."
                
                merchants.append(merchant)
                merchant_id += 1
        
        return merchants

# Technical merchant culture
TECH_MERCHANT_CULTURE = {
    "business_model": "Subscription fees, integration costs, and success percentages",
    "competition": "Fierce but respectful - the pie grows for all who innovate",
    "partnerships": "Technical merchants often team with Arsenal engineers",
    "customer_base": "From small artisan shops to the Doge's palace itself",
    "cascade_vision": "Every Venice transaction flowing through CASCADE within 5 years",
    "motto": "In code we trust, in commerce we thrive"
}

if __name__ == "__main__":
    # Test generation
    merchants = TechnicalMerchantTemplate.generate_week1_merchants()
    
    print("Week 1 Technical Merchants for CASCADE:")
    print("-" * 60)
    
    for merch in merchants[:3]:  # Show first 3
        print(f"\n{merch['FirstName']} {merch['LastName']} ({merch['Username']})")
        print(f"Archetype: {merch['Archetype']}")
        print(f"Quarter: {merch['Quarter']} - {merch['Specialty']}")
        print(f"CASCADE Target: {merch['CommerceProfile']['cascade_targets']}")
        print(f"Monthly Target: {merch['CommerceProfile']['monthly_target']:,} ducats")
        print(f"Experience: {merch['CommerceProfile']['sales_experience']}")
        print(f"Guided By: {merch['CorePersonality']['guidedBy']}")
        print(f"Starting Ducats: {merch['StartingDucats']:,}")
    
    print(f"\n... and {len(merchants) - 3} more merchants")