import json
import subprocess
from datetime import datetime, timezone

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

now = datetime.now(timezone.utc)
print(f"🕐 Time: {now.strftime('%H:%M:%S')} UTC\n")

# Find immediate needs (overdue or due in next 5 min)
immediate = []
for a in activities:
    start = datetime.fromisoformat(a['startDate'].replace('Z', '+00:00'))
    mins = (start - now).total_seconds() / 60
    if mins < 5:  # Overdue or due very soon
        immediate.append((a, mins))

immediate.sort(key=lambda x: x[1])

print(f"🚨 IMMEDIATE AWAKENINGS NEEDED ({len(immediate)} souls):\n")
for a, mins in immediate[:15]:
    if mins < 0:
        print(f"OVERDUE: {a['citizen']} - {a['type']} ({abs(int(mins))} min late)")
    else:
        print(f"URGENT: {a['citizen']} - {a['type']} (in {int(mins)} min)")