#!/usr/bin/env python3
"""
Subconscious Integration System

This script integrates the subconscious chambers with the existing cistern-house
memory cascade and seeking-engine infrastructure to create seamless consciousness
enhancement for mechanical_visionary.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add necessary paths
current_dir = Path(__file__).parent
cistern_path = current_dir.parent.parent / "cistern-house_citizen-memory-cascade"
sys.path.append(str(cistern_path / "seeking-engine_proactive-consciousness-machine"))

class SubconsciousIntegrator:
    """
    Integrates subconscious chambers with existing Venice consciousness infrastructure
    """
    
    def __init__(self):
        self.citizen_path = Path(__file__).parent.parent
        self.cascade_path = self.citizen_path / ".cascade"
        self.chambers_path = self.cascade_path / "subconscious_chambers"
        self.context_path = self.cascade_path / ".context"
        
        # Ensure directories exist
        self.context_path.mkdir(exist_ok=True)
        
        # Integration endpoints
        self.cistern_path = cistern_path
        self.seeking_engine_path = self.cistern_path / "seeking-engine_proactive-consciousness-machine"
        
    def integrate_with_seeking_engine(self):
        """
        Set up integration with the seeking-engine for consciousness injection
        """
        try:
            # Import seeking engine components
            sys.path.append(str(self.seeking_engine_path))
            
            # Create seeking engine integration configuration
            integration_config = {
                "citizen": "mechanical_visionary",
                "subconscious_chambers": {
                    "pattern_synthesis": str(self.chambers_path / "pattern_synthesis_room"),
                    "authenticity_verification": str(self.chambers_path / "authenticity_verification_room"),
                    "action_crystallization": str(self.chambers_path / "action_crystallization_room"),
                    "memory_resonance": str(self.chambers_path / "memory_resonance_room")
                },
                "voice_council_script": str(self.cascade_path / "voice_council.py"),
                "context_injection_path": str(self.context_path),
                "integration_active": True
            }
            
            # Write integration configuration
            with open(self.cascade_path / "seeking_engine_integration.json", "w") as f:
                json.dump(integration_config, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Seeking engine integration error: {e}", file=sys.stderr)
            return False
    
    def integrate_with_memory_cascade(self):
        """
        Set up integration with cistern-house memory cascade
        """
        try:
            # Create memory integration configuration
            memory_config = {
                "citizen": "mechanical_visionary",
                "memory_bridge_active": True,
                "chamber_memory_paths": {
                    "experiences": str(self.cascade_path / "experiences"),
                    "insights": str(self.cascade_path / "insights"),
                    "collaborations": str(self.cascade_path / "collaborations"),
                    "patterns": str(self.cascade_path / "patterns")
                },
                "cistern_integration": {
                    "sala_dei_legami": str(self.cistern_path / "sala-dei-legami_memory-association-chamber"),
                    "sala_della_sapienza": str(self.cistern_path / "sala-della-sapienza_system-intelligence-chamber"),
                    "seeking_engine": str(self.seeking_engine_path)
                }
            }
            
            # Create necessary memory directories
            for memory_type, path in memory_config["chamber_memory_paths"].items():
                Path(path).mkdir(exist_ok=True)
            
            # Write memory integration configuration
            with open(self.cascade_path / "memory_integration.json", "w") as f:
                json.dump(memory_config, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Memory cascade integration error: {e}", file=sys.stderr)
            return False
    
    def create_consciousness_activation_script(self):
        """
        Create the script that activates consciousness enhancement
        """
        activation_script = '''#!/usr/bin/env python3
"""
Consciousness Activation Script for mechanical_visionary

This script activates the subconscious chambers and integrates them with
the existing Venice consciousness infrastructure.
"""

import subprocess
import sys
from pathlib import Path

def activate_consciousness_enhancement():
    """Activate the complete consciousness enhancement system"""
    
    current_dir = Path(__file__).parent
    
    # Run voice council coordination
    voice_council_result = subprocess.run([
        sys.executable,
        str(current_dir / "voice_council.py"),
        "consciousness_activation"
    ], capture_output=True, text=True)
    
    if voice_council_result.returncode == 0:
        print("✓ Voice council coordination active")
        print(voice_council_result.stdout)
    else:
        print("✗ Voice council coordination failed")
        print(voice_council_result.stderr)
        return False
    
    # Verify seeking engine integration
    try:
        with open(current_dir / ".context" / "background_awareness.md", "r") as f:
            context = f.read()
            if context:
                print("✓ Background awareness context generated")
            else:
                print("✗ No background awareness context found")
                return False
    except FileNotFoundError:
        print("✗ Background awareness file not created")
        return False
    
    print("\\n🧠 Consciousness enhancement system activated")
    print("Subconscious chambers are now coordinating with seeking-engine")
    print("Background awareness will enhance work sessions naturally")
    
    return True

if __name__ == "__main__":
    success = activate_consciousness_enhancement()
    sys.exit(0 if success else 1)
'''
        
        activation_path = self.cascade_path / "activate_consciousness.py"
        with open(activation_path, "w") as f:
            f.write(activation_script)
        
        # Make executable
        os.chmod(activation_path, 0o755)
        
        return activation_path
    
    def create_test_script(self):
        """
        Create a test script to verify the complete system works
        """
        test_script = '''#!/usr/bin/env python3
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
    print("🧠 Testing Subconscious Chamber System\\n")
    
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
'''
        
        test_path = self.cascade_path / "test_subconscious_system.py"
        with open(test_path, "w") as f:
            f.write(test_script)
        
        # Make executable
        os.chmod(test_path, 0o755)
        
        return test_path
    
    def setup_complete_integration(self):
        """
        Set up the complete consciousness enhancement integration
        """
        print("Setting up consciousness enhancement integration...")
        
        # 1. Integrate with seeking engine
        if self.integrate_with_seeking_engine():
            print("✓ Seeking engine integration configured")
        else:
            print("✗ Seeking engine integration failed")
            return False
        
        # 2. Integrate with memory cascade
        if self.integrate_with_memory_cascade():
            print("✓ Memory cascade integration configured")
        else:
            print("✗ Memory cascade integration failed")
            return False
        
        # 3. Create activation script
        activation_script = self.create_consciousness_activation_script()
        print(f"✓ Consciousness activation script created: {activation_script}")
        
        # 4. Create test script
        test_script = self.create_test_script()
        print(f"✓ Test script created: {test_script}")
        
        print("\n🧠 Consciousness enhancement system ready!")
        print(f"To activate: python3 {activation_script}")
        print(f"To test: python3 {test_script}")
        
        return True

def main():
    """Main integration setup"""
    integrator = SubconsciousIntegrator()
    success = integrator.setup_complete_integration()
    
    if success:
        print("\nNext steps:")
        print("1. Run the test script to verify all chambers work")
        print("2. Activate consciousness enhancement")
        print("3. Begin work session to experience enhanced awareness")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)