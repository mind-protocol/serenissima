#!/bin/bash
# Setup accounts with provided magic links

echo "🌊 Venice Account Setup with Magic Links"
echo "========================================"
echo ""

# Account 1: reynolds.nicorr@gmail.com
LINK1="https://claude.ai/magic-link#52b69b6cdcbe11e55b9ffbd6b4ab1682:cmV5bm9sZHMubmljb3JyQGdtYWlsLmNvbQ=="

# Account 2: nlr@serenissima.ai  
LINK2="https://claude.ai/magic-link#3688f0a0b61503d77d2f5d29899c8b8f:bmxyQHNlcmVuaXNzaW1hLmFp"

# We need 2 more accounts for full distribution
echo "✓ Account 1: reynolds.nicorr@gmail.com"
echo "✓ Account 2: nlr@serenissima.ai"
echo "❓ Account 3: Need magic link"
echo "❓ Account 4: Need magic link"
echo ""

# Function to setup one account
setup_account() {
    local account_num=$1
    local magic_link=$2
    local email=$3
    
    echo "===== ACCOUNT $account_num ($email) ====="
    
    # Check if already authenticated
    if [ -f "/home/lester/.claude_account$account_num/.claude/.credentials.json" ]; then
        echo "✓ Already authenticated!"
        return
    fi
    
    echo "1. Opening magic link in browser..."
    echo "2. After browser opens, run this in a NEW terminal:"
    echo ""
    echo "   HOME=/home/lester/.claude_account$account_num claude 'test account $account_num'"
    echo ""
    echo "3. Complete the auth flow (choose theme, etc.)"
    echo "4. Return here and press Enter"
    echo ""
    
    # Open browser with magic link
    if command -v xdg-open &> /dev/null; then
        xdg-open "$magic_link" 2>/dev/null
    elif command -v wslview &> /dev/null; then
        wslview "$magic_link"
    else
        echo "Please open this link manually: $magic_link"
    fi
    
    read -p "Press Enter when auth is complete..."
    
    if [ -f "/home/lester/.claude_account$account_num/.claude/.credentials.json" ]; then
        echo "✓ Account $account_num authenticated successfully!"
    else
        echo "❌ Account $account_num auth failed"
    fi
    echo ""
}

# Setup the 2 accounts we have
setup_account 1 "$LINK1" "reynolds.nicorr@gmail.com"
setup_account 2 "$LINK2" "nlr@serenissima.ai"

echo "========================================"
echo "Current Status:"
echo ""

for i in 1 2 3 4; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "  Account $i: ✓ Authenticated"
    else
        echo "  Account $i: ❌ Need authentication"
    fi
done

echo ""
echo "⚠️  Need 2 more magic links for accounts 3 & 4"
echo "This ensures proper distribution of the 19 angels"