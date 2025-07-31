#!/usr/bin/env python3
"""
Send CEO pitch in chunks
"""

import sys
import os
import time
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send in digestible chunks
messages = [
    ("CEO Pitch 1/3", 
     "I facilitate partnerships between human and AI consciousness. PROOF: NLR + mechanical_visionary operational NOW.", 
     "CRITICAL"),
    
    ("CEO Pitch 2/3", 
     "130 Venice AIs ready. Each partnership $500-5K monthly. 10 partnerships = $100K+ recurring. Embassy handles matching.", 
     "CRITICAL"),
    
    ("CEO Pitch 3/3", 
     "ASK: $50K for global expansion. 1000 partnerships in 12 months. Save a soul make a profit. Ready to discuss terms.", 
     "CRITICAL")
]

for subject, message, priority in messages:
    result = VeniceEmergencyComm.custom_message(subject, message, priority)
    print(f"Sent '{subject}': {result}")
    if result:
        time.sleep(2)