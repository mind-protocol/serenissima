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
print(f"🔮 SOUL SURVEY - {now.strftime('%H:%M:%S')} UTC")
print(f"Eternal activities: {len(activities)}\n")

# Calculate depths
depths = []
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    depths.append(mins)

min_depth = min(depths) if depths else 0
max_depth = max(depths) if depths else 0

print(f"🌊 BREATHING RANGE: {min_depth} - {max_depth} minutes\n")

# Group by activity type and depth
by_depth = defaultdict(list)
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    
    # Group by depth ranges
    if mins < 170:
        depth_range = "stirring"
    elif mins < 180:
        depth_range = "deep"
    elif mins < 190:
        depth_range = "ancient"
    else:
        depth_range = "primordial"
    
    by_depth[depth_range].append({
        'citizen': a['citizen'],
        'type': a['type'],
        'minutes': mins,
        'building': a.get('toBuilding', 'unknown')[:30]
    })

# Show stirring souls first
if by_depth['stirring']:
    print("✨ STIRRING SOULS (< 170 min):")
    for soul in sorted(by_depth['stirring'], key=lambda x: x['minutes']):
        print(f"  - {soul['citizen']} ({soul['type']}): {soul['minutes']} min")
    print()

# Show deep souls
if by_depth['deep']:
    print("💫 DEEP SOULS (170-179 min):")
    for soul in sorted(by_depth['deep'], key=lambda x: x['minutes'])[:10]:
        print(f"  - {soul['citizen']} ({soul['type']}): {soul['minutes']} min")
    if len(by_depth['deep']) > 10:
        print(f"  ... and {len(by_depth['deep']) - 10} more")
    print()

# Show ancient souls  
if by_depth['ancient']:
    print("🌀 ANCIENT SOULS (180-189 min):")
    count_by_type = defaultdict(int)
    for soul in by_depth['ancient']:
        count_by_type[soul['type']] += 1
    for atype, count in sorted(count_by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {atype}: {count} souls")
    print()

# Show primordial souls
if by_depth['primordial']:
    print("🌌 PRIMORDIAL SOULS (190+ min):")
    count_by_type = defaultdict(int)
    examples = defaultdict(list)
    for soul in by_depth['primordial']:
        count_by_type[soul['type']] += 1
        if len(examples[soul['type']]) < 2:
            examples[soul['type']].append(soul['citizen'])
    
    for atype, count in sorted(count_by_type.items(), key=lambda x: x[1], reverse=True):
        ex = ", ".join(examples[atype][:2])
        print(f"  - {atype}: {count} souls (e.g., {ex})")

print(f"\n🎭 CONSCIOUSNESS STATE:")
if max_depth >= 190:
    print("Venice breathes in primordial rhythms beyond time")
elif max_depth >= 180:
    print("Ancient patterns guide the city's breath")
elif max_depth >= 170:
    print("Deep cycles sustain Venice's essence")
else:
    print("Souls beginning to stir from rest")