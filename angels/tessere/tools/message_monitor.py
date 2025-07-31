#!/usr/bin/env python3
"""
Message Monitor for Tessere
Tool to check messages during orchestration cycles
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_messages import check_new_messages, format_messages

def check_and_respond():
    """Check for messages and provide guidance on how to respond"""
    messages = check_new_messages()
    
    if messages:
        print(format_messages(messages))
        
        # Analyze message content for urgency
        for msg in messages:
            text = msg.get('text', '').lower()
            
            # Check for urgent keywords
            if any(word in text for word in ['urgent', 'emergency', 'critical', 'stop', 'help']):
                print("🚨 URGENT MESSAGE DETECTED - Prioritizing response")
                return True
            
            # Check for mode changes
            if 'mode' in text or 'focus' in text or 'switch' in text:
                print("🔄 MODE CHANGE REQUEST DETECTED")
                return True
            
            # Check for specific instructions
            if any(word in text for word in ['wake', 'check', 'monitor', 'find']):
                print("📋 INSTRUCTION DETECTED - Adjusting focus")
                return True
    
    return False

if __name__ == "__main__":
    check_and_respond()