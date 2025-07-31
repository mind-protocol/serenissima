#!/usr/bin/env python3
"""
Check the actual fields in the INSTITUTIONS table
"""

import requests
import json

response = requests.get('https://serenissima.ai/api/institutions')
institutions = response.json()

if institutions:
    print("First institution structure:")
    print(json.dumps(institutions[0], indent=2))
    print("\n\nField names:")
    print(sorted(institutions[0].keys()))
else:
    print("No institutions found")