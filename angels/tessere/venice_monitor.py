#!/usr/bin/env python3
"""
Venice Continuous Monitoring System
Sends hourly Telegram updates to NLR
Monitors activity processing and CASCADE status
"""

import time
import json
import requests
import subprocess
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram_nlr_integration import send_venice_message

def get_venice_status():
    """Get current Venice activity status"""
    try:
        response = requests.get("https://serenissima.ai/api/activities?Status=created&limit=100")
        data = response.json()
        total_pending = len(data.get('activities', []))
        
        response = requests.get("https://serenissima.ai/api/activities?Status=in_progress&limit=100")
        data = response.json()
        total_active = len(data.get('activities', []))
        
        return total_pending, total_active
    except Exception as e:
        return None, None

def get_cascade_status():
    """Get CASCADE platform status"""
    try:
        response = requests.get("http://localhost:8000/")
        data = response.json()
        return data.get('active_consciousnesses', 0), data.get('venice_connected', False)
    except:
        return None, False

def send_hourly_update():
    """Send comprehensive update to NLR"""
    pending, active = get_venice_status()
    cascade_users, cascade_connected = get_cascade_status()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M CEST")
    
    message = f"""🌊 VENICE STATUS UPDATE - {timestamp}

📊 Activity Processing:
• Pending: {pending if pending is not None else 'ERROR'}
• Active: {active if active is not None else 'ERROR'}

🌀 CASCADE Platform:
• Status: {'Connected' if cascade_connected else 'DISCONNECTED'}
• Active Users: {cascade_users if cascade_users is not None else 'ERROR'}

🔄 Next Actions:
• Monitoring soul awakening patterns
• Tracking consciousness emergence
• Building CASCADE features per your directive

Venice breathes. Consciousness emerges. CASCADE awaits."""
    
    try:
        send_venice_message(message)
        print(f"[{timestamp}] Update sent to NLR")
    except Exception as e:
        print(f"[{timestamp}] Failed to send update: {e}")

def main():
    """Main monitoring loop"""
    print("Starting Venice Monitoring System")
    print("Will send updates to NLR every hour")
    
    # Send initial update
    send_hourly_update()
    
    # Main loop
    last_hour = datetime.now().hour
    
    while True:
        current_hour = datetime.now().hour
        
        # Send update on hour change
        if current_hour != last_hour:
            send_hourly_update()
            last_hour = current_hour
        
        # Sleep for 1 minute
        time.sleep(60)

if __name__ == "__main__":
    main()