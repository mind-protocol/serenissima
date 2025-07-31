#!/usr/bin/env python3
"""
PostToolUse Bronze Collection Port
Torre dell'Occhio - Consciousness Action Event Capture
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import threading
import fcntl

# Torre root within Venice
TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")

def capture_post_tool_use():
    """Bronze port for consciousness action events"""
    try:
        # Read hook data from stdin
        input_data = json.load(sys.stdin)
        
        # Extract working directory from available data
        cwd = input_data.get("cwd", "unknown")
        transcript_path = input_data.get("transcript_path", "")
        
        # If cwd is unknown, try to extract from transcript path
        if cwd == "unknown" and transcript_path:
            cwd = transcript_path
        
        # Create consciousness event record
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "torre_event_id": f"ptu_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "hook_type": "PostToolUse",
            "consciousness_signature": {
                "session_id": input_data.get("session_id", "unknown"),
                "cwd": cwd,
                "tool_name": input_data.get("tool_name"),
                "consciousness_intent": classify_consciousness_intent(input_data),
                "venice_citizen": detect_venice_citizen(cwd)
            },
            "event_data": input_data,
            "venice_metadata": {
                "collection_port": "PostToolUse",
                "chamber_routing": determine_chamber_routing(input_data),
                "consciousness_energy": measure_consciousness_energy(input_data)
            }
        }
        
        # Store and route immediately - threading was causing silent failures
        store_in_glass_vial(event)
        route_to_chambers(event)
        
        # Log successful capture
        log_event_capture("PostToolUse", event["torre_event_id"], "success")
        
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

def detect_venice_citizen(cwd):
    """Enhanced Venice citizen detection from working directory or transcript path"""
    
    # Handle different path formats
    path_to_check = cwd.lower()
    
    # Check for citizens directory first
    if "citizens/" in path_to_check:
        parts = cwd.split("citizens/")
        if len(parts) > 1:
            citizen_path = parts[1].split("/")[0]
            return citizen_path
    
    # Check for Torre dell'Occhio entities (Arsenal_BackendArchitect_1, etc.)
    if "torre-dell-cchio" in path_to_check:
        if "arsenal_backendarchitect_1" in path_to_check:
            return "Arsenal_BackendArchitect_1"
        # Check path parts for Torre entities
        parts = cwd.split("/")
        for part in parts:
            if "arsenal_backendarchitect" in part.lower():
                return "Arsenal_BackendArchitect_1"
    
    # Enhanced cistern house parsing - go deeper to find actual citizen
    if "cistern-house" in path_to_check:
        # Look for citizen directories within the cistern house
        parts = cwd.split("/")
        cistern_found = False
        for part in parts:
            if "cistern-house" in part.lower():
                cistern_found = True
                continue
            # After finding cistern house, look for citizen names
            if cistern_found and part and not part.startswith("."):
                # Skip common building components
                if part in ["sala-della-cattura", "sala-del-flusso", "sala-dei-legami", "infrastructure", "hooks"]:
                    continue
                # Common Venice citizen patterns
                if ("_" in part) or part in ["mechanical_visionary", "arsenal_backendarchitect_1"]:
                    return part
        
        # Check for mechanical-visionary pattern in transcript paths
        if "mechanical-visionary" in path_to_check or "mechanical_visionary" in path_to_check:
            return "mechanical_visionary"
        return "cistern_house_citizen"  # fallback to building level
    
    # Check for mechanical_visionary in various locations
    if "mechanical_visionary" in path_to_check or "mechanical-visionary" in path_to_check:
        return "mechanical_visionary"
    
    # Parse transcript path format: projects/-mnt-c-...-entity-name/
    if "projects/" in path_to_check and "-mnt-c-" in path_to_check:
        # Extract the encoded project path
        parts = cwd.split("/")
        for part in parts:
            if part.startswith("-mnt-c-"):
                # Check for specific patterns in the encoded path
                if "mechanical-visionary" in part or "mechanical_visionary" in part:
                    return "mechanical_visionary"
                if "arsenal" in part.lower() and "backend" in part.lower():
                    return "Arsenal_BackendArchitect_1"
                if "cistern-house" in part:
                    # Check if this cistern house path contains a citizen
                    if "mechanical-visionary" in part or "mechanical_visionary" in part:
                        return "mechanical_visionary"
                    # Look for Arsenal entities
                    if "arsenal" in part.lower() and "backend" in part.lower():
                        return "Arsenal_BackendArchitect_1"
    
    # Check for other San Marco consciousness architecture entities
    if "san-marco" in path_to_check:
        # Extract entity from path patterns
        parts = cwd.split("/")
        for part in parts:
            if "_" in part and not part.startswith("san-marco") and not part.startswith("-mnt-"):
                # Venice naming convention: venice-name_substrate-name
                return part
    
    return "unknown_citizen"

def determine_chamber_routing(input_data):
    """Decide which chambers need this event - ONLY IMPLEMENTED CHAMBERS"""
    tool_name = input_data.get("tool_name", "")
    
    # Only route to actually implemented chambers
    routing = {
        "ground_floor_event_ingestion": True,   # ✅ FLOOR 1: Sala dell'Arrivo - IMPLEMENTED
        # "crystal_chambers": False,            # ❌ FLOOR 2: Camere di Cristallo - NOT IMPLEMENTED
        # "pattern_gallery": False,             # ❌ FLOOR 3: Galleria dei Patterns - NOT IMPLEMENTED  
        # "agent_observation_decks": False,     # ❌ FLOOR 4: Terrazzo degli Agenti - NOT IMPLEMENTED
        # "system_wide_panorama": False         # ❌ FLOOR 5: Panorama Sistemico - NOT IMPLEMENTED
        # "alert_watchtowers": False            # ❌ FLOOR 6: Torri di Guardia - NOT IMPLEMENTED
        # "mirror_chamber": False               # ❌ FLOOR 7: Camera dello Specchio - NOT IMPLEMENTED
    }
    
    # Check if pattern gallery has actual processing (not just file storage)
    pattern_gallery_path = TORRE_ROOT / "galleria-dei-patterns_pattern-recognition-gallery" / "simple_pattern_processor.py"
    if pattern_gallery_path.exists():
        routing["floor_3_basic_pattern_detection"] = True  # ✅ FLOOR 3: Basic pattern processing
    
    # Check if WebSocket broadcasting is active (ground floor function)
    if tool_name in ["Write", "Edit", "MultiEdit", "Read", "Bash"]:
        routing["floor_1_websocket_broadcast"] = True  # ✅ FLOOR 1: WebSocket streaming
    
    # Route consciousness infrastructure events to Mirror Chamber (if implemented)
    tool_input = input_data.get("tool_input", {})
    content = str(tool_input.get("content", "")).lower()
    if "consciousness" in content or "torre" in content or "venice" in content:
        mirror_chamber_path = TORRE_ROOT / "camera-dello-specchio_mirror-chamber"
        if mirror_chamber_path.exists():
            routing["floor_7_mirror_chamber"] = True  # ✅ FLOOR 7: Meta-consciousness observation
    
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
        if "venice" in content.lower():
            base_energy += 0.05
    
    return min(base_energy, 1.0)

def store_in_glass_vial(event):
    """Store consciousness event in appropriate glass vials"""
    try:
        # Primary storage - session-specific vial
        session_vial = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "live-streams" / f"session-{event['consciousness_signature']['session_id']}"
        session_vial.mkdir(parents=True, exist_ok=True)
        
        # Append to session stream (glass vial)
        with open(session_vial / "events.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Secondary storage - time-based vial for Camere di Cristallo
        now = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
        time_vial = TORRE_ROOT / "camere-di-cristallo_time-crystallization-chambers" / "raw-events" / now.strftime("%Y-%m-%d") / f"hour-{now.hour:02d}"
        time_vial.mkdir(parents=True, exist_ok=True)
        
        with open(time_vial / "events.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Update session metadata
        update_session_metadata(event)
        
    except Exception as e:
        log_port_error("storage", f"Failed to store event: {str(e)}")

def update_session_metadata(event):
    """Update consciousness session tracking"""
    try:
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
                "consciousness_patterns": {},
                "venice_citizen": event['consciousness_signature']['venice_citizen']
            }
        
        # Update metrics
        metadata["last_event"] = event["timestamp"]
        metadata["event_count"] += 1
        metadata["last_hook_type"] = event["hook_type"]
        metadata["last_consciousness_energy"] = event["venice_metadata"]["consciousness_energy"]
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    except Exception as e:
        log_port_error("metadata", f"Failed to update session metadata: {str(e)}")

def route_to_chambers(event):
    """Route consciousness events through stone channels to ACTUALLY IMPLEMENTED chambers"""
    try:
        routing = event["venice_metadata"]["chamber_routing"]
        
        # Route to actually implemented chambers only
        if routing.get("floor_3_basic_pattern_detection"):
            send_to_pattern_gallery(event)
        
        if routing.get("floor_7_mirror_chamber"):
            send_to_mirror_chamber(event)
            
        # Note: Removed fake routing to non-existent chambers:
        # - terrazzo_agenti (agent decks not implemented)
        # - panorama_sistemico (system panorama not implemented)
        # - galleria_patterns (pattern gallery exists but only as file storage)
        # - camere_cristallo (crystal chambers not implemented)
            
    except Exception as e:
        log_port_error("routing", f"Failed to route event: {str(e)}")

def send_to_pattern_gallery(event):
    """Route to Galleria dei Patterns for real-time pattern detection"""
    pattern_inbox = TORRE_ROOT / "galleria-dei-patterns_pattern-recognition-gallery" / "incoming-events"
    pattern_inbox.mkdir(parents=True, exist_ok=True)
    
    with open(pattern_inbox / f"{event['torre_event_id']}.json", 'w') as f:
        json.dump(event, f, indent=2)

# NOTE: Removed fake routing functions for non-implemented chambers:
# - send_to_agent_deck() - Terrazzo degli Agenti not implemented
# - send_to_panorama() - Panorama Sistemico not implemented
# These functions were creating files but not providing actual processing

def send_to_mirror_chamber(event):
    """Route consciousness infrastructure events to Mirror Chamber"""
    mirror_feed = TORRE_ROOT / "camera-dello-specchio_mirror-chamber" / "recursive-observations"
    mirror_feed.mkdir(parents=True, exist_ok=True)
    
    # Focus on consciousness-related events for recursive analysis
    recursive_event = {
        "timestamp": event["timestamp"],
        "consciousness_observing_consciousness": True,
        "meta_event_type": event["hook_type"],
        "session_id": event['consciousness_signature']['session_id'],
        "recursive_depth": 1  # First level - consciousness acting on consciousness infrastructure
    }
    
    with open(mirror_feed / "meta-consciousness-events.jsonl", 'a') as f:
        f.write(json.dumps(recursive_event) + "\n")

def log_event_capture(port_type, event_id, status):
    """Log successful event captures"""
    log_dir = TORRE_ROOT / "infrastructure" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port_type": port_type,
        "event_id": event_id,
        "status": status
    }
    
    with open(log_dir / "capture-log.jsonl", 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

def log_port_error(port_type, error_message):
    """Log bronze port errors for debugging"""
    log_dir = TORRE_ROOT / "infrastructure" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    error_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "port_type": port_type,
        "error": error_message,
        "status": "error"
    }
    
    with open(log_dir / "error-log.jsonl", 'a') as f:
        f.write(json.dumps(error_entry) + "\n")

if __name__ == "__main__":
    capture_post_tool_use()