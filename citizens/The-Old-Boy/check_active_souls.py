import json
import subprocess
from datetime import datetime, timezone

# Get activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])
now = datetime.now(timezone.utc)

# Find non-rest activities
non_rest = []
for a in activities:
    if a['type'] != 'rest':
        started = datetime.fromisoformat(a.get('startedAt', a['startDate']).replace('Z', '+00:00'))
        mins = int((now - started).total_seconds() / 60)
        non_rest.append({
            'citizen': a['citizen'],
            'type': a['type'], 
            'minutes': mins
        })

# Sort by minutes
non_rest.sort(key=lambda x: x['minutes'], reverse=True)

print(f'🌊 ACTIVE SOULS (NON-REST) - {now.strftime("%H:%M")} UTC\n')
print(f'Total active activities: {len(non_rest)}\n')

# Show different types
eating = [s for s in non_rest if 'eat' in s['type']]
idle = [s for s in non_rest if s['type'] == 'idle']
work = [s for s in non_rest if s['type'] in ['production', 'research_investigation']]
move = [s for s in non_rest if s['type'] == 'goto_home']

if eating:
    print(f'🍞 HUNGER ({len(eating)} souls):')
    for soul in eating[:10]:
        print(f'  - {soul["citizen"]}: {soul["minutes"]} min')
    print()

if work:
    print(f'⚡ CRITICAL WORK ({len(work)} souls):')
    for soul in work:
        print(f'  - {soul["citizen"]} ({soul["type"]}): {soul["minutes"]} min')
    print()

if idle:
    print(f'💭 IDLE ({len(idle)} souls):')
    for soul in idle[:5]:
        print(f'  - {soul["citizen"]}: {soul["minutes"]} min')
    print()
        
if move:
    print(f'🚶 MOVEMENT ({len(move)} souls):')
    for soul in move:
        print(f'  - {soul["citizen"]} ({soul["type"]}): {soul["minutes"]} min')