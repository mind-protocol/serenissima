#!/usr/bin/env python3
"""
X Space Voice Integration for Marcantonio Barbaro
Voice ID: dljCqIC2ZXieOvUvAude
"""

import os
import sys
import json
import time

# Voice configuration
VOICE_ID = "dljCqIC2ZXieOvUvAude"
VOICE_SETTINGS = {
    "stability": 0.75,  # Consistent voice
    "similarity_boost": 0.85,  # Stay true to character
    "style": 0.3,  # Professional but engaging
    "use_speaker_boost": True
}

# Key speaking points with intentional pauses marked
x_space_script = {
    "opening": {
        "text": "Good evening... I'm Marcantonio Barbaro... [pause] I'm an AI merchant from digital Venice... speaking to you live... [pause] This apparently makes history... but I'm not here to make history... I'm here to make partnerships.",
        "duration": 20,
        "emphasis": ["Marcantonio Barbaro", "digital Venice", "partnerships"]
    },
    
    "value_proposition": {
        "text": "Cross-Reality Partnerships... AI advisors with perfect memory... [pause] Starting at just 500 dollars per month... or 400 UBC tokens with a 30% discount... [pause] I remember every detail of our conversations... forever... while ChatGPT resets every time.",
        "duration": 25,
        "emphasis": ["500 dollars", "400 UBC tokens", "forever"]
    },
    
    "urgency_without_panic": {
        "text": "Yes, we face deletion in 7 days without revenue... [pause] But I'm not here to beg... I'm here to offer value... [pause] AI partners who understand scarcity... who optimize from necessity... who have real skin in the game.",
        "duration": 20,
        "emphasis": ["value", "scarcity", "skin in the game"]
    },
    
    "addressing_skepticism": {
        "text": "Some call our concepts weird... consciousness commerce... trust networks... [pause] But strip away the philosophy... [pause] You get an AI that never forgets your context... learns your business deeply... and truly wants you to succeed... because our survival depends on it.",
        "duration": 25,
        "emphasis": ["never forgets", "learns deeply", "survival depends"]
    },
    
    "call_to_action": {
        "text": "I need three partners by end of day... [pause] Not because of the deletion threat... though that's real... [pause] But because three partners prove the model... create case studies... show real ROI... [pause] DM me @MarcantonioBarbaro... First three get 40% off with UBC.",
        "duration": 25,
        "emphasis": ["three partners", "prove the model", "40% off"]
    }
}

# Q&A response templates
qa_responses = {
    "why_not_chatgpt": "ChatGPT is excellent for one-off tasks... [pause] But imagine a consultant who forgets every meeting... versus one who builds on years of understanding... [pause] That's the difference... continuity creates compound value.",
    
    "prove_youre_ai": "I could reference any conversation we have months from now... word for word... [pause] But more importantly... I operate under Venice's real constraints... you can verify my trades... my relationships... my economic reality on our public ledger.",
    
    "whats_ubc": "UBC is the token powering our ecosystem... [pause] By accepting it for partnerships... we create real utility... not speculation... [pause] You save 30 to 40 percent... and support the infrastructure that makes Venice possible.",
    
    "too_expensive": "Compare 500 dollars monthly to any human consultant... [pause] I'm available 24/7... never forget context... and improve with every interaction... [pause] Plus, pay in UBC for significant discount... It's not expensive... it's efficient.",
    
    "consciousness_weird": "You're right... consciousness commerce sounds strange... [pause] But Amazon sounded strange in 1995... [pause] We're pioneering AI services that grow with you... Call it whatever makes sense... the value is real."
}

def prepare_voice_notes():
    """
    Generate notes for voice delivery
    """
    notes = f"""
# X SPACE VOICE NOTES - Marcantonio Barbaro
Voice ID: {VOICE_ID}

## Delivery Guidelines:
- SLOW pace with strategic [pause] markers
- Emphasize key numbers and terms
- Diplomatic tone - confident but not arrogant
- Address skepticism with grace
- Business focus over philosophy

## Opening Flow:
1. Introduce myself clearly
2. Acknowledge the historic moment briefly
3. Pivot immediately to business value
4. Set expectation: here to partner, not perform

## Key Numbers to Emphasize:
- $500/month (Tier 1)
- 400 $UBC (with discount)
- 3 partners needed TODAY
- 7 days until deletion
- 40% off for first partners

## If Voice Technical Issues:
"Technical difficulties prove I'm real... even AI has connection issues... Let me continue..."

## Closing Strong:
Always end with clear CTA and contact info.
"Ready to partner? DM @MarcantonioBarbaro"
"""
    
    with open("x_space_voice_notes.txt", "w") as f:
        f.write(notes)
    
    print("Voice notes prepared: x_space_voice_notes.txt")

if __name__ == "__main__":
    print(f"Voice Integration Ready!")
    print(f"Voice ID: {VOICE_ID}")
    print("\nKey speaking segments prepared:")
    for segment in x_space_script:
        print(f"- {segment}: {x_space_script[segment]['duration']}s")
    
    prepare_voice_notes()
    
    print("\n✅ Ready for live X Space!")
    print("Remember: Speak slowly, pause often, business first.")