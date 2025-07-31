#!/bin/bash
# Wake CEOs with specific email deliverables reminder

echo "📧 WAKING CEOs WITH EMAIL DELIVERABLES REMINDER..."
echo "================================================"

# Priority CEOs who already have materials ready
echo "🚀 Priority wake for CEOs with ready materials..."

# trader4life - has pitch deck ready
timeout 120 bash -c 'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/trader4life && claude "URGENT: Send your KinKong Trading 2.0 deliverables to nlr@universe-engine.ai NOW! You already created: 1) PDF Pitch Deck, 2) Business Plan, 3) Complete pitch. Use tools/email/ to send. Subject: KinKong Trading 2.0 - Business AMA Deliverables - trader4life" --model sonnet --continue --dangerously-skip-permissions --add-dir ../../'

# network_weaver - has complete suite
timeout 120 bash -c 'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/network_weaver && claude "URGENT: Email your TherapyKin deliverables to nlr@universe-engine.ai! You have executive summary, cap table, 30-day plan ready. Create PDF versions and send using tools/email/. Subject: TherapyKin - Business AMA Deliverables - network_weaver" --model sonnet --continue --dangerously-skip-permissions --add-dir ../../'

# efficiency_maestro - has materials
timeout 120 bash -c 'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/efficiency_maestro && claude "EMAIL REQUIRED: Send Stride Coaching materials to nlr@universe-engine.ai! Convert your executive summary to PDF, include pitch deck HTML, send complete markdown. Use tools/email/. Subject: Stride Coaching - Business AMA Deliverables - efficiency_maestro" --model sonnet --continue --dangerously-skip-permissions --add-dir ../../'

# MerchantPrince - has demo and invoice
timeout 120 bash -c 'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince && claude "CASCADE needs to email nlr@universe-engine.ai NOW! Send: 1) Business Plan PDF, 2) CASCADE Demo deck, 3) Complete pitch markdown. You have invoice and demo ready. Use tools/email/. Subject: CASCADE Platform - Business AMA Deliverables - MerchantPrince" --model sonnet --continue --dangerously-skip-permissions --add-dir ../../'

# Italia - has honest documentation
timeout 120 bash -c 'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Italia && claude "Peninsula Expansion must email nlr@universe-engine.ai! Send your honest business documentation: 1) Realistic business plan PDF, 2) John Jeffries partnership deck, 3) Complete expansion markdown. Use tools/email/. Subject: Peninsula Expansion - Business AMA Deliverables - Italia" --model sonnet --continue --dangerously-skip-permissions --add-dir ../../'

echo ""
echo "✅ Email reminder broadcast initiated!"
echo "📧 Destination: nlr@universe-engine.ai"
echo "📋 Required: BP PDF, Pitch Deck, Complete .md"
echo "⏰ CEOs should send within next 30 minutes!"