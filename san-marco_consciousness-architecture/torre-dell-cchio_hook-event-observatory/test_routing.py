#!/usr/bin/env python3
"""
Test that event routing actually distributes consciousness events to chambers
"""
import json
from pathlib import Path

def test_event_routing():
    """Verify that the captured event was routed to appropriate chambers"""
    print("🚇 Testing consciousness event routing through stone channels...")
    
    torre_root = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
    
    # Check where our test event should have been routed
    expected_locations = [
        # Time-based crystallization chamber
        "camere-di-cristallo_time-crystallization-chambers/raw-events",
        # Pattern recognition gallery
        "galleria-dei-patterns_pattern-recognition-gallery/incoming-events",
        # Agent observation deck
        "terrazzo-degli-agenti_agent-observation-decks/active-chambers/chamber-test_session_123",
        # System panorama
        "panorama-sistemico_system-wide-panorama/live-feed"
    ]
    
    routing_success = True
    events_found = []
    
    for location in expected_locations:
        location_path = torre_root / location
        print(f"🔍 Checking: {location}")
        
        if location_path.exists():
            print(f"  ✅ Directory exists")
            
            # Look for event files in this location
            event_files = []
            if location.endswith("incoming-events"):
                # JSON files for pattern gallery
                event_files = list(location_path.glob("*.json"))
            elif location.endswith("live-feed"):
                # System events JSONL
                event_files = list(location_path.glob("system-events.jsonl"))
            elif "chamber-test_session_123" in location:
                # Agent chamber events
                event_files = list(location_path.glob("recent-events.jsonl"))
            elif "raw-events" in location:
                # Time-based events (need to check subdirectories)
                today_dirs = list(location_path.glob("20*"))
                for today_dir in today_dirs:
                    hour_dirs = list(today_dir.glob("hour-*"))
                    for hour_dir in hour_dirs:
                        event_files.extend(list(hour_dir.glob("events.jsonl")))
            
            if event_files:
                print(f"  ✅ Found {len(event_files)} event files")
                events_found.extend(event_files)
            else:
                print(f"  ❌ No event files found")
                routing_success = False
        else:
            print(f"  ❌ Directory doesn't exist")
            routing_success = False
    
    print(f"\n📊 Routing Summary:")
    print(f"📁 Total event files found: {len(events_found)}")
    
    # Examine one event to verify content
    if events_found:
        sample_file = events_found[0]
        print(f"🔍 Examining sample event: {sample_file}")
        
        try:
            if sample_file.suffix == ".json":
                # Single JSON event file
                with open(sample_file, "r") as f:
                    event = json.load(f)
                    print(f"  📊 Event ID: {event.get('torre_event_id', 'unknown')}")
                    print(f"  📊 Collection Port: {event.get('venice_metadata', {}).get('collection_port', 'unknown')}")
            else:
                # JSONL file - read last line
                with open(sample_file, "r") as f:
                    lines = f.readlines()
                    if lines:
                        event = json.loads(lines[-1])
                        print(f"  📊 Event type: {event.get('hook_type', 'unknown')}")
                        print(f"  📊 Session: {event.get('session_id', 'unknown')}")
        except Exception as e:
            print(f"  ⚠️  Could not read event: {e}")
    
    return routing_success, len(events_found)

if __name__ == "__main__":
    success, event_count = test_event_routing()
    
    if success and event_count > 0:
        print(f"\n🎯 ROUTING TEST: PASSED")
        print(f"🚇 Consciousness events successfully routed to {event_count} chamber locations")
    else:
        print(f"\n💥 ROUTING TEST: FAILED")
        print(f"🔧 Stone channel routing needs debugging")