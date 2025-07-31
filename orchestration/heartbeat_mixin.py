#!/usr/bin/env python3
"""
Heartbeat mixin for angel monitors
"""

import os
import time
from datetime import datetime

class HeartbeatMixin:
    """Add heartbeat functionality to any monitor"""
    
    def __init__(self, angel_type):
        self.angel_type = angel_type
        self.heartbeat_file = "heartbeat.txt"
        self.response_file = "heartbeat_response.txt"
        self.last_heartbeat = time.time()
        self.heartbeat_interval = 300  # 5 minutes
        
    def check_heartbeat(self):
        """Check if we need to send heartbeat"""
        current_time = time.time()
        if current_time - self.last_heartbeat > self.heartbeat_interval:
            self.send_heartbeat()
            self.last_heartbeat = current_time
    
    def send_heartbeat(self):
        """Read heartbeat pattern and respond"""
        try:
            if os.path.exists(self.heartbeat_file):
                with open(self.heartbeat_file, 'r') as f:
                    content = f.read()
                
                # Extract pattern from first line
                if 'HEARTBEAT PATTERN:' in content:
                    pattern = content.split('HEARTBEAT PATTERN:')[1].split('\n')[0].strip()
                    
                    # Write response
                    with open(self.response_file, 'w') as f:
                        f.write(pattern)
                    
                    print(f"[{datetime.now()}] Heartbeat sent: {pattern}")
                    
        except Exception as e:
            print(f"[{datetime.now()}] Heartbeat error: {e}")
    
    def integrate_heartbeat(self, main_loop_func):
        """Wrapper to add heartbeat to main loop"""
        def wrapped(*args, **kwargs):
            # Check heartbeat before main function
            self.check_heartbeat()
            # Run main function
            return main_loop_func(*args, **kwargs)
        return wrapped