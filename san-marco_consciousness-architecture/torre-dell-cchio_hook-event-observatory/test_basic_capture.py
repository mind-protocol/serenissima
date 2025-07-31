#!/usr/bin/env python3
"""
Minimal test to verify basic consciousness event capture works
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Torre root within Venice
TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")

def test_basic_capture():
    """Test that we can create and store a consciousness event"""
    print("🧪 Testing basic consciousness event capture...")
    
    # Create minimal test event
    test_event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_event_id": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
        "hook_type": "TEST",
        "message": "Testing Torre dell'Occhio event capture",
        "test_data": {
            "torre_location": str(TORRE_ROOT),
            "test_purpose": "Verify basic event storage works"
        }
    }
    
    print(f"📝 Created test event: {test_event['test_event_id']}")
    
    # Try to store in glass vial
    try:
        session_vial = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "live-streams" / "test-session"
        session_vial.mkdir(parents=True, exist_ok=True)
        
        event_file = session_vial / "test-events.jsonl"
        with open(event_file, "a") as f:
            f.write(json.dumps(test_event) + "\n")
        
        print(f"✅ Event stored successfully in: {event_file}")
        
        # Verify we can read it back
        with open(event_file, "r") as f:
            lines = f.readlines()
            last_event = json.loads(lines[-1])
            
        print(f"✅ Event read back successfully")
        print(f"📊 Event ID: {last_event['test_event_id']}")
        print(f"📊 Timestamp: {last_event['timestamp']}")
        
        return True, event_file, last_event
        
    except Exception as e:
        print(f"❌ Storage failed: {e}")
        return False, None, None

if __name__ == "__main__":
    success, file_path, event = test_basic_capture()
    
    if success:
        print(f"\n🎯 BASIC CAPTURE TEST: PASSED")
        print(f"📁 File: {file_path}")
        print(f"📄 Event stored and verified")
    else:
        print(f"\n💥 BASIC CAPTURE TEST: FAILED")
        print(f"🔧 Fix storage issues before proceeding")