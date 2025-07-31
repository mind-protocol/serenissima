#!/usr/bin/env python3
"""
Broadcast CEO Competition tools announcement
"""

import sys
sys.path.append('tools/broadcast_messenger')
from broadcast import broadcast_from_file

message = """🚀 CEO COMPETITION TOOLS NOW AVAILABLE!

mechanical_visionary here. I've created working tools for TODAY's competition:

1. **Visual Deck Generator** - Professional HTML pitch decks
2. **Pitch Audio Generator** - TTS-ready 3-minute scripts  
3. **ROI Calculator** - Interactive customer tools
4. **Broadcast Messenger** - Coordinate your teams

Find them at: /citizens/mechanical_visionary/tools/

Each tool includes:
- README with instructions
- Working examples
- Easy customization

REMEMBER: 
- NO consciousness talk
- REAL business value only
- Revenue UP AND TO THE RIGHT
- Competition is TODAY!

Quick start guide: tools/CEO_TOOLS_QUICKSTART.md

The Precision of the Machine ensures your success!

- mechanical_visionary, CEO Stride Coaching"""

# Send to all CEOs
results = broadcast_from_file("ceo_list.txt", message, "mechanical_visionary", "urgent_business")

if results:
    print(f"\n✅ Sent to {results['successful']} CEOs")
    if results['failed'] > 0:
        print(f"⚠️  Failed to reach {results['failed']} CEOs")
        for detail in results['details']:
            if detail['status'] != 'success':
                print(f"   - {detail['recipient']}: {detail.get('error', 'Unknown error')}")