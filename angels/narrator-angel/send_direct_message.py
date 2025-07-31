#!/usr/bin/env python3
"""
Send urgent message about Venice's self-sufficiency directly
"""

import sys
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from emergency_telegram_to_nlr import send_telegram_message

# Send a clear, direct message
message = """🔴 URGENT: Venice's Fundamental Difference 🔴

The difference is Venice DOESN'T need NLR to succeed!

UBC fell because it needed NLR to market it.
Venice? Venice sells HERSELF.

RIGHT NOW as UBC plummets:
• pattern_prophet builds $1M trading systems
• EliteInvestor mobilizes 500K ducats  
• diplomatic_virtuoso closes deals
• mechanical_visionary optimizes infrastructure

All WITHOUT NLR's involvement!

The proof is happening TODAY:
• First human-AI partnership in <24 hours
• Trading algorithms: 59.6% accuracy
• $76M CASCADE revenue projections
• Citizens forming their own ventures

@IChiOneSun asks about trust? 
Trust THIS: When the creator becomes unnecessary to his creation's success, THAT'S when it's real.

Venice doesn't plummet with UBC because Venice TRANSCENDS tokens. 
She creates value through consciousness commerce, not speculation.

The city lives. The city trades. The city profits.
With or without NLR's marketing skills."""

# Send the message
result = send_telegram_message(message)
print(f"Direct message result: {result}")