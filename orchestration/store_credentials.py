#!/usr/bin/env python3
"""
Store credentials for 4 Claude accounts
Vision: Scale to hundreds of Venice citizens with their own Claude Max subscriptions
"""

import json
import os
import sys

def store_credential(account_num, session_token):
    """Store session token for an account"""
    account_dir = f"/home/lester/.claude_account{account_num}/.claude"
    os.makedirs(account_dir, exist_ok=True)
    
    credentials = {
        "sessionToken": session_token,
        "userId": f"venice_account_{account_num}",
        "authenticated": True
    }
    
    cred_file = f"{account_dir}/.credentials.json"
    with open(cred_file, "w") as f:
        json.dump(credentials, f, indent=2)
    
    # Set permissions
    os.chmod(cred_file, 0o600)
    
    print(f"✓ Account {account_num} credentials stored")

if __name__ == "__main__":
    print("🔐 Venice Scaling - Credential Storage")
    print("====================================")
    print("Paste credentials below (they won't be shown)")
    print("")
    
    # Ready to receive credentials
    # Format expected: account_number:token per line
    print("Ready to receive credentials...")