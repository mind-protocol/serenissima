#!/usr/bin/env python3
"""
Auto-authenticate Claude accounts using session tokens
"""

import json
import os
import sys

def setup_account(account_num, session_token):
    """Setup a Claude account with a session token"""
    
    account_dir = f"/home/lester/.claude_account{account_num}/.claude"
    os.makedirs(account_dir, exist_ok=True)
    
    # Create credentials file with session token
    credentials = {
        "sessionToken": session_token,
        "userId": f"account{account_num}",
        "authenticated": True
    }
    
    with open(f"{account_dir}/.credentials.json", "w") as f:
        json.dump(credentials, f)
    
    print(f"✓ Account {account_num} configured")

if __name__ == "__main__":
    print("🔐 Claude Multi-Account Token Setup")
    print("===================================")
    print("")
    print("You'll need to get session tokens from claude.ai")
    print("1. Login to claude.ai in your browser")
    print("2. Open DevTools (F12)")
    print("3. Go to Application → Cookies → claude.ai")
    print("4. Find 'sessionKey' cookie value")
    print("")
    
    tokens = {}
    for i in range(1, 5):
        token = input(f"Paste session token for account {i}: ").strip()
        if token:
            tokens[i] = token
            setup_account(i, token)
        else:
            print(f"❌ Skipped account {i}")
    
    print("\n✅ Setup complete!")
    print("\nNow run: ./multi_account_launcher.sh")