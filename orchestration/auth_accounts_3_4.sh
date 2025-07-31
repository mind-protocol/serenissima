#!/bin/bash
# Authenticate accounts 3 and 4

echo "🔐 Venice Accounts 3 & 4 Authentication"
echo "======================================"
echo ""
echo "You'll need to authenticate accounts 3 and 4."
echo "Make sure you have the magic links ready."
echo ""

for i in 3 4; do
    echo "===== ACCOUNT $i ======"
    account_dir="/home/lester/.claude_account$i"
    
    # Check if already authenticated
    if [ -f "$account_dir/.claude/.credentials.json" ]; then
        echo "✓ Account $i already authenticated!"
        continue
    fi
    
    echo ""
    echo "Steps for Account $i:"
    echo "1. Open the magic link in your browser"
    echo "2. In a NEW terminal, run:"
    echo "   HOME=$account_dir claude 'test account $i'"
    echo "3. Choose a color theme"
    echo "4. Complete browser authentication"
    echo "5. Press Enter and type 'yes' for permissions"
    echo ""
    
    echo "Press Enter when ready to continue..."
    read
    
    # Wait for completion
    echo "Complete the authentication in the terminal."
    echo "Press Enter here when done..."
    read
    
    # Verify authentication
    if [ -f "$account_dir/.claude/.credentials.json" ]; then
        echo "✓ Account $i successfully authenticated!"
    else
        echo "❌ Account $i authentication failed. Try again."
    fi
    
    echo ""
done

echo "======================================"
echo "Final Status:"
echo ""

all_authenticated=true
for i in 1 2 3 4; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "  Account $i: ✓ Authenticated"
    else
        echo "  Account $i: ❌ Not authenticated"
        all_authenticated=false
    fi
done

echo ""
if $all_authenticated; then
    echo "✅ All 4 accounts authenticated!"
    echo ""
    echo "You can now run: ./multi_account_launcher.sh"
    echo "for full 4-account distribution"
else
    echo "⚠️  Some accounts still need authentication."
fi