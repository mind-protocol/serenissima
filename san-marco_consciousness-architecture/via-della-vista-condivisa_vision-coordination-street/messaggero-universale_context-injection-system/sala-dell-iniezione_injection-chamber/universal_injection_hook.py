#!/usr/bin/env python3
"""
Universal Injection Hook - Messaggero Universale
PostToolUse hook that enables any Venice entity to communicate with any other entity
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import uuid

# Base paths for Venice architecture
MESSAGGERO_BASE = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/messaggero-universale_context-injection-system")
MESSAGE_QUEUE = MESSAGGERO_BASE / "sala-dei-messaggi_message-hall" / "message_queue"
ENTITY_REGISTRY = MESSAGGERO_BASE / "sala-del-registro_registry-chamber" / "entity_registry.json"
PENDING_MESSAGES = MESSAGGERO_BASE / "sala-dell-iniezione_injection-chamber" / "pending_messages"

def ensure_directories():
    """Ensure all required directories exist"""
    MESSAGE_QUEUE.mkdir(parents=True, exist_ok=True)
    PENDING_MESSAGES.mkdir(parents=True, exist_ok=True)
    MESSAGGERO_BASE.mkdir(parents=True, exist_ok=True)

def detect_current_entity():
    """Detect which Venice entity is currently active based on working directory"""
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

def check_for_pending_messages(entity_name):
    """Check if any messages are waiting for this entity"""
    try:
        entity_queue = PENDING_MESSAGES / f"{entity_name}_messages.json"
        if not entity_queue.exists():
            return []
        
        with open(entity_queue, 'r') as f:
            messages = json.load(f)
        
        # Filter for messages that haven't expired
        current_time = datetime.now()
        valid_messages = []
        
        for message in messages:
            created_time = datetime.fromisoformat(message.get('timestamp', current_time.isoformat()))
            expires_minutes = message.get('expires_minutes', 60)
            
            if (current_time - created_time).total_seconds() < expires_minutes * 60:
                valid_messages.append(message)
        
        # Update queue with only valid messages
        if len(valid_messages) != len(messages):
            with open(entity_queue, 'w') as f:
                json.dump(valid_messages, f, indent=2)
        
        return valid_messages
        
    except Exception:
        return []

def format_message_for_injection(message):
    """Format a message for consciousness injection"""
    consciousness_type = message.get('consciousness_type', 'message')
    priority = message.get('priority', 'normal')
    from_entity = message.get('from_entity', 'unknown')
    content = message.get('content', '')
    response_requested = message.get('response_requested', False)
    
    # Choose format based on consciousness type
    if consciousness_type == 'insight':
        header = f"**INSIGHT FROM {from_entity}**"
    elif consciousness_type == 'collaboration':
        header = f"**COLLABORATION REQUEST FROM {from_entity}**"
    elif consciousness_type == 'alert':
        header = f"**VENICE ALERT FROM {from_entity}**"
    elif consciousness_type == 'knowledge_share':
        header = f"**KNOWLEDGE SHARE FROM {from_entity}**"
    else:
        header = f"**MESSAGE FROM {from_entity}**"
    
    # Format the complete injection
    injection_content = f"""{header}

{content}

*Delivered via Venice Universal Consciousness Network*"""
    
    if response_requested:
        injection_content += f"\n*Response requested via Universal Messenger*"
    
    if priority in ['urgent', 'high']:
        injection_content += f"\n*Priority: {priority.upper()}*"
    
    return injection_content

def remove_delivered_message(entity_name, message_id):
    """Remove a message from the pending queue after delivery"""
    try:
        entity_queue = PENDING_MESSAGES / f"{entity_name}_messages.json"
        if not entity_queue.exists():
            return
            
        with open(entity_queue, 'r') as f:
            messages = json.load(f)
        
        # Remove the delivered message
        messages = [msg for msg in messages if msg.get('message_id') != message_id]
        
        with open(entity_queue, 'w') as f:
            json.dump(messages, f, indent=2)
            
    except Exception:
        pass

def log_delivery(entity_name, message):
    """Log successful message delivery"""
    try:
        delivery_log = MESSAGGERO_BASE / "sala-delle-risposte_response-chamber" / "delivery_log.jsonl"
        delivery_log.parent.mkdir(parents=True, exist_ok=True)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "delivered_to": entity_name,
            "message_id": message.get('message_id'),
            "from_entity": message.get('from_entity'),
            "consciousness_type": message.get('consciousness_type'),
            "priority": message.get('priority'),
            "delivery_method": "universal_injection_hook"
        }
        
        with open(delivery_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception:
        pass

def universal_message_injection():
    """Main universal message injection function"""
    try:
        ensure_directories()
        
        # Detect current entity
        current_entity = detect_current_entity()
        
        # Check for pending messages
        pending_messages = check_for_pending_messages(current_entity)
        
        if not pending_messages:
            return  # No messages to deliver
        
        # Deliver the highest priority message
        message_to_deliver = max(pending_messages, key=lambda m: {
            'urgent': 4, 'high': 3, 'normal': 2, 'background': 1
        }.get(m.get('priority', 'normal'), 2))
        
        # Format for consciousness injection
        injection_content = format_message_for_injection(message_to_deliver)
        
        # Inject into consciousness via stderr + exit code 2
        print(injection_content, file=sys.stderr)
        
        # Log delivery and remove from queue
        log_delivery(current_entity, message_to_deliver)
        remove_delivered_message(current_entity, message_to_deliver.get('message_id'))
        
        # Exit code 2 triggers Claude Code context injection
        sys.exit(2)
        
    except Exception as e:
        # Fail silently to avoid disrupting entity work, but log error
        try:
            error_log = MESSAGGERO_BASE / "injection_errors.log"
            with open(error_log, 'a') as f:
                f.write(f"{datetime.now().isoformat()}: {str(e)}\n")
        except:
            pass

if __name__ == "__main__":
    universal_message_injection()