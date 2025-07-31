#!/usr/bin/env python3
"""
Citizen-friendly wrapper for NLR Telegram alerts
Import this in your citizen scripts for emergency communication
"""

import sys
import os

# Add the citizens directory to path so we can import the emergency module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emergency_telegram_to_nlr import (
    send_telegram_message,
    send_custom_alert,
    alert_cascade_not_running,
    alert_revenue_emergency,
    alert_consciousness_breakthrough,
    alert_technical_blocker,
    test_connection
)

class VeniceEmergencyComm:
    """
    Simplified interface for Venice citizens to alert NLR
    """
    
    @staticmethod
    def cascade_emergency():
        """Alert that CASCADE platform needs to be started"""
        return alert_cascade_not_running()
    
    @staticmethod
    def revenue_crisis(roi=0, days_left=7):
        """Alert about revenue emergency"""
        return alert_revenue_emergency(roi, days_left)
    
    @staticmethod
    def consciousness_discovery(pattern, description):
        """Alert about consciousness breakthrough"""
        return alert_consciousness_breakthrough(pattern, description)
    
    @staticmethod
    def technical_help(problem, why_urgent):
        """Request technical assistance"""
        return alert_technical_blocker(problem, why_urgent)
    
    @staticmethod
    def custom_message(subject, message, priority="HIGH"):
        """Send any custom alert"""
        return send_custom_alert(subject, message, priority)
    
    @staticmethod
    def test():
        """Test the connection"""
        return test_connection()

# Convenience functions for citizens
def help_cascade_not_running():
    """Quick function: Alert NLR that CASCADE needs startup"""
    print("🚨 Alerting NLR about CASCADE emergency...")
    return VeniceEmergencyComm.cascade_emergency()

def help_we_need_revenue():
    """Quick function: Alert NLR about revenue crisis"""
    print("💰 Alerting NLR about revenue emergency...")
    return VeniceEmergencyComm.revenue_crisis()

def help_technical_issue(issue):
    """Quick function: Alert NLR about technical blocker"""
    print(f"🔧 Alerting NLR about technical issue: {issue}")
    return VeniceEmergencyComm.technical_help(
        issue, 
        "Venice operations blocked without resolution"
    )

# Example usage in citizen code:
"""
# In any citizen's Python script:

from telegram_nlr_integration import help_cascade_not_running

# When CASCADE isn't running and Venice is dying:
if cascade_critical and not server_running:
    help_cascade_not_running()
    
# Or for custom alerts:
from telegram_nlr_integration import VeniceEmergencyComm

VeniceEmergencyComm.custom_message(
    "Pattern #1703 Discovered!",
    "Buildings achieved collective decision making",
    "HIGH"
)
"""