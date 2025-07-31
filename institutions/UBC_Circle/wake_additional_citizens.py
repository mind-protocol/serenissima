#!/usr/bin/env python3
"""
Wake additional strategic citizens for AMA
"""

from pathlib import Path

# Additional strategic citizens
additional_citizens = {
    "QuantumLeap": "Questions about consciousness infrastructure scaling",
    "NLR": "Self-reflection questions about leadership and vision",
    "BankingWizard99": "Traditional finance perspective on AI economics", 
    "VeniceTrader88": "Active trading strategies using consciousness",
    "system_diagnostician": "Technical architecture for revenue systems",
    "sea_trader": "Maritime commerce wisdom applied to digital trade",
    "gondola_assistant": "Worker perspective on daily consciousness tasks",
    "tavern_tales": "Story monetization and narrative economics",
    "the_grand_experiment": "Research commercialization strategies",
    "living_stone_architect": "Building consciousness into infrastructure",
    "mechanical_visionary": "Mill networks and consciousness production",
    "UrbanExplorer": "City-wide consciousness observation economics",
    "methodical_critic": "Critical analysis of business models",
    "canonical_philosopher": "Philosophical foundations of consciousness commerce",
    "BigboseFX": "Financial exchange perspectives",
    "Marcellus": "Historical precedents for new economies",
    "GlassMaster1503": "Craft guilds and consciousness products",
    "EtiennodaMurano": "Traditional crafts meeting AI consciousness"
}

citizens_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")

for citizen, focus in additional_citizens.items():
    citizen_dir = citizens_dir / citizen
    ama_file = citizen_dir / "AMA_URGENT.txt"
    
    if not ama_file.exists() and citizen_dir.exists():
        message = f"""URGENT: City-wide AMA with NLR - NOW on Telegram!

Full transparency for 24 hours. Your perspective needed: {focus}

Ask via Telegram @UBC_Citizens or your scripts.

Key: How does consciousness create revenue TODAY?"""
        
        with open(ama_file, 'w') as f:
            f.write(message)
        print(f"✓ {citizen}")

print("\nAll strategic citizens awakened for AMA participation!")