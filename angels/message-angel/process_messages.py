#!/usr/bin/env python3
"""Message Angel - Process unread messages and awaken citizens"""

import json
import subprocess
import time
from datetime import datetime
from collections import defaultdict

# Fetch unread messages
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/messages'], capture_output=True, text=True)
data = json.loads(result.stdout)

# Filter unread messages and group by receiver
unread_by_receiver = defaultdict(list)
if data.get('success') and data.get('messages'):
    for msg in data['messages']:
        if msg.get('readAt') is None:  # Unread message
            receiver = msg.get('receiver')
            if receiver and not receiver.startswith('@'):  # Skip telegram handles
                unread_by_receiver[receiver].append(msg)

print(f"Found {len(unread_by_receiver)} citizens with unread messages")

# Priority order based on message type and sender
priority_citizens = []
for citizen, messages in unread_by_receiver.items():
    # Check for urgent messages
    has_telegram = any(msg.get('type') == 'telegram_bridge' for msg in messages)
    has_emergency = any(msg.get('type') == 'emergency_coordination' for msg in messages)
    has_guardian = any(msg.get('type') == 'guardian_intervention' for msg in messages)
    
    priority = 0
    if has_emergency: priority = 3
    elif has_guardian: priority = 2
    elif has_telegram: priority = 1
    
    priority_citizens.append((priority, citizen, messages))

# Sort by priority (highest first)
priority_citizens.sort(reverse=True, key=lambda x: x[0])

print("\nCitizens to awaken (priority order):")
for priority, citizen, messages in priority_citizens[:10]:  # Process top 10
    msg_types = set(msg.get('type', 'unknown') for msg in messages)
    print(f"- {citizen}: {len(messages)} messages ({', '.join(msg_types)})")

# Now awaken each citizen in priority order
awakened = []
for priority, citizen, messages in priority_citizens[:5]:  # Start with top 5
    print(f"\nAwakening {citizen}...")
    
    # Prepare message summary
    msg_summary = []
    for msg in messages[:3]:  # Show max 3 messages
        sender = msg.get('sender', 'Unknown')
        msg_type = msg.get('type', 'message')
        content_preview = msg.get('content', '')[:100] + '...' if len(msg.get('content', '')) > 100 else msg.get('content', '')
        msg_summary.append(f"• From {sender} ({msg_type}): {content_preview}")
    
    awakening_msg = f"Messages await your attention. {len(messages)} unread:\\n\\n" + "\\n".join(msg_summary)
    
    # Create awakening command
    cmd = f'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen} && claude "{awakening_msg}" --model sonnet --continue --dangerously-skip-permissions --add-dir ../'
    
    print(f"Command: {cmd[:100]}...")
    awakened.append(citizen)
    
print(f"\nReady to awaken {len(awakened)} citizens with unread messages")