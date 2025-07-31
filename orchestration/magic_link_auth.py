#!/usr/bin/env python3
"""
Automate Claude authentication using magic links
Opens browser for each account to complete auth flow
"""

import webbrowser
import time
import os
import json

def auth_with_magic_link(account_num, magic_link):
    """Open magic link in browser and wait for auth completion"""
    
    print(f"\n🔮 Account {account_num}")
    print(f"Opening magic link in browser...")
    
    # Open the magic link
    webbrowser.open(magic_link)
    
    print("Steps:")
    print("1. Browser will open with Claude")
    print("2. You'll be logged in automatically")
    print("3. Open a NEW terminal and run:")
    print(f"   HOME=/home/lester/.claude_account{account_num} claude 'test'")
    print("4. Complete the CLI auth flow in that terminal")
    print("5. Come back here and press Enter when done")
    
    input("\nPress Enter after completing auth...")
    
    # Check if auth succeeded
    cred_file = f"/home/lester/.claude_account{account_num}/.claude/.credentials.json"
    if os.path.exists(cred_file):
        print(f"✓ Account {account_num} authenticated!")
        return True
    else:
        print(f"❌ Account {account_num} auth failed")
        return False

def main():
    print("🌊 Venice Multi-Account Magic Link Authentication")
    print("================================================")
    print("")
    print("This will open each magic link in your browser.")
    print("You'll need to complete Claude CLI auth for each.")
    print("")
    
    magic_links = {}
    
    # Collect all magic links first
    for i in range(1, 5):
        link = input(f"Paste magic link for account {i} (or Enter to skip): ").strip()
        if link:
            magic_links[i] = link
    
    if not magic_links:
        print("No magic links provided!")
        return
    
    print(f"\n📋 Will authenticate {len(magic_links)} accounts")
    input("Press Enter to start...")
    
    # Process each account
    for account_num, magic_link in magic_links.items():
        auth_with_magic_link(account_num, magic_link)
        
        if account_num < max(magic_links.keys()):
            print("\n⏳ Waiting 5 seconds before next account...")
            time.sleep(5)
    
    # Summary
    print("\n" + "="*50)
    print("Authentication Summary:")
    for i in range(1, 5):
        cred_file = f"/home/lester/.claude_account{i}/.claude/.credentials.json"
        if os.path.exists(cred_file):
            print(f"  Account {i}: ✓ Authenticated")
        else:
            print(f"  Account {i}: ❌ Not authenticated")
    
    print("\nRun ./multi_account_launcher.sh to start all angels!")

if __name__ == "__main__":
    main()