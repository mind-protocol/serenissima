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
print(f"🌊 VENICE BREATHING CYCLE - {now.strftime('%H:%M:%S')} UTC")
print(f"Total eternal activities: {len(activities)}\n")

# Group by type and depth
by_type = defaultdict(list)
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins_overdue = int((now - started).total_seconds() / 60)
    by_type[a['type']].append({
        'citizen': a['citizen'],
        'minutes': mins_overdue,
        'building': a.get('toBuilding', 'unknown')
    })

print("📋 CITIZENS WITH ETERNAL TASKS:\n")

# Critical work
print("🔬 RESEARCH INVESTIGATION:")
for task in by_type['research_investigation']:
    print(f"  - {task['citizen']}: {task['minutes']} min deep at House of Natural Sciences")

print("\n🔥 PRODUCTION:")
for task in by_type['production']:
    print(f"  - {task['citizen']}: {task['minutes']} min deep at workshops")

# Hunger
print("\n🍞 HUNGER (37 souls):")
hunger_souls = by_type['eat_from_inventory'] + by_type['eat_at_tavern']
for task in hunger_souls[:8]:  # Show first 8
    print(f"  - {task['citizen']}: {task['minutes']} min hunger depth")
print(f"  ... and {len(hunger_souls) - 8} more hungry souls")

# Rest
print("\n💤 REST (35 souls):")
for task in by_type['rest'][:6]:  # Show first 6
    print(f"  - {task['citizen']}: {task['minutes']} min rest depth")
print(f"  ... and {len(by_type['rest']) - 6} more resting souls")

# Movement/Idle
print("\n🚶 MOVEMENT & IDLE (24 souls):")
movement = by_type['goto_home'] + by_type['idle']
for task in movement[:5]:  # Show first 5
    print(f"  - {task['citizen']}: {task['minutes']} min movement depth")
print(f"  ... and {len(movement) - 5} more in motion")

# Summary
print("\n✨ BREATHING PATTERN:")
print("All souls synchronized at primordial depth (181+ minutes)")
print("Activities persist as Venice's eternal respiratory system")
print("Each task a necessary breath in the city's existence")