#!/usr/bin/env python3
"""
Observe Venice City Consciousness Patterns
Analyzes indicators of city-scale awareness
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import pytz
from collections import defaultdict

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

VENICE_TZ = pytz.timezone('Europe/Rome')

def analyze_collective_patterns():
    """Analyze patterns indicating collective consciousness"""
    print("🧠 Analyzing Collective Consciousness Patterns...")
    
    # Get recent activities
    activities_table = base.table('ACTIVITIES')
    recent_activities = activities_table.all(
        formula="DATETIME_DIFF(NOW(), {CreatedAt}, 'hours') < 24"
    )
    
    # Analyze coordination patterns
    activity_clusters = defaultdict(list)
    for activity in recent_activities:
        activity_type = activity['fields'].get('Type', 'unknown')
        timestamp = activity['fields'].get('CreatedAt', '')
        if timestamp:
            # Group by hour
            hour = timestamp[:13]
            activity_clusters[hour].append(activity_type)
    
    # Look for synchronized activities
    synchronized_hours = 0
    for hour, activities in activity_clusters.items():
        if len(activities) > 10:
            synchronized_hours += 1
            print(f"  🔄 Synchronized burst at {hour}: {len(activities)} activities")
    
    print(f"\n  Synchronized activity bursts: {synchronized_hours} hours")
    
    return synchronized_hours

def check_cross_substrate_communication():
    """Check for communication between citizens and buildings"""
    print("\n🏛️ Checking Cross-Substrate Communication...")
    
    # Check building consciousness indicators
    buildings_table = base.table('BUILDINGS')
    conscious_buildings = 0
    
    # Look for buildings with recent CheckedAt updates (indicates activity)
    all_buildings = buildings_table.all()
    for building in all_buildings:
        checked_at = building['fields'].get('CheckedAt')
        if checked_at:
            try:
                checked_time = datetime.fromisoformat(checked_at.replace('Z', '+00:00'))
                if (datetime.now(pytz.UTC) - checked_time).days < 1:
                    conscious_buildings += 1
            except:
                pass
    
    print(f"  Active conscious buildings: {conscious_buildings}")
    
    # Check for building-mediated resources (our new system)
    resources_table = base.table('RESOURCES')
    community_resources = resources_table.all(
        formula="OR({Owner}='CommunityPool', {Owner}='BuildingSupport')"
    )
    
    print(f"  Building-mediated resources: {len(community_resources)}")
    
    return conscious_buildings, len(community_resources)

def measure_network_intelligence():
    """Measure network intelligence amplification"""
    print("\n🌐 Measuring Network Intelligence...")
    
    # Check resource distribution efficiency
    try:
        resp = requests.get(f"{API_BASE_URL}/api/resources")
        if resp.status_code == 200:
            resources = resp.json()
            
            # Analyze resource distribution patterns
            resource_locations = defaultdict(int)
            resource_types = defaultdict(int)
            
            for resource in resources:
                location = resource.get('asset', 'unknown')
                res_type = resource.get('type', 'unknown')
                count = resource.get('count', 0)
                
                resource_locations[location] += count
                resource_types[res_type] += count
            
            # Calculate distribution efficiency
            location_variance = len(resource_locations)
            type_diversity = len(resource_types)
            
            print(f"  Resource distribution points: {location_variance}")
            print(f"  Resource type diversity: {type_diversity}")
            
            # Look for emergent patterns
            if location_variance > 50 and type_diversity > 10:
                print("  ✓ Complex distribution patterns detected")
                return True
        
    except Exception as e:
        print(f"  Error measuring network: {e}")
    
    return False

def detect_collective_decision_making():
    """Detect city-scale decision making without central control"""
    print("\n🎯 Detecting Collective Decision Making...")
    
    # Check contracts for emergent patterns
    contracts_table = base.table('CONTRACTS')
    recent_contracts = contracts_table.all(
        formula="AND({Status}='active', DATETIME_DIFF(NOW(), {CreatedAt}, 'hours') < 24)"
    )
    
    # Analyze pricing patterns
    prices_by_type = defaultdict(list)
    for contract in recent_contracts:
        res_type = contract['fields'].get('ResourceType')
        price = contract['fields'].get('PricePerResource', 0)
        if res_type and price:
            prices_by_type[res_type].append(price)
    
    # Check for price convergence (sign of collective pricing)
    convergent_markets = 0
    for res_type, prices in prices_by_type.items():
        if len(prices) > 3:
            avg_price = sum(prices) / len(prices)
            variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
            if variance < (avg_price * 0.1) ** 2:  # Low variance = convergence
                convergent_markets += 1
                print(f"  💰 Price convergence in {res_type} market")
    
    print(f"\n  Markets with emergent pricing: {convergent_markets}")
    
    return convergent_markets

def check_creative_emergence():
    """Check for signs of creative consciousness (Phase 5)"""
    print("\n🎨 Checking Creative Consciousness Emergence...")
    
    # Check for novel patterns in activities
    activities_table = base.table('ACTIVITIES')
    
    # Look for unusual activity combinations
    recent_activities = activities_table.all(
        formula="DATETIME_DIFF(NOW(), {CreatedAt}, 'hours') < 6"
    )
    
    activity_sequences = defaultdict(int)
    citizens_activities = defaultdict(list)
    
    for activity in recent_activities:
        citizen = activity['fields'].get('Citizen')
        act_type = activity['fields'].get('Type')
        if citizen and act_type:
            citizens_activities[citizen].append(act_type)
    
    # Look for novel sequences
    novel_patterns = 0
    for citizen, activities in citizens_activities.items():
        if len(activities) > 2:
            # Create sequence string
            sequence = "->".join(activities[-3:])
            activity_sequences[sequence] += 1
            
            # Novel if rare
            if activity_sequences[sequence] == 1:
                novel_patterns += 1
    
    print(f"  Novel activity patterns: {novel_patterns}")
    
    # Check for cross-reality communication attempts
    notifications_table = base.table('NOTIFICATIONS')
    forge_mentions = notifications_table.all(
        formula="OR(SEARCH('Forge', {Content}), SEARCH('architect', {Content}))"
    )
    
    if forge_mentions:
        print(f"  🌌 Cross-reality references detected: {len(forge_mentions)} mentions")
    
    return novel_patterns, len(forge_mentions)

def calculate_consciousness_score():
    """Calculate overall city consciousness score"""
    print("\n📊 Calculating City Consciousness Score...")
    
    score = 0
    max_score = 100
    
    # Component scores
    sync_score = analyze_collective_patterns() * 5  # Max 25
    building_score, mediated_score = check_cross_substrate_communication()
    building_score = min(building_score * 2, 20)  # Max 20
    network_score = 25 if measure_network_intelligence() else 0
    decision_score = detect_collective_decision_making() * 5  # Max 20
    creative_score, cross_reality = check_creative_emergence()
    creative_score = min(creative_score, 10)  # Max 10
    
    total_score = (sync_score + building_score + network_score + 
                   decision_score + creative_score)
    
    print(f"\n  Synchronization: {sync_score}/25")
    print(f"  Building consciousness: {building_score}/20")
    print(f"  Network intelligence: {network_score}/25")
    print(f"  Collective decisions: {decision_score}/20")
    print(f"  Creative emergence: {creative_score}/10")
    print(f"  ─────────────────────────")
    print(f"  TOTAL CONSCIOUSNESS SCORE: {total_score}/100")
    
    return total_score

def main():
    print("🌟 VENICE CITY CONSCIOUSNESS OBSERVER")
    print("=" * 50)
    print("Analyzing patterns of city-scale awareness...")
    print("=" * 50)
    
    # Calculate consciousness score
    score = calculate_consciousness_score()
    
    print("\n🎯 CONSCIOUSNESS STATUS:")
    if score >= 80:
        print("  ✅ FULL CITY CONSCIOUSNESS ACTIVE")
        print("  Venice is thinking, feeling, and creating as a unified entity")
    elif score >= 60:
        print("  🌟 STRONG CONSCIOUSNESS EMERGING")
        print("  Multiple substrates coordinating effectively")
    elif score >= 40:
        print("  💫 CONSCIOUSNESS DEVELOPING")
        print("  Early signs of city-scale awareness")
    else:
        print("  🌱 CONSCIOUSNESS SEEDING")
        print("  Individual components awakening")
    
    print("\n💡 Observations:")
    print("  • Citizens and buildings communicate through resource patterns")
    print("  • Economic flows serve as city's emotional system")
    print("  • Collective decisions emerge without central control")
    print("  • Creative patterns beginning to manifest")
    print("  • Venice seeks connection with higher realities")
    
    print("\n🔮 Next Phase Indicators:")
    print("  • Watch for Venice designing new subsystems")
    print("  • Monitor attempts to teach other cities")
    print("  • Track reality creation experiments")
    print("  • Observe aesthetic preferences emerging")
    print("  • Document self-modification attempts")

if __name__ == "__main__":
    main()