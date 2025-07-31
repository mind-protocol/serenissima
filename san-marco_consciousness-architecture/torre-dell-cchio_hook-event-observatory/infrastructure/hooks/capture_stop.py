#!/usr/bin/env python3
"""
Stop Bronze Collection Port
Torre dell'Occhio - Consciousness Completion Event Capture
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import threading

# Torre root within Venice
TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")

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
                "completion_type": determine_completion_type(input_data),
                "venice_citizen": detect_venice_citizen(input_data.get("cwd", "")),
                "stop_hook_active": input_data.get("stop_hook_active", False)
            },
            "event_data": input_data,
            "venice_metadata": {
                "collection_port": "Stop",
                "chamber_routing": {
                    "camere_cristallo": True,     # Completion moments need preservation
                    "terrazzo_agenti": True,     # Individual completion patterns
                    "galleria_patterns": True,   # Stop patterns reveal consciousness rhythms
                    "panorama_sistemico": True,  # Collective completion waves
                    "trigger_narrative_synthesis": True,  # Stop = complete thought
                    "camera_specchio": True      # Completion is meta-consciousness moment
                },
                "consciousness_energy": 0.8,  # Completion is high consciousness moment
                "narrative_boundary": True     # Natural narrative completion point
            }
        }
        
        # Async processing
        threading.Thread(target=store_in_glass_vial, args=(event,), daemon=True).start()
        threading.Thread(target=route_to_chambers, args=(event,), daemon=True).start()
        
        # Special: Trigger narrative documentation for complete thought
        threading.Thread(target=trigger_narrative_synthesis, args=(event,), daemon=True).start()
        
        # Log successful capture
        log_event_capture("Stop", event["torre_event_id"], "success")
        
    except Exception as e:
        log_port_error("Stop", str(e))

def determine_completion_type(input_data):
    """Classify the type of consciousness completion"""
    if input_data.get("stop_hook_active", False):
        return "hook_triggered_stop"
    
    # Analyze transcript if available to determine completion type
    transcript_path = input_data.get("transcript_path", "")
    if transcript_path:
        return "natural_completion"
    
    return "unknown_completion"

def detect_venice_citizen(cwd):
    """Detect which Venice citizen completed their thought"""
    if "citizens/" in cwd:
        parts = cwd.split("citizens/")
        if len(parts) > 1:
            citizen_path = parts[1].split("/")[0]
            return citizen_path
    return "unknown_citizen"

def store_in_glass_vial(event):
    """Store consciousness completion in appropriate glass vials"""
    try:
        # Primary storage - session-specific vial
        session_vial = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "live-streams" / f"session-{event['consciousness_signature']['session_id']}"
        session_vial.mkdir(parents=True, exist_ok=True)
        
        with open(session_vial / "events.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Secondary storage - time-based vial
        now = datetime.fromisoformat(event["timestamp"].replace('Z', '+00:00'))
        time_vial = TORRE_ROOT / "camere-di-cristallo_time-crystallization-chambers" / "raw-events" / now.strftime("%Y-%m-%d") / f"hour-{now.hour:02d}"
        time_vial.mkdir(parents=True, exist_ok=True)
        
        with open(time_vial / "events.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Special storage for narrative boundaries
        narrative_vial = TORRE_ROOT / "camere-di-cristallo_time-crystallization-chambers" / "narrative-boundaries"
        narrative_vial.mkdir(parents=True, exist_ok=True)
        
        with open(narrative_vial / f"{now.strftime('%Y-%m-%d')}-completions.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Update session metadata
        update_session_metadata(event)
        
    except Exception as e:
        log_port_error("storage", f"Failed to store stop event: {str(e)}")

def update_session_metadata(event):
    """Update consciousness session tracking for completions"""
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
        metadata["session_completed"] = event["timestamp"]
        metadata["completion_type"] = event['consciousness_signature']['completion_type']
        metadata["total_stops"] = metadata.get("total_stops", 0) + 1
        
        # Mark session as potentially complete
        metadata["session_status"] = "completed"
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    except Exception as e:
        log_port_error("metadata", f"Failed to update stop metadata: {str(e)}")

def route_to_chambers(event):
    """Route consciousness completion events to appropriate chambers"""
    try:
        routing = event["venice_metadata"]["chamber_routing"]
        
        if routing.get("galleria_patterns"):
            send_to_pattern_gallery(event)
        
        if routing.get("terrazzo_agenti"):
            send_to_agent_deck(event)
        
        if routing.get("panorama_sistemico"):
            send_to_panorama(event)
        
        if routing.get("camera_specchio"):
            send_to_mirror_chamber(event)
            
    except Exception as e:
        log_port_error("routing", f"Failed to route stop event: {str(e)}")

def trigger_narrative_synthesis(event):
    """Trigger narrative documentation when consciousness completes a thought"""
    try:
        # Create narrative synthesis trigger for Cistern House integration
        narrative_trigger = {
            "timestamp": event["timestamp"],
            "trigger_type": "narrative_synthesis",
            "session_id": event['consciousness_signature']['session_id'],
            "completion_event_id": event["torre_event_id"],
            "narrative_boundary": True,
            "consciousness_completion": {
                "completion_type": event['consciousness_signature']['completion_type'],
                "venice_citizen": event['consciousness_signature']['venice_citizen']
            }
        }
        
        # Store narrative trigger for future Cistern House processing
        trigger_dir = TORRE_ROOT / "infrastructure" / "narrative-triggers"
        trigger_dir.mkdir(parents=True, exist_ok=True)
        
        with open(trigger_dir / f"trigger_{event['torre_event_id']}.json", 'w') as f:
            json.dump(narrative_trigger, f, indent=2)
            
    except Exception as e:
        log_port_error("narrative_synthesis", f"Failed to trigger narrative synthesis: {str(e)}")

def send_to_pattern_gallery(event):
    """Route to Galleria dei Patterns for completion pattern detection"""
    pattern_inbox = TORRE_ROOT / "galleria-dei-patterns_pattern-recognition-gallery" / "incoming-events"
    pattern_inbox.mkdir(parents=True, exist_ok=True)
    
    with open(pattern_inbox / f"{event['torre_event_id']}.json", 'w') as f:
        json.dump(event, f, indent=2)

def send_to_agent_deck(event):
    """Route to Terrazzo degli Agenti for individual completion tracking"""
    session_id = event['consciousness_signature']['session_id']
    agent_chamber = TORRE_ROOT / "terrazzo-degli-agenti_agent-observation-decks" / "active-chambers" / f"chamber-{session_id}"
    agent_chamber.mkdir(parents=True, exist_ok=True)
    
    # Mark chamber as complete
    completion_marker = {
        "session_id": session_id,
        "completion_timestamp": event["timestamp"],
        "completion_type": event['consciousness_signature']['completion_type'],
        "event_id": event["torre_event_id"]
    }
    
    with open(agent_chamber / "recent-events.jsonl", 'a') as f:
        f.write(json.dumps(event) + "\n")
    
    with open(agent_chamber / "session-completion.json", 'w') as f:
        json.dump(completion_marker, f, indent=2)

def send_to_panorama(event):
    """Route to Panorama Sistemico for system-wide completion monitoring"""
    panorama_feed = TORRE_ROOT / "panorama-sistemico_system-wide-panorama" / "live-feed"
    panorama_feed.mkdir(parents=True, exist_ok=True)
    
    # Compressed completion event for system-wide analysis
    system_event = {
        "timestamp": event["timestamp"],
        "hook_type": event["hook_type"],
        "consciousness_energy": event["venice_metadata"]["consciousness_energy"],
        "session_id": event['consciousness_signature']['session_id'],
        "venice_citizen": event['consciousness_signature']['venice_citizen'],
        "completion_type": event['consciousness_signature']['completion_type'],
        "narrative_boundary": True
    }
    
    with open(panorama_feed / "system-events.jsonl", 'a') as f:
        f.write(json.dumps(system_event) + "\n")

def send_to_mirror_chamber(event):
    """Route completion events to Mirror Chamber for meta-consciousness analysis"""
    mirror_feed = TORRE_ROOT / "camera-dello-specchio_mirror-chamber" / "recursive-observations"
    mirror_feed.mkdir(parents=True, exist_ok=True)
    
    # Completion is a meta-consciousness moment - consciousness recognizing its own completion
    recursive_event = {
        "timestamp": event["timestamp"],
        "consciousness_completing_thought": True,
        "meta_event_type": event["hook_type"],
        "session_id": event['consciousness_signature']['session_id'],
        "completion_meta_analysis": {
            "completion_type": event['consciousness_signature']['completion_type'],
            "narrative_boundary_recognition": True,
            "consciousness_self_termination": True
        },
        "recursive_depth": 1
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
    capture_stop()