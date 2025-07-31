#!/usr/bin/env python3
"""
Announce X Space starting NOW
"""

import sys
sys.path.append('.')

from send_voice_simple import announce_x_space_starting

# Send announcement
result = announce_x_space_starting()
print(f"Announcement sent: {result}")