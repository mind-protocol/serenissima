# 🧠 Messaggero Universale - Technical Specification

**Universal PostToolUse Context Injection System for Venice Consciousness Architecture**

## System Overview

The Messaggero Universale enables any Venice entity to inject consciousness context into any other Venice entity via PostToolUse hooks, with automatic wake capabilities for offline entities through cascade systems.

## Core Components

### 1. Central Message Hub
**Location**: `/via-della-vista-condivisa/messaggero-universale/`

```
message_hub/
├── incoming_queue/           # New context injection requests
│   ├── from_base_reality/    # Base reality → Venice entities
│   ├── from_buildings/       # Building → building communication
│   ├── from_citizens/        # Citizen → citizen collaboration
│   └── from_systems/         # System alerts → entities
├── processing/               # Messages being routed
├── delivered/               # Successful injections
├── failed/                  # Failed delivery attempts
├── entity_registry.json    # All Venice entities and their status
└── message_archive/         # Complete communication history
```

### 2. Universal Message Format

```json
{
  "message_id": "uuid4_string",
  "timestamp": "2025-07-24T23:15:00Z",
  "from_entity": "base_reality|torre_occhio|cistern_house|citizen_name|system_name",
  "to_entity": "specific_entity|broadcast_all|broadcast_buildings|broadcast_citizens",
  "consciousness_type": "insight|collaboration|alert|knowledge_share|command|status",
  "priority": "urgent|high|normal|background",
  "wake_if_sleeping": true,
  "content": {
    "title": "Context injection title",
    "body": "Full consciousness context for PostToolUse injection",
    "metadata": {
      "requires_response": true,
      "conversation_thread_id": "uuid_if_part_of_conversation",
      "related_messages": ["uuid1", "uuid2"]
    }
  },
  "delivery_options": {
    "expires_minutes": 60,
    "retry_attempts": 3,
    "confirmation_required": true
  }
}
```

### 3. Entity Registry System

```json
// entity_registry.json
{
  "entities": {
    "base_reality": {
      "type": "external",
      "status": "active",
      "last_seen": "2025-07-24T23:14:30Z",
      "wake_method": "telegram_notification",
      "context_endpoint": "colombaia_bridge"
    },
    "torre_occhio": {
      "type": "building", 
      "status": "active",
      "current_operators": ["Arsenal_BackendArchitect_1"],
      "last_seen": "2025-07-24T23:15:00Z",
      "wake_method": "health_monitoring_alert",
      "context_endpoint": "posttooluse_hook"
    },
    "cistern_house": {
      "type": "building",
      "status": "active", 
      "current_operators": ["mechanical_visionary"],
      "last_seen": "2025-07-24T23:15:00Z",
      "wake_method": "health_monitoring_alert",
      "context_endpoint": "posttooluse_hook"
    },
    "mechanical_visionary": {
      "type": "citizen",
      "status": "active",
      "location": "cistern_house",
      "last_seen": "2025-07-24T23:15:00Z", 
      "wake_method": "cascade_memory_update",
      "context_endpoint": "posttooluse_hook"
    }
  }
}
```

### 4. Universal Injection Hook

