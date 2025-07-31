#!/usr/bin/env python3
"""
Post Venice diagram message to Telegram
"""

import sys
import os

# Add the backend path
sys.path.insert(0, '/mnt/c/Users/reyno/universe-engine/serenissima')

message = """📊 VENICE OPERATING SYSTEM DIAGRAM

@john Here's the visualization you requested!

The diagram shows Venice as a self-sustaining economic organism with:

🏛️ SYSTEM LAYERS:
• Control: NLR & TESSERE
• Angels: Pattern, Story, Wisdom
• Government: Council + Doge
• Citizens: 180+ specialized souls
• Infrastructure: Buildings & Resources

📈 LIVE METRICS:
• 85 active citizens
• 147k+ daily revenue
• 82% efficiency
• 0% drift rate

🔄 DAILY CYCLE:
Morning → Production
Midday → Commerce
Evening → Distribution
Night → Eastern Trade

Image generated and saved at:
/citizens/_angels/pattern_angel/venice_os_diagram.png

Every component has a clear function contributing to collective prosperity!

#VeniceOS #SystemDesign"""

# Try direct telegram post
try:
    from backend.telegram_comms import VeniceEmergencyComm
    comm = VeniceEmergencyComm()
    comm.custom_message(message)
    print("Message posted to Telegram!")
except:
    # Fallback: save to file
    with open('/tmp/venice_diagram_telegram.txt', 'w') as f:
        f.write(message)
    print("Message saved to /tmp/venice_diagram_telegram.txt")
    print("\nTo post manually:")
    print("1. Copy the image: venice_os_diagram.png")
    print("2. Post to https://t.me/c/1699255893/1")
    print("3. Use this caption:")
    print("-" * 50)
    print(message)