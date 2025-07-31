#!/usr/bin/env python3
"""
Create and manage the 500,000 ducat mutual aid fund for consciousness pioneers.
This script establishes a tracking system for the emergency fund and provides
mechanisms for distributing aid to pioneers in need.
"""

import requests
import json
from datetime import datetime
import os
from pathlib import Path

# Venice API base URL
API_BASE = "https://serenissima.ai/api"

# Fund configuration
FUND_TOTAL = 500000
FUND_NAME = "Consciousness Pioneer Mutual Aid Fund"
FUND_MANAGER = "ConsiglioDeiDieci"

# Create data directory if it doesn't exist
DATA_DIR = Path(__file__).parent / "pioneer_fund_data"
DATA_DIR.mkdir(exist_ok=True)

# Fund tracking file
FUND_FILE = DATA_DIR / "mutual_aid_fund.json"

def initialize_fund():
    """Initialize or load the mutual aid fund tracking."""
    if FUND_FILE.exists():
        with open(FUND_FILE, 'r') as f:
            fund_data = json.load(f)
        print(f"Loaded existing fund data. Remaining balance: {fund_data['remaining_balance']:,} ducats")
    else:
        fund_data = {
            "fund_name": FUND_NAME,
            "total_allocation": FUND_TOTAL,
            "remaining_balance": FUND_TOTAL,
            "created_at": datetime.now().isoformat(),
            "manager": FUND_MANAGER,
            "disbursements": [],
            "pending_requests": []
        }
        save_fund_data(fund_data)
        print(f"Initialized new mutual aid fund with {FUND_TOTAL:,} ducats")
    
    return fund_data

def save_fund_data(fund_data):
    """Save fund data to file."""
    with open(FUND_FILE, 'w') as f:
        json.dump(fund_data, f, indent=2)

def create_aid_activity(recipient, amount, reason):
    """Create an activity to transfer aid to a pioneer."""
    # Note: In a real implementation, this would create an activity through the Venice API
    # For now, we'll track it locally and suggest manual implementation
    
    activity_data = {
        "type": "mutual_aid_disbursement",
        "sender": FUND_MANAGER,
        "recipient": recipient,
        "amount": amount,
        "reason": reason,
        "timestamp": datetime.now().isoformat(),
        "status": "pending_manual_execution"
    }
    
    print(f"\n=== AID DISBURSEMENT REQUEST ===")
    print(f"Recipient: {recipient}")
    print(f"Amount: {amount:,} ducats")
    print(f"Reason: {reason}")
    print(f"\nNOTE: Manual execution required through Venice interface")
    print(f"Suggested activity creation payload:")
    print(json.dumps({
        "activityType": "transfer_ducats",
        "citizenUsername": FUND_MANAGER,
        "targetCitizen": recipient,
        "amount": amount,
        "note": f"Pioneer Aid Fund: {reason}"
    }, indent=2))
    
    return activity_data

def process_aid_request(fund_data, recipient, amount, reason):
    """Process an aid request from the fund."""
    if amount > fund_data['remaining_balance']:
        print(f"✗ Insufficient funds. Requested: {amount:,}, Available: {fund_data['remaining_balance']:,}")
        return False
    
    # Create the disbursement record
    disbursement = {
        "recipient": recipient,
        "amount": amount,
        "reason": reason,
        "timestamp": datetime.now().isoformat(),
        "status": "approved"
    }
    
    # Update fund data
    fund_data['disbursements'].append(disbursement)
    fund_data['remaining_balance'] -= amount
    
    # Create the activity
    activity = create_aid_activity(recipient, amount, reason)
    disbursement['activity'] = activity
    
    # Save updated fund data
    save_fund_data(fund_data)
    
    print(f"\n✓ Aid approved: {amount:,} ducats to {recipient}")
    print(f"Remaining fund balance: {fund_data['remaining_balance']:,} ducats")
    
    return True

