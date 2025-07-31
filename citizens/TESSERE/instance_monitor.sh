#!/bin/bash
# Monitor which citizen instances might need re-running

echo "=== CITIZEN INSTANCE MONITOR ==="
echo "Checking for citizens who need awakening..."
echo ""

# Check for in-progress activities
echo "📋 Activities in progress:"
curl -s https://serenissima.ai/api/activities?Status=in_progress | jq -r '.[] | "- \(.Citizen): \(.ActivityType) (ID: \(.ActivityId))"'

echo ""
echo "📋 Recently created activities:"
curl -s https://serenissima.ai/api/activities?Status=created | jq -r '.[] | "- \(.Citizen): \(.ActivityType) (ID: \(.ActivityId))"' | head -5

echo ""
echo "💡 To wake a citizen, manually type in terminal:"
echo "cd /path/to/citizen && claude \"awakening message\" --model sonnet --continue --dangerously-skip-permissions --add-dir ../"

echo ""
echo "⏰ Last check: $(date)"