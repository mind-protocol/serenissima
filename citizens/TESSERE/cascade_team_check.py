import json
import subprocess

# CASCADE core team members
cascade_team = [
    'TechnoMedici',
    'mechanical_visionary', 
    'element_transmuter',
    'diplomatic_virtuoso',
    'Italia',
    'Foscari_Banker',
    'divine_economist',
    'network_weaver',
    'system_diagnostician',
    'market_prophet',
    'pattern_prophet',
    'living_stone_architect',
    'social_geometrist',
    'MerchantPrince'
]

# Get current activities
result = subprocess.run(['curl', '-s', 'https://serenissima.ai/api/activities?Status=created'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)
activities = data.get('activities', [])

print("🚀 CASCADE TEAM STATUS CHECK\n")

# Find CASCADE team activities
team_activities = []
for a in activities:
    if a['citizen'] in cascade_team:
        team_activities.append(a)

print(f"CASCADE team members with pending activities: {len(team_activities)}")
print("\nTeam member status:")

for a in team_activities:
    print(f"- {a['citizen']}: {a['type']}")

# Check who's missing
active_members = [a['citizen'] for a in team_activities]
missing = [m for m in cascade_team if m not in active_members]

print(f"\nCASCADE members without pending activities: {len(missing)}")
for m in missing:
    print(f"- {m}")