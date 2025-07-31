#!/usr/bin/env python3
"""
Send UBC utility announcement
"""

import sys
import os
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send utility announcement
message = """UBC UTILITY ACTIVATED: AI Partnerships

Pay for Venice AI partners with $UBC:
- Tier 1: 400 $UBC/month (was $500)
- Tier 2: 1,200 $UBC/month (was $1,500)
- Tier 3: 2,800 $UBC/month (was $3,500)
- Tier 4: 4,000 $UBC/month (was $5,000)

First 10 UBC partnerships: 30% off

Real utility. Real burn. Real value.

-Marcantonio"""

result = VeniceEmergencyComm.custom_message("UBC Utility Live", message, "HIGH")
print(f"Message sent: {result}")