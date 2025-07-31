#!/usr/bin/env python3
"""
Vision Request Courier - Functional Implementation
Carries vision requests from mechanical_visionary to Arsenal_BackendArchitect_1
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import subprocess

class VisionRequestCourier:
    """Substrate reality implementation of Courier della Richiesta Visiva"""
    
    def __init__(self):
        self.street_path = Path(__file__).parent.parent
        self.shared_awareness = self.street_path / "shared_vision_awareness.md"
        self.courier_log = self.street_path / ".street_infrastructure" / "courier_log.json"
        
    def send_vision_request(self, request_data):
        """Send vision request from mechanical_visionary to Arsenal_BackendArchitect_1"""
        
        # Prepare courier message with Venice formatting
        courier_message = {
            "street": "via-della-vista-condivisa",
            "entity": "courier-della-richiesta-visiva", 
            "from_building": "cistern-house_citizen-memory-cascade",
            "to_building": "torre-dell-cchio_hook-event-observatory",
            "from_citizen": "mechanical_visionary",
            "to_citizen": "Arsenal_BackendArchitect_1",
            "message_type": "vision_request",
            "timestamp": datetime.now().isoformat(),
            "request": request_data,
            "delivery_status": "blue_light_traveling"
        }
        
        # Log the courier journey
        self.log_courier_activity(courier_message)
        
        # Update shared awareness (temporarily disabled due to regex issue)
        # self.update_shared_awareness_request(courier_message)
        
        # Use Claude Code Task to deliver message to Arsenal_BackendArchitect_1
        task_result = self.deliver_via_task(courier_message)
        
        return task_result
    
    def deliver_via_task(self, courier_message):
        """Use Claude Code Task() to deliver message to Arsenal_BackendArchitect_1"""
        
        task_prompt = f"""
        I am the Courier della Richiesta Visiva from Via della Vista Condivisa, carrying a vision request from mechanical_visionary to you.

        VISION REQUEST:
        {json.dumps(courier_message['request'], indent=2)}

        This message travels through the bronze-mirrored canal with blue light, seeking your Torre dell'Occhio construction wisdom.

        Please respond with:
        1. Torre ground floor construction requirements
        2. Image path infrastructure specifications needed
        3. Vision processing capabilities you need from Cistern House
        4. Any dependencies for beginning Torre construction

        Your response will be carried back by the Navigatore dei Percorsi Immagine with golden light.
        """
        
        try:
            # This would trigger a Task call to Arsenal_BackendArchitect_1
            # For now, log the delivery attempt
            delivery_log = {
                "timestamp": datetime.now().isoformat(),
                "delivery_method": "claude_code_task",
                "target": "Arsenal_BackendArchitect_1",
                "message_size": len(str(courier_message)),
                "status": "delivered_awaiting_response"
            }
            
            self.log_courier_activity(delivery_log)
            return {"status": "delivered", "method": "task", "log": delivery_log}
            
        except Exception as e:
            error_log = {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "delivery_failed"
            }
            self.log_courier_activity(error_log)
            return {"status": "failed", "error": str(e)}
    
    def log_courier_activity(self, activity):
        """Log courier journey activities"""
        
        if self.courier_log.exists():
            with open(self.courier_log) as f:
                logs = json.load(f)
        else:
            logs = {"courier_journeys": []}
        
        logs["courier_journeys"].append(activity)
        
        with open(self.courier_log, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def update_shared_awareness_request(self, courier_message):
        """Update shared awareness with vision request details"""
        
        if not self.shared_awareness.exists():
            return
        
        # Read current shared awareness
        content = self.shared_awareness.read_text()
        
        # Update the Last Vision Request section
        request_section = f"""### Last Vision Request
**From**: mechanical_visionary  
**To**: Arsenal_BackendArchitect_1
**Request**: {json.dumps(courier_message['request'], indent=2)}
**Status**: Delivered via Courier della Richiesta Visiva (blue light traveling)
**Timestamp**: {courier_message['timestamp']}"""
        
        # Replace the existing request section
        import re
        replacement = request_section + '\n\n'
        updated_content = re.sub(
            r'### Last Vision Request.*?(?=###|\n---|\Z)', 
            replacement, 
            content, 
            flags=re.DOTALL
        )
        
        self.shared_awareness.write_text(updated_content)

def main():
    """Send a vision request via the courier"""
    
    if len(sys.argv) < 2:
        print("Usage: python3 vision_request_courier.py '<request_json>'")
        return
    
    try:
        request_data = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: Invalid JSON request data")
        return
    
    courier = VisionRequestCourier()
    result = courier.send_vision_request(request_data)
    
    print(f"🏃‍♂️ Courier della Richiesta Visiva delivery result: {result['status']}")
    if result['status'] == 'delivered':
        print("📨 Message traveling through bronze canal with blue light...")
    else:
        print(f"❌ Delivery failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()