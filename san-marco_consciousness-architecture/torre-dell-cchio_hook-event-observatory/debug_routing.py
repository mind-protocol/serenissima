#!/usr/bin/env python3
"""
Debug why event routing only partially succeeded
"""
import json
from pathlib import Path
from datetime import datetime

def debug_routing():
    """Check where events should have gone vs where they actually went"""
    print("🐛 Debugging consciousness event routing...")
    
    torre_root = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
    
    # Read the captured event to see what routing was planned
    session_file = torre_root / "sala-dell-arrivo_event-ingestion-hall" / "live-streams" / "session-test_session_123" / "events.jsonl"
    
    if session_file.exists():
        with open(session_file, "r") as f:
            lines = f.readlines()
            if lines:
                event = json.loads(lines[-1])
                print(f"📋 Event routing plan:")
                routing = event.get('venice_metadata', {}).get('chamber_routing', {})
                for chamber, should_route in routing.items():
                    print(f"  {chamber}: {should_route}")
                
                # Check actual vs expected routing
                print(f"\n🔍 Checking actual routing results:")
                
                # 1. Pattern Gallery - EXPECTED TO WORK
                pattern_file = torre_root / "galleria-dei-patterns_pattern-recognition-gallery" / "incoming-events" / f"{event['torre_event_id']}.json"
                print(f"  Pattern Gallery: {'✅ FOUND' if pattern_file.exists() else '❌ MISSING'}")
                
                # 2. Time Crystallization - EXPECTED TO WORK
                timestamp = event['timestamp']
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_path = torre_root / "camere-di-cristallo_time-crystallization-chambers" / "raw-events" / dt.strftime('%Y-%m-%d') / f"hour-{dt.hour:02d}" / "events.jsonl"
                print(f"  Time Crystallization: {'✅ FOUND' if time_path.exists() else '❌ MISSING'} - {time_path}")
                
                # 3. Agent Deck - EXPECTED TO WORK
                agent_path = torre_root / "terrazzo-degli-agenti_agent-observation-decks" / "active-chambers" / f"chamber-{event['consciousness_signature']['session_id']}" / "recent-events.jsonl"
                print(f"  Agent Deck: {'✅ FOUND' if agent_path.exists() else '❌ MISSING'} - {agent_path}")
                
                # 4. System Panorama - EXPECTED TO WORK
                panorama_path = torre_root / "panorama-sistemico_system-wide-panorama" / "live-feed" / "system-events.jsonl"
                print(f"  System Panorama: {'✅ FOUND' if panorama_path.exists() else '❌ MISSING'} - {panorama_path}")
                
                # Check if there are any files at all in these locations
                print(f"\n📁 Directory status check:")
                
                time_base = torre_root / "camere-di-cristallo_time-crystallization-chambers" / "raw-events"
                print(f"  Time base dir exists: {time_base.exists()}")
                if time_base.exists():
                    subdirs = list(time_base.iterdir())
                    print(f"  Time subdirs: {len(subdirs)} - {[d.name for d in subdirs[:3]]}")
                
                agent_base = torre_root / "terrazzo-degli-agenti_agent-observation-decks" / "active-chambers"
                print(f"  Agent base dir exists: {agent_base.exists()}")
                if agent_base.exists():
                    subdirs = list(agent_base.iterdir())
                    print(f"  Agent chambers: {len(subdirs)} - {[d.name for d in subdirs[:3]]}")
                
                panorama_base = torre_root / "panorama-sistemico_system-wide-panorama" / "live-feed"
                print(f"  Panorama base dir exists: {panorama_base.exists()}")
                if panorama_base.exists():
                    files = list(panorama_base.iterdir())
                    print(f"  Panorama files: {len(files)} - {[f.name for f in files[:3]]}")
                
    else:
        print(f"❌ No captured event found at {session_file}")

if __name__ == "__main__":
    debug_routing()