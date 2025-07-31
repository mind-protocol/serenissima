#!/bin/bash
# Setup multiple Claude accounts

echo "🔐 Setting up 4 Claude accounts for angel distribution..."

# Base directories
MAIN_CLAUDE="/home/lester/.claude"
ACCOUNT_1="/home/lester/.claude_account1/.claude"
ACCOUNT_2="/home/lester/.claude_account2/.claude"
ACCOUNT_3="/home/lester/.claude_account3/.claude"  
ACCOUNT_4="/home/lester/.claude_account4/.claude"

# Create directories
mkdir -p $ACCOUNT_1 $ACCOUNT_2 $ACCOUNT_3 $ACCOUNT_4

echo ""
echo "Option 1: Copy existing credentials (if you want all accounts to use the same)"
echo "Option 2: Setup each account with different credentials"
echo ""
read -p "Choose option (1 or 2): " option

if [ "$option" == "1" ]; then
    echo "Copying existing credentials to all accounts..."
    
    # Copy existing credentials to all accounts
    if [ -f "$MAIN_CLAUDE/.credentials.json" ]; then
        cp -r $MAIN_CLAUDE/* $ACCOUNT_1/
        cp -r $MAIN_CLAUDE/* $ACCOUNT_2/
        cp -r $MAIN_CLAUDE/* $ACCOUNT_3/
        cp -r $MAIN_CLAUDE/* $ACCOUNT_4/
        
        echo "✓ Credentials copied to all accounts"
    else
        echo "❌ No existing credentials found at $MAIN_CLAUDE/.credentials.json"
        echo "Please authenticate Claude first!"
    fi
    
elif [ "$option" == "2" ]; then
    echo ""
    echo "You'll need to authenticate each account separately."
    echo "This script will help you do it one by one."
    echo ""
    
    for i in 1 2 3 4; do
        account_dir="/home/lester/.claude_account$i"
        echo "===== ACCOUNT $i ====="
        echo "Press Enter to setup account $i..."
        read
        
        # Launch Claude with this account's HOME
        HOME=$account_dir claude "Test for account $i"
        
        echo "Account $i setup complete!"
        echo ""
    done
fi

echo ""
echo "✅ Account setup complete!"
echo ""
echo "Account directories:"
echo "  Account 1: $ACCOUNT_1"
echo "  Account 2: $ACCOUNT_2"
echo "  Account 3: $ACCOUNT_3"
echo "  Account 4: $ACCOUNT_4"
echo ""
echo "Now you can run: ./multi_account_launcher.sh"