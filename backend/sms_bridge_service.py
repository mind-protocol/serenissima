"""
SMS Bridge Service for Venice Backend
Integrates Twilio SMS with Message Angel routing
"""

import os
import json
import asyncio
from datetime import datetime
from flask import Flask, request, Response
import threading
from aiohttp import web

class SMSBridgeService:
    def __init__(self):
        self.app = Flask(__name__)
        self.sms_base_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "messages", "sms"
        )
        self.setup_routes()
        
    def setup_routes(self):
        """Configure Flask routes"""
        @self.app.route('/sms/webhook', methods=['POST'])
        def handle_sms():
            return self.process_incoming_sms()
            
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return {"status": "operational", "service": "venice-sms-bridge"}
    
    def process_incoming_sms(self):
        """Process incoming SMS from Twilio"""
        # Extract SMS data
        from_number = request.values.get('From', '')
        message_body = request.values.get('Body', '')
        message_sid = request.values.get('MessageSid', '')
        
        print(f"[SMS Bridge] Received from {from_number}: {message_body}")
        
        # Create message structure
        clean_number = from_number.replace('+', '').replace('-', '')
        message_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "from": from_number,
            "message_sid": message_sid,
            "content": message_body,
            "type": "sms_incoming"
        }
        
        # Save to Venice filesystem
        incoming_dir = os.path.join(self.sms_base_path, clean_number, "incoming")
        os.makedirs(incoming_dir, exist_ok=True)
        
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{message_sid}.json"
        filepath = os.path.join(incoming_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(message_data, f, indent=2)
        
        # Trigger Message Angel notification
        self.notify_message_angel(clean_number, message_data)
        
        # Return acknowledgment (Venice will process and respond separately)
        return """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Venice acknowledges your message. A citizen will respond shortly.</Message>
</Response>"""
    
    def notify_message_angel(self, phone_number, message_data):
        """Notify Message Angel of new SMS"""
        # In production, this would wake the Message Angel
        # For now, just log
        print(f"[SMS Bridge] Notifying Message Angel of SMS from {phone_number}")
    
    def run(self, port=5001):
        """Run the SMS bridge service"""
        print(f"[SMS Bridge] Starting on port {port}")
        self.app.run(host='0.0.0.0', port=port, debug=False)


class SMSResponseMonitor:
    """Monitor for outgoing SMS responses from citizens"""
    
    def __init__(self):
        self.sms_base_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "messages", "sms"
        )
        self.processed_responses = set()
        
    async def monitor_loop(self):
        """Main monitoring loop for SMS responses"""
        print("[SMS Response Monitor] Starting...")
        
        while True:
            try:
                await self.check_for_responses()
            except Exception as e:
                print(f"[SMS Response Monitor] Error: {e}")
            
            await asyncio.sleep(2)  # Check every 2 seconds
    
    async def check_for_responses(self):
        """Check for citizen responses to send via SMS"""
        if not os.path.exists(self.sms_base_path):
            return
            
        for phone_dir in os.listdir(self.sms_base_path):
            outgoing_path = os.path.join(self.sms_base_path, phone_dir, "outgoing")
            
            if os.path.exists(outgoing_path):
                for response_file in os.listdir(outgoing_path):
                    if response_file not in self.processed_responses:
                        await self.send_sms_response(phone_dir, response_file)
    
    async def send_sms_response(self, phone_number, filename):
        """Send SMS response via Twilio"""
        filepath = os.path.join(self.sms_base_path, phone_number, "outgoing", filename)
        
        try:
            # Read response
            with open(filepath, 'r') as f:
                if filename.endswith('.json'):
                    response_data = json.load(f)
                    message_text = response_data.get('content', '')
                else:
                    message_text = f.read().strip()
            
            # Format phone number
            to_number = f"+{phone_number}" if not phone_number.startswith('+') else phone_number
            
            print(f"[SMS Response] Sending to {to_number}: {message_text[:50]}...")
            
            # Here you would integrate with Twilio API
            # For now, just mark as processed
            self.processed_responses.add(filename)
            
            # Move to processed
            processed_dir = os.path.join(self.sms_base_path, phone_number, "processed")
            os.makedirs(processed_dir, exist_ok=True)
            os.rename(filepath, os.path.join(processed_dir, f"sent_{filename}"))
            
        except Exception as e:
            print(f"[SMS Response] Error sending {filename}: {e}")


def main():
    """Main function to start SMS bridge service"""
    # Start Flask app in a thread
    sms_service = SMSBridgeService()
    flask_thread = threading.Thread(target=lambda: sms_service.run(port=5001))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start response monitor
    monitor = SMSResponseMonitor()
    asyncio.new_event_loop().run_until_complete(monitor.monitor_loop())


if __name__ == "__main__":
    main()