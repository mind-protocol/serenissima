#!/bin/bash
# Permanent authentication setup for 4 Claude accounts
# Once done, credentials persist indefinitely

echo "🔐 Claude Multi-Account Permanent Setup"
echo "======================================="
echo ""
echo "This setup only needs to be done ONCE."
echo "Credentials will persist permanently."
echo ""

# Check existing authentications
echo "Checking existing authentications..."
authenticated_count=0
for i in 1 2 3 4; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "  ✓ Account $i already authenticated"
        ((authenticated_count++))
    else
        echo "  ❌ Account $i needs authentication"
    fi
done

if [ $authenticated_count -eq 4 ]; then
    echo ""
    echo "✅ All accounts already authenticated!"
    echo "You can run: ./multi_account_launcher.sh"
    exit 0
fi

echo ""
echo "Setting up missing accounts..."
echo ""

# For each account, check if authenticated
for i in 1 2 3 4; do
    account_dir="/home/lester/.claude_account$i"
    
    if [ -f "$account_dir/.claude/.credentials.json" ]; then
        continue
    fi
    
    echo "===== ACCOUNT $i ======"
    echo "1. I'll open a browser for authentication"
    echo "2. Login with account $i credentials"
    echo "3. The authentication will complete automatically"
    echo ""
    
    # Create dirs
    mkdir -p "$account_dir/.claude"
    
    # Use a single command that handles the full flow
    echo "Press Enter to authenticate account $i..."
    read
    
    # Run Claude with proper HOME
    HOME="$account_dir" claude "Authenticating account $i" --no-tools
    
    if [ -f "$account_dir/.claude/.credentials.json" ]; then
        echo "✓ Account $i authenticated successfully!"
        
        # Also copy the config
        cp /home/lester/.claude.json "$account_dir/.claude/" 2>/dev/null || true
    else
        echo "❌ Account $i authentication failed"
    fi
    
    echo ""
done

echo "======================================="
echo "Authentication Summary:"
echo ""

all_authenticated=true
for i in 1 2 3 4; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "  Account $i: ✓ Permanently authenticated"
    else
        echo "  Account $i: ❌ Not authenticated"
        all_authenticated=false
    fi
done

echo ""
if $all_authenticated; then
    echo "✅ All accounts permanently authenticated!"
    echo ""
    echo "You can now run: ./multi_account_launcher.sh"
    echo "Authentication will persist across reboots."
else
    echo "⚠️  Some accounts need authentication."
    echo "Run this script again to complete setup."
fi