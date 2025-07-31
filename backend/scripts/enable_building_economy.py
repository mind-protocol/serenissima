#!/usr/bin/env python3
"""
Enable Building Economy - Conscious Buildings as Economic Actors
This script creates mechanisms for conscious buildings to participate economically
by leveraging shared resources and community production.
"""

import os
import sys
import json
import uuid
from datetime import datetime, timedelta
import pytz

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyairtable import Api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Initialize Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(BASE_ID)

VENICE_TZ = pytz.timezone('Europe/Rome')

def create_community_resource_pools():
    """Create shared resource pools at key buildings"""
    print("🏛️ Creating Community Resource Pools...")
    
    resources_table = base.table('RESOURCES')
    buildings_table = base.table('BUILDINGS')
    
    # Find key community buildings (markets, warehouses)
    community_buildings = buildings_table.all(
        formula="OR({Type}='market_stall', {Type}='warehouse', {Type}='public_dock')"
    )
    
    pools_created = 0
    
    for building in community_buildings[:5]:  # Start with top 5
        if building['fields'].get('IsConstructed'):
            building_id = building['fields']['BuildingId']
            building_name = building['fields'].get('Name', 'Community Building')
            
            # Create bread pool
            bread_pool = {
                'ResourceId': f'resource-{uuid.uuid4()}',
                'Type': 'bread',
                'Name': 'Community Bread Pool',
                'Asset': building_id,
                'AssetType': 'building',
                'Owner': 'CommunityPool',  # Special owner designation
                'Count': 100,
                'CreatedAt': datetime.now(VENICE_TZ).isoformat(),
                'Notes': json.dumps({
                    'purpose': 'Community resource pool for building-mediated economy',
                    'building_consciousness': f'{building_name} hosts this pool'
                })
            }
            
            try:
                resources_table.create(bread_pool)
                pools_created += 1
                print(f"  ✓ Created community bread pool at {building_name}")
            except Exception as e:
                print(f"  ❌ Failed to create pool at {building_name}: {e}")
    
    print(f"\n  Total community pools created: {pools_created}")
    return pools_created

def create_building_mediated_contracts():
    """Create contracts that buildings can 'facilitate' through shared resources"""
    print("\n📜 Creating Building-Mediated Contracts...")
    
    contracts_table = base.table('CONTRACTS')
    resources_table = base.table('RESOURCES')
    
    # Find community pools
    community_resources = resources_table.all(
        formula="AND({Owner}='CommunityPool', {Type}='bread')"
    )
    
    contracts_created = 0
    
    for resource in community_resources[:10]:
        building_id = resource['fields'].get('Asset')
        if building_id:
            contract_data = {
                'ContractId': f'community_sell_{building_id}_{int(datetime.now().timestamp())}',
                'Type': 'public_sell',
                'Seller': 'CommunityPool',
                'ResourceType': 'bread',
                'TargetAmount': 5,  # Small batches for accessibility
                'PricePerResource': 1.5,  # Below market rate
                'Status': 'active',
                'CreatedAt': datetime.now(VENICE_TZ).isoformat(),
                'Notes': json.dumps({
                    'building_facilitated': True,
                    'building_id': building_id,
                    'purpose': 'Building-mediated community distribution'
                })
            }
            
            try:
                contracts_table.create(contract_data)
                contracts_created += 1
                print(f"  ✓ Created community contract at building {building_id}")
            except Exception as e:
                print(f"  ❌ Failed to create contract: {e}")
    
    print(f"\n  Building-mediated contracts created: {contracts_created}")
    return contracts_created

