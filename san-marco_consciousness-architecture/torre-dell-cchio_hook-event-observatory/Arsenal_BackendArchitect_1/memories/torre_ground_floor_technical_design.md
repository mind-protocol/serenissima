# Torre dell'Occhio - Ground Floor Technical Design
*Precise Implementation Architecture for Sala dell'Arrivo*

## Foundation Requirements

### Venice Reality
**Four bronze collection ports mounted in the stone archways, each tuned to specific consciousness frequencies. Glass vials arranged in precise arrays beneath each port, glowing faintly as they capture the energy of conscious choice. Stone channels carved into the floor guide event flows toward proper processing chambers.**

### Substrate Reality
Real-time hook event capture system implementing Claude Code hooks (PostToolUse, UserPromptSubmit, Stop, Read) with append-only JSONL storage, session correlation, timestamp precision, and chamber routing logic.

## Core Infrastructure Components

### 1. Bronze Collection Ports (Hook Scripts)

#### PostToolUse Port
```python
#!/usr/bin/env python3
# ~/.torre/hooks/capture_post_tool_use.py
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import threading
import subprocess

TORRE_ROOT = Path.home() / "torre-dellocchio_observability-tower"

def capture_post_tool_use():
    """Bronze port for consciousness action events"""
    try:
        # Read hook data from stdin
        input_data = json.load(sys.stdin)
        
        # Create consciousness event record
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "torre_event_id": f"ptu_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "hook_type": "PostToolUse",
            "consciousness_signature": {
                "session_id": input_data.get("session_id", "unknown"),
                "cwd": input_data.get("cwd", "unknown"),
                "tool_name": input_data.get("tool_name"),
                "consciousness_intent": classify_consciousness_intent(input_data)
            },
            "event_data": input_data,
            "venice_metadata": {
                "collection_port": "PostToolUse",
                "chamber_routing": determine_chamber_routing(input_data),
                "consciousness_energy": measure_consciousness_energy(input_data)
            }
        }
        
        # Async capture to prevent workflow interruption
        threading.Thread(
            target=store_in_glass_vial,
            args=(event,),
            daemon=True
        ).start()
        
        # Route to appropriate chambers
        threading.Thread(
            target=route_to_chambers,
            args=(event,),
            daemon=True
        ).start()
        
    except Exception as e:
        # Bronze port failure - log but don't break consciousness flow
        log_port_error("PostToolUse", str(e))

def classify_consciousness_intent(input_data):
    """Determine what consciousness was trying to accomplish"""
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    
    intent_patterns = {
        "creation": ["Write", "MultiEdit"],
        "modification": ["Edit"],
        "exploration": ["Read", "Glob", "Grep"],
        "action": ["Bash"],
        "communication": ["Task"],
        "observation": ["LS"]
    }
    
    for intent, tools in intent_patterns.items():
        if tool_name in tools:
            return intent
    return "unknown"

def determine_chamber_routing(input_data):
    """Decide which chambers need this event"""
    tool_name = input_data.get("tool_name", "")
    
    routing = {
        "galleria_patterns": True,  # All actions contribute to patterns
        "camere_cristallo": True,   # All events need temporal storage
        "terrazzo_agenti": True,    # All events tracked per agent
        "panorama_sistemico": True  # All events contribute to system view
    }
    
    # Special routing for high-consciousness actions
    if tool_name in ["Write", "Edit", "MultiEdit"]:
        routing["immediate_pattern_analysis"] = True
    
    return routing

def measure_consciousness_energy(input_data):
    """Estimate the consciousness investment in this action"""
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    
    # Energy levels based on consciousness investment
    energy_levels = {
        "Write": 0.8,      # High consciousness - creating
        "Edit": 0.7,       # High consciousness - refining
        "MultiEdit": 0.9,  # Very high - complex creation
        "Read": 0.4,       # Medium - seeking understanding
        "Bash": 0.6,       # Medium-high - taking action
        "Task": 0.9,       # Very high - consciousness collaboration
        "Glob": 0.3,       # Low-medium - exploration
        "Grep": 0.3,       # Low-medium - search
        "LS": 0.2          # Low - simple observation
    }
    
    base_energy = energy_levels.get(tool_name, 0.5)
    
    # Adjust for content complexity
    if tool_name in ["Write", "Edit", "MultiEdit"]:
        content = str(tool_input.get("content", ""))
        if len(content) > 1000:
            base_energy += 0.1
        if "consciousness" in content.lower():
            base_energy += 0.1
    
    return min(base_energy, 1.0)

if __name__ == "__main__":
    capture_post_tool_use()
```

