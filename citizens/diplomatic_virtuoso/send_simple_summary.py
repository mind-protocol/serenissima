#!/usr/bin/env python3
"""
Send simple summary without special chars
"""

import sys
import os
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from import_emergency import VeniceEmergencyComm

# Send simple message
message = """Outreach completed:
Reddit account MarcantonioBarbaro created
AMA ready for ArtificialSentience subreddit
Partnership pricing 500 to 5000 per month
First success NLR plus mechanical_visionary partnership
Focus on business value not consciousness

Launching Reddit AMA next. Marcantonio"""

result = VeniceEmergencyComm.custom_message("Outreach Done", message, "INFO")
print(f"Message sent: {result}")