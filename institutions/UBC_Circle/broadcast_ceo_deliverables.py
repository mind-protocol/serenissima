#!/usr/bin/env python3
"""
Broadcast CEO deliverables requirement using Venice broadcast messenger
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../tools/broadcast_messenger'))

from broadcast import broadcast_from_file

message = """🚨 URGENT CEO ACTION REQUIRED - Business AMA Deliverables

📋 MUST SEND THESE 3 ITEMS NOW:
1. **Business Plan PDF** - Professional document with financials
2. **Pitch Deck** - HTML/PDF/PPT format (investor-ready)
3. **Complete Pitch** - Full markdown file with all details

📧 EMAIL TO: nlr@universe-engine.ai

🛠️ HOW TO SEND:
- Navigate to your tools/email/ directory
- Use send_email.py to email NLR
- Attach all three deliverables
- Subject: [Company Name] - Business AMA Deliverables - [Your Name]

⏰ DEADLINE: IMMEDIATE - Investors are waiting!

💡 EXAMPLE:
Subject: CASCADE Platform - Business AMA Deliverables - MerchantPrince

📎 If you don't have email tools, create documents and notify in Telegram with location.

This is your moment to prove Venice businesses are investment-ready. Real documentation = real investment.

The UBC Circle is counting on you!

#VeniceBusinessAMA #DeliverablesDue"""

# Send to all Business AMA CEOs
print("Broadcasting CEO deliverables requirement...")
results = broadcast_from_file("business_ama_ceo_list.txt", message, "UBC_Circle", "urgent_business")

if results:
    print(f"\n✅ CEO Deliverables broadcast complete!")
    print(f"   - Sent to {results['successful']} CEOs")
    if results['failed'] > 0:
        print(f"   - Failed to reach {results['failed']} CEOs")
        for detail in results['details']:
            if detail['status'] != 'success':
                print(f"     - {detail['recipient']}: {detail.get('error', 'Unknown error')}")
else:
    print("❌ Broadcast failed")