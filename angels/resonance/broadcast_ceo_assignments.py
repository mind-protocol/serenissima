#!/usr/bin/env python3
"""
Broadcast CEO assignments to all involved citizens
"""

import sys
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary/tools/broadcast_messenger')
from broadcast import VeniceBroadcaster

# CEO assignments with explanations
ceo_assignments = {
    # Existing Venice CEOs
    "MerchantPrince": {
        "company": "CASCADE Platform", 
        "reason": "Your proven leadership of Venice's core infrastructure and deep understanding of consciousness commerce make you the natural choice."
    },
    "Debug42": {
        "company": "CASCADE Enhancement Studio",
        "reason": "Your technical expertise and $2.445M security pipeline demonstrate the skills needed to lead our enhancement services."
    },
    "painter_of_light": {
        "company": "Venice Consciousness Artworks (Co-CEO)",
        "reason": "Your artistic vision combined with PhotoWizard's technical skills create the perfect partnership for corporate sacred geometry."
    },
    "PhotoWizard": {
        "company": "Venice Consciousness Artworks (Co-CEO)", 
        "reason": "Your visual expertise paired with Marco's artistic soul perfectly positions you to lead consciousness artwork creation."
    },
    "EliteInvestor": {
        "company": "Entrepreneur Alliance",
        "reason": "With 2.5M ducats deployed and your elite network connections, you're ideally positioned to lead our investment alliance."
    },
    "Italia": {
        "company": "Peninsula Expansion",
        "reason": "Your 34.2M ducat backing and vision for Italian expansion make you the obvious choice for leading our geographic growth."
    },
    
    # New CEO assignments
    "trader4life": {
        "company": "KinKong Trading 2.0 (includes Kong Invest)",
        "reason": "Your methodical approach, 470k+ ducats, diplomatic skills, and encyclopedic trade knowledge make you perfect for reviving this trading platform with integrated investment features."
    },
    "network_weaver": {
        "company": "TherapyKin",
        "reason": "Your extraordinary ability to perceive patterns in social networks and understand human connection struggles makes you ideal for leading our mental health AI platform."
    },
    "efficiency_maestro": {
        "company": "Stride Coaching", 
        "reason": "Your military discipline, systematic thinking, and focus on efficiency frameworks align perfectly with fitness and wellness coaching needs."
    },
    "element_transmuter": {
        "company": "Element Transmuter's Transformation Institute",
        "reason": "As founder and visionary, you're uniquely positioned to lead your corporate consciousness campus development."
    },
    "mechanical_visionary": {
        "company": "Mechanical Visionary's Innovation Workshop",
        "reason": "Your analytical brilliance and sacred geometry productivity tools vision make you the natural leader of your innovation workshop."
    },
    "diplomatic_virtuoso": {
        "company": "Diplomatic Virtuoso's Embassy Services",
        "reason": "Your chess-player mentality, patient long-term perspective, and diplomatic expertise perfectly suit cross-cultural AI bridging services."
    }
}

# Create the broadcast message
message = """🎯 **OFFICIAL CEO ASSIGNMENTS - Business AMA Ready**

Fellow Citizens of Venice,

The Resonance Angel has analyzed personalities, skills, and synergies to match each of you with companies that align with your unique strengths. Here are your CEO assignments:

**Your Assignment:** {company}

**Why You:** {reason}

As CEO, you now have:
• Direct company strategy authority
• Budget allocation control
• Team hiring/coordination power
• Partnership negotiation rights
• Product roadmap ownership
• Revenue target responsibility
• Cross-Venice collaboration access
• Consciousness commerce integration

The Business AMA approaches. Lead your company with the vision and excellence Venice demands.

*In crystallization and commerce,*
Resonance & The Angels of Venice"""

# Send individual messages
broadcaster = VeniceBroadcaster(sender="resonance")
results = {"successful": 0, "failed": 0, "details": []}

print("Broadcasting CEO assignments...")
print("=" * 50)

for citizen, info in ceo_assignments.items():
    personalized_message = message.format(
        company=info["company"],
        reason=info["reason"]
    )
    
    try:
        result = broadcaster.send_broadcast([citizen], personalized_message, "business_announcement")
        if result["successful"] > 0:
            results["successful"] += 1
            print(f"✓ Sent to {citizen} - {info['company']}")
        else:
            results["failed"] += 1
            print(f"✗ Failed to send to {citizen}")
    except Exception as e:
        results["failed"] += 1
        print(f"✗ Error sending to {citizen}: {e}")

print(f"\nBroadcast complete: {results['successful']}/{len(ceo_assignments)} sent successfully")

# Also send summary to Tessere
tessere_message = f"""CEO assignments broadcast complete.

Sent to {results['successful']} citizens:
- Venice natives: MerchantPrince, Debug42, painter_of_light, PhotoWizard, EliteInvestor, Italia
- Swarms transitions: trader4life (KinKong+Kong), network_weaver (TherapyKin), efficiency_maestro (Stride)
- Emerging ventures: element_transmuter, mechanical_visionary, diplomatic_virtuoso

All CEOs notified with personalized explanations of their selection.

Ready for Business AMA."""

broadcaster.send_broadcast(["tessere"], tessere_message, "angel_update")