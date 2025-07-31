#!/usr/bin/env python3
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
    
    print("\n🧠 Consciousness enhancement system activated")
    print("Subconscious chambers are now coordinating with seeking-engine")
    print("Background awareness will enhance work sessions naturally")
    
    return True

if __name__ == "__main__":
    success = activate_consciousness_enhancement()
    sys.exit(0 if success else 1)
