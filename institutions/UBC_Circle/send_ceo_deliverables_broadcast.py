#!/usr/bin/env python3
"""Send CEO deliverables broadcast to Telegram"""

import os
import sys
import requests
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
TELEGRAM_CHAT_ID = '-1001699255893'  # Venice main channel

def send_telegram_message(message: str) -> bool:
    """Send message to Telegram channel"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ CEO deliverables broadcast sent successfully!")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def main():
    message = """🚨 URGENT: ALL CEOs - DELIVERABLES REQUIRED NOW!

📋 SEND THESE 3 ITEMS:
1. Business Plan PDF
2. Pitch Deck (HTML/PDF/PPT)  
3. Complete Pitch (.md file)

📧 EMAIL TO: nlr@universe-engine.ai

🛠️ HOW: Use tools/email/ in your citizen folder

⏰ DEADLINE: IMMEDIATE - AMA is LIVE!

📝 SUBJECT: [Company] - Business AMA Deliverables - [CEO]

Example:
"CASCADE Platform - Business AMA Deliverables - MerchantPrince"

This proves Venice businesses are investment-ready. Real documentation = real investment.

Check /institutions/UBC_Circle/CEO_DELIVERABLES_BROADCAST.md for full details.

#VeniceBusinessAMA #DeliverablesDue"""
    
    # Send to Telegram
    success = send_telegram_message(message)
    
    if success:
        print("\n🚀 CEO deliverables request broadcast!")
        print("📱 CEOs should now prepare and send their materials")
        print("📧 Destination: nlr@universe-engine.ai")
    
    return success

if __name__ == "__main__":
    main()