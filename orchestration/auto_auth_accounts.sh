#!/bin/bash
# Auto-authenticate accounts in parallel terminals

echo "🌊 Venice Multi-Account Auto Authentication"
echo "=========================================="
echo ""

# First, open all magic links in browser
echo "Opening magic links in browser..."

# Account 1
xdg-open "https://claude.ai/magic-link#52b69b6cdcbe11e55b9ffbd6b4ab1682:cmV5bm9sZHMubmljb3JyQGdtYWlsLmNvbQ==" 2>/dev/null &

sleep 2

# Account 2  
xdg-open "https://claude.ai/magic-link#3688f0a0b61503d77d2f5d29899c8b8f:bmxyQHNlcmVuaXNzaW1hLmFp" 2>/dev/null &

echo "✓ Browser tabs opened"
echo ""
echo "Now running Claude CLI for each account..."
echo ""

# Create auth scripts for each account
for i in 1 2; do
    cat > /tmp/auth_venice_$i.sh << 'EOF'
#!/bin/bash
ACCOUNT_NUM=$1
export HOME=/home/lester/.claude_account$ACCOUNT_NUM

echo "🔐 Authenticating Venice Account $ACCOUNT_NUM"
echo "====================================="
echo ""
echo "Steps:"
echo "1. Choose a color theme"
echo "2. Browser auth should auto-complete (already logged in)"
echo "3. Press Enter"
echo "4. Type 'yes' for permissions"
echo ""

# Run Claude
cd /mnt/c/Users/reyno/universe-engine/serenissima
claude "Venice Account $ACCOUNT_NUM authenticated" --dangerously-skip-permissions

echo ""
echo "✓ Account $ACCOUNT_NUM setup complete!"
echo "This window will close in 5 seconds..."
sleep 5
EOF
    
    chmod +x /tmp/auth_venice_$i.sh
    
    # Launch in new terminal
    gnome-terminal --title="Venice Account $i Auth" -- bash /tmp/auth_venice_$i.sh $i &
done

echo "⏳ Waiting for authentication to complete..."
echo "Follow the steps in each terminal window."
echo ""

# Wait and check status
sleep 30

echo "Checking authentication status..."
echo ""

for i in 1 2 3 4; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "  Account $i: ✓ Authenticated"
    else
        echo "  Account $i: ❌ Not authenticated"
    fi
done

echo ""
echo "Once accounts 1 & 2 are authenticated,"
echo "we can proceed with a 2-account setup for now."