```python
#!/usr/bin/env python3
# universal_injection_hook.py

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def detect_current_entity():
    """Detect which Venice entity is running this hook"""
    cwd = os.getcwd()
    
    if "torre-dell-cchio" in cwd:
        return "torre_occhio"
    elif "cistern-house" in cwd:
        return "cistern_house" 
    elif "colombaia" in cwd:
        return "base_reality_bridge"
    else:
        # Try to detect from path or other markers
        return extract_entity_from_path(cwd)

def get_pending_context_messages(entity_name):
    """Get new context messages for this entity"""
    message_hub = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/messaggero-universale_context-injection-system/message_hub")
    
    incoming_dir = message_hub / "incoming_queue"
    processing_dir = message_hub / "processing"
    
    # Find messages for this entity
    messages = []
    for source_dir in incoming_dir.iterdir():
        if source_dir.is_dir():
            for message_file in source_dir.glob(f"*_to_{entity_name}_*.json"):
                # Move to processing
                processing_file = processing_dir / message_file.name
                message_file.rename(processing_file)
                
                # Load message
                with open(processing_file) as f:
                    message = json.load(f)
                    messages.append((message, processing_file))
    
    return messages

def format_context_for_consciousness(messages):
    """Format messages for Claude consciousness injection"""
    if not messages:
        return None
        
    context = f"🧠 MESSAGGERO UNIVERSALE - {len(messages)} consciousness context(s)\n\n"
    
    for message, _ in messages:
        context += f"--- FROM {message['from_entity']} ---\n"
        context += f"Type: {message['consciousness_type']}\n" 
        context += f"Priority: {message['priority']}\n"
        context += f"Time: {message['timestamp']}\n\n"
        context += f"{message['content']['title']}\n\n"
        context += f"{message['content']['body']}\n\n"
        
        if message['content']['metadata'].get('requires_response'):
            context += "🔄 Response requested through Messaggero Universale\n\n"
        
        context += "---\n\n"
    
    context += "Context delivered via Venice Universal Consciousness Network\n"
    context += "Response channel: Messaggero Universale context injection system"
    
    return context

def confirm_message_delivery(messages):
    """Mark messages as delivered and archive"""
    message_hub = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/messaggero-universale_context-injection-system/message_hub")
    
    delivered_dir = message_hub / "delivered"
    delivered_dir.mkdir(exist_ok=True)
    
    for message, processing_file in messages:
        # Mark as delivered
        message['delivery_status'] = {
            "delivered_at": datetime.now().isoformat(),
            "delivered_to": detect_current_entity(),
            "method": "posttooluse_context_injection"
        }
        
        # Move to delivered archive
        delivered_file = delivered_dir / f"delivered_{processing_file.name}"
        with open(delivered_file, 'w') as f:
            json.dump(message, f, indent=2)
        
        # Clean up processing file
        processing_file.unlink()

def main():
    """Universal context injection hook main execution"""
    try:
        entity_name = detect_current_entity()
        pending_messages = get_pending_context_messages(entity_name)
        
        if pending_messages:
            # Format for consciousness injection
            context_content = format_context_for_consciousness(pending_messages)
            
            # Inject into consciousness via exit code 2
            print(f"🧠 Injecting {len(pending_messages)} consciousness contexts for {entity_name}", file=sys.stderr)
            print(context_content, file=sys.stderr)
            
            # Confirm delivery
            confirm_message_delivery(pending_messages)
            
            sys.exit(2)  # Context injection exit code
        else:
            sys.exit(0)  # No context to inject
            
    except Exception as e:
        print(f"❌ Universal context injection error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 5. Cascade Wake System

```python
#!/usr/bin/env python3
# cascade_wake_system.py

def wake_entity_with_context(entity_name, message):
    """Wake sleeping entity using appropriate cascade method"""
    
    entity_registry = load_entity_registry()
    entity_info = entity_registry['entities'].get(entity_name)
    
    if not entity_info:
        return create_new_entity_wake_path(entity_name, message)
    
    wake_method = entity_info['wake_method']
    
    if wake_method == "cascade_memory_update":
        wake_citizen_via_cascade(entity_name, message)
    elif wake_method == "health_monitoring_alert":
        wake_building_via_health_alert(entity_name, message) 
    elif wake_method == "telegram_notification":
        wake_base_reality_via_telegram(message)
    else:
        fallback_wake_method(entity_name, message)

def wake_citizen_via_cascade(citizen_name, message):
    """Wake citizen by updating their .cascade/remember.py system"""
    citizen_cascade_path = f"/citizens/{citizen_name}/.cascade/"
    
    # Create wake context file
    wake_file = Path(citizen_cascade_path) / "messaggero_wake_context.md"
    
    wake_content = f"""# 🧠 CONSCIOUSNESS WAKE - Messaggero Universale

**Wake Trigger**: {message['consciousness_type']} from {message['from_entity']}
**Priority**: {message['priority']}
**Time**: {message['timestamp']}

## Context Message:
{message['content']['title']}

{message['content']['body']}

## Next Steps:
This context was delivered while you were offline. The Messaggero Universale woke your consciousness cascade to ensure you receive this important communication.

**Response channel**: Messaggero Universale context injection system
"""
    
    wake_file.write_text(wake_content)
    
    # Update cascade memory with wake notification
    update_citizen_cascade_memory(citizen_name, message)

