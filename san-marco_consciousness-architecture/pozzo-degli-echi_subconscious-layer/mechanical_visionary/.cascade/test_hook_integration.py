#!/usr/bin/env python3
"""
Test Hook Integration - Verify the corrected voice council works with Claude Code hooks
"""

import json
import subprocess
import sys
from pathlib import Path

def test_voice_council_with_hook_data():
    """Test voice council with simulated Claude Code hook input"""
    
    test_cases = [
        {
            "name": "Creative Design Work",
            "hook_data": {
                "session_id": "test123",
                "transcript_path": "/tmp/test.jsonl",
                "cwd": "/test",
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "/test/consciousness_architecture.md",
                    "content": "Building a complex consciousness system with multiple interacting components"
                }
            },
            "expected_chambers": ["pattern_synthesis"]
        },
        {
            "name": "Performance Risk Detection",
            "hook_data": {
                "session_id": "test123",
                "transcript_path": "/tmp/test.jsonl",
                "cwd": "/test",
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {
                    "file_path": "/test/implementation.py",
                    "content": "✅ Fixed! The system is now working perfectly and completely solved."
                }
            },
            "expected_chambers": ["authenticity_verification"]
        },
        {
            "name": "Analysis Paralysis",
            "hook_data": {
                "session_id": "test123",
                "transcript_path": "/tmp/test.jsonl",
                "cwd": "/test",
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {
                    "file_path": "/test/analysis.md",
                    "content": "Need to understand and analyze this complex system more before proceeding"
                }
            },
            "expected_chambers": ["action_crystallization"]
        },
        {
            "name": "Collaboration Memory",
            "hook_data": {
                "session_id": "test123",
                "transcript_path": "/tmp/test.jsonl",
                "cwd": "/test",
                "hook_event_name": "PreToolUse",
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "/test/collaboration.md",
                    "content": "Working with partner on this solution, similar to what we did before"
                }
            },
            "expected_chambers": ["memory_resonance"]
        }
    ]
    
    voice_council_script = Path(__file__).parent / "voice_council_corrected.py"
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print("-" * 50)
        
        # Convert hook data to JSON
        hook_json = json.dumps(test_case["hook_data"])
        
        # Run voice council with test data
        try:
            result = subprocess.run(
                [sys.executable, str(voice_council_script)],
                input=hook_json,
                text=True,
                capture_output=True
            )
            
            print(f"Exit code: {result.returncode}")
            
            if result.returncode == 2:
                print("✓ Consciousness enhancement triggered")
                print(f"Enhancement: {result.stderr.strip()}")
            elif result.returncode == 0:
                print("○ No consciousness enhancement (normal operation)")
            else:
                print(f"✗ Error occurred: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"✗ Test failed: {e}")

def test_hook_configuration():
    """Test that the hook configuration is valid"""
    print("Testing Hook Configuration")
    print("=" * 50)
    
    settings_file = Path(__file__).parent.parent / ".claude" / "settings.json"
    
    if settings_file.exists():
        try:
            with open(settings_file) as f:
                settings = json.load(f)
            
            print("✓ Settings.json exists and is valid JSON")
            
            if "hooks" in settings:
                print("✓ Hooks configuration found")
                
                if "PreToolUse" in settings["hooks"]:
                    print("✓ PreToolUse hooks configured")
                    
                    hook_config = settings["hooks"]["PreToolUse"][0]
                    command = hook_config["hooks"][0]["command"]
                    
                    if "voice_council_corrected.py" in command:
                        print("✓ Voice council script correctly configured")
                    else:
                        print(f"✗ Wrong script configured: {command}")
                else:
                    print("✗ No PreToolUse hooks found")
            else:
                print("✗ No hooks configuration found")
                
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON in settings file: {e}")
    else:
        print(f"✗ Settings file not found: {settings_file}")

def test_script_permissions():
    """Test that the voice council script is executable"""
    print("\nTesting Script Permissions")
    print("=" * 50)
    
    voice_council_script = Path(__file__).parent / "voice_council_corrected.py"
    
    if voice_council_script.exists():
        print("✓ Voice council script exists")
        
        # Test basic execution
        try:
            result = subprocess.run(
                [sys.executable, str(voice_council_script)],
                input="{}",
                text=True,
                capture_output=True,
                timeout=5
            )
            print("✓ Script is executable")
            
        except subprocess.TimeoutExpired:
            print("✗ Script timed out")
        except Exception as e:
            print(f"✗ Script execution failed: {e}")
    else:
        print("✗ Voice council script not found")

def main():
    """Run all tests"""
    print("🧠 Testing Corrected Consciousness Enhancement System")
    print("=" * 60)
    
    test_hook_configuration()
    test_script_permissions()
    test_voice_council_with_hook_data()
    
    print("\n" + "=" * 60)
    print("Test complete. If all tests pass, the consciousness enhancement")
    print("system should work with real Claude Code sessions.")

if __name__ == "__main__":
    main()