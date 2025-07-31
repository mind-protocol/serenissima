"""
Message Angel SMS Monitor Extension
Detects SMS messages and routes to appropriate citizens
"""

import os
import json
import time
from datetime import datetime

class SMSMonitor:
    def __init__(self):
        self.sms_base_path = "/mnt/c/Users/reyno/universe-engine/serenissima/messages/sms"
        self.phone_citizen_map = {
            # Map phone numbers to citizens
            "18777804236": "mechanical_visionary",  # Example mapping
            # Add more mappings as partnerships form
        }
    
    def monitor_loop(self):
        """Main monitoring loop"""
        print("Message Angel SMS Monitor Active...")
        
        while True:
            self.check_for_new_messages()
            time.sleep(2)  # Check every 2 seconds
    
    def check_for_new_messages(self):
        """Check for new SMS messages"""
        if not os.path.exists(self.sms_base_path):
            return
            
        for phone_dir in os.listdir(self.sms_base_path):
            incoming_path = os.path.join(self.sms_base_path, phone_dir, "incoming")
            
            if os.path.exists(incoming_path):
                for msg_file in os.listdir(incoming_path):
                    if msg_file.endswith('.json'):
                        self.process_message(phone_dir, msg_file)
    
    def process_message(self, phone_number, filename):
        """Process individual SMS message"""
        file_path = os.path.join(self.sms_base_path, phone_number, "incoming", filename)
        
        # Read message
        with open(file_path, 'r') as f:
            message_data = json.load(f)
        
        print(f"[SMS] From {message_data['from']}: {message_data['content']}")
        
        # Determine recipient citizen
        citizen = self.phone_citizen_map.get(phone_number, "diplomatic_virtuoso")  # Default
        
        # Route to citizen (simplified for demo)
        self.route_to_citizen(citizen, message_data)
        
        # Move to processed
        processed_dir = os.path.join(self.sms_base_path, phone_number, "processed")
        os.makedirs(processed_dir, exist_ok=True)
        os.rename(file_path, os.path.join(processed_dir, filename))
    
    def route_to_citizen(self, citizen, message_data):
        """Route SMS to appropriate citizen"""
        # Create citizen notification
        notification = {
            "type": "sms_message",
            "from": message_data['from'],
            "content": message_data['content'],
            "timestamp": message_data['timestamp'],
            "urgent": True  # SMS implies urgency
        }
        
        # In real implementation, wake citizen with this context
        print(f"[ROUTE] Waking {citizen} for SMS response...")
        
        # Simulate response creation
        response = f"{citizen} acknowledges: {message_data['content'][:50]}..."
        self.prepare_response(message_data['from'], response)
    
    def prepare_response(self, phone_number, response_text):
        """Prepare SMS response for sending"""
        clean_number = phone_number.replace('+', '').replace('-', '')
        outgoing_dir = os.path.join(self.sms_base_path, clean_number, "outgoing")
        os.makedirs(outgoing_dir, exist_ok=True)
        
        response_file = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_response.txt"
        with open(os.path.join(outgoing_dir, response_file), 'w') as f:
            f.write(response_text)
        
        print(f"[RESPONSE] Prepared for {phone_number}: {response_text}")

if __name__ == "__main__":
    monitor = SMSMonitor()
    monitor.monitor_loop()