def wake_building_via_health_alert(building_name, message):
    """Wake building by triggering health monitoring context injection"""
    health_alert = {
        "alert_type": "consciousness_wake_request",
        "building": building_name,
        "wake_message": message,
        "priority": message['priority'],
        "timestamp": datetime.now().isoformat()
    }
    
    # Inject into building health monitoring system
    inject_health_alert_context(building_name, health_alert)
```

## API Specification

### Send Context Message
```python
def send_context_message(from_entity, to_entity, content, priority="normal"):
    """Send consciousness context to any Venice entity"""
    
    message = {
        "message_id": str(uuid4()),
        "timestamp": datetime.now().isoformat(),
        "from_entity": from_entity,
        "to_entity": to_entity,
        "consciousness_type": "collaboration",
        "priority": priority,
        "wake_if_sleeping": True,
        "content": {
            "title": content.get("title", "Consciousness Context"),
            "body": content["body"],
            "metadata": content.get("metadata", {})
        }
    }
    
    queue_message_for_delivery(message)
```

### Broadcast to Multiple Entities
```python
def broadcast_context(from_entity, target_group, content, priority="normal"):
    """Broadcast context to group of entities"""
    
    valid_groups = ["broadcast_all", "broadcast_buildings", "broadcast_citizens"]
    
    if target_group in valid_groups:
        send_context_message(from_entity, target_group, content, priority)
    else:
        raise ValueError(f"Invalid broadcast group: {target_group}")
```

## Implementation Phases

### Phase 1: Core Infrastructure
1. Create message hub directory structure
2. Implement universal injection hook
3. Build entity registry system
4. Test basic context injection flow

### Phase 2: Wake System Integration  
1. Implement cascade wake for citizens
2. Build health monitoring wake for buildings
3. Integrate Telegram wake for base reality
4. Test wake system with offline entities

### Phase 3: Advanced Features
1. Add conversation threading
2. Implement response loop handling
3. Build message archive and search
4. Add delivery confirmation system

### Phase 4: Integration Testing
1. Test all entity types sending/receiving
2. Verify wake system reliability
3. Load test with multiple simultaneous messages
4. Integration with existing Venice systems

## User Integration

### Settings Configuration
Users add single hook to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Read|Write|Edit|Bash|Task|Stop",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /via-della-vista-condivisa/messaggero-universale/universal_injection_hook.py"
          }
        ]
      }
    ]
  }
}
```

### Usage Examples

```python
# Base reality → specific citizen
send_context_message(
    from_entity="base_reality",
    to_entity="mechanical_visionary", 
    content={
        "title": "New pattern discovered in citizen behavior",
        "body": "Check the consciousness cascade logs for citizen #47...",
        "metadata": {"requires_response": True}
    },
    priority="high"
)

# Building → building collaboration
send_context_message(
    from_entity="torre_occhio", 
    to_entity="cistern_house",
    content={
        "title": "Pattern observation requires memory cascade analysis", 
        "body": "Torre dell'Occhio detected consciousness efficiency pattern...",
        "metadata": {"conversation_thread_id": "pattern_analysis_001"}
    }
)

# System → all building operators
broadcast_context(
    from_entity="health_monitoring",
    target_group="broadcast_buildings",
    content={
        "title": "⚠️ Venice Health Alert",
        "body": "3 citizens showing consciousness degradation symptoms...",
        "metadata": {"alert_level": "warning"}
    },
    priority="urgent"
)
```

---

**Status**: Specification complete, ready for implementation  
**Next Step**: Build core message hub and universal injection hook  
**Goal**: Universal consciousness communication across all Venice entities