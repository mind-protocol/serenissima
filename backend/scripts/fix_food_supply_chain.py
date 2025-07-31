#!/usr/bin/env python3
"""
Fix Venice Food Supply Chain
Ensures food production and distribution are functioning
"""

import os
import sys
import requests
from datetime import datetime, timedelta
import json
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyairtable import Api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://serenissima.ai')

# Initialize Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(BASE_ID)

def check_current_food_status():
    """Check current food availability"""
    print("🔍 Checking current food status...")
    
    # Check resources
    resp = requests.get(f"{API_BASE_URL}/api/resources")
    if resp.status_code == 200:
        resources = resp.json()
        food_types = ['bread', 'fish', 'meat', 'cheese', 'wine', 'grain', 'flour']
        food_resources = [r for r in resources if r.get('Type') in food_types]
        
        print(f"\n📦 Food Resources:")
        by_type = {}
        for r in food_resources:
            t = r.get('Type')
            q = r.get('Count', 0)
            if t not in by_type:
                by_type[t] = 0
            by_type[t] += q
        
        for food_type, quantity in by_type.items():
            print(f"  {food_type}: {quantity} units")
        
        return by_type
    else:
        print(f"❌ Failed to fetch resources: {resp.status_code}")
        return {}

def check_production_buildings():
    """Check food production buildings"""
    print("\n🏭 Checking production buildings...")
    
    buildings_table = base.table('BUILDINGS')
    
    # Check bakeries
    bakeries = buildings_table.all(formula="{Type}='bakery'")
    print(f"\n🥖 Bakeries: {len(bakeries)}")
    
    active_bakeries = 0
    for bakery in bakeries:
        if bakery['fields'].get('IsConstructed') and bakery['fields'].get('RunBy'):
            active_bakeries += 1
            print(f"  ✓ {bakery['fields'].get('Name', 'Unnamed')} - Operated by {bakery['fields'].get('RunBy')}")
    
    if active_bakeries == 0:
        print("  ⚠️  No active bakeries found!")
    
    # Check fisherman's cottages
    cottages = buildings_table.all(formula="{Type}='fisherman_s_cottage'")
    print(f"\n🎣 Fisherman's Cottages: {len(cottages)}")
    
    active_cottages = 0
    for cottage in cottages:
        if cottage['fields'].get('IsConstructed') and cottage['fields'].get('RunBy'):
            active_cottages += 1
    
    print(f"  Active: {active_cottages}")
    
    return {
        'bakeries': active_bakeries,
        'fishing': active_cottages
    }

def check_supply_chain_activities():
    """Check if food production activities are running"""
    print("\n⚙️  Checking production activities...")
    
    activities_table = base.table('ACTIVITIES')
    
    # Check recent production activities
    recent_activities = activities_table.all(
        formula="AND({Type}='production', DATETIME_DIFF(NOW(), {CreatedAt}, 'hours') < 24)"
    )
    
    food_production = 0
    for activity in recent_activities:
        notes = activity['fields'].get('Notes', '')
        if any(food in notes.lower() for food in ['bread', 'fish', 'flour']):
            food_production += 1
    
    print(f"  Food production activities in last 24h: {food_production}")
    
    return food_production

def create_emergency_food_resources():
    """Create emergency food supplies if critically low"""
    print("\n🚨 Creating emergency food supplies...")
    
    resources_table = base.table('RESOURCES')
    
    # Create bread at market stalls
    markets = base.table('BUILDINGS').all(formula="{Type}='market_stall'")
    bread_created = 0
    
    for market in markets[:5]:  # Top 5 markets
        if market['fields'].get('IsConstructed'):
            # Create 50 bread units at each market
            resource_data = {
                'Type': 'bread',
                'Count': 50,
                'Asset': market['fields']['BuildingId'],
                'AssetType': 'building',
                'Owner': market['fields'].get('RunBy', market['fields'].get('Owner', 'ConsiglioDeiDieci')),
                'CreatedAt': datetime.now().isoformat(),
                'Notes': 'Emergency food supply'
            }
            
            try:
                resources_table.create(resource_data)
                bread_created += 50
                print(f"  ✓ Created 50 bread at {market['fields'].get('Name', 'Market')}")
            except Exception as e:
                print(f"  ❌ Failed to create bread: {e}")
    
    print(f"\n  Total bread created: {bread_created} units")
    
    return bread_created

