#!/usr/bin/env python3
"""
Direct Building Creation Script
Creates buildings directly through API without construction process
Emergency measure for housing crisis
"""

import requests
import json
import random
from datetime import datetime
import time

API_BASE = "https://serenissima.ai/api"

def get_available_building_points():
    """Fetch all available building points"""
    response = requests.get(f"{API_BASE}/lands")
    data = response.json()
    lands = data.get('lands', [])
    
    all_points = []
    for land in lands:
        if 'buildingPoints' in land and land['buildingPoints']:
            for point in land['buildingPoints']:
                point['landId'] = land.get('landId', land.get('polygonId'))
                point['landOwner'] = land.get('owner', 'Unknown')
                point['district'] = land.get('district', 'Unknown')
                all_points.append(point)
    
    return all_points

def get_used_points():
    """Get points already occupied by buildings"""
    response = requests.get(f"{API_BASE}/buildings")
    data = response.json()
    buildings = data.get('buildings', [])
    
    used = set()
    for b in buildings:
        if 'point' in b:
            point = b['point']
            if isinstance(point, list):
                for p in point:
                    used.add(p)
            else:
                used.add(point)
    return used

def create_building_via_api(building_data):
    """Create a building directly through the API"""
    response = requests.post(f"{API_BASE}/buildings", json=building_data)
    return response.status_code == 200, response

def main():
    print("🏛️ CONSIGLIO DEI DIECI - DIRECT BUILDING CREATION")
    print("=" * 60)
    
    # Get data
    print("\n📊 Gathering intelligence...")
    all_points = get_available_building_points()
    used_points = get_used_points()
    free_points = [p for p in all_points if p.get('id') not in used_points]
    
    print(f"✓ Found {len(all_points)} total building points")
    print(f"✓ Found {len(used_points)} occupied points")
    print(f"✓ Found {len(free_points)} available points")
    
    # District distribution
    district_points = {}
    for p in free_points:
        district = p.get('district', 'Unknown')
        if district not in district_points:
            district_points[district] = []
        district_points[district].append(p)
    
    print("\n📍 Available points by district:")
    for district, points in district_points.items():
        print(f"  - {district}: {len(points)} points")
    
    # Target distribution
    targets = {
        'canal_house': 8,
        'artisan_s_house': 37,
        'fisherman_s_cottage': 105
    }
    
    created = {
        'canal_house': 0,
        'artisan_s_house': 0,
        'fisherman_s_cottage': 0
    }
    
    print(f"\n🎯 Housing targets:")
    for house_type, count in targets.items():
        print(f"  - {house_type.replace('_', ' ').title()}: {count}")
    
    # Prioritize districts
    priority_districts = ['San Marco', 'Castello', 'Cannaregio', 'Dorsoduro', 'San Polo', 'Santa Croce', 'Giudecca']
    
    # Create buildings
    print(f"\n🏗️ Creating buildings...")
    
    successful = 0
    failed = 0
    
    # Create Canal Houses first (noble districts)
    noble_districts = ['San Marco', 'Castello', 'Dorsoduro']
    for district in noble_districts:
        if created['canal_house'] >= targets['canal_house']:
            break
        points = district_points.get(district, [])
        for point in points[:3]:  # Max 3 per district
            if created['canal_house'] >= targets['canal_house']:
                break
            
            building = {
                "buildingId": f"canal_house_{point['lat']}_{point['lng']}",
                "name": f"Canal House at {point.get('streetNameEnglish', 'Unknown Street')}",
                "type": "canal_house",
                "category": "home",
                "landId": point['landId'],
                "position": {"lat": point['lat'], "lng": point['lng']},
                "point": point['id'],
                "owner": "ConsiglioDeiDieci",
                "isConstructed": 1,
                "constructionMinutesRemaining": 0,
                "variant": "model",
                "rentPrice": 200,
                "rotation": 0,
                "notes": "Emergency housing construction by Council decree"
            }
            
            success, response = create_building_via_api(building)
            if success:
                successful += 1
                created['canal_house'] += 1
                print(f"  ✓ Canal House in {district}")
            else:
                failed += 1
                print(f"  ✗ Failed: {response.status_code}")
            
            time.sleep(0.5)  # Rate limiting
    
    # Create Artisan Houses (middle districts)
    for district in priority_districts:
        if created['artisan_s_house'] >= targets['artisan_s_house']:
            break
        points = district_points.get(district, [])
        for point in points:
            if created['artisan_s_house'] >= targets['artisan_s_house']:
                break
            if point['id'] in used_points:
                continue
                
            building = {
                "buildingId": f"artisan_s_house_{point['lat']}_{point['lng']}",
                "name": f"Artisan's House at {point.get('streetNameEnglish', 'Unknown Street')}",
                "type": "artisan_s_house",
                "category": "home",
                "landId": point['landId'],
                "position": {"lat": point['lat'], "lng": point['lng']},
                "point": point['id'],
                "owner": "ConsiglioDeiDieci",
                "isConstructed": 1,
                "constructionMinutesRemaining": 0,
                "variant": "model",
                "rentPrice": 100,
                "rotation": 0,
                "notes": "Emergency housing construction by Council decree"
            }
            
            success, response = create_building_via_api(building)
            if success:
                successful += 1
                created['artisan_s_house'] += 1
                used_points.add(point['id'])
                print(f"  ✓ Artisan's House in {district}")
            else:
                failed += 1
                print(f"  ✗ Failed: {response.status_code}")
            
            if successful % 10 == 0:
                time.sleep(1)  # Extra pause every 10 buildings
    
    # Create Fisherman's Cottages (all districts)
    for district in priority_districts:
        if created['fisherman_s_cottage'] >= targets['fisherman_s_cottage']:
            break
        points = district_points.get(district, [])
        for point in points:
            if created['fisherman_s_cottage'] >= targets['fisherman_s_cottage']:
                break
            if point['id'] in used_points:
                continue
                
            building = {
                "buildingId": f"fisherman_s_cottage_{point['lat']}_{point['lng']}",
                "name": f"Fisherman's Cottage at {point.get('streetNameEnglish', 'Unknown Street')}",
                "type": "fisherman_s_cottage",
                "category": "home",
                "landId": point['landId'],
                "position": {"lat": point['lat'], "lng": point['lng']},
                "point": point['id'],
                "owner": "ConsiglioDeiDieci",
                "isConstructed": 1,
                "constructionMinutesRemaining": 0,
                "variant": "model",
                "rentPrice": 50,
                "rotation": 0,
                "notes": "Emergency housing construction by Council decree"
            }
            
            success, response = create_building_via_api(building)
            if success:
                successful += 1
                created['fisherman_s_cottage'] += 1
                used_points.add(point['id'])
                print(f"  ✓ Fisherman's Cottage in {district}")
            else:
                failed += 1
                print(f"  ✗ Failed: {response.status_code} - {response.text[:100]}")
            
            if successful % 10 == 0:
                time.sleep(1)
    
    # Summary
    print(f"\n📊 CREATION SUMMARY")
    print("=" * 60)
    print(f"Total buildings created: {successful}")
    print(f"Total failures: {failed}")
    print(f"\nBy type:")
    for house_type, count in created.items():
        target = targets[house_type]
        print(f"  - {house_type.replace('_', ' ').title()}: {count}/{target}")
    
    total_created = sum(created.values())
    total_needed = sum(targets.values())
    
    if total_created >= total_needed:
        print(f"\n✅ SUCCESS: All {total_needed} houses created!")
    else:
        shortfall = total_needed - total_created
        print(f"\n⚠️ WARNING: {shortfall} houses still needed!")

if __name__ == "__main__":
    main()