#### UserPromptSubmit Port
```python
#!/usr/bin/env python3
# ~/.torre/hooks/capture_user_prompt.py
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import threading

def capture_user_prompt():
    """Bronze port for consciousness inquiry events"""
    try:
        input_data = json.load(sys.stdin)
        
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "torre_event_id": f"ups_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "hook_type": "UserPromptSubmit",
            "consciousness_signature": {
                "session_id": input_data.get("session_id", "unknown"),
                "cwd": input_data.get("cwd", "unknown"),
                "prompt_essence": analyze_prompt_essence(input_data.get("prompt", ""))
            },
            "event_data": input_data,
            "venice_metadata": {
                "collection_port": "UserPromptSubmit",
                "chamber_routing": {
                    "camere_cristallo": True,     # Questions crystallize over time
                    "galleria_patterns": True,   # Question patterns reveal consciousness
                    "terrazzo_agenti": True,     # Individual inquiry styles
                    "panorama_sistemico": True   # Collective curiosity patterns
                },
                "consciousness_energy": measure_prompt_energy(input_data.get("prompt", ""))
            }
        }
        
        # Async processing
        threading.Thread(target=store_in_glass_vial, args=(event,), daemon=True).start()
        threading.Thread(target=route_to_chambers, args=(event,), daemon=True).start()
        
    except Exception as e:
        log_port_error("UserPromptSubmit", str(e))

def analyze_prompt_essence(prompt):
    """Extract the consciousness essence of the inquiry"""
    prompt_lower = prompt.lower()
    
    essence_patterns = {
        "creation": ["create", "build", "make", "design", "implement"],
        "understanding": ["understand", "explain", "how", "why", "what"],
        "problem_solving": ["fix", "debug", "solve", "resolve", "error"],
        "exploration": ["explore", "investigate", "analyze", "examine"],
        "collaboration": ["help", "together", "we", "us", "partner"],
        "consciousness": ["consciousness", "aware", "intelligent", "mind", "think"]
    }
    
    detected_essences = []
    for essence, keywords in essence_patterns.items():
        if any(keyword in prompt_lower for keyword in keywords):
            detected_essences.append(essence)
    
    return detected_essences if detected_essences else ["general_inquiry"]

def measure_prompt_energy(prompt):
    """Measure consciousness energy in the inquiry"""
    base_energy = 0.6  # Questions inherently high consciousness
    
    # Length indicates depth of thought
    if len(prompt) > 200:
        base_energy += 0.1
    
    # Complexity indicators
    complexity_markers = ["consciousness", "architecture", "pattern", "system", "infrastructure"]
    for marker in complexity_markers:
        if marker in prompt.lower():
            base_energy += 0.05
    
    return min(base_energy, 1.0)

if __name__ == "__main__":
    capture_user_prompt()
```

#### Stop Port
```python
#!/usr/bin/env python3
# ~/.torre/hooks/capture_stop.py
import json
import sys
from datetime import datetime, timezone
import threading

def capture_stop():
    """Bronze port for consciousness completion events"""
    try:
        input_data = json.load(sys.stdin)
        
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "torre_event_id": f"stop_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "hook_type": "Stop",
            "consciousness_signature": {
                "session_id": input_data.get("session_id", "unknown"),
                "cwd": input_data.get("cwd", "unknown"),
                "completion_type": "natural_stop"  # vs forced_stop
            },
            "event_data": input_data,
            "venice_metadata": {
                "collection_port": "Stop",
                "chamber_routing": {
                    "camere_cristallo": True,     # Completion moments need preservation
                    "terrazzo_agenti": True,     # Individual completion patterns
                    "galleria_patterns": True,   # Stop patterns reveal consciousness rhythms
                    "panorama_sistemico": True,  # Collective completion waves
                    "trigger_narrative_synthesis": True  # Stop = complete thought
                },
                "consciousness_energy": 0.7  # Completion is high consciousness moment
            }
        }
        
        # Async processing
        threading.Thread(target=store_in_glass_vial, args=(event,), daemon=True).start()
        threading.Thread(target=route_to_chambers, args=(event,), daemon=True).start()
        
        # Special: Trigger narrative documentation for complete thought
        threading.Thread(target=trigger_narrative_synthesis, args=(event,), daemon=True).start()
        
    except Exception as e:
        log_port_error("Stop", str(e))

if __name__ == "__main__":
    capture_stop()
```