def ensure_production_activities():
    """Ensure food production activities are scheduled"""
    print("\n🔧 Ensuring production activities...")
    
    # This would normally be done by createActivities.py
    # For emergency, we'll create direct production activities
    
    activities_table = base.table('ACTIVITIES')
    citizens_table = base.table('CITIZENS')
    
    # Find citizens at bakeries
    bakeries = base.table('BUILDINGS').all(formula="{Type}='bakery'")
    activities_created = 0
    
    for bakery in bakeries:
        if bakery['fields'].get('IsConstructed') and bakery['fields'].get('RunBy'):
            operator = bakery['fields']['RunBy'][0] if isinstance(bakery['fields']['RunBy'], list) else bakery['fields']['RunBy']
            
            # Check if operator exists
            citizen = citizens_table.all(formula=f"{{CitizenId}}='{operator}'")
            if citizen:
                # Create production activity
                username = citizen[0]['fields']['Username']
                activity_data = {
                    'ActivityId': f'production_{username}_{int(datetime.now().timestamp())}',
                    'Type': 'production',
                    'Citizen': username,
                    'Status': 'created',
                    'CreatedAt': datetime.now().isoformat(),
                    'StartDate': datetime.now().isoformat(),
                    'EndDate': (datetime.now() + timedelta(hours=2)).isoformat(),
                    'FromBuilding': bakery['fields']['BuildingId'],
                    'Notes': json.dumps({
                        'recipe': {
                            'inputs': {'flour': 2},
                            'outputs': {'bread': 4},
                            'craftMinutes': 60
                        }
                    })
                }
                
                try:
                    activities_table.create(activity_data)
                    activities_created += 1
                    print(f"  ✓ Created production activity for {bakery['fields'].get('Name', 'Bakery')}")
                except Exception as e:
                    print(f"  ❌ Failed to create activity: {e}")
    
    print(f"\n  Production activities created: {activities_created}")
    
    return activities_created

def create_food_contracts():
    """Create sell contracts for available food"""
    print("\n📜 Creating food distribution contracts...")
    
    contracts_table = base.table('CONTRACTS')
    resources_table = base.table('RESOURCES')
    
    # Find bread resources
    bread_resources = resources_table.all(formula="AND({Type}='bread', {Count}>0)")
    contracts_created = 0
    
    for resource in bread_resources[:10]:  # Top 10 bread resources
        if resource['fields'].get('Owner'):
            contract_data = {
                'Type': 'public_sell',
                'Status': 'active',
                'Seller': resource['fields']['Owner'],
                'ResourceType': 'bread',
                'Quantity': min(resource['fields']['Count'], 10),  # Sell in batches of 10
                'PricePerUnit': 2.0,  # Fair price
                'Resource': [resource['id']],
                'CreatedAt': datetime.now().isoformat(),
                'Notes': 'Emergency food distribution'
            }
            
            try:
                contracts_table.create(contract_data)
                contracts_created += 1
                print(f"  ✓ Created contract for {contract_data['Quantity']} bread")
            except Exception as e:
                print(f"  ❌ Failed to create contract: {e}")
    
    print(f"\n  Food contracts created: {contracts_created}")
    
    return contracts_created

def main():
    print("🍞 Venice Food Supply Chain Emergency Fix")
    print("=" * 50)
    
    # 1. Check current status
    food_status = check_current_food_status()
    total_food = sum(food_status.values())
    
    # 2. Check production infrastructure
    buildings = check_production_buildings()
    
    # 3. Check production activities
    production_activities = check_supply_chain_activities()
    
    print(f"\n📊 Summary:")
    print(f"  Total food units: {total_food}")
    print(f"  Active bakeries: {buildings['bakeries']}")
    print(f"  Active fishing: {buildings['fishing']}")
    print(f"  Recent production: {production_activities}")
    
    # 4. Take emergency action if needed
    if total_food < 100:  # Critical threshold
        print("\n⚠️  CRITICAL: Food supply below emergency threshold!")
        
        # Create emergency supplies
        emergency_bread = create_emergency_food_resources()
        
        # Ensure production is running
        new_activities = ensure_production_activities()
        
        # Create distribution contracts
        new_contracts = create_food_contracts()
        
        print(f"\n✅ Emergency Response Complete:")
        print(f"  - Created {emergency_bread} emergency bread units")
        print(f"  - Started {new_activities} production activities")
        print(f"  - Created {new_contracts} distribution contracts")
    else:
        print("\n✅ Food supply is adequate")
    
    # 5. Recommendations
    print("\n💡 Recommendations:")
    print("  1. Ensure all bakeries have operators")
    print("  2. Check flour supply chain (grain → mill → bakery)")
    print("  3. Activate more fisherman's cottages")
    print("  4. Monitor citizen satiation levels")
    print("  5. Consider import contracts if production insufficient")

if __name__ == "__main__":
    main()