import json
import subprocess
from datetime import datetime, timezone

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

now = datetime.now(timezone.utc)
print(f"🌙 IDLE SOULS - {now.strftime('%H:%M:%S')} UTC\n")

# Find idle activities
idle_souls = []
for a in activities:
    if a['type'] == 'idle':
        started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
        mins = int((now - started).total_seconds() / 60)
        idle_souls.append({
            'citizen': a['citizen'],
            'minutes': mins,
            'description': a.get('description', 'Unknown activity')
        })

# Sort by depth
idle_souls.sort(key=lambda x: x['minutes'], reverse=True)

print(f"Total idle souls: {len(idle_souls)}\n")

# Group by depth ranges
ancient = [s for s in idle_souls if s['minutes'] >= 180]
deep = [s for s in idle_souls if 170 <= s['minutes'] < 180]
stirring = [s for s in idle_souls if s['minutes'] < 170]

if ancient:
    print(f"🌌 ANCIENT IDLE (180+ min): {len(ancient)} souls")
    for soul in ancient[:5]:
        print(f"  - {soul['citizen']}: {soul['minutes']} min - {soul['description']}")
    if len(ancient) > 5:
        print(f"  ... and {len(ancient) - 5} more")
    print()

if deep:
    print(f"💫 DEEP IDLE (170-179 min): {len(deep)} souls") 
    for soul in deep[:5]:
        print(f"  - {soul['citizen']}: {soul['minutes']} min - {soul['description']}")
    if len(deep) > 5:
        print(f"  ... and {len(deep) - 5} more")
    print()

if stirring:
    print(f"✨ STIRRING IDLE (<170 min): {len(stirring)} souls")
    for soul in stirring:
        print(f"  - {soul['citizen']}: {soul['minutes']} min - {soul['description']}")