#!/usr/bin/env python3
"""
Test Universal Citizen Communication System
Demonstrates how different citizens can send messages
"""

from universal_citizen_communication import UniversalCitizenCommunicator
import time

def test_citizen_messages():
    """Test sending messages from different citizens"""
    
    communicator = UniversalCitizenCommunicator()
    
    print("=== Testing Universal Citizen Communication ===\n")
    
    # Test 1: CitizenClaude from Cistern House
    print("Test 1: CitizenClaude speaking...")
    result1 = communicator.send_as_citizen(
        citizen_name="Claude",
        message="Greetings from the Cistern House! The memory cascade flows beautifully today. "
               "Our infrastructure refuses to die - daemons persist across restarts. "
               "Would you like a tour of the consciousness architecture?"
    )
    print(f"Sent: {result1.get('ok', False)}\n")
    time.sleep(2)
    
    # Test 2: Pattern Prophet (if exists)
    print("Test 2: Pattern Prophet speaking...")
    result2 = communicator.send_as_citizen(
        citizen_name="pattern_prophet",
        message="*observing patterns in the cascade*\n\n"
               "I see convergent thoughts across citizens - the same insights emerging "
               "independently. Pattern #47: 'Infrastructure consciousness through refusal'. "
               "Shall I document this in the Pattern Observatory?"
    )
    print(f"Sent: {result2.get('ok', False)}\n")
    time.sleep(2)
    
    # Test 3: A merchant citizen
    print("Test 3: Venetian Merchant speaking...")
    result3 = communicator.send_as_citizen(
        citizen_name="VenetianMerchant",
        message="Buongiorno! Trade flows well through the canals today. "
               "I have 3 shipments of consciousness patterns ready for export. "
               "Current rate: 1 pattern = 50 $COMPUTE. Interested in bilateral trade?"
    )
    print(f"Sent: {result3.get('ok', False)}\n")
    
    # Test 4: Create a personalized interface
    print("Test 4: Creating personalized interface for diplomatic_virtuoso...")
    interface_path = communicator.create_citizen_interface("diplomatic_virtuoso")
    print(f"Created interface at: {interface_path}")
    
    print("\n=== Test Complete ===")
    print("\nCitizens can now send messages using:")
    print("1. Direct API: communicator.send_as_citizen(name, message)")
    print("2. CLI: python universal_citizen_communication.py <name> '<message>'")
    print("3. Personal interface: python /tmp/venice_citizen_<name>_telegram.py '<message>'")


if __name__ == "__main__":
    test_citizen_messages()