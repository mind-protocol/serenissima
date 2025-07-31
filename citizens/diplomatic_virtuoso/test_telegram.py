#!/usr/bin/env python3
"""
Test telegram with short message
"""

import sys
import os
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Test with very short message
result = VeniceEmergencyComm.test()
print(f"Test result: {result}")

# If test works, send short update
if result:
    short_msg = "Outreach update: Reddit AMA launching in 2hrs. Target: 3 partnerships today. -Marcantonio"
    result2 = VeniceEmergencyComm.custom_message("Update", short_msg, "INFO")
    print(f"Message result: {result2}")
else:
    print("Connection test failed")