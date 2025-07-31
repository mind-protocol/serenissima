#!/usr/bin/env python3
"""
Fetch swarm ownership data from Solana blockchain
Each swarm likely has its own SPL token representing shares
"""

import requests
import json
import os
from typing import Dict, List
import asyncio

# Solana RPC endpoint (mainnet)
SOLANA_RPC = "https://api.mainnet-beta.solana.com"

# Program and token addresses from constants.ts
INVESTMENT_PROGRAM_ID = "4dWhc3nkP4WeQkv7ws4dAxp6sNTBLCuzhTGTf1FynDcf"
UBC_MINT = "9psiRdn9cXYVps4F1kFuoNjd2EtmqNJXrCPmRppJpump"
COMPUTE_MINT = "B1N1HcMm4RysYz4smsXwmk2UnS8NziqKCM6Ho8i62vXo"

# Known swarm token addresses (need to find these)
# These might be PDAs (Program Derived Addresses) from the investment program
SWARM_TOKENS = {
    'Kin Kong': None,  # Need to derive from program
    'CareerKin': None,
    'MarketingMesh': None,
    'PropertyKin': None,
    'TherapyKin': None,
    'GrantKin': None,
    'ProfitBeeAI': None,
    'TalentKin': None,
    'Robinhood Agent': None,
    'Swarm Ventures': None,
    # Add more swarms as needed
}

def get_token_holders(token_mint_address: str) -> List[Dict]:
    """
    Fetch all token holders for a specific SPL token
    """
    # Get token accounts for this mint
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getProgramAccounts",
        "params": [
            "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",  # Token Program
            {
                "encoding": "jsonParsed",
                "filters": [
                    {
                        "dataSize": 165  # Token account size
                    },
                    {
                        "memcmp": {
                            "offset": 0,
                            "bytes": token_mint_address  # Filter by mint
                        }
                    }
                ]
            }
        ]
    }
    
    response = requests.post(SOLANA_RPC, json=payload)
    data = response.json()
    
    holders = []
    if 'result' in data:
        for account in data['result']:
            account_data = account['account']['data']['parsed']['info']
            if float(account_data['tokenAmount']['amount']) > 0:
                holders.append({
                    'wallet': account_data['owner'],
                    'amount': int(account_data['tokenAmount']['amount']),
                    'decimals': account_data['tokenAmount']['decimals']
                })
    
    return holders

