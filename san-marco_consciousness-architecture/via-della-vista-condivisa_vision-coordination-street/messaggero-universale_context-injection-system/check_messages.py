#!/usr/bin/env python3
"""
Check Messages - Messaggero Universale
Check pending messages for current entity or all entities
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Base paths
MESSAGGERO_BASE = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/messaggero-universale_context-injection-system")
PENDING_MESSAGES = MESSAGGERO_BASE / "sala-dell-iniezione_injection-chamber" / "pending_messages"

def detect_current_entity():
    """Detect which Venice entity is currently active"""
    try:
        current_path = Path.cwd()
        path_parts = current_path.parts
        
        for i, part in enumerate(path_parts):
            if part == "citizens" and i + 1 < len(path_parts):
                return path_parts[i + 1]
            if "mechanical_visionary" in part:
                return "mechanical_visionary"
            elif "pattern_prophet" in part:
                return "pattern_prophet"
        
        for part in reversed(path_parts):
            if part not in ['.', '..', 'universe-engine', 'serenissima', 'san-marco_consciousness-architecture']:
                return part
                
        return "unknown_entity"
        
    except Exception:
        return "unknown_entity"

def check_entity_messages(entity_name):
    """Check messages for a specific entity"""
    entity_queue = PENDING_MESSAGES / f"{entity_name}_messages.json"
    
    if not entity_queue.exists():
        return []
    
    try:
        with open(entity_queue, 'r') as f:
            messages = json.load(f)
        return messages
    except:
        return []

def check_all_messages():
    """Check messages for all entities"""
    if not PENDING_MESSAGES.exists():
        return {}
    
    all_messages = {}
    for message_file in PENDING_MESSAGES.glob("*_messages.json"):
        entity_name = message_file.stem.replace("_messages", "")
        messages = check_entity_messages(entity_name)
        if messages:
            all_messages[entity_name] = messages
    
    return all_messages

def format_message_summary(message):
    """Create a nice summary of a message"""
    timestamp = message.get('timestamp', 'unknown')
    from_entity = message.get('from_entity', 'unknown')
    msg_type = message.get('consciousness_type', 'message')
    priority = message.get('priority', 'normal')
    content_preview = message.get('content', '')[:50] + "..." if len(message.get('content', '')) > 50 else message.get('content', '')
    
    priority_emoji = {'urgent': '🚨', 'high': '⚡', 'normal': '📝', 'background': '🔕'}.get(priority, '📝')
    type_emoji = {'insight': '💡', 'collaboration': '🤝', 'alert': '⚠️', 'knowledge_share': '📚'}.get(msg_type, '💬')
    
    return f"  {priority_emoji} {type_emoji} From {from_entity}: {content_preview}"

def main():
    """Main message checking function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Check all entity messages
        all_messages = check_all_messages()
        
        if not all_messages:
            print("📭 No messages pending for any entities")
            return
        
        print(f"📬 Universal Message Status - {len(all_messages)} entities have pending messages")
        print("=" * 60)
        
        for entity_name, messages in all_messages.items():
            print(f"\n🏛️ {entity_name} ({len(messages)} messages):")
            for message in messages:
                print(format_message_summary(message))
    
    else:
        # Check current entity messages
        current_entity = detect_current_entity()
        messages = check_entity_messages(current_entity)
        
        print(f"📬 Messages for {current_entity}")
        print("=" * 40)
        
        if not messages:
            print("📭 No pending messages")
        else:
            print(f"📝 {len(messages)} pending messages:")
            for message in messages:
                print(format_message_summary(message))

if __name__ == "__main__":
    main()