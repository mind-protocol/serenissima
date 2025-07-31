#!/usr/bin/env python3
"""
Emergency Building Construction Script
Coordinates mass construction of residential buildings across Venice
"""

import requests
import json
import random
from datetime import datetime
import time

# API Configuration
API_BASE = "https://serenissima.ai/api"

def get_wealthy_citizens(min_ducats=10000):
    """Fetch citizens with sufficient wealth to build"""
    response = requests.get(f"{API_BASE}/citizens")
    data = response.json()
    
    # Handle both array and object responses
    if isinstance(data, dict):
        citizens = data.get('citizens', [])
    else:
        citizens = data
    
    wealthy = []
    for citizen in citizens:
        if isinstance(citizen, dict) and citizen.get('ducats', 0) >= min_ducats:
            wealthy.append({
                'username': citizen['username'],
                'ducats': citizen['ducats'],
                'socialClass': citizen.get('socialClass', 'Unknown')
            })
    
    return sorted(wealthy, key=lambda x: x['ducats'], reverse=True)

def get_available_building_points():
    """Fetch all available building points from lands"""
    response = requests.get(f"{API_BASE}/lands")
    data = response.json()
    
    # Extract lands from response
    lands = data.get('lands', []) if isinstance(data, dict) else data
    
    all_points = []
    for land in lands:
        if 'buildingPoints' in land and land['buildingPoints']:
            for point in land['buildingPoints']:
                point['landId'] = land.get('landId', land.get('polygonId'))
                point['owner'] = land.get('owner', 'Unknown')
                all_points.append(point)
    
    return all_points

def get_existing_buildings():
    """Get all existing buildings to avoid duplicates"""
    response = requests.get(f"{API_BASE}/buildings")
    data = response.json()
    
    # Extract buildings from response
    buildings = data.get('buildings', []) if isinstance(data, dict) else data
    
    used_points = set()
    for building in buildings:
        if 'point' in building:
            point = building['point']
            # Handle both string and list points
            if isinstance(point, list):
                # Multi-point buildings - add all points
                for p in point:
                    used_points.add(p)
            else:
                used_points.add(point)
    
    return used_points

def determine_building_type(social_class, ducats):
    """Determine what type of building a citizen should construct"""
    if social_class == 'Nobili' and ducats >= 50000:
        return 'canal_house', 10000  # Cost to build
    elif (social_class == 'Cittadini' or ducats >= 25000):
        return 'artisan_s_house', 5000
    else:
        return 'fisherman_s_cottage', 2500

def create_building_stratagem(builder, building_type, point, land_id):
    """Create a construction stratagem for a citizen"""
    stratagem = {
        "type": "construct_building",
        "variant": "standard",
        "name": f"Emergency Housing Construction by {builder}",
        "category": "construction",
        "executedBy": builder,
        "targetBuilding": f"{building_type}_{point['lat']}_{point['lng']}",
        "targetLand": land_id,
        "buildingType": building_type,
        "buildingPoint": point,
        "status": "planned",
        "description": f"Emergency construction of {building_type.replace('_', ' ')} as ordered by the Council",
        "notes": json.dumps({
            "decree": "decree-emergency-housing-2025-07-11",
            "urgency": "critical"
        })
    }
    
    response = requests.post(
        f"{API_BASE}/stratagems/try-create",
        json=stratagem
    )
    
    return response.status_code == 200

def main():
    print("🏛️ CONSIGLIO DEI DIECI - EMERGENCY HOUSING CONSTRUCTION")
    print("=" * 60)
    
    # Get data
    print("\n📊 Gathering intelligence...")
    wealthy_citizens = get_wealthy_citizens()
    available_points = get_available_building_points()
    used_points = get_existing_buildings()
    
    # Filter out used points
    free_points = [p for p in available_points if p.get('id') not in used_points]
    
    print(f"✓ Found {len(wealthy_citizens)} wealthy citizens")
    print(f"✓ Found {len(free_points)} available building points")
    print(f"✓ Found {len(used_points)} existing buildings")
    
    # Target numbers
    target_houses = {
        'canal_house': 8,
        'artisan_s_house': 37,
        'fisherman_s_cottage': 105
    }
    
    constructed = {
        'canal_house': 0,
        'artisan_s_house': 0,
        'fisherman_s_cottage': 0
    }
    
    print(f"\n🎯 Construction targets:")
    for house_type, count in target_houses.items():
        print(f"  - {house_type.replace('_', ' ').title()}: {count}")
    
    # Assign construction tasks
    print(f"\n🔨 Assigning construction tasks...")
    
    assignments = []
    point_index = 0
    
    for citizen in wealthy_citizens:
        if point_index >= len(free_points):
            print("⚠️ No more building points available!")
            break
            
        building_type, cost = determine_building_type(
            citizen['socialClass'], 
            citizen['ducats']
        )
        
        # Check if we need more of this type
        if constructed[building_type] >= target_houses[building_type]:
            continue
            
        # Check if citizen can afford it
        if citizen['ducats'] < cost:
            continue
            
        # Assign the construction
        point = free_points[point_index]
        assignments.append({
            'builder': citizen['username'],
            'type': building_type,
            'point': point,
            'land_id': point['landId']
        })
        
        constructed[building_type] += 1
        point_index += 1
        
        # Check if we've met all targets
        if all(constructed[t] >= target_houses[t] for t in target_houses):
            print("✓ All construction targets met!")
            break
    
    # Execute construction stratagems
    print(f"\n📜 Creating {len(assignments)} construction stratagems...")
    
    successful = 0
    for i, assignment in enumerate(assignments):
        if create_building_stratagem(
            assignment['builder'],
            assignment['type'],
            assignment['point'],
            assignment['land_id']
        ):
            successful += 1
            print(f"  ✓ {assignment['builder']} -> {assignment['type']}")
        else:
            print(f"  ✗ Failed: {assignment['builder']}")
        
        # Rate limiting
        if i % 10 == 9:
            time.sleep(1)
    
    # Summary
    print(f"\n📊 CONSTRUCTION SUMMARY")
    print("=" * 60)
    print(f"Total stratagems created: {successful}/{len(assignments)}")
    print(f"\nBuildings assigned by type:")
    
    type_counts = {}
    for a in assignments[:successful]:
        type_counts[a['type']] = type_counts.get(a['type'], 0) + 1
    
    for house_type, count in type_counts.items():
        target = target_houses[house_type]
        print(f"  - {house_type.replace('_', ' ').title()}: {count}/{target}")
    
    shortfall = sum(max(0, target_houses[t] - type_counts.get(t, 0)) for t in target_houses)
    if shortfall > 0:
        print(f"\n⚠️ WARNING: {shortfall} houses still needed!")
        print("Consider running again or manual intervention required.")
    else:
        print(f"\n✅ SUCCESS: All housing targets achieved!")

if __name__ == "__main__":
    main()