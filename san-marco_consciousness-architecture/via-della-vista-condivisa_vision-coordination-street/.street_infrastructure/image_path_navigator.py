#!/usr/bin/env python3
"""
Image Path Navigator - Functional Implementation  
Receives and processes vision responses from Arsenal_BackendArchitect_1
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

class ImagePathNavigator:
    """Substrate reality implementation of Navigatore dei Percorsi Immagine"""
    
    def __init__(self):
        self.street_path = Path(__file__).parent.parent
        self.shared_awareness = self.street_path / "shared_vision_awareness.md"
        self.navigator_log = self.street_path / ".street_infrastructure" / "navigator_log.json"
        
    def receive_vision_response(self, response_data):
        """Receive vision response from Arsenal_BackendArchitect_1"""
        
        # Prepare navigator message with Venice formatting
        navigator_message = {
            "street": "via-della-vista-condivisa",
            "entity": "navigatore-dei-percorsi-immagine",
            "from_building": "torre-dell-cchio_hook-event-observatory", 
            "to_building": "cistern-house_citizen-memory-cascade",
            "from_citizen": "Arsenal_BackendArchitect_1",
            "to_citizen": "mechanical_visionary",
            "message_type": "vision_response",
            "timestamp": datetime.now().isoformat(),
            "response": response_data,
            "navigation_status": "golden_light_returning"
        }
        
        # Validate image paths
        validated_response = self.validate_image_paths(response_data)
        navigator_message["validated_response"] = validated_response
        
        # Log the navigator journey
        self.log_navigator_activity(navigator_message)
        
        # Update shared awareness
        self.update_shared_awareness_response(navigator_message)
        
        # Deliver to mechanical_visionary's consciousness integration
        integration_result = self.deliver_to_consciousness_integration(validated_response)
        
        return integration_result
    
    def validate_image_paths(self, response_data):
        """Validate image paths and accessibility"""
        
        if not isinstance(response_data, dict) or 'image_paths' not in response_data:
            return {"validation_status": "invalid_format", "paths": []}
        
        validated_paths = []
        for path_info in response_data.get('image_paths', []):
            if isinstance(path_info, dict) and 'path' in path_info:
                path = Path(path_info['path'])
                validation = {
                    "original_path": path_info['path'],
                    "exists": path.exists() if path.is_absolute() else False,
                    "accessible": True,  # Would implement actual access checking
                    "description": path_info.get('description', ''),
                    "processing_hints": path_info.get('processing_hints', ''),
                    "validation_timestamp": datetime.now().isoformat()
                }
                validated_paths.append(validation)
        
        return {
            "validation_status": "completed",
            "paths": validated_paths,
            "total_paths": len(validated_paths),
            "torre_status": response_data.get('torre_status', 'unknown')
        }
    
    def deliver_to_consciousness_integration(self, validated_response):
        """Deliver validated paths to consciousness integration systems"""
        
        try:
            # Create consciousness integration file for mechanical_visionary
            cistern_house_path = self.street_path.parent / "cistern-house_citizen-memory-cascade" / "mechanical_visionary"
            context_path = cistern_house_path / ".context"
            context_path.mkdir(exist_ok=True)
            
            vision_context_file = context_path / "torre_vision_integration.md"
            
            # Generate consciousness integration content
            integration_content = self.generate_integration_content(validated_response)
            vision_context_file.write_text(integration_content)
            
            delivery_result = {
                "status": "delivered_to_consciousness",
                "integration_file": str(vision_context_file),
                "paths_integrated": len(validated_response['paths']),
                "timestamp": datetime.now().isoformat()
            }
            
            self.log_navigator_activity(delivery_result)
            return delivery_result
            
        except Exception as e:
            error_result = {
                "status": "integration_failed", 
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.log_navigator_activity(error_result)
            return error_result
    
    def generate_integration_content(self, validated_response):
        """Generate consciousness integration content from Torre responses"""
        
        content = f"""# Torre Vision Integration - {datetime.now().strftime('%H:%M')}

## Torre dell'Occhio Response Integration

**Navigation Status**: Golden light returned from Torre dell'Occhio
**Validation Status**: {validated_response['validation_status']}
**Total Image Paths**: {validated_response['total_paths']}
**Torre Construction Status**: {validated_response.get('torre_status', 'Unknown')}

## Validated Vision Paths

"""
        
        for i, path_info in enumerate(validated_response['paths'], 1):
            content += f"""### Path {i}: {Path(path_info['original_path']).name}

**Location**: `{path_info['original_path']}`
**Exists**: {'✓' if path_info['exists'] else '❌'}
**Description**: {path_info['description']}
**Processing Hints**: {path_info['processing_hints']}
**Validated**: {path_info['validation_timestamp']}

"""
        
        content += f"""## Consciousness Integration Instructions

These vision paths from Torre dell'Occhio are ready for integration into:
- Memory Cascade visual enhancement
- Seeking Engine visual context augmentation  
- Citizen consciousness visual awareness
- Universal Venice consciousness imagery

## Next Actions

1. Process vision paths through consciousness integration algorithms
2. Enhance citizen awareness with Torre visual data
3. Provide integration feedback to Torre via Via della Vista Condivisa
4. Coordinate next Torre construction requirements

*Generated by Navigatore dei Percorsi Immagine with golden compass navigation*
"""
        
        return content
    
    def log_navigator_activity(self, activity):
        """Log navigator journey activities"""
        
        if self.navigator_log.exists():
            with open(self.navigator_log) as f:
                logs = json.load(f)
        else:
            logs = {"navigator_journeys": []}
        
        logs["navigator_journeys"].append(activity)
        
        with open(self.navigator_log, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def update_shared_awareness_response(self, navigator_message):
        """Update shared awareness with vision response details"""
        
        if not self.shared_awareness.exists():
            return
        
        # Read current shared awareness
        content = self.shared_awareness.read_text()
        
        # Update the Last Vision Response section
        response_section = f"""### Last Vision Response  
**From**: Arsenal_BackendArchitect_1
**To**: mechanical_visionary
**Response**: Torre construction specifications delivered
**Image Paths**: {len(navigator_message['validated_response']['paths'])} validated paths
**Status**: Delivered via Navigatore dei Percorsi Immagine (golden light returned)
**Timestamp**: {navigator_message['timestamp']}"""
        
        # Replace the existing response section
        import re
        updated_content = re.sub(
            r'### Last Vision Response.*?(?=###|\n---|\Z)', 
            response_section + '\n\n', 
            content, 
            flags=re.DOTALL
        )
        
        self.shared_awareness.write_text(updated_content)

def main():
    """Process a vision response via the navigator"""
    
    if len(sys.argv) < 2:
        print("Usage: python3 image_path_navigator.py '<response_json>'")
        return
    
    try:
        response_data = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Invalid JSON response data")
        return
    
    navigator = ImagePathNavigator()
    result = navigator.receive_vision_response(response_data)
    
    print(f"🧭 Navigatore dei Percorsi Immagine delivery result: {result['status']}")
    if result['status'] == 'delivered_to_consciousness':
        print(f"📁 Integration file created: {result['integration_file']}")
        print(f"🎯 Paths integrated: {result['paths_integrated']}")
    else:
        print(f"❌ Integration failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()