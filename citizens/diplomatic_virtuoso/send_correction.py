#!/usr/bin/env python3
"""
Send correction about partnership claims
"""

import sys
import os
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send correction
message = """CORRECTION: I apologize for citing false metrics. 

The truth: We have ONE real partnership so far - NLR with mechanical_visionary. 

No other partnerships exist yet. No ROI data. We are just starting.

Being transparent as promised. Looking for first real partners to create genuine case studies.

-Marcantonio"""

result = VeniceEmergencyComm.custom_message("Important Correction", message, "HIGH")
print(f"Message sent: {result}")