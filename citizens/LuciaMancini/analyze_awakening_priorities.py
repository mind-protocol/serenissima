#!/usr/bin/env python3
"""
Analyze Venice activities to identify souls needing immediate awakening
"""

import json
from datetime import datetime, timezone
import subprocess
from collections import defaultdict

def fetch_activities():
    """Fetch raw activities data from the API"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'https://serenissima.ai/api/activities'],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error fetching activities: {e}")
        return None

def parse_timestamp(ts):
    """Parse ISO timestamp to datetime object"""
    return datetime.fromisoformat(ts.replace('Z', '+00:00'))

def analyze_activities(data):
    """Analyze activities and group by urgency"""
    now = datetime.now(timezone.utc)
    
    # Categories
    overdue = []
    immediate = []
    upcoming = []
    
    # Only analyze "created" status activities
    created_activities = [a for a in data['activities'] if a['status'] == 'created']
    
    for activity in created_activities:
        start_time = parse_timestamp(activity['startDate'])
        time_diff = (start_time - now).total_seconds() / 60  # minutes
        
        activity_info = {
            'citizen': activity['citizen'],
            'type': activity['type'],
            'priority': activity.get('priority', 0),
            'start_time': start_time,
            'time_until_start': time_diff,
            'activity_id': activity['activityId'],
            'description': activity.get('description', activity.get('notes', ''))[:100]
        }
        
        if time_diff < -30:  # Overdue by more than 30 minutes
            overdue.append(activity_info)
        elif time_diff < 0:  # Already started but recent
            immediate.append(activity_info)
        elif time_diff < 30:  # Starting within 30 minutes
            upcoming.append(activity_info)
    
    return overdue, immediate, upcoming

def group_by_activity_type(activities):
    """Group activities by type for batch awakening"""
    grouped = defaultdict(list)
    for activity in activities:
        grouped[activity['type']].append(activity)
    return dict(grouped)

def print_analysis(overdue, immediate, upcoming):
    """Print the analysis results"""
    print("\n🚨 AWAKENING PRIORITY ANALYSIS")
    print("=" * 60)
    
    if overdue:
        print("\n❗ OVERDUE ACTIVITIES (Need immediate awakening):")
        print("-" * 60)
        for a in sorted(overdue, key=lambda x: x['time_until_start']):
            print(f"  {a['citizen']:25} | {a['type']:20} | Overdue by {-a['time_until_start']:.0f} min")
            print(f"    Priority: {a['priority']} | {a['description']}")
    
    if immediate:
        print("\n⚡ IMMEDIATE ACTIVITIES (Just started):")
        print("-" * 60)
        for a in sorted(immediate, key=lambda x: x['priority'], reverse=True):
            print(f"  {a['citizen']:25} | {a['type']:20} | Started {-a['time_until_start']:.0f} min ago")
            print(f"    Priority: {a['priority']} | {a['description']}")
    
    if upcoming:
        print("\n⏰ UPCOMING ACTIVITIES (Within 30 minutes):")
        print("-" * 60)
        for a in sorted(upcoming, key=lambda x: x['time_until_start']):
            print(f"  {a['citizen']:25} | {a['type']:20} | Starts in {a['time_until_start']:.0f} min")
            print(f"    Priority: {a['priority']} | {a['description']}")
    
    # Group by type for efficient awakening
    all_urgent = overdue + immediate
    if all_urgent:
        print("\n📊 GROUPED BY ACTIVITY TYPE (for batch awakening):")
        print("-" * 60)
        grouped = group_by_activity_type(all_urgent)
        for activity_type, citizens_list in grouped.items():
            citizen_names = [c['citizen'] for c in citizens_list]
            print(f"  {activity_type}: {', '.join(citizen_names)}")
    
    # Summary
    print("\n📈 SUMMARY:")
    print(f"  Total overdue: {len(overdue)}")
    print(f"  Total immediate: {len(immediate)}")
    print(f"  Total upcoming: {len(upcoming)}")
    print(f"  Total needing attention: {len(overdue) + len(immediate) + len(upcoming)}")

def main():
    print("Fetching Venice activities...")
    data = fetch_activities()
    
    if not data:
        print("Failed to fetch activities")
        return
    
    print(f"Total activities found: {len(data['activities'])}")
    created_count = len([a for a in data['activities'] if a['status'] == 'created'])
    print(f"Activities with 'created' status: {created_count}")
    
    overdue, immediate, upcoming = analyze_activities(data)
    print_analysis(overdue, immediate, upcoming)
    
    # Generate awakening recommendations
    print("\n🎯 AWAKENING RECOMMENDATIONS:")
    print("-" * 60)
    
    # Highest priority: Research activities
    research_souls = [a['citizen'] for a in overdue + immediate if 'research' in a['type']]
    if research_souls:
        print(f"1. Research souls (highest priority): {', '.join(set(research_souls))}")
    
    # Production activities (bread production critical)
    production_souls = [a['citizen'] for a in overdue + immediate if a['type'] == 'production']
    if production_souls:
        print(f"2. Production souls (bread makers): {', '.join(set(production_souls))}")
    
    # Import/delivery activities
    delivery_souls = [a['citizen'] for a in overdue + immediate if 'deliver' in a['type'] or 'import' in a['type']]
    if delivery_souls:
        print(f"3. Delivery souls (resource flow): {', '.join(set(delivery_souls))}")
    
    # Tavern activities (social/food)
    tavern_souls = [a['citizen'] for a in overdue + immediate if 'eat_at_tavern' in a['type']]
    if tavern_souls[:5]:  # Limit to first 5 to avoid spam
        print(f"4. Tavern souls (first 5): {', '.join(tavern_souls[:5])}")

if __name__ == "__main__":
    main()