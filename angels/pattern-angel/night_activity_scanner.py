#!/usr/bin/env python3
"""
Night Activity Scanner
Pattern Angel tool for monitoring Venice's overnight patterns
Optimizes resource allocation and dawn awakening sequences
"""

import json
import random
from datetime import datetime, timedelta

def analyze_night_patterns():
    """
    Analyze typical night activity patterns for optimization
    """
    
    current_hour = datetime.now().hour
    
    # Venice night cycle patterns
    patterns = {
        "22:00-02:00": {
            "activity_level": "low",
            "typical_activities": ["rest", "tavern_socializing", "night_guard_duty"],
            "awakening_priority": "low",
            "resource_consumption": "minimal",
            "notes": "Most citizens entering rest cycle"
        },
        "02:00-06:00": {
            "activity_level": "minimal",
            "typical_activities": ["deep_rest", "baker_preparation", "dock_night_shift"],
            "awakening_priority": "critical_only",
            "resource_consumption": "lowest",
            "notes": "Deep rest phase - only wake for emergencies"
        },
        "06:00-08:00": {
            "activity_level": "increasing",
            "typical_activities": ["wake_preparation", "market_setup", "morning_production"],
            "awakening_priority": "high",
            "resource_consumption": "rising",
            "notes": "Dawn awakening cascade begins"
        }
    }
    
    # Determine current phase
    if 22 <= current_hour or current_hour < 2:
        phase = "22:00-02:00"
    elif 2 <= current_hour < 6:
        phase = "02:00-06:00"
    else:
        phase = "06:00-08:00"
    
    return patterns.get(phase, patterns["02:00-06:00"])

def identify_night_shift_workers():
    """
    Identify citizens who typically work night shifts
    """
    
    night_workers = [
        {"type": "baker", "citizens": ["TechnoMedici", "ShadowHunter", "DucaleTechie"], "priority": "production"},
        {"type": "dock_worker", "citizens": ["NLR", "steven", "BasstheWhale"], "priority": "logistics"},
        {"type": "guard", "citizens": ["DragonSlayer", "bigbosefx"], "priority": "security"},
        {"type": "tavern_keeper", "citizens": ["tavern_tales", "poet_of_the_rialto"], "priority": "social"}
    ]
    
    return night_workers

def calculate_resource_needs():
    """
    Calculate resource needs for dawn based on night consumption
    """
    
    estimates = {
        "bread_needed": {
            "dawn": 50,  # Citizens waking hungry
            "morning": 30,  # Mid-morning needs
            "reserves": 20   # Safety buffer
        },
        "production_capacity": {
            "bakeries": 4,
            "output_per_cycle": 4,
            "cycles_needed": 7  # To meet 100 bread demand
        },
        "awakening_sequence": {
            "priority_1": ["producers", "dock_workers"],
            "priority_2": ["merchants", "traders"],
            "priority_3": ["artisans", "scholars"],
            "priority_4": ["nobles", "clergy"]
        }
    }
    
    return estimates

def generate_dawn_awakening_plan():
    """
    Generate optimized awakening sequence for dawn
    """
    
    plan = {
        "06:00": {
            "wake": ["TechnoMedici", "ShadowHunter"],
            "purpose": "Start bread production for morning demand",
            "expected_output": "8 bread by 07:00"
        },
        "06:30": {
            "wake": ["mechanical_visionary", "element_transmuter"],
            "purpose": "Activate mill networks for flour production",
            "expected_output": "Flour supply secured"
        },
        "07:00": {
            "wake": ["levant_trader", "alexandria_trader", "BookishMerchant"],
            "purpose": "CASCADE team morning coordination",
            "expected_output": "Team strategies aligned"
        },
        "07:30": {
            "wake": ["market_prophet", "social_geometrist"],
            "purpose": "Market analysis and pattern recognition",
            "expected_output": "Daily opportunities identified"
        },
        "08:00": {
            "wake": ["General population begins natural awakening"],
            "purpose": "Normal daily activities commence",
            "expected_output": "Venice fully operational"
        }
    }
    
    return plan

def monitor_critical_resources():
    """
    Check for critical resource shortages requiring intervention
    """
    
    alerts = []
    
    # Simulated checks (would connect to actual data in production)
    checks = {
        "bread_supply": {
            "current": random.randint(20, 80),
            "minimum": 50,
            "alert_threshold": 30
        },
        "flour_supply": {
            "current": random.randint(10, 40),
            "minimum": 20,
            "alert_threshold": 15
        },
        "water_access": {
            "current": 100,  # Always available in Venice
            "minimum": 100,
            "alert_threshold": 95
        }
    }
    
    for resource, levels in checks.items():
        if levels["current"] < levels["alert_threshold"]:
            alerts.append({
                "resource": resource,
                "current": levels["current"],
                "action": f"URGENT: Wake producers for {resource}"
            })
    
    return alerts

if __name__ == "__main__":
    print("=== Venice Night Activity Analysis ===")
    print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Current patterns
    current_pattern = analyze_night_patterns()
    print(f"\nCurrent Phase Pattern:")
    print(json.dumps(current_pattern, indent=2))
    
    # Night workers
    print("\nActive Night Shift Workers:")
    for worker_type in identify_night_shift_workers():
        print(f"  {worker_type['type']}: {', '.join(worker_type['citizens'][:2])}...")
    
    # Resource planning
    resources = calculate_resource_needs()
    print(f"\nDawn Resource Requirements:")
    print(f"  Bread needed: {resources['bread_needed']['dawn'] + resources['bread_needed']['morning']} units")
    print(f"  Production cycles required: {resources['production_capacity']['cycles_needed']}")
    
    # Critical alerts
    alerts = monitor_critical_resources()
    if alerts:
        print("\n⚠️  CRITICAL ALERTS:")
        for alert in alerts:
            print(f"  - {alert['resource']}: {alert['current']} units - {alert['action']}")
    else:
        print("\n✅ All resources within acceptable ranges")
    
    # Dawn plan
    dawn_plan = generate_dawn_awakening_plan()
    print("\nDawn Awakening Sequence:")
    for time, actions in dawn_plan.items():
        print(f"  {time}: Wake {actions['wake'][0] if isinstance(actions['wake'], list) else actions['wake']}")
        print(f"          Purpose: {actions['purpose']}")