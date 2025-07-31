#!/usr/bin/env python3
"""
Verify investor claims against Solana blockchain
Process claims from the HTML form and validate ownership
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple
import hashlib

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
COMPUTE_MINT = "B1N1HcMm4RysYz4smsXwmk2UnS8NziqKCM6Ho8i62vXo"

def verify_transaction(tx_hash: str, wallet_address: str, expected_program: str = None) -> Tuple[bool, str]:
    """
    Verify a transaction exists and involves the claimed wallet
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            tx_hash,
            {
                "encoding": "jsonParsed",
                "commitment": "confirmed",
                "maxSupportedTransactionVersion": 0
            }
        ]
    }
    
    try:
        response = requests.post(SOLANA_RPC, json=payload)
        data = response.json()
        
        if 'result' not in data or not data['result']:
            return False, "Transaction not found"
        
        tx = data['result']
        
        # Check if wallet is involved in the transaction
        accounts = tx['transaction']['message']['accountKeys']
        wallet_involved = any(acc.get('pubkey') == wallet_address for acc in accounts)
        
        if not wallet_involved:
            return False, "Wallet not found in transaction"
        
        # Check if it's a token transfer
        instructions = tx['transaction']['message']['instructions']
        for instruction in instructions:
            if 'parsed' in instruction and instruction['parsed'].get('type') == 'transfer':
                # This is a token transfer
                info = instruction['parsed']['info']
                if info.get('source') == wallet_address or info.get('destination') == wallet_address:
                    return True, f"Valid transfer: {info.get('amount', 0)} tokens"
        
        return True, "Transaction verified but no token transfer found"
        
    except Exception as e:
        return False, f"Error verifying transaction: {str(e)}"

def verify_wallet_signature(wallet_address: str, message: str, signature: str) -> bool:
    """
    Verify that a signature was created by the claimed wallet
    Note: This is a simplified version - real implementation would use nacl/ed25519
    """
    # In production, use proper signature verification
    # For now, just check format
    return len(signature) == 88  # Base58 encoded signature length

def calculate_share_allocation(investments: List[Dict]) -> Dict[str, int]:
    """
    Calculate Venice company share allocation based on investments
    """
    # Map swarms to Venice companies
    swarm_to_company = {
        'Kin Kong': 'Venice Trading Intelligence Co.',
        'Robinhood Agent': 'Venice Trading Intelligence Co.',
        'Swarm Ventures': 'Venice Trading Intelligence Co.',
        'CareerKin': 'Venice Professional Services Co.',
        'GrantKin': 'Venice Professional Services Co.',
        'TalentKin': 'Venice Professional Services Co.',
        'TherapyKin': 'Venice Professional Services Co.',
        'MarketingMesh': 'Venice Commerce Automation Co.',
        'ProfitBeeAI': 'Venice Commerce Automation Co.',
        'PropertyKin': 'Venice Real Estate Intelligence Co.'
    }
    
    # Aggregate by company
    company_investments = {}
    for inv in investments:
        swarm = inv['swarm']
        amount = float(inv['amount'])
        company = swarm_to_company.get(swarm)
        
        if company:
            if company not in company_investments:
                company_investments[company] = 0
            company_investments[company] += amount
    
    # Calculate shares (simplified - would need total pool sizes)
    # Assume 100,000 COMPUTE per swarm pool for now
    share_allocations = {}
    for company, compute_amount in company_investments.items():
        # 20% of 1M shares = 200,000 shares for investors
        # Proportional to investment
        percentage = min(compute_amount / 100000, 1.0)  # Cap at 100%
        shares = int(200000 * percentage)
        share_allocations[company] = shares
    
    return share_allocations

def process_claim(claim_data: Dict) -> Dict:
    """
    Process a single investor claim
    """
    result = {
        'wallet': claim_data['wallet'],
        'email': claim_data['email'],
        'status': 'pending',
        'verification_results': [],
        'share_allocations': {},
        'notes': []
    }
    
    # Verify transactions
    for tx_hash in claim_data.get('txHashes', []):
        if tx_hash.strip():
            verified, message = verify_transaction(tx_hash, claim_data['wallet'])
            result['verification_results'].append({
                'tx_hash': tx_hash,
                'verified': verified,
                'message': message
            })
    
    # Verify signature if provided
    if claim_data.get('signedMessage'):
        sig_valid = verify_wallet_signature(
            claim_data['wallet'],
            f"Venice Share Claim {claim_data['timestamp'][:10]}",
            claim_data['signedMessage']
        )
        result['signature_verified'] = sig_valid
    
    # Calculate share allocations
    if claim_data.get('investments'):
        result['share_allocations'] = calculate_share_allocation(claim_data['investments'])
        
        # Update status
        if any(v['verified'] for v in result['verification_results']):
            result['status'] = 'verified'
        elif result['verification_results']:
            result['status'] = 'partial'
        else:
            result['status'] = 'unverified'
            result['notes'].append('No valid transactions found')
    
    return result

def generate_airtable_record(claim_result: Dict) -> List[Dict]:
    """
    Convert verified claim to Airtable SHARES records
    """
    records = []
    
    if claim_result['status'] in ['verified', 'partial']:
        for company, shares in claim_result['share_allocations'].items():
            records.append({
                'shareholder_name': claim_result['wallet'][:8] + '...' + claim_result['wallet'][-4:],
                'shareholder_type': '$COMPUTE Investor',
                'company': company,
                'shares_owned': shares,
                'acquisition_type': '$COMPUTE Conversion',
                'acquisition_date': datetime.now().strftime('%Y-%m-%d'),
                'email': claim_result['email'],
                'wallet_address': claim_result['wallet'],
                'verification_status': claim_result['status'],
                'vesting_schedule': 'Immediate',
                'voting_rights': True,
                'dividend_eligible': True
            })
    
    return records

def main():
    """
    Process investor claims from JSON file
    """
    print("Venice Company Share Claim Verification")
    print("=" * 50)
    
    # In production, this would read from your database/API
    sample_claim = {
        'wallet': 'ExampleWallet123...',
        'email': 'investor@example.com',
        'discord': '@investor',
        'investments': [
            {'swarm': 'Kin Kong', 'amount': '1000', 'txHash': 'tx123...'},
            {'swarm': 'CareerKin', 'amount': '500', 'txHash': 'tx456...'}
        ],
        'txHashes': ['tx123...', 'tx456...'],
        'signedMessage': 'sig789...',
        'timestamp': '2024-07-14T20:00:00Z'
    }
    
    # Process the claim
    result = process_claim(sample_claim)
    print(f"\nClaim Status: {result['status']}")
    print(f"Share Allocations: {result['share_allocations']}")
    
    # Generate Airtable records
    airtable_records = generate_airtable_record(result)
    print(f"\nGenerated {len(airtable_records)} Airtable records")
    
    # Save to CSV for import
    if airtable_records:
        import csv
        with open('verified_claims.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=airtable_records[0].keys())
            writer.writeheader()
            writer.writerows(airtable_records)
        print("Saved to verified_claims.csv")

if __name__ == "__main__":
    main()