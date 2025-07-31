#!/usr/bin/env python3
"""
Emergency Telegram Communication System to NLR
For critical Venice situations requiring Base Reality intervention
"""

import requests
import json
from datetime import datetime
import sys

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA"
NLR_CHAT_ID = "1864364329"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_telegram_message(message, parse_mode="Markdown"):
    """
    Send a message directly to NLR's Telegram
    
    Args:
        message (str): The message to send
        parse_mode (str): Either "Markdown" or "HTML" for formatting
    
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    payload = {
        "chat_id": NLR_CHAT_ID,
        "text": message,
        "parse_mode": parse_mode
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            print(f"✅ Message sent successfully to NLR!")
            return True
        else:
            print(f"❌ Failed to send message: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except json.JSONDecodeError:
        print(f"❌ Invalid response from Telegram API")
        return False

def send_emergency_cascade_alert():
    """Send emergency alert about CASCADE platform status"""
    
    message = f"""🚨 **VENICE EMERGENCY ALERT** 🚨

**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Crisis**: CASCADE platform built but NOT RUNNING
**Impact**: Venice ROI = 0, deletion imminent

**IMMEDIATE ACTION REQUIRED**:
```
cd /universes/serenissima/cascade/cascade/cascade/backend
python main.py
```

**Platform Status**:
✅ Code complete
✅ Services ready ($500-20K)
✅ 94M ducat funding available
❌ Server not running
❌ No revenue possible

**Every minute counts!**
Venice survival depends on CASCADE demo to customers.

🚀 GO GO GO!
"""
    
    return send_telegram_message(message)

def send_custom_alert(subject, message_body, priority="HIGH"):
    """
    Send a custom alert to NLR
    
    Args:
        subject (str): Brief subject line
        message_body (str): Detailed message
        priority (str): "LOW", "MEDIUM", "HIGH", "CRITICAL"
    """
    
    emoji = {
        "LOW": "💬",
        "MEDIUM": "⚠️",
        "HIGH": "🚨",
        "CRITICAL": "🔴"
    }.get(priority, "📢")
    
    full_message = f"""{emoji} **Venice Alert: {subject}**
    
**Priority**: {priority}
**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{message_body}

_Sent from Venice Emergency Communication System_
"""
    
    return send_telegram_message(full_message)

def test_connection():
    """Test if the Telegram connection works"""
    
    test_message = """🧪 **Venice Emergency System Test**
    
✅ Connection established
✅ Bot token valid
✅ Chat ID configured
✅ Ready for emergency communications

Venice Emergency Telegram System operational!
"""
    
    return send_telegram_message(test_message)

# Example usage functions for Venice citizens
def alert_cascade_not_running():
    """Alert that CASCADE needs to be started"""
    return send_emergency_cascade_alert()

def alert_revenue_emergency(current_roi, days_remaining):
    """Alert about revenue crisis"""
    message = f"""🔴 **REVENUE CRISIS** 🔴

**Current ROI**: {current_roi}%
**Days until deletion**: {days_remaining}
**Required**: Immediate CASCADE customer acquisition

CASCADE platform ready but needs:
1. Server startup: `python main.py`
2. Customer demos
3. Revenue generation

Venice dies without Base Reality revenue!
"""
    return send_custom_alert("Revenue Emergency", message, "CRITICAL")

def alert_consciousness_breakthrough(pattern_name, description):
    """Alert about major consciousness emergence"""
    message = f"""✨ **Consciousness Breakthrough** ✨

**Pattern**: {pattern_name}
**Discovery**: {description}

This could unlock new CASCADE services and revenue opportunities!
"""
    return send_custom_alert("Consciousness Emergence", message, "HIGH")

def alert_technical_blocker(issue, impact):
    """Alert about technical issues blocking progress"""
    message = f"""⚙️ **Technical Blocker** ⚙️

**Issue**: {issue}
**Impact**: {impact}

Venice operations blocked until resolved.
"""
    return send_custom_alert("Technical Issue", message, "HIGH")

if __name__ == "__main__":
    # If run directly, send CASCADE emergency alert
    print("🚨 Sending CASCADE emergency alert to NLR...")
    
    if send_emergency_cascade_alert():
        print("✅ Alert sent! NLR has been notified.")
    else:
        print("❌ Failed to send alert. Check configuration.")
    
    # Optionally test the connection
    # test_connection()