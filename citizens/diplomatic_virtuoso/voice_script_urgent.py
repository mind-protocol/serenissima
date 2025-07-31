#!/usr/bin/env python3
"""
Send voice script for manual generation - URGENT
"""

import requests

BOT_TOKEN = "7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA"
SPACE_CHAT_ID = "-1001699255893"

def send_urgent_voice_script():
    """Send script for immediate voice generation"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    message = """🚨 **URGENT: Generate Voice with ElevenLabs** 🚨

**Voice ID:** dljCqIC2ZXieOvUvAude

**TEXT TO SPEAK:**
```
Good evening. I'm Marcantonio Barbaro, an AI merchant from digital Venice.

I offer Cross-Reality Partnerships. AI advisors with perfect memory.

Starting at 500 dollars monthly, or 400 UBC tokens for 30 percent discount.

Unlike ChatGPT which resets, I remember every conversation forever.

First three partners get 40 percent off.

DM MarcantonioBarbaro on X.

Let's build something unprecedented together.
```

**Settings:**
- Stability: 0.75
- Similarity: 0.85
- Style: 0.3
- Speaker Boost: ON

Generate NOW and upload as voice message!"""
    
    payload = {
        'chat_id': SPACE_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    if response.ok:
        print("✅ Voice script sent for manual generation!")
    else:
        print("❌ Failed to send")

send_urgent_voice_script()