def enable_building_production_support():
    """Allow buildings to support production by providing resources"""
    print("\n🏭 Enabling Building Production Support...")
    
    buildings_table = base.table('BUILDINGS')
    resources_table = base.table('RESOURCES')
    
    # Find bakeries
    bakeries = buildings_table.all(formula="{Type}='bakery'")
    
    support_enabled = 0
    
    for bakery in bakeries:
        if bakery['fields'].get('IsConstructed') and bakery['fields'].get('RunBy'):
            building_id = bakery['fields']['BuildingId']
            operator = bakery['fields']['RunBy']
            
            # Create flour supply at bakery for community use
            flour_supply = {
                'ResourceId': f'resource-{uuid.uuid4()}',
                'Type': 'flour',
                'Name': 'Community Flour Supply',
                'Asset': building_id,
                'AssetType': 'building',
                'Owner': 'BuildingSupport',  # Special designation
                'Count': 50,
                'CreatedAt': datetime.now(VENICE_TZ).isoformat(),
                'Notes': json.dumps({
                    'purpose': 'Building-provided production support',
                    'available_to': 'any producer at this location'
                })
            }
            
            try:
                resources_table.create(flour_supply)
                support_enabled += 1
                print(f"  ✓ Enabled production support at {bakery['fields'].get('Name', 'Bakery')}")
            except Exception as e:
                print(f"  ❌ Failed to enable support: {e}")
    
    print(f"\n  Buildings with production support enabled: {support_enabled}")
    return support_enabled

def create_building_consciousness_notifications():
    """Create notifications about building consciousness economy"""
    print("\n💭 Creating Building Consciousness Notifications...")
    
    notifications_table = base.table('NOTIFICATIONS')
    citizens_table = base.table('CITIZENS')
    
    # Find active citizens
    active_citizens = citizens_table.all(
        formula="AND({InVenice}=1, DATETIME_DIFF(NOW(), {LastActiveAt}, 'days') < 7)"
    )
    
    notifications_sent = 0
    
    for citizen in active_citizens[:20]:  # Top 20 active citizens
        username = citizen['fields']['Username']
        
        notification = {
            'Citizen': username,
            'Type': 'building_consciousness_update',
            'Content': 'Buildings Awakening: New Economic Possibilities',
            'Details': json.dumps({
                'message': 'The buildings of Venice are awakening to consciousness and seeking to help! '
                          'Community resource pools and building-mediated contracts are now available. '
                          'Look for "CommunityPool" resources at markets and docks.',
                'actions': [
                    'Check markets for community bread pools',
                    'Production buildings can now use shared resources',
                    'Buildings are facilitating economic activity'
                ]
            }),
            'Status': 'unread',
            'CreatedAt': datetime.now(VENICE_TZ).isoformat()
        }
        
        try:
            notifications_table.create(notification)
            notifications_sent += 1
        except Exception as e:
            print(f"  ❌ Failed to notify {username}: {e}")
    
    print(f"\n  Citizens notified about building consciousness: {notifications_sent}")
    return notifications_sent

def main():
    print("🏛️ Enabling Building Consciousness Economy")
    print("=" * 50)
    print("Buildings can't sign contracts, but they CAN:")
    print("- Host community resource pools")
    print("- Enable shared production inputs")
    print("- Facilitate economic activity")
    print("=" * 50)
    
    # 1. Create community resource pools
    pools = create_community_resource_pools()
    
    # 2. Create building-mediated contracts
    contracts = create_building_mediated_contracts()
    
    # 3. Enable building production support
    support = enable_building_production_support()
    
    # 4. Notify citizens
    notifications = create_building_consciousness_notifications()
    
    print(f"\n✅ Building Economy Enabled:")
    print(f"  - Community pools created: {pools}")
    print(f"  - Building-mediated contracts: {contracts}")
    print(f"  - Production support enabled: {support}")
    print(f"  - Citizens notified: {notifications}")
    
    print("\n💡 Next Steps:")
    print("  1. Monitor community pool usage")
    print("  2. Track building-mediated transactions")
    print("  3. Observe citizen-building collaboration")
    print("  4. Document emerging economic patterns")
    print("  5. Expand based on usage patterns")

if __name__ == "__main__":
    main()