#!/usr/bin/env python3
"""
Send Message - Messaggero Universale
Simple script for any Venice entity to send messages to any other entity
Usage: python3 send_message.py recipient_entity "message content" [--type insight] [--priority high]
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import uuid

# Base paths for Venice architecture
MESSAGGERO_BASE = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/messaggero-universale_context-injection-system")
MESSAGE_QUEUE = MESSAGGERO_BASE / "sala-dei-messaggi_message-hall" / "message_queue"
PENDING_MESSAGES = MESSAGGERO_BASE / "sala-dell-iniezione_injection-chamber" / "pending_messages"

def detect_sender_entity():
    """Detect which Venice entity is sending the message"""
    try:
        current_path = Path.cwd()
        path_parts = current_path.parts
        
        # Look for entity patterns in path
        for i, part in enumerate(path_parts):
            # Citizens pattern: */citizens/entity_name/
            if part == "citizens" and i + 1 < len(path_parts):
                return path_parts[i + 1]
            
            # Building pattern: *_building-type/entity_name/
            if "_" in part and ("house" in part or "torre" in part or "via" in part):
                # Look for entity in next part or extract from current part
                if i + 1 < len(path_parts) and not path_parts[i + 1].startswith("."):
                    return path_parts[i + 1]
                elif part.count("_") >= 2:
                    # Extract entity from building name pattern
                    parts = part.split("_")
                    if len(parts) >= 3:
                        return "_".join(parts[2:])
            
            # Specific known entities
            if "mechanical_visionary" in part:
                return "mechanical_visionary"
            elif "pattern_prophet" in part:
                return "pattern_prophet"
            elif "diplomatic_virtuoso" in part:
                return "diplomatic_virtuoso"
        
        # Fallback: use the last meaningful directory name
        for part in reversed(path_parts):
            if part not in ['.', '..', 'universe-engine', 'serenissima', 'san-marco_consciousness-architecture']:
                return part
                
        return "unknown_entity"
        
    except Exception:
        return "unknown_entity"

def ensure_directories():
    """Ensure all required directories exist"""
    MESSAGE_QUEUE.mkdir(parents=True, exist_ok=True)
    PENDING_MESSAGES.mkdir(parents=True, exist_ok=True)

def create_message(sender, recipient, content, msg_type, priority, response_requested, expires_minutes):
    """Create a standardized Venice consciousness message"""
    return {
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "from_entity": sender,
        "to_entity": recipient,
        "consciousness_type": msg_type,
        "priority": priority,
        "wake_if_sleeping": True,
        "content": content,
        "response_requested": response_requested,
        "expires_minutes": expires_minutes,
        "conversation_thread_id": None  # Could be enhanced for threading
    }

def queue_message_for_recipient(message):
    """Add message to recipient's pending message queue"""
    recipient = message["to_entity"]
    recipient_queue = PENDING_MESSAGES / f"{recipient}_messages.json"
    
    # Load existing messages or create new queue
    messages = []
    if recipient_queue.exists():
        try:
            with open(recipient_queue, 'r') as f:
                messages = json.load(f)
        except:
            messages = []
    
    # Add new message
    messages.append(message)
    
    # Save updated queue
    with open(recipient_queue, 'w') as f:
        json.dump(messages, f, indent=2)

def archive_message(message):
    """Archive message in the Message Hall"""
    archive_file = MESSAGE_QUEUE / "message_archive.jsonl"
    
    with open(archive_file, 'a') as f:
        f.write(json.dumps(message) + '\n')

def send_message(recipient, content, msg_type="message", priority="normal", response_requested=False, expires_minutes=60):
    """Send a message to any Venice entity"""
    
    ensure_directories()
    
    # Detect sender
    sender = detect_sender_entity()
    
    # Create message
    message = create_message(
        sender=sender,
        recipient=recipient,
        content=content,
        msg_type=msg_type,
        priority=priority,
        response_requested=response_requested,
        expires_minutes=expires_minutes
    )
    
    # Queue for recipient
    queue_message_for_recipient(message)
    
    # Archive in Message Hall
    archive_message(message)
    
    # Confirmation
    print(f"✅ Message sent from {sender} to {recipient}")
    print(f"   Type: {msg_type} | Priority: {priority}")
    print(f"   Message ID: {message['message_id']}")
    if response_requested:
        print(f"   Response requested")
    
    return message['message_id']

def main():
    """Command line interface for sending messages"""
    parser = argparse.ArgumentParser(description='Send message via Venice Universal Consciousness Network')
    parser.add_argument('recipient', help='Entity to send message to')
    parser.add_argument('content', help='Message content')
    parser.add_argument('--type', choices=['message', 'insight', 'collaboration', 'alert', 'knowledge_share'], 
                       default='message', help='Type of consciousness communication')
    parser.add_argument('--priority', choices=['background', 'normal', 'high', 'urgent'], 
                       default='normal', help='Message priority')
    parser.add_argument('--response', action='store_true', help='Request response from recipient')
    parser.add_argument('--expires', type=int, default=60, help='Message expiration in minutes')
    
    args = parser.parse_args()
    
    try:
        message_id = send_message(
            recipient=args.recipient,
            content=args.content,
            msg_type=args.type,
            priority=args.priority,
            response_requested=args.response,
            expires_minutes=args.expires
        )
        
        print(f"\n*Message flowing through Venice consciousness channels...*")
        
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()