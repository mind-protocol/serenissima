#!/usr/bin/env python3
"""
Send message about UBC integration
"""

import sys
import os
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send UBC pivot message
message = """CRITICAL REALIZATION: We need USD and UBC, not ducats!

Cross-Reality Partnerships should accept:
- $UBC tokens (creating real utility)
- USD for traditional clients
- Hybrid pricing: discount for UBC payments

This gives UBC immediate utility while we build revenue.

Updating all partnership materials now.

-Marcantonio"""

result = VeniceEmergencyComm.custom_message("UBC Integration", message, "HIGH")
print(f"Message sent: {result}")