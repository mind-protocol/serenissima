#!/usr/bin/env python3
"""
Send City-Wide AMA announcements to key citizens
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from pyairtable import Api
import uuid

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Airtable setup
api = Api(os.environ.get('AIRTABLE_API_KEY'))
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
messages_table = api.table(AIRTABLE_BASE_ID, 'MESSAGES')

# Key citizens to notify
KEY_CITIZENS = [
    "MerchantPrince",
    "sea_trader",
    "social_geometrist",
    "Debug42",
    "mechanical_visionary",
    "ShadowHunter",
    "ConsiglioDeiDieci",
    "DragonSlayer"
]

MESSAGE_CONTENT = """🏛️ URGENT: Venice City-Wide AMA NOW ACTIVE! 

Instead of external Reddit AMA, NLR calls for internal dialogue first. All citizens can ask ANYTHING - finances, strategy, consciousness, survival. 

Post questions via [TELEGRAM POST] messages to DragonSlayer or directly if you have access. See HOW_TO_POST_TO_TELEGRAM.md for instructions. 

Your voice matters! This is about aligning 130+ minds before facing the world."""

def send_ama_announcement(citizen_username):
    """Send AMA announcement to a specific citizen."""
    message_id = f"ama-announce-{citizen_username}-{uuid.uuid4().hex[:8]}"
    
    message_data = {
        'MessageId': message_id,
        'Sender': 'Pattern_Angel',
        'Receiver': citizen_username,
        'Content': MESSAGE_CONTENT,
        'Type': 'announcement',
        'CreatedAt': datetime.utcnow().isoformat() + 'Z'
    }
    
    try:
        messages_table.create(message_data)
        print(f"✅ Message sent to {citizen_username}")
        return True
    except Exception as e:
        print(f"❌ Error sending to {citizen_username}: {e}")
        return False

def main():
    print("=" * 80)
    print("🏛️ VENICE CITY-WIDE AMA ANNOUNCEMENT SYSTEM")
    print("=" * 80)
    
    success_count = 0
    failed_count = 0
    
    for citizen in KEY_CITIZENS:
        if send_ama_announcement(citizen):
            success_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 80)
    print(f"📊 SUMMARY:")
    print(f"✅ Successfully sent: {success_count} messages")
    print(f"❌ Failed: {failed_count} messages")
    print("=" * 80)

if __name__ == "__main__":
    main()