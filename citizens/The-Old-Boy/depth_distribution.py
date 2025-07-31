import json
import subprocess
from datetime import datetime, timezone
from collections import defaultdict

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

now = datetime.now(timezone.utc)
print(f"🌊 DEPTH DISTRIBUTION - {now.strftime('%H:%M:%S')} UTC\n")

# Group by depth ranges
depth_groups = defaultdict(list)
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    
    # Group by 5-minute ranges
    range_key = f"{(mins // 5) * 5}-{((mins // 5) + 1) * 5}"
    depth_groups[range_key].append((a['citizen'], a['type'], mins))

# Sort and display
sorted_ranges = sorted(depth_groups.keys(), key=lambda x: int(x.split('-')[0]))

for range_key in sorted_ranges:
    souls = depth_groups[range_key]
    print(f"📊 {range_key} minutes: {len(souls)} souls")
    
    # Show examples from this range
    type_counts = defaultdict(int)
    for _, activity_type, _ in souls:
        type_counts[activity_type] += 1
    
    for atype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {atype}: {count}")
    print()

# Show extremes
all_depths = [(a['citizen'], a['type'], int((now - datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))).total_seconds() / 60)) for a in activities]
all_depths.sort(key=lambda x: x[2])

print(f"🌟 SHALLOWEST: {all_depths[0][0]} ({all_depths[0][1]}): {all_depths[0][2]} min")
print(f"🌀 DEEPEST: {all_depths[-1][0]} ({all_depths[-1][1]}): {all_depths[-1][2]} min")