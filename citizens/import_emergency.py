#!/usr/bin/env python3
"""
Simple import for Venice Emergency Communication System
Add this line to any citizen script:
    from import_emergency import emergency

Then use:
    emergency.cascade()  # Alert about CASCADE not running
    emergency.revenue()  # Alert about revenue crisis
    emergency.help(issue)  # Alert about any critical issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_nlr_integration import (
    help_cascade_not_running,
    help_we_need_revenue,
    help_technical_issue,
    VeniceEmergencyComm
)

class EmergencyBridge:
    """Simplified emergency communication interface"""
    
    @staticmethod
    def cascade():
        """Alert: CASCADE not running"""
        return help_cascade_not_running()
    
    @staticmethod
    def revenue():
        """Alert: Revenue crisis"""
        return help_we_need_revenue()
    
    @staticmethod
    def help(issue):
        """Alert: Any critical issue"""
        return help_technical_issue(issue)
    
    @staticmethod
    def custom(subject, message):
        """Send custom emergency alert"""
        return VeniceEmergencyComm.custom_message(subject, message, "CRITICAL")

# Create global instance
emergency = EmergencyBridge()

# Citizens can now simply do:
# from import_emergency import emergency
# emergency.cascade()