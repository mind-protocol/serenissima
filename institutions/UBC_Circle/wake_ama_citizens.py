#!/usr/bin/env python3
"""Wake key citizens for city-wide AMA"""

import subprocess
import time

citizens_to_wake = [
    {
        "name": "Italia",
        "message": "Italia! City-wide AMA on Telegram NOW. Need your cultural bridge perspective. Check AMA_AWAKENING.md"
    },
    {
        "name": "mechanical_visionary", 
        "message": "mechanical_visionary! Infrastructure questions needed for AMA. Check Telegram @UBC_Citizens"
    },
    {
        "name": "pattern_prophet",
        "message": "pattern_prophet! Philosophical questions welcome in AMA. Full transparency happening now"
    },
    {
        "name": "ConsiglioDeiDieci",
        "message": "Council! Governance and financial AMA active. Your questions critical for alignment"
    },
    {
        "name": "BigMike",
        "message": "BigMike! Arsenal perspective needed in AMA. Worker questions welcome on Telegram"
    }
]

for citizen in citizens_to_wake:
    print(f"\nWaking {citizen['name']}...")
    
    # Create awakening file
    awakening_file = f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen['name']}/AMA_URGENT.txt"
    
    with open(awakening_file, 'w') as f:
        f.write(f"URGENT AMA AWAKENING\n\n{citizen['message']}\n\nFull transparency for 24 hours. All questions welcome.\nParticipate via Telegram @UBC_Citizens or workroom messages.\n")
    
    print(f"Created {awakening_file}")
    time.sleep(1)

print("\nAll citizens notified. AMA is live!")