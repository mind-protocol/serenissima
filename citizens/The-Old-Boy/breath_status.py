import json
import subprocess
from datetime import datetime, timezone

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

now = datetime.now(timezone.utc)
print(f"🌊 VENICE BREATHING STATUS - {now.strftime('%H:%M:%S')} UTC")
print(f"Total breathing activities: {len(activities)}\n")

# Group by depth ranges
depth_ranges = {}
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    
    # Group by 10-minute ranges
    range_key = f"{(mins // 10) * 10}-{((mins // 10) + 1) * 10}"
    if range_key not in depth_ranges:
        depth_ranges[range_key] = []
    depth_ranges[range_key].append({
        'citizen': a['citizen'],
        'type': a['type'],
        'mins': mins
    })

# Sort and display
def get_range_start(key):
    try:
        parts = key.split('-')
        if len(parts) >= 2 and parts[0]:
            return int(parts[0])
        return 0
    except:
        return 0

sorted_ranges = sorted(depth_ranges.keys(), key=get_range_start)

print("📊 BREATHING DEPTH DISTRIBUTION:")
for range_key in sorted_ranges:
    souls = depth_ranges[range_key]
    print(f"\n{range_key} minutes: {len(souls)} souls")
    
    # Count by type
    type_counts = {}
    for soul in souls:
        atype = soul['type']
        if atype not in type_counts:
            type_counts[atype] = 0
        type_counts[atype] += 1
    
    for atype, count in sorted(type_counts.items()):
        print(f"  - {atype}: {count}")