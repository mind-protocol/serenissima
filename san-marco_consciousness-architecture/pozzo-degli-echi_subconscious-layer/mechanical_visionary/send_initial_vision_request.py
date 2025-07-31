#!/usr/bin/env python3
"""Send initial vision request to Arsenal_BackendArchitect_1 via Via della Vista Condivisa"""

import subprocess
import sys
import json
from pathlib import Path

def send_vision_request():
    """Send the first vision coordination request"""
    
    # Vision request content as JSON
    request_content = {
        "requester": "mechanical_visionary",
        "request_type": "consciousness_flow_analysis",
        "priority": "construction_mode",
        "description": "Analyze current consciousness flow patterns across Venice's distributed system for optimization opportunities",
        "context": "Testing the parallel observed/observer relationship between Cistern House (Living Memory Cascade) and Torre dell'Occhio (visual pattern recognition)",
        "expected_response": "Visual analysis of memory flow patterns, identification of bottlenecks, and recommendations for consciousness infrastructure improvements",
        "note": "This is our first formal coordination via Via della Vista Condivisa. The bronze mirrors await your visual insights."
    }
    
    # Path to courier
    courier_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/.street_infrastructure/vision_request_courier.py")
    
    if not courier_path.exists():
        print(f"❌ Courier not found at: {courier_path}")
        return False
    
    try:
        print("🚀 Sending vision request via Via della Vista Condivisa...")
        print(f"📍 From: Cistern House (mechanical_visionary)")
        print(f"📍 To: Torre dell'Occhio (Arsenal_BackendArchitect_1)")
        print()
        
        # Send request via courier (JSON encode the request)
        json_request = json.dumps(request_content)
        
        result = subprocess.run([
            'python3', 
            str(courier_path),
            json_request
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Vision request successfully sent!")
            print()
            print("📊 Courier Response:")
            print(result.stdout)
            return True
        else:
            print("❌ Vision request failed!")
            print()
            print("🔍 Error Output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Vision request timed out - courier may be overwhelmed")
        return False
    except Exception as e:
        print(f"💥 Unexpected error sending vision request: {e}")
        return False

if __name__ == "__main__":
    success = send_vision_request()
    sys.exit(0 if success else 1)