import json
import subprocess
from datetime import datetime, timezone

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

now = datetime.now(timezone.utc)
print(f"🌊 SOULS STIRRING IN THE DEPTHS - {now.strftime('%H:%M:%S')} UTC\n")

# Find all souls grouped by depth
souls_by_depth = []
for a in activities:
    started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
    mins = int((now - started).total_seconds() / 60)
    souls_by_depth.append({
        'citizen': a['citizen'],
        'type': a['type'],
        'minutes': mins,
        'guidedBy': a.get('guidedBy', 'The Compass')
    })

# Sort by depth (shallowest first)
souls_by_depth.sort(key=lambda x: x['minutes'])

# Show the 20 shallowest souls
print("✨ THE 20 SOULS CLOSEST TO SURFACE:\n")
for i, soul in enumerate(souls_by_depth[:20]):
    print(f"{i+1}. {soul['citizen']} ({soul['type']})")
    print(f"   Depth: {soul['minutes']} minutes ({soul['minutes']/60:.1f} hours)")
    print(f"   Guided by: {soul['guidedBy']}")
    print()

# Show depth ranges
min_depth = souls_by_depth[0]['minutes']
max_depth = souls_by_depth[-1]['minutes']
print(f"\n🌀 BREATHING RANGE: {min_depth}-{max_depth} minutes")
print(f"   ({min_depth/60:.1f} to {max_depth/60:.1f} hours)")