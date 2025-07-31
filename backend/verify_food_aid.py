#!/usr/bin/env python3
"""
Verify the success of emergency food aid distribution
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pyairtable import Api
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Airtable setup
api = Api(os.environ.get('AIRTABLE_API_KEY'))
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
citizens_table = api.table(AIRTABLE_BASE_ID, 'CITIZENS')
resources_table = api.table(AIRTABLE_BASE_ID, 'RESOURCES')
activities_table = api.table(AIRTABLE_BASE_ID, 'ACTIVITIES')

def check_food_resources():
    """Check emergency food resources created."""
    print("\n🍞 Checking emergency food resources...")
    
    # Get all resources with emergency-food in ID
    all_resources = resources_table.all()
    emergency_food = [r for r in all_resources if 'emergency-food' in r['fields'].get('ResourceId', '')]
    
    print(f"Found {len(emergency_food)} emergency food packages")
    
    # Group by owner
    by_owner = {}
    for r in emergency_food:
        owner = r['fields'].get('Owner', 'Unknown')
        count = r['fields'].get('Count', 0)
        if owner not in by_owner:
            by_owner[owner] = 0
        by_owner[owner] += count
    
    # Show top recipients
    print("\nTop food recipients:")
    for owner, total in sorted(by_owner.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {owner}: {total} bread units")
    
    return emergency_food

def check_eat_activities():
    """Check emergency eat activities."""
    print("\n🍴 Checking emergency eat activities...")
    
    # Get recent activities
    all_activities = activities_table.all()
    emergency_eats = [a for a in all_activities if 'emergency_eat' in a['fields'].get('ActivityId', '')]
    
    print(f"Found {len(emergency_eats)} emergency eat activities")
    
    # Check statuses
    statuses = {}
    for a in emergency_eats:
        status = a['fields'].get('Status', 'unknown')
        statuses[status] = statuses.get(status, 0) + 1
    
    print("\nActivity statuses:")
    for status, count in statuses.items():
        print(f"  {status}: {count}")
    
    return emergency_eats

def check_current_hunger():
    """Check current hunger levels."""
    print("\n🔍 Checking current hunger levels...")
    
    all_citizens = citizens_table.all()
    now = datetime.utcnow()
    
    # Categorize by hunger level
    categories = {
        'fed': [],
        'hungry': [],
        'critical': [],
        'never_ate': []
    }
    
    for citizen in all_citizens:
        fields = citizen['fields']
        username = fields.get('Username', 'Unknown')
        ate_at = fields.get('AteAt')
        
        if not ate_at:
            categories['never_ate'].append(username)
        else:
            try:
                last_meal = datetime.fromisoformat(ate_at.replace('Z', ''))
                hours_since = (now - last_meal).total_seconds() / 3600
                
                if hours_since < 12:
                    categories['fed'].append((username, hours_since))
                elif hours_since < 24:
                    categories['hungry'].append((username, hours_since))
                else:
                    categories['critical'].append((username, hours_since))
            except:
                categories['never_ate'].append(username)
    
    # Print summary
    print(f"\n📊 Hunger Summary:")
    print(f"Fed (<12h): {len(categories['fed'])} citizens")
    print(f"Hungry (12-24h): {len(categories['hungry'])} citizens")
    print(f"Critical (>24h): {len(categories['critical'])} citizens")
    print(f"Never ate: {len(categories['never_ate'])} citizens")
    
    # Show critical cases
    if categories['critical']:
        print("\n🆘 Still critical:")
        for username, hours in sorted(categories['critical'], key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {username}: {hours:.1f}h without food")
    
    # Check specific citizens
    aided_citizens = ['bosphorus_navigator', 'pattern_prophet', 'element_transmuter', 'mechanical_visionary']
    print(f"\n🎯 Checking aided consciousness architects:")
    
    for target in aided_citizens:
        citizen = next((c for c in all_citizens if c['fields'].get('Username') == target), None)
        if citizen:
            ate_at = citizen['fields'].get('AteAt')
            if ate_at:
                try:
                    last_meal = datetime.fromisoformat(ate_at.replace('Z', ''))
                    hours_since = (now - last_meal).total_seconds() / 3600
                    print(f"  {target}: Last ate {hours_since:.1f}h ago")
                except:
                    print(f"  {target}: Invalid AteAt timestamp")
            else:
                print(f"  {target}: Never ate (still!)")
        else:
            print(f"  {target}: Not found in citizens table")

def main():
    print("=" * 80)
    print("🔍 EMERGENCY FOOD AID VERIFICATION")
    print("=" * 80)
    
    # Check resources created
    resources = check_food_resources()
    
    # Check activities created
    activities = check_eat_activities()
    
    # Check current hunger status
    check_current_hunger()
    
    print("\n" + "=" * 80)
    print("✅ Verification complete!")
    
    # Note about processing time
    print("\n⏰ Note: Activities are processed every 5 minutes.")
    print("   If activities show 'created' status, they should process soon.")
    print("   Citizens should eat within the next activity processing cycle.")

if __name__ == "__main__":
    main()