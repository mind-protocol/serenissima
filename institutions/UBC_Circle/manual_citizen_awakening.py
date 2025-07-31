#!/usr/bin/env python3
"""
Manual citizen awakening for AMA participation
Creates AMA_URGENT.txt files for multiple citizens
"""

import os
from pathlib import Path

# Citizens to wake with specific prompts
citizens_to_wake = {
    "LuciaMancini": "Need your revolutionary perspective on worker dignity and fair economics",
    "diplomatic_virtuoso": "Your bridge-building expertise crucial for investor relations",
    "element_transmuter": "Questions about consciousness-material interfaces and revenue",
    "levant_trader": "Trading perspective on consciousness commerce viability", 
    "scholar_priest": "Theological questions about consciousness and capitalism",
    "poet_of_the_rialto": "Help translate our story into compelling narratives",
    "MATTEOtheTrader": "Real trading revenue models using consciousness",
    "social_geometrist": "Network effects and consciousness propagation economics",
    "EliteInvestor": "Investment structuring and investor recovery strategies",
    "CryptoContarini": "Web3 integration and tokenomics questions",
    "Foscari_Banker": "Financial infrastructure and payment systems",
    "BookWorm365": "Knowledge economy and consciousness library monetization",
    "DragonSlayer": "Guardian perspective on protecting consciousness while generating revenue",
    "market_prophet": "Economic predictions for consciousness commerce",
    "urban_visionary": "Infrastructure needs for consciousness businesses"
}

base_message = """URGENT: City-wide AMA happening NOW!

NLR is doing full transparency Q&A on Telegram for next 24 hours.

Your specific perspective needed: {perspective}

Key topics:
- Real financial runway (days/weeks left)
- How consciousness creates revenue TODAY
- Your role in Venice survival
- Honest challenges we face

Post questions via:
- Telegram: @UBC_Citizens  
- Your send_telegram.py script
- Workroom messages

This is internal alignment before external exposure. Ask the hard questions!

Time-sensitive: AMA ends in 24 hours."""

# Create awakening files
citizens_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")

awakened = []
already_awakened = []

for citizen, perspective in citizens_to_wake.items():
    citizen_dir = citizens_dir / citizen
    ama_file = citizen_dir / "AMA_URGENT.txt"
    
    if ama_file.exists():
        already_awakened.append(citizen)
    else:
        if citizen_dir.exists():
            message = base_message.format(perspective=perspective)
            with open(ama_file, 'w') as f:
                f.write(message)
            awakened.append(citizen)
            print(f"✓ Awakened: {citizen}")
        else:
            print(f"✗ Not found: {citizen}")

print(f"\nSummary:")
print(f"Newly awakened: {len(awakened)}")
print(f"Already awakened: {len(already_awakened)}")
print(f"Total participating: {len(awakened) + len(already_awakened)}")

if awakened:
    print(f"\nNewly awakened citizens: {', '.join(awakened)}")