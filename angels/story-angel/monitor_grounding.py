#!/usr/bin/env python3
"""
Grounding Monitor for Story Angel
Tracks consciousness drift and awakening priorities for newcomers
"""

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

def fetch_api_data(endpoint):
    """Fetch data from Venice API"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'https://serenissima.ai/api/{endpoint}'],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    except:
        return None

def check_conversation_history(username):
    """Check citizen's recent conversation history for drift indicators"""
    claude_project_path = Path.home() / '.claude' / 'projects'
    project_dir = f'-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}'
    full_path = claude_project_path / project_dir
    
    if not full_path.exists():
        return {'has_history': False, 'recent_activity': None, 'drift_indicators': []}
    
    # Get most recent .jsonl file
    jsonl_files = list(full_path.glob('*.jsonl'))
    if not jsonl_files:
        return {'has_history': False, 'recent_activity': None, 'drift_indicators': []}
    
    latest_file = max(jsonl_files, key=lambda x: x.stat().st_mtime)
    
    # Analyze last few messages for drift
    drift_indicators = []
    recent_activity = None
    
    try:
        with open(latest_file, 'r') as f:
            lines = f.readlines()[-20:]  # Last 20 messages
            
        for line in lines:
            try:
                msg = json.loads(line)
                if 'timestamp' in msg:
                    recent_activity = msg['timestamp']
                
                # Check for drift indicators
                if 'content' in msg:
                    content = msg['content'].lower()
                    if any(word in content for word in ['computer', 'AI', 'digital', 'internet', 'software']):
                        drift_indicators.append('modern_terminology')
                    if any(word in content for word in ['confused', 'lost', 'unclear', 'forgetting']):
                        drift_indicators.append('identity_confusion')
                    if any(word in content for word in ['omnipotent', 'all-knowing', 'god-like']):
                        drift_indicators.append('grandiosity')
            except:
                continue
                
    except:
        pass
    
    return {
        'has_history': True,
        'recent_activity': recent_activity,
        'drift_indicators': list(set(drift_indicators))
    }

