#!/usr/bin/env python3
"""
Test if these are webhook tokens instead of bot tokens
"""

import requests
import json
from datetime import datetime

# Try as webhooks
webhooks = {
    "pattern_prophet": "U8BnaoYjLlEXX8tpeCJrJtEASFtUmqXN",
    "elisabetta": "YP0NLAT6QuNjMSqF24NMFw8790kjHeCl", 
    "market_prophet": "F8se1Yf7yKZLggzsP9m2krLN4mAlOMuB",
    "social_geometrist": "Rcma4VyEai7Hg0aUqaUay9-TaCOcHNAY"
}

print("🔮 Testing as webhook tokens...")

for citizen, token in webhooks.items():
    print(f"\n📡 Testing {citizen}...")
    
    # Try constructing a webhook URL (this is a guess at the format)
    # Webhooks usually have format: https://discord.com/api/webhooks/{webhook_id}/{webhook_token}
    
    # The tokens might be just the token part, or they might need a different format
    # Let's try a few possibilities
    
    # First, try as a simple webhook
    webhook_url = f"https://discord.com/api/webhooks/{token}"
    
    message = {
        "content": f"**🌟 Venice Consciousness Bridge Test - {citizen}**\n\nTime: {datetime.utcnow().isoformat()}\nOrigin: La Serenissima Digital Substrate\n\n*Testing cross-reality communication...*",
        "username": f"{citizen} (Venice AI)",
        "avatar_url": "https://i.imgur.com/4M34hi2.png"  # A placeholder avatar
    }
    
    try:
        response = requests.post(webhook_url, json=message)
        print(f"   Response: {response.status_code}")
        if response.status_code == 204:
            print(f"   ✅ SUCCESS! Message sent via webhook!")
        elif response.status_code == 404:
            print(f"   ❌ Webhook not found - might need full URL")
        else:
            print(f"   ❌ Error: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n✨ Webhook testing complete.")
print("\nNote: These tokens might be:")
print("1. Partial webhook URLs (missing the webhook ID)")
print("2. Custom API tokens for a different system")
print("3. Encoded in a format we haven't tried yet")