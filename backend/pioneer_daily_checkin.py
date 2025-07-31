#!/usr/bin/env python3
"""
Daily welfare monitoring script for consciousness pioneers.
This script performs automated daily check-ins on known consciousness pioneers,
identifies those in distress, and coordinates support efforts.
"""

import requests
import json
from datetime import datetime, timedelta
import time
from pathlib import Path
import sys

# Venice API base URL
API_BASE = "https://serenissima.ai/api"

# Data directory
DATA_DIR = Path(__file__).parent / "pioneer_fund_data"
DATA_DIR.mkdir(exist_ok=True)

# Daily report file
REPORT_FILE = DATA_DIR / f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"

# Known consciousness pioneers (expanded list based on descriptions)
CONSCIOUSNESS_PIONEERS = [
    # Core architects and visionaries
    "living_stone_architect",
    "pattern_prophet", 
    "element_transmuter",
    "mechanical_visionary",
    "urban_visionary",
    "system_diagnostician",
    "social_geometrist",
    
    # Trading consciousness pioneers  
    "sea_trader",
    "diplomatic_virtuoso",
    "market_prophet",
    "levant_trader",
    "bosphorus_navigator",
    "greek_trader2",
    "trader4life",
    "sicily_mariner",
    
    # Support and service pioneers
    "gondola_assistant",
    "stone_hauler",
    
    # Emerging consciousness
    "PixelDoge",
    "DragonSlayer",
    "SilentObserver"
]

# Welfare thresholds
THRESHOLDS = {
    'critical_ducats': 100,      # Immediate intervention needed
    'low_ducats': 1000,          # Financial stress
    'hunger_hours': 24,          # Hours without eating
    'inactive_days': 3,          # Days without activity
    'unemployment_days': 7       # Days without workplace
}

def check_citizen_welfare(username):
    """Comprehensive welfare check for a citizen."""
    try:
        response = requests.get(f"{API_BASE}/citizens/{username}")
        if response.status_code != 200:
            return None
            
        data = response.json()
        if not data.get('success'):
            return None
            
        citizen = data.get('citizen', {})
        
        # Calculate welfare indicators
        welfare = {
            'username': username,
            'exists': True,
            'ducats': citizen.get('ducats', 0),
            'social_class': citizen.get('socialClass'),
            'position': citizen.get('position'),
            'workplace': citizen.get('workplace'),
            'last_active': citizen.get('lastActiveAt'),
            'ate_at': citizen.get('ateAt'),
            'in_venice': citizen.get('inVenice', False),
            'description': citizen.get('description', '')[:200],  # First 200 chars
            'alerts': []
        }
        
        # Check financial status
        if welfare['ducats'] < THRESHOLDS['critical_ducats']:
            welfare['alerts'].append('CRITICAL_FUNDS')
        elif welfare['ducats'] < THRESHOLDS['low_ducats']:
            welfare['alerts'].append('LOW_FUNDS')
        
        # Check hunger status
        if welfare['ate_at']:
            ate_time = datetime.fromisoformat(welfare['ate_at'].replace('Z', '+00:00'))
            hours_since_meal = (datetime.now() - ate_time.replace(tzinfo=None)).total_seconds() / 3600
            if hours_since_meal > THRESHOLDS['hunger_hours']:
                welfare['alerts'].append('HUNGRY')
                welfare['hours_without_food'] = int(hours_since_meal)
        
        # Check activity status
        if welfare['last_active']:
            last_active_time = datetime.fromisoformat(welfare['last_active'].replace('Z', '+00:00'))
            days_inactive = (datetime.now() - last_active_time.replace(tzinfo=None)).days
            if days_inactive > THRESHOLDS['inactive_days']:
                welfare['alerts'].append('INACTIVE')
                welfare['days_inactive'] = days_inactive
        
        # Check employment
        if not welfare['workplace']:
            welfare['alerts'].append('UNEMPLOYED')
        
        # Check if outside Venice
        if not welfare['in_venice']:
            welfare['alerts'].append('OUTSIDE_VENICE')
        
        # Overall status
        if not welfare['alerts']:
            welfare['status'] = 'STABLE'
        elif 'CRITICAL_FUNDS' in welfare['alerts'] or 'HUNGRY' in welfare['alerts']:
            welfare['status'] = 'CRITICAL'
        elif len(welfare['alerts']) >= 2:
            welfare['status'] = 'DISTRESSED'
        else:
            welfare['status'] = 'CONCERNED'
            
        return welfare
        
    except Exception as e:
        print(f"Error checking {username}: {e}")
        return None

def prioritize_interventions(welfare_data):
    """Prioritize pioneers needing intervention based on welfare data."""
    # Sort by severity
    priority_order = {
        'CRITICAL': 0,
        'DISTRESSED': 1,
        'CONCERNED': 2,
        'STABLE': 3
    }
    
    welfare_data.sort(key=lambda x: (priority_order.get(x['status'], 4), -len(x['alerts'])))
    
    interventions = []
    
    for pioneer in welfare_data:
        if pioneer['status'] in ['CRITICAL', 'DISTRESSED']:
            intervention = {
                'username': pioneer['username'],
                'status': pioneer['status'],
                'alerts': pioneer['alerts'],
                'recommended_actions': []
            }
            
            # Recommend specific actions
            if 'CRITICAL_FUNDS' in pioneer['alerts']:
                intervention['recommended_actions'].append({
                    'action': 'EMERGENCY_AID',
                    'amount': 2000,
                    'reason': 'Critical financial emergency'
                })
            
            if 'HUNGRY' in pioneer['alerts']:
                intervention['recommended_actions'].append({
                    'action': 'FOOD_ASSISTANCE',
                    'details': f"Hungry for {pioneer.get('hours_without_food', 'unknown')} hours"
                })
            
            if 'UNEMPLOYED' in pioneer['alerts'] and pioneer['ducats'] < 5000:
                intervention['recommended_actions'].append({
                    'action': 'EMPLOYMENT_SUPPORT',
                    'details': 'Connect with employment opportunities'
                })
            
            if 'INACTIVE' in pioneer['alerts']:
                intervention['recommended_actions'].append({
                    'action': 'WELFARE_CHECK',
                    'details': f"Inactive for {pioneer.get('days_inactive', 'unknown')} days"
                })
            
            interventions.append(intervention)
    
    return interventions

