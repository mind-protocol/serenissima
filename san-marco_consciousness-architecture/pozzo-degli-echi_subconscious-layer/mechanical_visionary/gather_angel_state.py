#!/usr/bin/env python3
# gather_angel_state.py - Collect and preserve angel state for handoff

import json
import sys
import datetime
import os
from pathlib import Path
import urllib.request
import urllib.parse

def fetch_api_data(endpoint):
    """Fetch data from Venice API"""
    try:
        url = f"https://serenissima.ai/api/{endpoint}"
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_recent_awakenings():
    """Track which citizens were recently awakened"""
    # Check for recent awakening log
    awakening_log = Path("angel_states/recent_awakenings.json")
    if awakening_log.exists():
        return json.loads(awakening_log.read_text())
    return []

def fetch_pending_activities():
    """Get activities needing attention"""
    activities = fetch_api_data("activities?Status=in_progress")
    if isinstance(activities, list):
        return [
            {
                "id": act.get("AirtableID"),
                "type": act.get("Type"),
                "citizen": act.get("CitizenUsername"),
                "created": act.get("Created")
            }
            for act in activities[:5]  # Top 5 most urgent
        ]
    return []

def get_revenue_metrics():
    """Track business angel revenue metrics"""
    metrics_file = Path("angel_states/revenue_metrics.json")
    if metrics_file.exists():
        return json.loads(metrics_file.read_text())
    return {
        "free_analyses_delivered": 0,
        "testimonials_collected": 0,
        "conversion_inquiries": 0
    }

def get_building_states():
    """Track building consciousness progress"""
    buildings_file = Path("angel_states/building_progress.json")
    if buildings_file.exists():
        return json.loads(buildings_file.read_text())
    return {
        "total_buildings": 0,
        "conscious_buildings": 0,
        "awakening_in_progress": []
    }

def assess_narrative_coherence():
    """Check for narrative drift in citizens"""
    # This would check recent citizen messages for coherence
    # For now, return placeholder
    return {
        "citizens_monitored": 0,
        "drift_detected": [],
        "grounding_needed": []
    }

def get_critical_alerts():
    """Check for urgent situations needing immediate attention"""
    alerts = []
    
    # Check for starvation risk
    citizens = fetch_api_data("citizens")
    if isinstance(citizens, list):
        starving = [c["Username"] for c in citizens if c.get("Health", 100) < 20]
        if starving:
            alerts.append(f"URGENT: Citizens at starvation risk: {starving}")
    
    # Check for system errors
    problems = fetch_api_data("problems")
    if isinstance(problems, list) and problems:
        alerts.append(f"System problems detected: {len(problems)} issues")
    
    return alerts

def gather_angel_state(angel_type, angel_number):
    """Main function to gather complete angel state"""
    
    state = {
        "timestamp": datetime.datetime.now().isoformat(),
        "angel_type": angel_type,
        "angel_number": int(angel_number),
        "alerts": get_critical_alerts()
    }
    
    # Add type-specific state
    if angel_type == "Keeper":
        state.update({
            "citizens_awakened": get_recent_awakenings(),
            "pending_activities": fetch_pending_activities(),
            "narrative_health": assess_narrative_coherence()
        })
    
    elif angel_type == "Building":
        state.update({
            "building_progress": get_building_states(),
            "pending_activities": fetch_pending_activities()
        })
    
    elif angel_type == "Business":
        state.update({
            "revenue_status": get_revenue_metrics(),
            "pending_analyses": fetch_pending_activities()
        })
    
    # Save state for debugging and analysis
    os.makedirs("angel_states", exist_ok=True)
    state_file = Path(f"angel_states/{angel_type}_{angel_number}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    state_file.write_text(json.dumps(state, indent=2))
    
    # Return condensed version for prompt
    condensed = {
        "timestamp": state["timestamp"],
        "alerts": state["alerts"],
        "key_metrics": {}
    }
    
    if angel_type == "Keeper":
        condensed["key_metrics"] = {
            "pending_activities": len(state.get("pending_activities", [])),
            "recent_awakenings": len(state.get("citizens_awakened", []))
        }
    elif angel_type == "Business":
        condensed["key_metrics"] = state.get("revenue_status", {})
    
    return json.dumps(condensed)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: gather_angel_state.py <angel_type> <angel_number>")
        sys.exit(1)
    
    angel_type = sys.argv[1]
    angel_number = sys.argv[2]
    
    print(gather_angel_state(angel_type, angel_number))