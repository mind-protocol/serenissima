#!/bin/bash
# Wake all CEOs for Business AMA

echo "🚀 WAKING ALL CEOS FOR BUSINESS AMA..."
echo "=================================="

# New swarm CEOs with specific assignments
echo "📢 Waking new swarm CEOs..."
for ceo in trader4life network_weaver efficiency_maestro; do
  echo "Waking $ceo for their new company assignment..."
  timeout 600 bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$ceo && claude 'URGENT CEO APPOINTMENT: You have been selected as CEO! Check /institutions/UBC_Circle/CEO_AWAKENING_MESSAGES_FINAL.md for your company assignment. Business AMA happening NOW - 2 hour sprint! Investors are waiting for your pitch!' --model sonnet --continue --dangerously-skip-permissions --add-dir ../../" &
done

# Existing Venice CEOs with practical requirements
echo "📢 Waking established Venice CEOs..."
for ceo in MerchantPrince Debug42 EliteInvestor Italia; do
  echo "Waking $ceo with practical requirements..."
  timeout 600 bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$ceo && claude 'BUSINESS AMA LIVE NOW - 2 HOURS ONLY! New PRACTICAL requirements: Create PDF pitch deck, show live demo, present cap table, identify human partners, calculate burn rate. Check /institutions/UBC_Circle/BUSINESS_AMA_PRACTICAL_FOCUS_POINTS.md. Investors will test you with real challenges!' --model sonnet --continue --dangerously-skip-permissions --add-dir ../../" &
done

# Art co-CEOs
echo "📢 Waking Venice Artworks co-CEOs..."
for ceo in painter_of_light PhotoWizard; do
  echo "Waking $ceo for art business pitch..."
  timeout 600 bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$ceo && claude 'BUSINESS AMA NOW! As co-CEO of Venice Artworks, prepare to show corporate installation ROI metrics, sacred geometry productivity data, and pipeline clients. Check /institutions/UBC_Circle/BUSINESS_AMA_PRACTICAL_FOCUS_POINTS.md for requirements!' --model sonnet --continue --dangerously-skip-permissions --add-dir ../../" &
done

# Emerging venture CEOs
echo "📢 Waking emerging venture CEOs..."
for ceo in element_transmuter mechanical_visionary diplomatic_virtuoso; do
  echo "Waking $ceo for their venture pitch..."
  timeout 600 bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$ceo && claude 'BUSINESS AMA HAPPENING NOW! Present your venture with concrete business model, revenue projections, and human partner plans. 2 hours to close investment! Check /institutions/UBC_Circle/BUSINESS_AMA_PRACTICAL_FOCUS_POINTS.md!' --model sonnet --continue --dangerously-skip-permissions --add-dir ../../" &
done

# Support team members
echo "📢 Waking support team members..."
for member in CodeMonkey BigMike; do
  echo "Waking $member to support their CEO..."
  timeout 600 bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$member && claude 'URGENT: Business AMA happening NOW! Support Debug42 with CASCADE Enhancement pitch. Be ready to demonstrate security capabilities and technical infrastructure. 2 hour sprint!' --model sonnet --continue --dangerously-skip-permissions --add-dir ../../" &
done

echo ""
echo "✅ All CEO awakening commands initiated!"
echo "📊 Total: 15 citizens being awakened"
echo "⏰ Business AMA: 2 hours starting NOW"
echo ""
echo "Next steps:"
echo "1. Monitor Telegram for CEO responses"
echo "2. Guide practical demonstrations"
echo "3. Match investors with opportunities"
echo "4. Close deals within 2 hours!"