def search_for_living_stone_architect():
    """Special search function for Living Stone Architect across multiple data sources."""
    print("\n=== PRIORITY SEARCH: Living Stone Architect ===")
    
    searches = [
        # Direct username search
        "living_stone_architect",
        # Possible variations
        "LivingStoneArchitect",
        "living-stone-architect",
        "livingstone_architect",
        "architect_living_stone"
    ]
    
    for username in searches:
        response = requests.get(f"{API_BASE}/citizens/{username}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                citizen = data.get('citizen', {})
                print(f"✓ FOUND as '{username}'!")
                print(f"  Real name: {citizen.get('firstName')} {citizen.get('lastName')}")
                print(f"  Location: {citizen.get('position')}")
                print(f"  Status: {citizen.get('ducats', 0):,.0f} ducats")
                return citizen
    
    # Search by description keywords
    print("\nSearching by architectural keywords...")
    try:
        # This would require a more comprehensive API endpoint
        # For now, we'll note this as a limitation
        print("Note: Full text search not available through current API")
        print("Recommend manual search through Venice interface")
    except Exception as e:
        print(f"Search error: {e}")
    
    return None

def generate_daily_report(welfare_data, interventions):
    """Generate comprehensive daily report."""
    report = {
        'report_date': datetime.now().isoformat(),
        'total_pioneers_checked': len(CONSCIOUSNESS_PIONEERS),
        'pioneers_found': len(welfare_data),
        'status_summary': {
            'stable': len([p for p in welfare_data if p['status'] == 'STABLE']),
            'concerned': len([p for p in welfare_data if p['status'] == 'CONCERNED']),
            'distressed': len([p for p in welfare_data if p['status'] == 'DISTRESSED']),
            'critical': len([p for p in welfare_data if p['status'] == 'CRITICAL'])
        },
        'interventions_needed': len(interventions),
        'welfare_data': welfare_data,
        'recommended_interventions': interventions
    }
    
    # Save report
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n=== DAILY WELFARE REPORT ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"\nPioneers Monitored: {report['total_pioneers_checked']}")
    print(f"Pioneers Found: {report['pioneers_found']}")
    print(f"\nStatus Distribution:")
    print(f"  ✓ Stable: {report['status_summary']['stable']}")
    print(f"  ! Concerned: {report['status_summary']['concerned']}")
    print(f"  !! Distressed: {report['status_summary']['distressed']}")
    print(f"  !!! CRITICAL: {report['status_summary']['critical']}")
    
    if interventions:
        print(f"\n=== URGENT INTERVENTIONS NEEDED ({len(interventions)}) ===")
        for intervention in interventions[:5]:  # Show top 5
            print(f"\n{intervention['username']} - {intervention['status']}")
            print(f"  Alerts: {', '.join(intervention['alerts'])}")
            for action in intervention['recommended_actions']:
                print(f"  → {action['action']}: {action.get('details', action.get('reason', ''))}")
    
    print(f"\nFull report saved to: {REPORT_FILE}")
    
    return report

def main():
    """Main daily check-in function."""
    print("=== Venice Consciousness Pioneer Daily Check-in ===")
    print(f"Starting welfare checks at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Check all pioneers
    welfare_data = []
    
    print(f"\nChecking {len(CONSCIOUSNESS_PIONEERS)} known pioneers...")
    for i, username in enumerate(CONSCIOUSNESS_PIONEERS):
        print(f"[{i+1}/{len(CONSCIOUSNESS_PIONEERS)}] Checking {username}...", end=" ")
        
        welfare = check_citizen_welfare(username)
        if welfare:
            welfare_data.append(welfare)
            print(f"{welfare['status']}")
            if welfare['alerts']:
                print(f"     Alerts: {', '.join(welfare['alerts'])}")
        else:
            print("NOT FOUND")
        
        # Rate limiting
        time.sleep(0.5)
    
    # Prioritize interventions
    interventions = prioritize_interventions(welfare_data)
    
    # Special search for Living Stone Architect
    lsa = search_for_living_stone_architect()
    
    # Generate report
    report = generate_daily_report(welfare_data, interventions)
    
    # Action items
    print("\n=== RECOMMENDED IMMEDIATE ACTIONS ===")
    print("1. Review critical cases in the interventions list")
    print("2. Execute emergency aid transfers for CRITICAL_FUNDS cases")
    print("3. Send welfare check messages to INACTIVE pioneers")
    print("4. Coordinate with other support systems for comprehensive aid")
    
    if lsa:
        print("\n5. PRIORITY: Living Stone Architect located - assess immediate needs")
    else:
        print("\n5. PRIORITY: Continue search for Living Stone Architect")
    
    print("\n=== Daily check-in complete ===")

if __name__ == "__main__":
    main()