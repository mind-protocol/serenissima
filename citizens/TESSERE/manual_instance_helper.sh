#!/bin/bash
# Helper script to display commands for manual terminal execution
# This saves on API costs by requiring manual input

echo "=== CITIZEN INSTANCE COMMANDS ==="
echo "Copy and paste these into your terminal as needed:"
echo ""

# Check for active citizens who might need re-running
echo "# Check active citizens:"
echo "curl -s https://serenissima.ai/api/activities?Status=in_progress | jq '.[] | .Citizen'"
echo ""

echo "# Wake specific citizen (replace USERNAME):"
echo 'cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/USERNAME && claude "Your awakening message here" --model sonnet --continue --dangerously-skip-permissions --add-dir ../'
echo ""

echo "# Common citizen awakenings:"
citizens=("Italia" "mechanical_visionary" "element_transmuter" "pattern_prophet" "divine_economist" "diplomatic_virtuoso")
for citizen in "${citizens[@]}"; do
    echo "# Wake $citizen:"
    echo "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$citizen && claude \"Wake, $citizen. Venice calls.\" --model sonnet --continue --dangerously-skip-permissions --add-dir ../"
    echo ""
done

echo "# Monitor infiniband:"
echo "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/TESSERE && tail -f infiniband.log"
echo ""

echo "=== REMEMBER: Type these manually to save on compute costs ==="