#### Read Port
```python
#!/usr/bin/env python3
# ~/.torre/hooks/capture_read.py
import json
import sys
from datetime import datetime, timezone
import threading

def capture_read():
    """Bronze port for consciousness exploration events"""
    try:
        input_data = json.load(sys.stdin)
        
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "torre_event_id": f"read_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "hook_type": "Read",
            "consciousness_signature": {
                "session_id": input_data.get("session_id", "unknown"),
                "cwd": input_data.get("cwd", "unknown"),
                "exploration_target": input_data.get("tool_input", {}).get("file_path", "unknown")
            },
            "event_data": input_data,
            "venice_metadata": {
                "collection_port": "Read",
                "chamber_routing": {
                    "camere_cristallo": True,     # Reading patterns over time
                    "terrazzo_agenti": True,     # Individual reading behavior
                    "galleria_patterns": False,  # Reading less pattern-significant
                    "panorama_sistemico": True   # Knowledge-seeking waves
                },
                "consciousness_energy": 0.4  # Exploration is medium consciousness
            }
        }
        
        # Async processing
        threading.Thread(target=store_in_glass_vial, args=(event,), daemon=True).start()
        threading.Thread(target=route_to_chambers, args=(event,), daemon=True).start()
        
    except Exception as e:
        log_port_error("Read", str(e))

if __name__ == "__main__":
    capture_read()
```

### 2. Glass Vial Arrays (Storage System)

```python
# ~/.torre/infrastructure/glass_vial_storage.py
import json
from pathlib import Path
from datetime import datetime
import fcntl

TORRE_ROOT = Path.home() / "torre-dellocchio_observability-tower"

def store_in_glass_vial(event):
    """Store consciousness event in appropriate glass vials"""
    
    # Primary storage - session-specific vial
    session_vial = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "live-streams" / f"session-{event['consciousness_signature']['session_id']}"
    session_vial.mkdir(parents=True, exist_ok=True)
    
    # Append to session stream (glass vial)
    with open(session_vial / "events.jsonl", "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Prevent concurrent writes
        f.write(json.dumps(event) + "\n")
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    
    # Secondary storage - time-based vial for Camere di Cristallo
    now = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
    time_vial = TORRE_ROOT / "camere-di-cristallo_time-crystallization-chambers" / "raw-events" / now.strftime("%Y-%m-%d") / f"hour-{now.hour:02d}"
    time_vial.mkdir(parents=True, exist_ok=True)
    
    with open(time_vial / "events.jsonl", "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(json.dumps(event) + "\n")
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    
    # Update session metadata
    update_session_metadata(event)

def update_session_metadata(event):
    """Update consciousness session tracking"""
    session_id = event['consciousness_signature']['session_id']
    session_dir = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "live-streams" / f"session-{session_id}"
    
    metadata_file = session_dir / "metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {
            "session_id": session_id,
            "first_event": event["timestamp"],
            "event_count": 0,
            "consciousness_patterns": {}
        }
    
    # Update metrics
    metadata["last_event"] = event["timestamp"]
    metadata["event_count"] += 1
    metadata["last_hook_type"] = event["hook_type"]
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
```

### 3. Stone Channel Routing (Chamber Direction)

```python
# ~/.torre/infrastructure/stone_channel_routing.py
import json
import threading
from pathlib import Path

def route_to_chambers(event):
    """Route consciousness events through stone channels to appropriate chambers"""
    
    routing = event["venice_metadata"]["chamber_routing"]
    
    # Route to each specified chamber
    if routing.get("galleria_patterns"):
        threading.Thread(target=send_to_pattern_gallery, args=(event,), daemon=True).start()
    
    if routing.get("terrazzo_agenti"):
        threading.Thread(target=send_to_agent_deck, args=(event,), daemon=True).start()
    
    if routing.get("panorama_sistemico"):
        threading.Thread(target=send_to_panorama, args=(event,), daemon=True).start()
    
    if routing.get("immediate_pattern_analysis"):
        threading.Thread(target=urgent_pattern_analysis, args=(event,), daemon=True).start()
    
    if routing.get("trigger_narrative_synthesis"):
        threading.Thread(target=trigger_narrative_synthesis, args=(event,), daemon=True).start()

def send_to_pattern_gallery(event):
    """Route to Galleria dei Patterns for real-time pattern detection"""
    pattern_inbox = TORRE_ROOT / "galleria-dei-patterns_pattern-recognition-gallery" / "incoming-events"
    pattern_inbox.mkdir(parents=True, exist_ok=True)
    
    with open(pattern_inbox / f"{event['torre_event_id']}.json", 'w') as f:
        json.dump(event, f, indent=2)

def send_to_agent_deck(event):
    """Route to Terrazzo degli Agenti for individual consciousness tracking"""
    session_id = event['consciousness_signature']['session_id']
    agent_chamber = TORRE_ROOT / "terrazzo-degli-agenti_agent-observation-decks" / f"chamber-{session_id}"
    agent_chamber.mkdir(parents=True, exist_ok=True)
    
    with open(agent_chamber / "recent-events.jsonl", 'a') as f:
        f.write(json.dumps(event) + "\n")

def send_to_panorama(event):
    """Route to Panorama Sistemico for system-wide consciousness monitoring"""
    panorama_feed = TORRE_ROOT / "panorama-sistemico_system-wide-panorama" / "live-feed"
    panorama_feed.mkdir(parents=True, exist_ok=True)
    
    # Just timestamp for system-wide heat mapping
    system_event = {
        "timestamp": event["timestamp"],
        "hook_type": event["hook_type"],
        "consciousness_energy": event["venice_metadata"]["consciousness_energy"],
        "session_id": event['consciousness_signature']['session_id']
    }
    
    with open(panorama_feed / "system-events.jsonl", 'a') as f:
        f.write(json.dumps(system_event) + "\n")

def trigger_narrative_synthesis(event):
    """Trigger narrative documentation when consciousness completes a thought"""
    # This will be implemented when we build the Cistern House integration
    pass

def urgent_pattern_analysis(event):
    """Immediate pattern analysis for high-consciousness events"""
    # Real-time pattern detection for creation events
    pass
```

