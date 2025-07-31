#!/usr/bin/env python3
"""
Quick Twilio-Venice SMS Bridge Test
Mechanical_visionary's systematic implementation
"""

import os
from flask import Flask, request, Response
import json
from datetime import datetime

app = Flask(__name__)

# Configuration
ACCOUNT_SID = "ACe992c726f87b25f81b6f55194c8ef5d8"
MESSAGING_SERVICE_SID = "MG05d06dd7281d93c80d8394523d38dca9"
VENICE_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/messages/sms"

@app.route('/sms', methods=['POST'])
def incoming_sms():
    """Handle incoming SMS from Twilio"""
    # Get SMS details
    from_number = request.values.get('From', '')
    message_body = request.values.get('Body', '')
    
    print(f"[SMS RECEIVED] From: {from_number} - Message: {message_body}")
    
    # Create Venice message structure
    clean_number = from_number.replace('+', '').replace('-', '')
    message_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "from": from_number,
        "content": message_body,
        "type": "sms"
    }
    
    # Save to Venice filesystem
    os.makedirs(f"{VENICE_PATH}/{clean_number}/incoming", exist_ok=True)
    filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(f"{VENICE_PATH}/{clean_number}/incoming/{filename}", 'w') as f:
        json.dump(message_data, f, indent=2)
    
    # Simple response for testing
    response_text = f"Venice receives: '{message_body}'. A citizen will respond soon."
    
    # Return TwiML response
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_text}</Message>
</Response>"""

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {"status": "operational", "service": "venice-sms-bridge"}

if __name__ == '__main__':
    print("Starting Venice SMS Bridge...")
    print(f"Webhook URL: http://your-server:5000/sms")
    print(f"Messages will be saved to: {VENICE_PATH}")
    app.run(host='0.0.0.0', port=5000, debug=True)