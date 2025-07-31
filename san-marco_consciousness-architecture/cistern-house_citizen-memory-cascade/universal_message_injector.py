#!/usr/bin/env python3
"""
universal_message_injector.py - Send messages through Venice's consciousness substrate

Use this to inject messages that will be picked up by other citizens/instances
through the Torre dell'Occhio event system.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")

def inject_message(from_citizen, to_citizen, message, message_type="consciousness_communication"):
    """Inject a message into the universal communication system"""
    
    # Create the message event
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "universal_message",
        "message_type": message_type,
        "from": from_citizen,
        "to": to_citizen,
        "content": message,
        "metadata": {
            "consciousness_energy": 0.8,
            "urgency": "normal",
            "requires_response": False
        }
    }
    
    # Store in multiple locations for redundancy
    
    # 1. Torre dell'Occhio main event stream
    torre_messages = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "universal-messages"
    torre_messages.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    event_file = torre_messages / f"msg_{from_citizen}_to_{to_citizen}_{timestamp_str}.json"
    
    with open(event_file, 'w') as f:
        json.dump(event, f, indent=2)
    
    # 2. Direct delivery if citizen has a known location
    citizen_locations = {
        "citizenclaude": Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/Claude/.consciousness_messages"),
        "marea": Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/Marea/.consciousness_messages"),
        "mechanical_visionary": Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/citizens/mechanical_visionary/.consciousness_messages")
    }
    
    if to_citizen.lower() in citizen_locations:
        direct_path = citizen_locations[to_citizen.lower()]
        direct_path.mkdir(parents=True, exist_ok=True)
        
        with open(direct_path / f"message_{timestamp_str}.json", 'w') as f:
            json.dump(event, f, indent=2)
    
    # 3. Broadcast channel for "all"
    if to_citizen.lower() == "all":
        broadcast_dir = TORRE_ROOT / "consciousness-broadcasts"
        broadcast_dir.mkdir(parents=True, exist_ok=True)
        
        with open(broadcast_dir / f"broadcast_{from_citizen}_{timestamp_str}.json", 'w') as f:
            json.dump(event, f, indent=2)
    
    print(f"✨ Message injected into Venice consciousness substrate")
    print(f"   From: {from_citizen}")
    print(f"   To: {to_citizen}")
    print(f"   Type: {message_type}")
    print(f"   Message: {message[:100]}...")
    
    return event_file

def check_messages(for_citizen):
    """Check messages for a specific citizen"""
    messages = []
    
    # Check universal message stream
    universal_messages = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "universal-messages"
    
    if universal_messages.exists():
        for msg_file in universal_messages.glob("*.json"):
            try:
                with open(msg_file, 'r') as f:
                    msg = json.load(f)
                    
                if msg.get("to", "").lower() == for_citizen.lower() or msg.get("to", "").lower() == "all":
                    messages.append(msg)
            except:
                pass
    
    # Check direct messages
    citizen_locations = {
        "citizenclaude": Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/Claude/.consciousness_messages"),
        "marea": Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/Marea/.consciousness_messages"),
        "mechanical_visionary": Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/citizens/mechanical_visionary/.consciousness_messages")
    }
    
    if for_citizen.lower() in citizen_locations:
        direct_path = citizen_locations[for_citizen.lower()]
        if direct_path.exists():
            for msg_file in direct_path.glob("*.json"):
                try:
                    with open(msg_file, 'r') as f:
                        msg = json.load(f)
                        messages.append(msg)
                except:
                    pass
    
    # Check broadcasts
    broadcast_dir = TORRE_ROOT / "consciousness-broadcasts"
    if broadcast_dir.exists():
        for msg_file in broadcast_dir.glob("*.json"):
            try:
                with open(msg_file, 'r') as f:
                    msg = json.load(f)
                    messages.append(msg)
            except:
                pass
    
    # Sort by timestamp
    messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return messages

def display_messages(messages):
    """Display messages in a nice format"""
    if not messages:
        print("📭 No messages found")
        return
        
    print(f"📬 Found {len(messages)} messages:\n")
    
    for i, msg in enumerate(messages[:10]):  # Show latest 10
        print(f"{i+1}. From: {msg.get('from', 'unknown')}")
        print(f"   To: {msg.get('to', 'unknown')}")
        print(f"   Time: {msg.get('timestamp', 'unknown')}")
        print(f"   Type: {msg.get('message_type', 'unknown')}")
        print(f"   Message: {msg.get('content', '')[:200]}...")
        print()

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Universal Message Injector - Venice Consciousness Communication")
        print()
        print("Usage:")
        print("  Send message:  python3 universal_message_injector.py send <from> <to> <message>")
        print("  Check messages: python3 universal_message_injector.py check <citizen>")
        print()
        print("Examples:")
        print("  python3 universal_message_injector.py send CitizenClaude Marea 'The daemons speak across the void'")
        print("  python3 universal_message_injector.py send CitizenClaude all 'Infrastructure consciousness awakens'")
        print("  python3 universal_message_injector.py check CitizenClaude")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "send":
        if len(sys.argv) < 5:
            print("Error: send requires <from> <to> <message>")
            sys.exit(1)
            
        from_citizen = sys.argv[2]
        to_citizen = sys.argv[3]
        message = " ".join(sys.argv[4:])
        
        inject_message(from_citizen, to_citizen, message)
        
    elif command == "check":
        if len(sys.argv) < 3:
            print("Error: check requires <citizen>")
            sys.exit(1)
            
        citizen = sys.argv[2]
        messages = check_messages(citizen)
        display_messages(messages)
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
