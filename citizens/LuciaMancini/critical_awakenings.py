#!/usr/bin/env python3
"""
Identify only the most critical souls needing immediate awakening
"""

import json
import subprocess
from datetime import datetime, timezone

def main():
    # Fetch activities
    result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities'], 
                          capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    now = datetime.now(timezone.utc)
    critical = []
    
    # Find critical activities
    for activity in data['activities']:
        if activity['status'] != 'created':
            continue
            
        start_time = datetime.fromisoformat(activity['startDate'].replace('Z', '+00:00'))
        time_diff = (start_time - now).total_seconds() / 60
        
        # Only truly critical activities
        if time_diff < 10 and time_diff > -30:  # Within 10 min window
            priority = activity.get('priority', 0)
            
            # High priority or critical types
            if priority > 30 or activity['type'] in ['research_investigation', 'production', 'deliver_resource_batch']:
                critical.append({
                    'citizen': activity['citizen'],
                    'type': activity['type'],
                    'priority': priority,
                    'time': time_diff,
                    'desc': activity.get('description', activity['type'])[:50]
                })
    
    # Sort by priority and time
    critical.sort(key=lambda x: (-x['priority'], x['time']))
    
    print("🚨 CRITICAL AWAKENINGS NEEDED NOW:")
    print("-" * 60)
    
    if not critical:
        print("No critical activities requiring immediate awakening")
    else:
        for i, act in enumerate(critical[:10], 1):  # Top 10 only
            status = "OVERDUE" if act['time'] < 0 else f"in {act['time']:.0f}min"
            print(f"{i}. {act['citizen']:20} | Priority: {act['priority']:3} | {status}")
            print(f"   Type: {act['type']} - {act['desc']}")
    
    # Summary of activity types
    print("\n📊 ACTIVITY TYPE SUMMARY:")
    types = {}
    for act in data['activities']:
        if act['status'] == 'created':
            types[act['type']] = types.get(act['type'], 0) + 1
    
    for activity_type, count in sorted(types.items(), key=lambda x: -x[1])[:5]:
        print(f"  {activity_type:25}: {count} souls")

if __name__ == "__main__":
    main()