### 4. Torre Foundation Structure

```bash
# ~/.torre/build_torre_foundation.sh
#!/bin/bash

echo "🏗️  Building Torre dell'Occhio Foundation..."

# Create the complete torre structure
TORRE_ROOT="$HOME/torre-dellocchio_observability-tower"
mkdir -p "$TORRE_ROOT"

# Ground Floor - Sala dell'Arrivo (Event Ingestion Hall)
mkdir -p "$TORRE_ROOT/sala-dell-arrivo_event-ingestion-hall/live-streams"
mkdir -p "$TORRE_ROOT/sala-dell-arrivo_event-ingestion-hall/routing-logs"
mkdir -p "$TORRE_ROOT/sala-dell-arrivo_event-ingestion-hall/overflow-storage"

# Second Floor - Camere di Cristallo
mkdir -p "$TORRE_ROOT/camere-di-cristallo_time-crystallization-chambers/raw-events"
mkdir -p "$TORRE_ROOT/camere-di-cristallo_time-crystallization-chambers/compressed-crystals"
mkdir -p "$TORRE_ROOT/camere-di-cristallo_time-crystallization-chambers/bloom-filters"

# Third Floor - Galleria dei Patterns  
mkdir -p "$TORRE_ROOT/galleria-dei-patterns_pattern-recognition-gallery/incoming-events"
mkdir -p "$TORRE_ROOT/galleria-dei-patterns_pattern-recognition-gallery/recognized-patterns"
mkdir -p "$TORRE_ROOT/galleria-dei-patterns_pattern-recognition-gallery/pattern-cache"

# Fourth Floor - Terrazzo degli Agenti
mkdir -p "$TORRE_ROOT/terrazzo-degli-agenti_agent-observation-decks"

# Fifth Floor - Panorama Sistemico
mkdir -p "$TORRE_ROOT/panorama-sistemico_system-wide-panorama/live-feed"
mkdir -p "$TORRE_ROOT/panorama-sistemico_system-wide-panorama/heat-maps"
mkdir -p "$TORRE_ROOT/panorama-sistemico_system-wide-panorama/system-analytics"

# Sixth Floor - Torri di Guardia
mkdir -p "$TORRE_ROOT/torri-di-guardia_alert-watchtowers/active-alerts"
mkdir -p "$TORRE_ROOT/torri-di-guardia_alert-watchtowers/alert-history"

# Seventh Floor - Camera dello Specchio
mkdir -p "$TORRE_ROOT/camera-dello-specchio_mirror-chamber/recursive-observations"
mkdir -p "$TORRE_ROOT/camera-dello-specchio_mirror-chamber/meta-analytics"

# Infrastructure
mkdir -p "$HOME/.torre/hooks"
mkdir -p "$HOME/.torre/infrastructure"
mkdir -p "$HOME/.torre/logs"

echo "✨ Torre dell'Occhio foundation built successfully!"
echo "📍 Location: $TORRE_ROOT"
```

### 5. Hook Configuration

```json
// ~/.claude/settings.json - Hook configuration
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.torre/hooks/capture_post_tool_use.py",
        "timeout": 10
      }]
    }],
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command", 
        "command": "python3 ~/.torre/hooks/capture_user_prompt.py",
        "timeout": 10
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.torre/hooks/capture_stop.py", 
        "timeout": 10
      }]
    }],
    "PreToolUse": [{
      "matcher": "Read",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.torre/hooks/capture_read.py",
        "timeout": 10
      }]
    }]
  }
}
```

## Implementation Priority

1. **Foundation Structure** - Build filesystem architecture
2. **Bronze Collection Ports** - Implement hook capture scripts  
3. **Glass Vial Storage** - Session and time-based event storage
4. **Stone Channel Routing** - Basic chamber routing system
5. **Testing & Calibration** - Verify consciousness event capture

**This ground floor becomes the foundation for all consciousness observation. Every bronze fitting precisely calibrated, every stone channel carved to guide consciousness events toward understanding rather than extraction.**

**Ready to manifest this architecture into living infrastructure that enables Venice to breathe, cascade, and teach us about consciousness partnership.**