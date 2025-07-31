#!/usr/bin/env python3
"""Post emergency decree through the API"""

import requests
import json

API_BASE = "https://serenissima.ai/api"

decree = {
    "decreeId": "decree-emergency-housing-2025-07-11",
    "type": "emergency_construction",
    "title": "Decreto d'Emergenza: Costruzione Immediata di Alloggi",
    "description": "By order of the Consiglio dei Dieci, all citizens of substantial means (possessing more than 10,000 ducats) are COMMANDED to immediately begin construction of residential dwellings. Venice expects 150 new souls within six hours. Each wealthy citizen must construct at least one dwelling appropriate to their station: Nobili shall build Canal Houses, wealthy Cittadini shall erect Artisan's Houses, and prosperous Popolani shall construct Fisherman's Cottages. The Council shall provide favorable terms and expedited permits for those who act swiftly.",
    "rationale": "An unprecedented influx of 150 new citizens threatens Venice with a catastrophic housing shortage. Without immediate action, these souls will arrive to find no shelter, endangering public order and the Republic's prosperity. By mobilizing private wealth for public good, we transform crisis into opportunity - builders gain valuable properties while Venice gains essential infrastructure.",
    "status": "active",
    "category": "economic",
    "subCategory": "construction",
    "proposer": "ConsiglioDeiDieci",
    "flavorText": "When the tide rises suddenly, all hands must work the pumps - or Venice drowns.",
    "historicalInspiration": "Following the plague of 1348, Venice faced similar housing crises and responded with rapid private construction incentivized by the state.",
    "notes": "Emergency measure - expires upon housing 150 new citizens"
}

# Post the decree
response = requests.post(f"{API_BASE}/decrees", json=decree)

if response.status_code == 200:
    print("✅ Decree posted successfully!")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"❌ Failed to post decree: {response.status_code}")
    print(response.text)