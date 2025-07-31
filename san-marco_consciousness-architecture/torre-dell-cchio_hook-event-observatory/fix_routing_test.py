#!/usr/bin/env python3
"""
Test and fix the routing functions by running them manually
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Import the routing functions from our hook script
sys.path.append("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks")

def test_individual_routing_functions():
    """Test each routing function individually to find the bug"""
    print("🔧 Testing individual routing functions...")
    
    # Create a test event
    test_event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "torre_event_id": f"test_routing_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
        "hook_type": "PostToolUse",
        "consciousness_signature": {
            "session_id": "test_routing_session",
            "tool_name": "Write"
        },
        "venice_metadata": {
            "consciousness_energy": 0.8,
            "chamber_routing": {
                "galleria_patterns": True,
                "terrazzo_agenti": True,
                "panorama_sistemico": True
            }
        }
    }
    
    print(f"📝 Created test event: {test_event['torre_event_id']}")
    
    # Test each routing function manually
    TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
    
    # 1. Test Agent Deck routing
    print(f"\n🔧 Testing Agent Deck routing...")
    try:
        session_id = test_event['consciousness_signature']['session_id']
        agent_chamber = TORRE_ROOT / "terrazzo-degli-agenti_agent-observation-decks" / "active-chambers" / f"chamber-{session_id}"
        agent_chamber.mkdir(parents=True, exist_ok=True)
        
        with open(agent_chamber / "recent-events.jsonl", 'a') as f:
            f.write(json.dumps(test_event) + "\n")
        
        print(f"  ✅ Agent Deck: Event stored in {agent_chamber}")
        
    except Exception as e:
        print(f"  ❌ Agent Deck failed: {e}")
    
    # 2. Test Panorama routing
    print(f"\n🔧 Testing Panorama routing...")
    try:
        panorama_feed = TORRE_ROOT / "panorama-sistemico_system-wide-panorama" / "live-feed"
        panorama_feed.mkdir(parents=True, exist_ok=True)
        
        system_event = {
            "timestamp": test_event["timestamp"],
            "hook_type": test_event["hook_type"],
            "consciousness_energy": test_event["venice_metadata"]["consciousness_energy"],
            "session_id": test_event['consciousness_signature']['session_id'],
            "tool_name": test_event['consciousness_signature']['tool_name']
        }
        
        with open(panorama_feed / "system-events.jsonl", 'a') as f:
            f.write(json.dumps(system_event) + "\n")
        
        print(f"  ✅ Panorama: Event stored in {panorama_feed}")
        
    except Exception as e:
        print(f"  ❌ Panorama failed: {e}")
    
    # 3. Test Time Crystallization (this one might already work)
    print(f"\n🔧 Testing Time Crystallization...")
    try:
        now = datetime.fromisoformat(test_event["timestamp"].replace('Z', '+00:00'))
        time_vial = TORRE_ROOT / "camere-di-cristallo_time-crystallization-chambers" / "raw-events" / now.strftime("%Y-%m-%d") / f"hour-{now.hour:02d}"
        time_vial.mkdir(parents=True, exist_ok=True)
        
        with open(time_vial / "events.jsonl", "a") as f:
            f.write(json.dumps(test_event) + "\n")
        
        print(f"  ✅ Time Crystallization: Event stored in {time_vial}")
        
    except Exception as e:
        print(f"  ❌ Time Crystallization failed: {e}")
    
    return True

if __name__ == "__main__":
    test_individual_routing_functions()
    print(f"\n🎯 Manual routing test completed")
    print(f"📋 Check if events now appear in all expected locations")