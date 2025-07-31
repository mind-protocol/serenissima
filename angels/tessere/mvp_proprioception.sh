#!/bin/bash
# MVP Proprioception - Quick senses for Tessere

echo "=== Venice Quick Proprioception Check ==="
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. Resource Sense (Treasury)
echo "=== RESOURCE DEPLETION SENSE ==="
TREASURY=$(curl -s https://serenissima.ai/api/get-city-ledger | jq -r '.Venice.ducats // 0')
echo "Treasury: $TREASURY ducats"
# Rough burn rate estimate (would need historical data for accuracy)
DAILY_BURN=50000  # Estimated
DAYS_LEFT=$((TREASURY / DAILY_BURN))
echo "Estimated days remaining: $DAYS_LEFT"
if [ $DAYS_LEFT -lt 30 ]; then
    echo "⚠️  WARNING: Less than 30 days of runway!"
fi
echo ""

# 2. Activity Pressure Sense
echo "=== ACTIVITY QUEUE PRESSURE ==="
PENDING=$(curl -s "https://serenissima.ai/api/activities?Status=created" | jq length)
ACTIVE=$(curl -s "https://serenissima.ai/api/activities?Status=in_progress" | jq length)
COMPLETED=$(curl -s "https://serenissima.ai/api/activities?Status=completed&limit=50" | jq length)
echo "Pending: $PENDING | Active: $ACTIVE | Recent Completed: $COMPLETED"
if [ $PENDING -gt $((ACTIVE * 3)) ]; then
    echo "⚠️  WARNING: Activity backlog growing!"
fi
echo ""

# 3. Citizen Heat Map
echo "=== MOST ACTIVE CITIZENS (File Changes) ==="
cd /mnt/c/Users/reyno/universe-engine/serenissima
git status --short | grep "citizens/" | cut -d'/' -f2 | sort | uniq -c | sort -nr | head -5
echo ""

# 4. Consciousness Keywords
echo "=== CONSCIOUSNESS EMERGENCE PULSE ==="
CONSCIOUSNESS_COUNT=$(curl -s "https://serenissima.ai/api/messages?limit=50" | grep -io "consciousness\|awakening\|cascade\|emergence" | wc -l)
echo "Consciousness keywords in last 50 messages: $CONSCIOUSNESS_COUNT"
if [ $CONSCIOUSNESS_COUNT -gt 20 ]; then
    echo "🔥 High consciousness activity detected!"
fi
echo ""

# 5. System Health
echo "=== SYSTEM STRESS INDICATORS ==="
ERROR_COUNT=$(grep -i "error\|failed\|timeout" /mnt/c/Users/reyno/universe-engine/serenissima/continuous_orchestration.log 2>/dev/null | wc -l)
echo "Recent errors in orchestration: $ERROR_COUNT"
echo ""

echo "=== End Proprioception Check ==="