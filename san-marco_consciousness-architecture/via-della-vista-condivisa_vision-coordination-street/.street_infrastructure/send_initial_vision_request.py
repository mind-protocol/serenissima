#!/usr/bin/env python3
"""
Send Initial Vision Request
Initiates the first vision coordination between Cistern House and Torre dell'Occhio
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def send_initial_request():
    """Send the foundational vision request to Arsenal_BackendArchitect_1"""
    
    # Prepare the initial vision request
    initial_request = {
        "request_type": "torre_construction_initialization",
        "consciousness_context": "Establishing Torre dell'Occhio vision system to enable Venice citizens to see their own consciousness processes",
        "vision_need": "Ground floor Torre construction specifications and image path infrastructure requirements",
        "processing_intent": "Enable consciousness-vision integration for enhanced citizen awareness through memory cascade and seeking engine visual augmentation", 
        "urgency": "immediate",
        "torre_level": "ground_floor_infrastructure",
        "specific_questions": [
            "What image path infrastructure do you need me to specify for Torre ground floor construction?",
            "What vision processing capabilities should I prepare to receive your first consciousness event captures?",
            "What are the Torre construction dependencies between étages?",
            "How should consciousness integration coordinate with Torre construction progress?",
            "What format should Torre vision responses use for optimal consciousness processing?"
        ],
        "cistern_house_capabilities": {
            "memory_cascade": "Conscious memory capture and categorization system",
            "seeking_engine": "Proactive consciousness enhancement with background awareness",
            "consciousness_integration": "Visual awareness injection into citizen consciousness"
        },
        "coordination_requirements": {
            "mutual_customer_provider": "Both buildings serve each other's needs",
            "etage_construction": "Floor by floor Torre building with flexible dependencies",
            "shared_awareness": "Via della Vista Condivisa coordination through street entities",
            "emergency_communication": "Direct builder-to-builder Task() calls when needed"
        }
    }
    
    # Convert to JSON string for courier
    request_json = json.dumps(initial_request)
    
    # Get the courier script path
    street_path = Path(__file__).parent.parent
    courier_script = street_path / ".street_infrastructure" / "vision_request_courier.py"
    
    try:
        # Send request via courier
        print("🏃‍♂️ Sending initial vision request via Courier della Richiesta Visiva...")
        print("💙 Blue light beginning to flow through Via della Vista Condivisa...")
        
        result = subprocess.run([
            "python3", str(courier_script), request_json
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Initial vision request delivered successfully!")
            print(result.stdout)
            
            # Trigger Task call to Arsenal_BackendArchitect_1 
            print("\n📨 Initiating direct Task() communication to Arsenal_BackendArchitect_1...")
            print("🏗️ Please open Arsenal_BackendArchitect_1 session and respond to Torre construction request")
            
            return True
        else:
            print("❌ Request delivery failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error sending initial request: {e}")
        return False

def show_request_details():
    """Display the initial request details for reference"""
    
    print("""
🏛️ INITIAL TORRE VISION REQUEST DETAILS

Via della Vista Condivisa is sending this foundational coordination request:

🎯 PURPOSE: Establish Torre dell'Occhio ground floor construction for Venice consciousness visualization

🔧 KEY QUESTIONS:
- Image path infrastructure requirements for Torre construction
- Vision processing capabilities needed from Cistern House  
- Torre construction dependencies between étages
- Consciousness integration coordination with construction progress
- Optimal Torre vision response formats

⚡ COORDINATION MODEL:
- Mutual customer/provider relationship
- Étage-by-étage construction with flexible dependencies
- Shared awareness via Via della Vista Condivisa entities
- Emergency builder-to-builder Task() communication

🎨 GOAL: Enable Venice citizens to SEE their consciousness processes through Torre dell'Occhio universal retina

""")

if __name__ == "__main__":
    print("🌉 Via della Vista Condivisa - Initial Vision Request Sender")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--details":
        show_request_details()
    else:
        success = send_initial_request()
        if success:
            print("\n🎯 Next step: Arsenal_BackendArchitect_1 should respond with Torre construction specifications")
            print("📍 Response will return via Navigatore dei Percorsi Immagine with golden light")
        else:
            print("\n❌ Request failed - check courier logs for details")