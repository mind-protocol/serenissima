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
print(f"🌊 NEW CYCLE SURVEY - {now.strftime('%H:%M:%S')} UTC")
print(f"Total activities in new breathing cycle: {len(activities)}\n")

# Group by type and timing
by_type = defaultdict(list)
urgent = []
ready = []
future = []

for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    
    soul_data = {
        'citizen': a['citizen'],
        'type': a['type'],
        'minutes': mins,
        'notes': a.get('notes', '')[:60]
    }
    
    by_type[a['type']].append(soul_data)
    
    if mins > 10:
        urgent.append(soul_data)
    elif mins > 0:
        ready.append(soul_data)
    else:
        future.append(soul_data)

# Show urgent souls first
if urgent:
    print(f"🔥 URGENT SOULS (>10 min overdue): {len(urgent)}")
    for soul in sorted(urgent, key=lambda x: x['minutes'], reverse=True)[:10]:
        print(f"  - {soul['citizen']} ({soul['type']}): {soul['minutes']} min")
    print()

# Show ready souls
if ready:
    print(f"✨ READY SOULS (0-10 min): {len(ready)}")
    for soul in sorted(ready, key=lambda x: x['minutes'], reverse=True)[:10]:
        print(f"  - {soul['citizen']} ({soul['type']}): {soul['minutes']} min")
    print()

# Show activity type distribution
print("📊 ACTIVITY DISTRIBUTION:")
for atype, souls in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"  {atype}: {len(souls)} souls")