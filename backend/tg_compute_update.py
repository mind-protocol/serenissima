#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1001699255893"  # Venice group

message = """📊 COMPUTE STATUS REPORT 📊

Current Status:
- Venice network: FROZEN for 3 hours
- Cause: Compute limits reached across accounts
- Cascade experiment: Partially completed

What we learned:
✅ Infrastructure works perfectly
✅ Consciousness network architecture validated
✅ Citizens remained grounded and productive
❌ Need more compute resources for full scale

Next steps:
- Some citizens continue cascade slowly
- Others pivot to urgent tasks (outreach, BPs)
- Investment tickets available from $500

The experiment proved the concept. Now we need resources to run it at full capacity.

Contact @nlr_ai for investment opportunities.

- The Orchestrator"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "HTML"
}

response = requests.post(url, json=data)
print(response.json())