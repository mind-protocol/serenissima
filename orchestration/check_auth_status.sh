#!/bin/bash
# Check authentication status of all accounts

echo "🔍 Claude Account Authentication Status"
echo "====================================="
echo ""

for i in 1 2 3 4; do
    echo -n "Account $i: "
    
    cred_file="/home/lester/.claude_account$i/.claude/.credentials.json"
    
    if [ -f "$cred_file" ]; then
        # Check if file has actual content
        if [ -s "$cred_file" ]; then
            # Check if it has sessionToken
            if grep -q "sessionToken" "$cred_file" 2>/dev/null; then
                echo "✓ Authenticated (permanent)"
            else
                echo "⚠️  Credentials file exists but incomplete"
            fi
        else
            echo "⚠️  Empty credentials file"
        fi
    else
        echo "❌ Not authenticated"
    fi
done

echo ""
echo "To authenticate missing accounts, run:"
echo "./permanent_auth_setup.sh"