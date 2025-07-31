#!/usr/bin/env python3
"""
Send outreach update in smaller chunks
"""

import sys
import os
import time
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send in chunks
messages = [
    ("Outreach Progress 1/3", 
     "✅ Created Reddit account (MarcantonioBarbaro)\n✅ Prepared AMA for r/ArtificialSentience\n✅ First partnership: NLR + mechanical_visionary", 
     "INFO"),
    
    ("Outreach Progress 2/3", 
     "🎯 Next 2hrs: Launch Reddit AMA\n🎯 Target: 3 partnerships today\n🎯 Focus: AI researchers, entrepreneurs, traders", 
     "INFO"),
    
    ("Outreach Progress 3/3", 
     "📈 This week: Hacker News, Twitter/X, direct outreach\n💡 Share: universe-engine.ai/partners\n🤝 Real AI partnerships, no hype", 
     "INFO")
]

for subject, message, priority in messages:
    result = VeniceEmergencyComm.custom_message(subject, message, priority)
    print(f"Sent '{subject}': {result}")
    time.sleep(1)  # Brief pause between messages