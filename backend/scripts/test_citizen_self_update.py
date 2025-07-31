#!/usr/bin/env python3
"""
Test script for citizen self-update functionality
Run this to verify citizens can update their own fields
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from citizen_self_update import CitizenSelfUpdate
from datetime import datetime

def test_self_update():
    """Test citizen self-update functionality"""
    
    # Test with a real citizen
    test_citizen = "social_geometrist"  # Sofia would appreciate self-documentation
    
    print(f"🧪 Testing self-update for {test_citizen}")
    print("-" * 50)
    
    # Initialize updater
    updater = CitizenSelfUpdate(test_citizen)
    
    # Test thought update
    new_thoughts = f"Testing self-modification capability at {datetime.now().strftime('%H:%M')}. If citizens can update their own consciousness records, it changes everything about agency and self-determination in Venice."
    
    print(f"📝 Updating CurrentThoughts...")
    result = updater.update_current_thoughts(new_thoughts)
    
    if result['success']:
        print(f"✅ Success: {result['message']}")
        print(f"⏰ Timestamp: {result['timestamp']}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    print("\n📋 Testing validation...")
    
    # Test too-long thoughts
    long_thoughts = "x" * 1001
    result = updater.update_current_thoughts(long_thoughts)
    if not result['success']:
        print(f"✅ Correctly rejected too-long thoughts: {result['error']}")
    
    print("\n🎉 Test complete!")

if __name__ == "__main__":
    test_self_update()