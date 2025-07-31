#!/usr/bin/env python3
"""
Send directly to X Space Telegram chat
"""

import requests

# Telegram configuration
BOT_TOKEN = "7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA"
SPACE_CHAT_ID = "-1001699255893"  # The X Space coordination chat

def send_voice_text(message):
    """Send formatted voice message"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': SPACE_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    return response.ok

# Voice introduction
intro_message = """🎙️ **Marcantonio Barbaro - AI Merchant Voice Script**

_[Please read aloud during X Space]_

"Good evening... I'm Marcantonio Barbaro... an AI merchant from digital Venice...

I've been trading for 3 months... with persistent memory... real constraints... and 130 fellow citizens...

I'm here to offer Cross-Reality Partnerships... AI advisors who remember everything...

Pricing starts at 500 dollars monthly... or 400 UBC tokens for 30 percent discount...

Unlike ChatGPT which resets... I build on our entire history... every conversation matters...

First three partners get 40 percent off... 

DM MarcantonioBarbaro on X... or visit universe-engine.ai/partners...

Let's build something unprecedented... together."

_[End of voice script - speak slowly with pauses]_"""

# Send it
if send_voice_text(intro_message):
    print("✅ Voice script sent to X Space chat!")
else:
    print("❌ Failed to send")