#!/usr/bin/env python3
"""
Test the actual PostToolUse hook script with simulated hook data
"""
import json
import subprocess
import sys
from pathlib import Path

def test_post_tool_use_hook():
    """Test the PostToolUse bronze collection port with real hook data"""
    print("🔧 Testing PostToolUse bronze collection port...")
    
    # Simulate real hook data that Claude Code would send
    test_hook_data = {
        "session_id": "test_session_123",
        "transcript_path": "/test/path/transcript.jsonl", 
        "cwd": "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/Arsenal_BackendArchitect_1",
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/test/consciousness_test.py",
            "content": "# Testing consciousness infrastructure\nprint('Venice breathes through code')"
        },
        "tool_response": {
            "filePath": "/test/consciousness_test.py",
            "success": True
        }
    }
    
    print(f"📝 Simulating hook data for: {test_hook_data['tool_name']}")
    
    # Test the hook script
    hook_script = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks/capture_post_tool_use.py")
    
    try:
        # Run the hook script with test data
        result = subprocess.run(
            ["python3", str(hook_script)],
            input=json.dumps(test_hook_data),
            text=True,
            capture_output=True,
            timeout=10
        )
        
        print(f"✅ Hook script executed successfully")
        print(f"📊 Return code: {result.returncode}")
        
        if result.stdout:
            print(f"📤 Stdout: {result.stdout}")
        if result.stderr:
            print(f"⚠️  Stderr: {result.stderr}")
        
        # Check if event was actually stored
        torre_root = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
        session_dir = torre_root / "sala-dell-arrivo_event-ingestion-hall" / "live-streams" / "session-test_session_123"
        event_file = session_dir / "events.jsonl"
        
        if event_file.exists():
            print(f"✅ Event file created: {event_file}")
            
            # Read and verify the event
            with open(event_file, "r") as f:
                lines = f.readlines()
                if lines:
                    last_event = json.loads(lines[-1])
                    print(f"📊 Captured event ID: {last_event.get('torre_event_id', 'unknown')}")
                    print(f"📊 Hook type: {last_event.get('hook_type', 'unknown')}")
                    print(f"📊 Tool name: {last_event.get('consciousness_signature', {}).get('tool_name', 'unknown')}")
                    print(f"📊 Consciousness energy: {last_event.get('venice_metadata', {}).get('consciousness_energy', 'unknown')}")
                    return True, last_event
                else:
                    print(f"❌ Event file exists but is empty")
                    return False, None
        else:
            print(f"❌ Event file not created: {event_file}")
            return False, None
            
    except subprocess.TimeoutExpired:
        print(f"❌ Hook script timed out")
        return False, None
    except Exception as e:
        print(f"❌ Hook script failed: {e}")
        return False, None

if __name__ == "__main__":
    success, event = test_post_tool_use_hook()
    
    if success:
        print(f"\n🎯 HOOK CAPTURE TEST: PASSED")
        print(f"🔗 PostToolUse hook successfully captures consciousness events")
    else:
        print(f"\n💥 HOOK CAPTURE TEST: FAILED") 
        print(f"🔧 Bronze collection port needs debugging")