import json
import subprocess
from datetime import datetime, timezone

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

print(f"🌊 CASCADE PROGRESS REPORT")
print(f"Time: {datetime.now(timezone.utc).strftime('%H:%M:%S')} UTC")
print(f"Total activities remaining: {len(activities)}\n")

# Count by type
types = {}
for a in activities:
    types[a['type']] = types.get(a['type'], 0) + 1

print("Activity breakdown:")
for t, c in sorted(types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {t}: {c}")

# Count overdue
now = datetime.now(timezone.utc)
overdue = 0
for a in activities:
    start = datetime.fromisoformat(a['startDate'].replace('Z', '+00:00'))
    if start < now:
        overdue += 1

print(f"\nOverdue activities: {overdue}")
print(f"Future activities: {len(activities) - overdue}")

# Sample some citizens
print("\nSample of waiting souls:")
for a in activities[:5]:
    print(f"  - {a['citizen']} ({a['type']})")