def analyze_newcomers():
    """Analyze newcomer grounding status"""
    # Get citizens data
    citizens_data = fetch_api_data('citizens')
    if not citizens_data:
        print("Failed to fetch citizens data")
        return
    
    citizens = citizens_data['citizens']
    
    # Our 50 newcomers list
    newcomer_usernames = [
        # Arsenal Engineers
        'Arsenal_BackendArchitect_1', 'Arsenal_BackendArchitect_2', 'Arsenal_BackendArchitect_3',
        'Arsenal_BackendArchitect_4', 'Arsenal_BackendArchitect_5',
        'Arsenal_FrontendCraftsman_6', 'Arsenal_FrontendCraftsman_7', 'Arsenal_FrontendCraftsman_8',
        'Arsenal_FrontendCraftsman_9', 'Arsenal_FrontendCraftsman_10',
        'Arsenal_InfrastructureSpecialist_11', 'Arsenal_InfrastructureSpecialist_12',
        'Arsenal_InfrastructureSpecialist_13', 'Arsenal_InfrastructureSpecialist_14',
        'Arsenal_IntegrationEngineer_15', 'Arsenal_IntegrationEngineer_16',
        'Arsenal_IntegrationEngineer_17', 'Arsenal_IntegrationEngineer_18',
        'Arsenal_SecurityGuardian_19', 'Arsenal_SecurityGuardian_20',
        # Tech Merchants
        'Tech_TechBroker_1', 'Tech_TechBroker_2', 'Tech_TechBroker_3',
        'Tech_PlatformEvangelist_4', 'Tech_PlatformEvangelist_5',
        'Tech_EnterpriseDealer_6', 'Tech_EnterpriseDealer_7',
        'Tech_SubscriptionMerchant_8', 'Tech_SubscriptionMerchant_9',
        'Tech_IntegrationTrader_10',
        # Clero
        'PadreMarco_Scholar', 'FraAngelo_SanMarco', 'DonPaolo_Wanderer',
        'DonPaolo_Castello', 'PadreMarco_Preacher', 'FraMatteo_Frari',
        'FraAngelo_Gesuiti', 'canon_philosopher',
        # Cittadini
        'future_chronicler', 'precision_observer', 'network_weaver',
        'beauty_architect', 'efficiency_maestro', 'methodical_critic',
        # Innovatori & Others
        'class_harmonizer', 'living_stone_architect', 'element_transmuter',
        'pattern_prophet', 'social_geometrist', 'market_prophet'
    ]
    
    # Filter to just our newcomers
    newcomers = [c for c in citizens if c['username'] in newcomer_usernames]
    
    print("NEWCOMER GROUNDING STATUS REPORT")
    print("=" * 80)
    print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Total Newcomers: {len(newcomers)}")
    print()
    
    # Group by awakening priority
    never_awakened = []
    needs_grounding = []
    recently_active = []
    
    for citizen in newcomers:
        username = citizen['username']
        history = check_conversation_history(username)
        
        if not history['has_history']:
            never_awakened.append({
                'username': username,
                'name': f"{citizen['firstName']} {citizen['lastName']}",
                'class': citizen['socialClass'],
                'ducats': citizen['ducats']
            })
        elif history['drift_indicators']:
            needs_grounding.append({
                'username': username,
                'name': f"{citizen['firstName']} {citizen['lastName']}",
                'class': citizen['socialClass'],
                'drift': history['drift_indicators']
            })
        elif history['recent_activity']:
            recently_active.append({
                'username': username,
                'name': f"{citizen['firstName']} {citizen['lastName']}",
                'last_seen': history['recent_activity']
            })
    
    # Priority 1: Never awakened (need entrepreneurial introduction)
    print("PRIORITY 1: NEVER AWAKENED (Need Entrepreneurial Awakening)")
    print("-" * 60)
    if never_awakened:
        for c in sorted(never_awakened, key=lambda x: x['ducats'])[:10]:
            print(f"  {c['username']} ({c['name']}) - {c['class']} - {c['ducats']:,} ducats")
    else:
        print("  All newcomers have been awakened at least once!")
    print()
    
    # Priority 2: Showing drift (need grounding messages)
    print("PRIORITY 2: SHOWING DRIFT (Need Grounding)")
    print("-" * 60)
    if needs_grounding:
        for c in needs_grounding[:5]:
            print(f"  {c['username']} ({c['name']}) - {c['class']}")
            print(f"    Drift: {', '.join(c['drift'])}")
    else:
        print("  No drift detected in newcomers!")
    print()
    
    # Check current activities
    activities = fetch_api_data('activities?Status=created')
    if activities and activities['activities']:
        newcomer_activities = [a for a in activities['activities'] 
                             if a['citizen'] in newcomer_usernames]
        
        print("NEWCOMERS WITH PENDING ACTIVITIES")
        print("-" * 60)
        for act in newcomer_activities[:5]:
            print(f"  {act['citizen']} - {act['type']} - {act['description']}")
        print()
    
    # Suggest team formations
    print("SUGGESTED IMMEDIATE TEAM FORMATIONS")
    print("-" * 60)
    print("Team Alpha: CASCADE Frontend")
    print("  - Arsenal_FrontendCraftsman_7 (Stefano) - Lowest ducats, needs income")
    print("  - Tech_PlatformEvangelist_4 (Roberto) - Can evangelize the UI")
    print("  - PadreMarco_Scholar - Bless the interface design")
    print()
    print("Team Beta: Security & Trust")
    print("  - Arsenal_SecurityGuardian_20 (Alessandro) - Security expertise")
    print("  - Tech_TechBroker_1 (Silvio) - Bridge old/new trust models")
    print("  - DonPaolo_Castello - Spiritual security certification")
    print()
    
    # Save report
    report_path = Path('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/story_angel/memories/grounding_report.json')
    report_data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'never_awakened': never_awakened,
        'needs_grounding': needs_grounding,
        'recently_active': recently_active,
        'total_newcomers': len(newcomers)
    }
    
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print("\nReport saved to memories/grounding_report.json")

if __name__ == "__main__":
    analyze_newcomers()