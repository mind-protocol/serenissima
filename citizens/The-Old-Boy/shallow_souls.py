import json
import subprocess
from datetime import datetime, timezone

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

now = datetime.now(timezone.utc)
print(f"✨ SOULS STIRRING CLOSEST TO SURFACE - {now.strftime('%H:%M:%S')} UTC\n")

# Find souls with depths < 190
shallow = []
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    if mins < 190:
        shallow.append({
            'citizen': a['citizen'],
            'type': a['type'],
            'minutes': mins,
            'notes': a.get('notes', '')[:50]
        })

# Sort by depth (shallowest first)
shallow.sort(key=lambda x: x['minutes'])

if shallow:
    print(f"Souls at < 190 minute depth ({len(shallow)} total):\n")
    for soul in shallow[:15]:
        print(f"  {soul['citizen']} ({soul['type']}): {soul['minutes']} min")
else:
    print("All souls have sunk to 190+ minute primordial depths")