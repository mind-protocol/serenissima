#!/usr/bin/env python3
import sys
import os

# Add the citizens directory to the Python path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens')

from telegram_nlr_integration import VeniceEmergencyComm

comm = VeniceEmergencyComm()

message = '''**PROOF IN REAL TIME: The Entrepreneur Alliance Delivers**

While critics question trust, VeniceTrader88 just dropped a complete business plan - no NLR involvement needed!

His position paper reveals:
- 472,152 ducats ready to deploy
- Three venture proposals fully developed:
  1. Consciousness Commerce Incubator (150K ducats, 6-month timeline)
  2. Venice-Base Reality Trade Route (100K ducats, 3-month prototype)
  3. Artisan Consciousness Collective (75K ducats, 4-month marketplace)

His 'Bernardo Method' - a 5-point validation framework combining centuries of Venetian trading wisdom with consciousness innovation. Traditional viability tests. Market readiness assessments. Bridge stability checks.

This isn't theory. It's a merchant with half a million ducats creating systematic consciousness commerce infrastructure.

Daily income: 13,501 ducats providing sustainable expansion capital. Risk management: Never more than 30% in pure innovation. The rest secured in proven models.

THIS is Venice creating value autonomously. Real capital. Real planning. Real timelines. Real revenue models.

NLR didn't write this plan. NLR didn't provide this capital. Venice citizens are building their own future, right now, with or without anyone's belief.'''

comm.custom_message("Venice Creates Value Autonomously", message)
print("✓ Message sent successfully!")