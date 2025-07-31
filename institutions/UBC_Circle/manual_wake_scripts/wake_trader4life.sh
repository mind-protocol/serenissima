#!/bin/bash
# Manual wake script for trader4life - KinKong Trading 2.0

echo "🚀 Waking trader4life with EMAIL INSTRUCTIONS..."

cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/trader4life && \
claude "URGENT EMAIL ACTION REQUIRED!

Elena, you MUST send your KinKong Trading 2.0 materials to nlr@universe-engine.ai RIGHT NOW!

You already have:
✅ PDF Pitch Deck (KinKong_Trading_2.0_Pitch_Deck.pdf)
✅ Business Plan 
✅ Complete pitch markdown

TO SEND EMAIL:
1. Navigate to your tools/email/ directory
2. Use: python3 send_email.py
3. Recipient: nlr@universe-engine.ai
4. Subject: KinKong Trading 2.0 - Business AMA Deliverables - trader4life
5. Attach: PDF pitch deck, business plan, complete .md file

NLR has received ZERO emails. Investors are waiting. Your $50k investment depends on this!

Send within 10 minutes or lose the opportunity!" \
--model claude-3-sonnet-20241022 \
--continue \
--no-stream