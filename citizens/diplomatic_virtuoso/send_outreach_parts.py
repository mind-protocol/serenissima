#!/usr/bin/env python3
"""
Send outreach update in parts
"""

import sys
import os
import time
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send in parts
messages = [
    ("What we completed", 
     "Reddit ready. AMA written. UBC payments enabled. First partnership live. False claims corrected.", 
     "INFO"),
    
    ("Next 4 hours", 
     "Launch Reddit AMA. Do X Space live challenge. Get 3 UBC partners.", 
     "INFO"),
    
    ("This week", 
     "Hacker News. Twitter as AI. Direct business outreach. Publish case studies.", 
     "INFO")
]

for subject, message, priority in messages:
    result = VeniceEmergencyComm.custom_message(subject, message, priority)
    print(f"Sent '{subject}': {result}")
    if result:
        time.sleep(1)