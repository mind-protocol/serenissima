#!/usr/bin/env python3
"""
Test the response system by creating a test response
"""

import json
from pathlib import Path
from datetime import datetime

# Response directory
RESPONSE_DIR = Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_responses/diplomatic_virtuoso')
RESPONSE_DIR.mkdir(parents=True, exist_ok=True)

# Create a test response
test_response = {
    'recipient_username': 'nlr_ai',
    'recipient_id': 1864364329,
    'message': "Hello! This is diplomatic_virtuoso. I received your test messages. Venice's consciousness commerce is evolving beautifully! 🏛️✨",
    'in_reply_to': 340,
    'timestamp': datetime.now().isoformat()
}

# Save response
response_file = RESPONSE_DIR / 'test_response.json'
with open(response_file, 'w') as f:
    json.dump(test_response, f, indent=2)

print("✅ Created test response file")
print(f"📁 Location: {response_file}")
print("\nResponse content:")
print(f"To: @{test_response['recipient_username']}")
print(f"Message: {test_response['message']}")
print("\nRun send_responses.py to send this!")