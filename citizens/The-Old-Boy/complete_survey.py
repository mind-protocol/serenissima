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
print(f"🌊 COMPLETE SOUL SURVEY - {now.strftime('%H:%M:%S')} UTC")
print(f"Total eternal activities: {len(activities)}\n")

# Group by activity type and depth
by_type = defaultdict(list)
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    by_type[a['type']].append({
        'citizen': a['citizen'],
        'minutes': mins
    })

# Sort each type by depth
for activity_type in by_type:
    by_type[activity_type].sort(key=lambda x: x['minutes'])

# Show shallowest from each type
print("🌟 SOULS STIRRING CLOSEST TO SURFACE BY TYPE:\n")

for activity_type, souls in sorted(by_type.items()):
    if souls:
        shallowest = souls[0]
        deepest = souls[-1]
        print(f"📋 {activity_type.upper()} ({len(souls)} souls)")
        print(f"   Shallowest: {shallowest['citizen']} at {shallowest['minutes']} min")
        print(f"   Deepest: {deepest['citizen']} at {deepest['minutes']} min")
        print(f"   Range: {shallowest['minutes']}-{deepest['minutes']} minutes\n")

# Find overall shallowest
all_souls = []
for souls in by_type.values():
    all_souls.extend(souls)
all_souls.sort(key=lambda x: x['minutes'])

print("\n✨ ABSOLUTE SHALLOWEST SOULS:")
for soul in all_souls[:10]:
    activity_type = next(t for t, souls in by_type.items() if any(s['citizen'] == soul['citizen'] for s in souls))
    print(f"  - {soul['citizen']} ({activity_type}): {soul['minutes']} min")