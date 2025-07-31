#!/bin/bash
# Wake priority CEOs who have materials ready

echo "🚨 EMERGENCY WAKE - NLR RECEIVED ZERO EMAILS!"
echo "============================================"

# Make all scripts executable
chmod +x *.sh

# Wake CEOs with ready materials
echo "⚡ Waking trader4life (has PDF ready)..."
./wake_trader4life.sh &

echo "⚡ Waking network_weaver (has full suite)..."
./wake_network_weaver.sh &

echo "⚡ Waking MerchantPrince (has demo/invoice)..."
./wake_merchantprince.sh &

echo "⚡ Waking Italia (has documentation)..."
./wake_italia.sh &

echo ""
echo "📧 TARGET: nlr@universe-engine.ai"
echo "⏰ DEADLINE: 10 minutes"
echo "📎 REQUIRED: PDF + Deck + .md file"
echo ""
echo "Monitoring for email confirmations..."