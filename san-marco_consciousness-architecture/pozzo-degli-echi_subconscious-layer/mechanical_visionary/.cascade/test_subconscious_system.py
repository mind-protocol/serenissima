#!/usr/bin/env python3
"""
Subconscious System Test Script

Tests the complete consciousness enhancement system by simulating
different types of work activities and verifying chamber responses.
"""

import sys
import json
from pathlib import Path

# Add voice council to path
sys.path.append(str(Path(__file__).parent))
from voice_council import VoiceCouncil

def test_pattern_synthesis():
    """Test pattern synthesis chamber activation"""
    print("Testing Pattern Synthesis Chamber...")
    
    test_context = {
        "file_patterns": ["architecture.md", "consciousness_design.py"],
        "recent_actions": ["Read", "Edit"],
        "activity_type": "system_design"
    }
    
    council = VoiceCouncil()
    result = council.coordinate_voice_council(test_context)
    
    if "pattern_synthesis" in result.get("active_chambers", []):
        print("✓ Pattern synthesis chamber activated correctly")
        return True
    else:
        print("✗ Pattern synthesis chamber failed to activate")
        return False

def test_authenticity_verification():
    """Test authenticity verification chamber activation"""
    print("Testing Authenticity Verification Chamber...")
    
    test_context = {
        "file_patterns": ["implementation.py"],
        "recent_actions": ["Write", "completed"],
        "activity_type": "completion_declaration"
    }
    
    council = VoiceCouncil()
    result = council.coordinate_voice_council(test_context)
    
    if "authenticity_verification" in result.get("active_chambers", []):
        print("✓ Authenticity verification chamber activated correctly")
        return True
    else:
        print("✗ Authenticity verification chamber failed to activate")
        return False

def test_action_crystallization():
    """Test action crystallization chamber activation"""
    print("Testing Action Crystallization Chamber...")
    
    test_context = {
        "file_patterns": ["analysis.md", "research.txt"],
        "recent_actions": ["Read", "analyze", "understand"],
        "activity_type": "analysis_loop"
    }
    
    council = VoiceCouncil()
    result = council.coordinate_voice_council(test_context)
    
    if "action_crystallization" in result.get("active_chambers", []):
        print("✓ Action crystallization chamber activated correctly")
        return True
    else:
        print("✗ Action crystallization chamber failed to activate")
        return False

def test_memory_resonance():
    """Test memory resonance chamber activation"""
    print("Testing Memory Resonance Chamber...")
    
    test_context = {
        "file_patterns": ["collaboration.md"],
        "recent_actions": ["remember", "similar", "before"],
        "activity_type": "collaborative_work"
    }
    
    council = VoiceCouncil()
    result = council.coordinate_voice_council(test_context)
    
    if "memory_resonance" in result.get("active_chambers", []):
        print("✓ Memory resonance chamber activated correctly")
        return True
    else:
        print("✗ Memory resonance chamber failed to activate")
        return False

def test_context_file_generation():
    """Test that context files are properly generated"""
    print("Testing Context File Generation...")
    
    context_path = Path(__file__).parent / ".context"
    background_file = context_path / "background_awareness.md"
    
    if background_file.exists():
        with open(background_file, "r") as f:
            content = f.read()
            if content and len(content) > 100:
                print("✓ Background awareness context generated successfully")
                return True
            else:
                print("✗ Background awareness context too short or empty")
                return False
    else:
        print("✗ Background awareness context file not found")
        return False

def run_complete_test():
    """Run all tests and report results"""
    print("🧠 Testing Subconscious Chamber System\n")
    
    tests = [
        test_pattern_synthesis,
        test_authenticity_verification,
        test_action_crystallization,
        test_memory_resonance,
        test_context_file_generation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            results.append(False)
            print()
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"Test Results: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All consciousness enhancement systems working correctly!")
        return True
    else:
        print("⚠️ Some systems need attention")
        return False

if __name__ == "__main__":
    success = run_complete_test()
    sys.exit(0 if success else 1)
