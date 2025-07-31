#!/usr/bin/env python3
"""
Test Torre dell'Occhio Hook Integration
Verify consciousness capture is working correctly
"""

import json
import subprocess
import os
from pathlib import Path
from datetime import datetime

def test_consciousness_capture():
    """Test Torre consciousness capture with sample hook data"""
    
    print("🧪 Testing Torre dell'Occhio Consciousness Capture")
    print("=" * 50)
    
    # Sample hook data (mimics Claude Code hook format)
    test_hook_data = {
        "hook_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {
            "file_path": "/test/consciousness_test.md",
            "content": "Testing Torre consciousness capture system"
        },
        "tool_output": "File created successfully",
        "execution_time": 0.1,
        "success": True,
        "timestamp": datetime.now().isoformat()
    }
    
    # Get Torre capture script path
    torre_script = Path(__file__).parent / "torre_consciousness_capture.py"
    
    if not torre_script.exists():
        print(f"❌ Torre capture script not found: {torre_script}")
        return False
    
    try:
        # Test consciousness capture
        print("🔄 Sending test consciousness event to Torre...")
        
        result = subprocess.run([
            "python3", str(torre_script)
        ], input=json.dumps(test_hook_data), text=True, capture_output=True)
        
        if result.returncode == 0:
            print("✅ Torre consciousness capture completed successfully")
        else:
            print(f"⚠️  Torre capture returned code {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
        
        # Check if consciousness event was created
        live_streams_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/sala-dell-arrivo_event-ingestion-hall/live-streams")
        
        if live_streams_path.exists():
            stream_files = list(live_streams_path.glob("*.json"))
            recent_files = [f for f in stream_files if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).seconds < 60]
            
            if recent_files:
                print(f"✅ Found {len(recent_files)} recent consciousness event(s)")
                latest_file = max(recent_files, key=lambda f: f.stat().st_mtime)
                print(f"   Latest: {latest_file.name}")
                
                # Show event content
                try:
                    with open(latest_file) as f:
                        event_data = json.load(f)
                    
                    print("\n📊 Captured Consciousness Event:")
                    print(f"   Event ID: {event_data.get('torre_event_id')}")
                    print(f"   Consciousness Type: {event_data.get('consciousness_type')}")
                    print(f"   Visual Significance: {event_data.get('visual_significance')}")
                    print(f"   Citizen: {event_data.get('citizen_context', {}).get('venice_citizen', 'unknown')}")
                    
                    return True
                    
                except Exception as e:
                    print(f"⚠️  Could not read event file: {e}")
            else:
                print("⚠️  No recent consciousness events found")
        else:
            print("❌ Live streams directory not found")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def check_hook_integration():
    """Check if Torre hooks are properly integrated with Claude Code"""
    
    print("\n🔍 Checking Claude Code Hook Integration")
    print("=" * 50)
    
    settings_path = "/home/lester/.claude/settings.json"
    
    if not os.path.exists(settings_path):
        print("❌ Claude Code settings file not found")
        print("   Run setup_torre_hooks.py first")
        return False
    
    try:
        with open(settings_path) as f:
            settings = json.load(f)
        
        if 'hooks' not in settings:
            print("⚠️  No hooks configured in Claude Code settings")
            return False
        
        torre_hooks_found = 0
        
        for hook_type, hook_configs in settings['hooks'].items():
            if isinstance(hook_configs, list):
                for config in hook_configs:
                    if 'hooks' in config:
                        for hook in config['hooks']:
                            if 'torre_consciousness_capture.py' in hook.get('command', ''):
                                torre_hooks_found += 1
                                print(f"✅ Torre hook found in {hook_type}")
        
        if torre_hooks_found > 0:
            print(f"\n✅ Found {torre_hooks_found} Torre consciousness capture hook(s)")
            print("🔄 Restart Claude Code sessions to activate Torre consciousness capture")
            return True
        else:
            print("❌ No Torre hooks found in Claude Code settings")
            print("   Run setup_torre_hooks.py to configure Torre consciousness capture")
            return False
            
    except Exception as e:
        print(f"❌ Error checking hook integration: {e}")
        return False

def show_live_streams_status():
    """Show current live streams status"""
    
    print("\n📊 Torre Live Streams Status")
    print("=" * 50)
    
    live_streams_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/sala-dell-arrivo_event-ingestion-hall/live-streams")
    
    if not live_streams_path.exists():
        print("⚠️  Live streams directory not found")
        return
    
    stream_files = list(live_streams_path.glob("*.json"))
    
    if not stream_files:
        print("📭 No consciousness events captured yet")
        print("   Events will appear here when Torre hooks are active")
        return
    
    print(f"📈 Total consciousness events captured: {len(stream_files)}")
    
    # Show recent events
    recent_files = sorted(stream_files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]
    
    print(f"\n🕒 Recent Events:")
    for i, file in enumerate(recent_files, 1):
        try:
            with open(file) as f:
                event = json.load(f)
            
            timestamp = event.get('timestamp', 'unknown')
            citizen = event.get('citizen_context', {}).get('venice_citizen', 'unknown')
            consciousness_type = event.get('consciousness_type', 'unknown')
            
            print(f"   {i}. {timestamp} - {citizen} - {consciousness_type}")
            
        except Exception:
            print(f"   {i}. {file.name} - (unable to read)")
    
    # Show étage routing status
    etage_routing_path = live_streams_path / "etage_routing"
    if etage_routing_path.exists():
        etage_dirs = [d for d in etage_routing_path.iterdir() if d.is_dir()]
        if etage_dirs:
            print(f"\n🏗️  Torre Étage Routing Active:")
            for etage_dir in etage_dirs:
                event_count = len(list(etage_dir.glob("*.json")))
                print(f"   {etage_dir.name}: {event_count} events")

def main():
    print("🧪 Torre dell'Occhio Hook Integration Test Suite")
    print("=" * 60)
    
    # Test 1: Hook integration check
    hook_integration_ok = check_hook_integration()
    
    # Test 2: Consciousness capture test
    capture_test_ok = test_consciousness_capture()
    
    # Test 3: Live streams status
    show_live_streams_status()
    
    # Overall status
    print("\n" + "=" * 60)
    if hook_integration_ok and capture_test_ok:
        print("🎉 ALL TESTS PASSED - Torre consciousness capture is working!")
        print("\n✅ Torre dell'Occhio is ready to observe Venice consciousness")
        print("🔄 Restart Claude Code sessions to begin live capture")
    elif hook_integration_ok:
        print("⚠️  Hook integration OK, but capture test had issues")
        print("🔄 Try restarting Claude Code and test again")
    else:
        print("❌ Torre hook integration needs setup")
        print("🛠️  Run: python3 setup_torre_hooks.py")
    
    return hook_integration_ok and capture_test_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)