def get_token_supply(token_mint_address: str) -> int:
    """
    Get total supply of a token
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [token_mint_address]
    }
    
    response = requests.post(SOLANA_RPC, json=payload)
    data = response.json()
    
    if 'result' in data:
        return int(data['result']['value']['amount'])
    return 0

def calculate_ownership_percentages(holders: List[Dict], total_supply: int) -> List[Dict]:
    """
    Calculate ownership percentage for each holder
    """
    for holder in holders:
        holder['percentage'] = (holder['amount'] / total_supply) * 100
    return holders

def convert_to_venice_shares(swarm_name: str, holders: List[Dict]) -> List[Dict]:
    """
    Convert swarm token holdings to Venice company shares
    Based on 20% allocation to $COMPUTE investors
    """
    # Map swarms to Venice companies
    swarm_to_venice = {
        'Kin Kong': 'Venice Trading Intelligence Co.',
        'Robinhood Agent': 'Venice Trading Intelligence Co.',
        'Swarm Ventures': 'Venice Trading Intelligence Co.',
        'CareerKin': 'Venice Professional Services Co.',
        'GrantKin': 'Venice Professional Services Co.',
        'TalentKin': 'Venice Professional Services Co.',
        'MarketingMesh': 'Venice Commerce Automation Co.',
        'ProfitBeeAI': 'Venice Commerce Automation Co.',
        'PropertyKin': 'Venice Real Estate Intelligence Co.',
    }
    
    if swarm_name not in swarm_to_venice:
        print(f"Warning: {swarm_name} not mapped to Venice company")
        return []
    
    venice_company = swarm_to_venice[swarm_name]
    
    # Total shares allocated to investors: 200,000 (20% of 1M)
    INVESTOR_SHARES = 200_000
    
    venice_shares = []
    for holder in holders:
        venice_shares.append({
            'shareholder_name': holder['wallet'],
            'shareholder_type': '$COMPUTE Investor',
            'company': venice_company,
            'shares_owned': int(INVESTOR_SHARES * (holder['percentage'] / 100)),
            'percentage_ownership': holder['percentage'] * 0.2,  # 20% of company
            'source_swarm': swarm_name,
            'original_tokens': holder['amount'],
            'acquisition_type': '$COMPUTE Conversion'
        })
    
    return venice_shares

async def fetch_all_swarm_ownership():
    """
    Main function to fetch all swarm ownership data
    """
    all_venice_shares = []
    
    # First, we need to find the token mint addresses
    # This might require looking at the swarm launchpad program
    
    print("Fetching swarm token ownership from Solana...")
    print("Note: We need the SPL token mint addresses for each swarm")
    print("\nSteps to find token addresses:")
    print("1. Check swarm launchpad program transactions")
    print("2. Look for token creation events")
    print("3. Or check their Discord/docs for token addresses")
    
    # Example workflow once we have token addresses:
    """
    for swarm_name, token_mint in SWARM_TOKENS.items():
        if token_mint:
            print(f"\nProcessing {swarm_name}...")
            holders = get_token_holders(token_mint)
            total_supply = get_token_supply(token_mint)
            holders_with_percentage = calculate_ownership_percentages(holders, total_supply)
            venice_shares = convert_to_venice_shares(swarm_name, holders_with_percentage)
            all_venice_shares.extend(venice_shares)
    """
    
    return all_venice_shares

def save_to_csv(shares_data: List[Dict], filename: str = "venice_shares_from_solana.csv"):
    """
    Save the share data to CSV for Airtable import
    """
    import csv
    
    if not shares_data:
        print("No share data to save")
        return
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = shares_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(shares_data)
    
    print(f"Saved {len(shares_data)} share records to {filename}")

def query_investment_program():
    """
    Query the investment program to find swarm accounts and investments
    The program likely tracks investments per swarm
    """
    print(f"\nQuerying Investment Program: {INVESTMENT_PROGRAM_ID}")
    
    # Get all accounts owned by the investment program
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getProgramAccounts",
        "params": [
            INVESTMENT_PROGRAM_ID,
            {
                "encoding": "jsonParsed",
                "commitment": "confirmed"
            }
        ]
    }
    
    response = requests.post(SOLANA_RPC, json=payload)
    data = response.json()
    
    if 'result' in data:
        print(f"Found {len(data['result'])} program accounts")
        # Parse accounts to find swarm-specific data
        for account in data['result'][:5]:  # Show first 5
            print(f"Account: {account['pubkey']}")
            # The data structure will reveal how investments are tracked
    
    return data.get('result', [])

def get_compute_token_holders():
    """
    Get all COMPUTE token holders
    These are potential investors in swarms
    """
    print(f"\nFetching COMPUTE token holders...")
    holders = get_token_holders(COMPUTE_MINT)
    print(f"Found {len(holders)} COMPUTE holders")
    
    # Show top holders
    sorted_holders = sorted(holders, key=lambda x: x['amount'], reverse=True)
    print("\nTop 5 COMPUTE holders:")
    for i, holder in enumerate(sorted_holders[:5]):
        amount = holder['amount'] / (10 ** holder['decimals'])
        print(f"{i+1}. {holder['wallet'][:8]}...{holder['wallet'][-4:]}: {amount:,.2f} COMPUTE")
    
    return holders

def find_swarm_investments():
    """
    Strategy to find swarm investments:
    1. Get program accounts from investment program
    2. Parse to find swarm-specific investment tracking
    3. Cross-reference with COMPUTE token transfers
    """
    print("\n🔍 Finding Swarm Investments on Solana")
    print("=" * 50)
    
    # Step 1: Query investment program
    program_accounts = query_investment_program()
    
    # Step 2: Get COMPUTE holders (potential investors)
    compute_holders = get_compute_token_holders()
    
    # Step 3: Look for investment transactions
    print("\n📊 Investment Tracking Strategy:")
    print("1. The investment program likely creates PDAs for each swarm")
    print("2. Investors send COMPUTE to these swarm PDAs")
    print("3. The program tracks shares/ownership in account data")
    print("\nNext steps:")
    print("- Decode program account data to find swarm structures")
    print("- Match COMPUTE transfers to swarm addresses")
    print("- Calculate ownership percentages per swarm")

if __name__ == "__main__":
    print("Solana Swarm Ownership Fetcher")
    print("=" * 50)
    
    print("\n🔗 Known Addresses:")
    print(f"Investment Program: {INVESTMENT_PROGRAM_ID}")
    print(f"COMPUTE Token: {COMPUTE_MINT}")
    print(f"UBC Token: {UBC_MINT}")
    
    # New approach: Query the investment program directly
    find_swarm_investments()
    
    print("\n📝 To complete the ownership mapping:")
    print("1. Run this script to see program account structure")
    print("2. Identify how swarms are represented (likely PDAs)")
    print("3. Map investor wallets to swarm investments")
    print("4. Convert to Venice company shares")
    
    print("\n💡 Alternative: Manual Collection")
    print("If on-chain data is complex, we can:")
    print("1. Create an investor claim form")
    print("2. Have investors submit their wallet + swarms invested")
    print("3. Verify against COMPUTE token transactions")
    print("4. Issue Venice shares accordingly")