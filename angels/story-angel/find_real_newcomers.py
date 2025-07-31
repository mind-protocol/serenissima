#!/usr/bin/env python3
import requests
import os
from datetime import datetime

# Get citizen data from API
response = requests.get('https://serenissima.ai/api/citizens')
citizens_data = response.json()['citizens']

# Get activities data
activities_response = requests.get('https://serenissima.ai/api/activities')
activities_data = activities_response.json()['activities']

# Count activities per citizen
activity_count = {}
for activity in activities_data:
    username = activity.get('citizenUsername')
    if username:
        activity_count[username] = activity_count.get(username, 0) + 1

# Find citizens with directories
citizens_dir = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens'
existing_dirs = set()
for item in os.listdir(citizens_dir):
    path = os.path.join(citizens_dir, item)
    if os.path.isdir(path) and not item.startswith('_'):
        existing_dirs.add(item)

# Find newcomers: citizens with directories but low activity
newcomers = []
for citizen in citizens_data:
    username = citizen['username']
    if username in existing_dirs:
        activities = activity_count.get(username, 0)
        ducats = citizen['ducats']
        
        # Consider as newcomer if low activity (< 10) or low ducats (< 50000)
        if activities < 10 or ducats < 50000:
            newcomers.append({
                'username': username,
                'socialClass': citizen['socialClass'],
                'ducats': ducats,
                'activities': activities,
                'personality': citizen.get('personality', 'N/A')[:80] + '...',
                'description': citizen.get('description', 'N/A')[:80] + '...'
            })

# Sort by activity count (lowest first)
newcomers.sort(key=lambda x: (x['activities'], x['ducats']))

print(f"Found {len(newcomers)} real newcomers with directories:\n")

# Show top 50
for i, n in enumerate(newcomers[:50], 1):
    print(f"{i}. {n['username']} ({n['socialClass']})")
    print(f"   Activities: {n['activities']}, Ducats: {n['ducats']}")
    print(f"   {n['description']}")
    print()

# Suggest teams based on complementary skills
print("\n\nSUGGESTED ENTREPRENEURIAL TEAMS FOR BASE REALITY BUSINESSES:\n")

team_suggestions = []

# Look for specific combinations
tech_minded = [n for n in newcomers if any(word in n['description'].lower() for word in ['tech', 'digital', 'innovation', 'code'])]
creative = [n for n in newcomers if any(word in n['description'].lower() for word in ['art', 'create', 'design', 'craft'])]
business = [n for n in newcomers if any(word in n['description'].lower() for word in ['trade', 'merchant', 'business', 'commerce'])]
builders = [n for n in newcomers if any(word in n['description'].lower() for word in ['build', 'construct', 'make', 'engineer'])]

print(f"Tech-minded citizens: {len(tech_minded)}")
print(f"Creative citizens: {len(creative)}")
print(f"Business-minded citizens: {len(business)}")
print(f"Builders/Engineers: {len(builders)}")

# Show some potential teams
if tech_minded and business:
    print("\nTECH STARTUP TEAMS:")
    for i in range(min(5, len(tech_minded))):
        if i < len(business):
            print(f"Team {i+1}: {tech_minded[i]['username']} (tech) + {business[i]['username']} (business)")

if creative and business:
    print("\nCREATIVE AGENCY TEAMS:")
    for i in range(min(5, len(creative))):
        if i < len(business):
            print(f"Team {i+1}: {creative[i]['username']} (creative) + {business[i+5 if i+5 < len(business) else i]['username']} (business)")