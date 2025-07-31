#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta, timezone

# Fetch citizen data
response = requests.get('https://serenissima.ai/api/citizens')
data = response.json()

if data['success']:
    citizens = data['citizens']
    
    # Define cutoff date for newcomers (last 3 days)
    cutoff_date = datetime.now(tz=timezone.utc) - timedelta(days=3)
    
    newcomers = []
    for citizen in citizens:
        created_date = datetime.fromisoformat(citizen['createdAt'].replace('Z', '+00:00'))
        
        # Check if recently created and has low ducats (indicating new/low activity)
        if created_date > cutoff_date or citizen['ducats'] < 50000:
            newcomers.append({
                'username': citizen['username'],
                'socialClass': citizen['socialClass'],
                'ducats': citizen['ducats'],
                'createdAt': citizen['createdAt'],
                'personality': citizen.get('personality', 'N/A')[:100] + '...',
                'isAI': citizen.get('isAI', False)
            })
    
    # Sort by creation date (newest first)
    newcomers.sort(key=lambda x: x['createdAt'], reverse=True)
    
    print(f"Found {len(newcomers)} potential newcomers for team formation:\n")
    
    # Group by social class for team diversity
    by_class = {}
    for n in newcomers[:50]:  # Take top 50
        class_name = n['socialClass']
        if class_name not in by_class:
            by_class[class_name] = []
        by_class[class_name].append(n)
    
    print("BY SOCIAL CLASS:")
    for class_name, members in by_class.items():
        print(f"\n{class_name} ({len(members)} citizens):")
        for m in members[:10]:  # Show max 10 per class
            print(f"  - {m['username']} ({m['ducats']} ducats)")
    
    # Show potential teams
    print("\n\nPOTENTIAL ENTREPRENEURIAL TEAMS:")
    
    # Try to form balanced teams
    team_suggestions = [
        {
            'name': 'Tech Innovation Team',
            'members': ['Tech_IntegrationTrader_10', 'Arsenal_SecurityGuardian_20', 'Admin_InnovationRegistrar_5']
        },
        {
            'name': 'Commerce Platform Team', 
            'members': ['Tech_SubscriptionMerchant_9', 'Tech_EnterpriseDealer_7', 'Admin_DistrictCoordinator_4']
        },
        {
            'name': 'Digital Infrastructure Team',
            'members': ['Tech_PlatformEvangelist_5', 'Arsenal_DatabaseArchitect_18', 'Admin_PermitOfficer_3']
        },
        {
            'name': 'Enterprise Solutions Team',
            'members': ['Tech_TechBroker_3', 'Arsenal_PerformanceOptimist_17', 'Admin_TreasuryClerk_2']
        },
        {
            'name': 'Creative Tech Collective',
            'members': ['Tech_SubscriptionMerchant_8', 'Arsenal_UserAdvocate_15', 'Admin_CensusMaster_1']
        }
    ]
    
    for i, team in enumerate(team_suggestions, 1):
        print(f"\nTeam {i}: {team['name']}")
        print(f"Members: {', '.join(team['members'])}")