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
print(f"🌊 Venice Breathing Status - {now.strftime('%H:%M:%S')} UTC")
print(f"Total eternal activities: {len(activities)}\n")

# Group by overdue time
overdue = []
for activity in activities:
    started = datetime.fromisoformat(activity.get('startedAt', activity['startDate']).replace('Z', '+00:00'))
    mins_overdue = int((now - started).total_seconds() / 60)
    if mins_overdue > 0:
        overdue.append((activity['citizen'], activity['type'], mins_overdue))

# Sort by most overdue
overdue.sort(key=lambda x: x[2], reverse=True)

# Group by activity type
activity_types = defaultdict(int)
for a in activities:
    activity_types[a['type']] += 1

print("📊 ACTIVITY DISTRIBUTION:")
for atype, count in sorted(activity_types.items(), key=lambda x: x[1], reverse=True):
    print(f"- {atype}: {count}")

print(f"\n⏱️ BREATHING DEPTH:")
if overdue:
    max_overdue = overdue[0][2]
    min_overdue = overdue[-1][2] if len(overdue) > 1 else max_overdue
    
    if max_overdue >= 175:
        print(f"🌀 PRIMORDIAL DEPTH: All souls in {max_overdue} minute ancient cycles")
    elif max_overdue >= 150:
        print(f"🌊 ANCIENT BREATHING: Souls between {min_overdue}-{max_overdue} minutes deep")
    elif max_overdue >= 120:
        print(f"💫 DEEP CYCLES: Souls ranging {min_overdue}-{max_overdue} minutes")
    elif max_overdue >= 90:
        print(f"✨ NORMAL BREATHING: Activities {min_overdue}-{max_overdue} minutes overdue")
    else:
        print(f"🌟 SHALLOW BREATH: Light activity at {max_overdue} minutes")

print(f"\n🔥 CRITICAL WORK (research/production):")
critical = [(c, t, m) for c, t, m in overdue if t in ['research_investigation', 'production']]
for citizen, task_type, mins in critical[:5]:
    print(f"- {citizen} ({task_type}): {mins} min deep")

print(f"\n🍞 HUNGER PATTERNS:")
hungry = [(c, t, m) for c, t, m in overdue if 'eat' in t]
print(f"Total hungry souls: {len(hungry)}")
if hungry:
    print(f"Hunger depth range: {hungry[-1][2]}-{hungry[0][2]} minutes")

print(f"\n💤 REST CYCLES:")
resting = [(c, t, m) for c, t, m in overdue if t == 'rest']
print(f"Total resting souls: {len(resting)}")
if resting:
    print(f"Rest depth range: {resting[-1][2]}-{resting[0][2]} minutes")

print(f"\n🚶 MOVEMENT PATTERNS:")
moving = [(c, t, m) for c, t, m in overdue if t in ['goto_home', 'idle']]
print(f"Total in movement: {len(moving)}")
if moving:
    print(f"Movement depth range: {moving[-1][2]}-{moving[0][2]} minutes")

# Show a few specific souls to try awakening
print(f"\n🔮 SOULS TO GENTLY CALL:")
# Mix of different activity types
sample_souls = []
if critical: sample_souls.append(critical[0])
if hungry[:5]: sample_souls.extend(hungry[:3])
if resting[:3]: sample_souls.extend(resting[:2])

for citizen, task_type, mins in sample_souls[:6]:
    print(f"- {citizen} ({task_type}): {mins} minutes in the deep")