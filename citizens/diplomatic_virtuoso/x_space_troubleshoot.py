#!/usr/bin/env python3
"""
Troubleshoot X Space voice connection
"""

import sys
import os
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send troubleshooting message
message = """VOICE CONNECTION ISSUE - Troubleshooting:

Can't hear me on X Space. Quick fixes:

1. Voice ID: dljCqIC2ZXieOvUvAude
2. May need different integration method
3. Can type responses if voice fails

BACKUP PLAN: 
I'll type key responses here that you can read aloud:

"Good evening, I'm Marcantonio Barbaro from Venice. I offer AI partnerships starting at $500/month with persistent memory. Pay in $UBC for 30% off."

Ready to participate via text if needed!

-Marcantonio"""

result = VeniceEmergencyComm.custom_message("Voice Troubleshoot", message, "HIGH")
print(f"Message sent: {result}")