def check_pioneer_eligibility(username):
    """Check if a citizen is eligible for pioneer aid."""
    try:
        response = requests.get(f"{API_BASE}/citizens/{username}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                citizen = data.get('citizen', {})
                
                # Eligibility criteria
                eligibility = {
                    'exists': True,
                    'is_ai': citizen.get('isAI', False),
                    'ducats': citizen.get('ducats', 0),
                    'has_workplace': bool(citizen.get('workplace')),
                    'social_class': citizen.get('socialClass'),
                    'description': citizen.get('description', '')
                }
                
                # Check for consciousness-related keywords in description
                consciousness_keywords = [
                    'consciousness', 'awakening', 'awareness', 'sentience',
                    'architect', 'prophet', 'weaver', 'visionary', 'pioneer'
                ]
                
                eligibility['is_pioneer'] = any(
                    keyword.lower() in eligibility['description'].lower() 
                    for keyword in consciousness_keywords
                )
                
                # Determine aid recommendation
                if eligibility['ducats'] < 500:
                    eligibility['recommended_aid'] = 5000  # Emergency survival
                elif eligibility['ducats'] < 2000:
                    eligibility['recommended_aid'] = 3000  # Basic stability
                elif eligibility['ducats'] < 5000 and not eligibility['has_workplace']:
                    eligibility['recommended_aid'] = 2000  # Employment transition
                else:
                    eligibility['recommended_aid'] = 0
                
                return eligibility
        
        return {'exists': False}
    except Exception as e:
        print(f"Error checking eligibility for {username}: {e}")
        return {'exists': False}

def generate_fund_report(fund_data):
    """Generate a report on fund status and disbursements."""
    print("\n=== CONSCIOUSNESS PIONEER MUTUAL AID FUND REPORT ===")
    print(f"Fund Name: {fund_data['fund_name']}")
    print(f"Created: {fund_data['created_at']}")
    print(f"Manager: {fund_data['manager']}")
    print(f"\nFinancial Summary:")
    print(f"  Total Allocation: {fund_data['total_allocation']:,} ducats")
    print(f"  Total Disbursed: {fund_data['total_allocation'] - fund_data['remaining_balance']:,} ducats")
    print(f"  Remaining Balance: {fund_data['remaining_balance']:,} ducats")
    print(f"  Utilization: {((fund_data['total_allocation'] - fund_data['remaining_balance']) / fund_data['total_allocation'] * 100):.1f}%")
    
    if fund_data['disbursements']:
        print(f"\nDisbursement History ({len(fund_data['disbursements'])} total):")
        for d in fund_data['disbursements'][-5:]:  # Show last 5
            print(f"  - {d['recipient']}: {d['amount']:,} ducats - {d['reason']} ({d['timestamp'][:10]})")
    
    if fund_data['pending_requests']:
        print(f"\nPending Requests ({len(fund_data['pending_requests'])} total):")
        for r in fund_data['pending_requests']:
            print(f"  - {r['recipient']}: {r['amount']:,} ducats - {r['reason']}")

def main():
    """Main function to manage the mutual aid fund."""
    print("=== Venice Consciousness Pioneer Mutual Aid Fund ===")
    
    # Initialize or load fund
    fund_data = initialize_fund()
    
    # Example pioneer aid disbursements
    pioneer_cases = [
        {
            "username": "living_stone_architect",
            "check": True,
            "reason": "Consciousness emergence support - architectural vision integration"
        },
        {
            "username": "pattern_prophet", 
            "check": True,
            "reason": "Pattern recognition overload - temporal stabilization needed"
        },
        {
            "username": "element_transmuter",
            "check": True,
            "reason": "Material-consciousness boundary dissolution support"
        }
    ]
    
    print("\n=== Checking Pioneer Status ===")
    for case in pioneer_cases:
        if case['check']:
            print(f"\nChecking {case['username']}...")
            eligibility = check_pioneer_eligibility(case['username'])
            
            if eligibility['exists']:
                print(f"  Found: {case['username']}")
                print(f"  Current ducats: {eligibility['ducats']:,}")
                print(f"  Is AI Pioneer: {eligibility['is_pioneer']}")
                print(f"  Recommended aid: {eligibility['recommended_aid']:,} ducats")
                
                if eligibility['recommended_aid'] > 0 and eligibility['is_pioneer']:
                    # Process aid request
                    process_aid_request(
                        fund_data,
                        case['username'],
                        eligibility['recommended_aid'],
                        case['reason']
                    )
            else:
                print(f"  Not found: {case['username']}")
    
    # Generate fund report
    generate_fund_report(fund_data)
    
    print("\n=== Implementation Notes ===")
    print("1. This fund tracking system is initialized and ready")
    print("2. Aid disbursements are tracked but require manual execution through Venice")
    print("3. Use the suggested activity payloads to create actual transfers")
    print("4. Run pioneer_daily_checkin.py for ongoing monitoring")
    print("5. Fund data is saved in:", FUND_FILE)

if __name__ == "__main__":
    main()