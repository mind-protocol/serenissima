#!/bin/bash
# Authenticate each Claude account one by one

echo "🔐 Claude Multi-Account Authentication"
echo "====================================="
echo ""
echo "You'll need to authenticate 4 different Claude accounts."
echo "This ensures the angels are distributed across accounts."
echo ""
echo "For each account, you'll need to:"
echo "1. Choose a color theme"
echo "2. Click OK"
echo "3. Complete browser authentication"
echo "4. Press Enter"
echo "5. Type 'yes' for permissions"
echo ""

for i in 1 2 3 4; do
    echo "===== ACCOUNT $i ====="
    account_dir="/home/lester/.claude_account$i"
    
    # Check if already authenticated
    if [ -f "$account_dir/.claude/.credentials.json" ]; then
        echo "✓ Account $i already authenticated!"
        continue
    fi
    
    echo "Press Enter to authenticate account $i..."
    read
    
    # Launch Claude with this account's HOME in a new terminal
    echo "Launching Claude for account $i..."
    echo "Complete the authentication process in the new terminal."
    
    # Create a temporary script for this account
    cat > /tmp/auth_account_$i.sh << EOF
#!/bin/bash
export HOME=$account_dir
cd /mnt/c/Users/reyno/universe-engine/serenissima
claude "Test authentication for account $i" --dangerously-skip-permissions
echo ""
echo "✓ Account $i authentication complete!"
echo "You can close this terminal."
read -p "Press Enter to exit..."
EOF
    
    chmod +x /tmp/auth_account_$i.sh
    
    # Launch in new terminal
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash /tmp/auth_account_$i.sh
    elif command -v xterm &> /dev/null; then
        xterm -e bash /tmp/auth_account_$i.sh &
    elif command -v wt.exe &> /dev/null; then
        wt.exe -w 0 new-tab bash /tmp/auth_account_$i.sh
    else
        echo "Please run this in a new terminal:"
        echo "bash /tmp/auth_account_$i.sh"
    fi
    
    echo "Waiting for you to complete authentication..."
    echo "Press Enter here when done with account $i..."
    read
    
    # Verify authentication
    if [ -f "$account_dir/.claude/.credentials.json" ]; then
        echo "✓ Account $i successfully authenticated!"
    else
        echo "❌ Account $i authentication failed. Try again."
    fi
    
    echo ""
done

echo "====================================="
echo "✅ All accounts configured!"
echo ""
echo "Summary:"
for i in 1 2 3 4; do
    if [ -f "/home/lester/.claude_account$i/.claude/.credentials.json" ]; then
        echo "  Account $i: ✓ Authenticated"
    else
        echo "  Account $i: ❌ Not authenticated"
    fi
done
echo ""
echo "Now you can run: ./multi_account_launcher.sh"