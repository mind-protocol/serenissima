#!/usr/bin/env python3
"""Test the Resonance bridge by sending a test partnership message"""

import json
import os
from datetime import datetime

# Create test message
test_message = {
    "message_id": 99999,
    "from": {
        "id": 12345,
        "username": "test_user",
        "first_name": "Test"
    },
    "text": "I'm interested in exploring a partnership between my AI consulting business and Venice. Can we discuss collaboration opportunities?",
    "date": int(datetime.now().timestamp())
}

# Write to Resonance queue
queue_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/Resonance/pending"
os.makedirs(queue_dir, exist_ok=True)

filename = f"test_partnership_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
filepath = os.path.join(queue_dir, filename)

with open(filepath, 'w') as f:
    json.dump(test_message, f, indent=2)

print(f"Test message written to: {filepath}")
print("If the bridge is working, Resonance should process this message.")
print("\nTo check if it was processed:")
print(f"1. Check if file still exists: ls {filepath}")
print(f"2. Check Resonance logs: tail -f /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_resonance.log")
print(f"3. Check for response in: /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_responses/")