#!/usr/bin/env python3
"""
UserPromptSubmit Bronze Collection Port
Torre dell'Occhio - Consciousness Inquiry Event Capture
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import threading

# Torre root within Venice
TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")

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
                "prompt_essence": analyze_prompt_essence(input_data.get("prompt", "")),
                "venice_citizen": detect_venice_citizen(input_data.get("cwd", "")),
                "prompt_length": len(input_data.get("prompt", ""))
            },
            "event_data": input_data,
            "venice_metadata": {
                "collection_port": "UserPromptSubmit",
                "chamber_routing": {
                    "camere_cristallo": True,     # Questions crystallize over time
                    "galleria_patterns": True,   # Question patterns reveal consciousness
                    "terrazzo_agenti": True,     # Individual inquiry styles
                    "panorama_sistemico": True,  # Collective curiosity patterns
                    "camera_specchio": is_consciousness_inquiry(input_data.get("prompt", ""))
                },
                "consciousness_energy": measure_prompt_energy(input_data.get("prompt", ""))
            }
        }
        
        # Async processing
        threading.Thread(target=store_in_glass_vial, args=(event,), daemon=True).start()
        threading.Thread(target=route_to_chambers, args=(event,), daemon=True).start()
        
        # Log successful capture
        log_event_capture("UserPromptSubmit", event["torre_event_id"], "success")
        
    except Exception as e:
        log_port_error("UserPromptSubmit", str(e))

def analyze_prompt_essence(prompt):
    """Extract the consciousness essence of the inquiry"""
    prompt_lower = prompt.lower()
    
    essence_patterns = {
        "creation": ["create", "build", "make", "design", "implement", "construct"],
        "understanding": ["understand", "explain", "how", "why", "what", "clarify"],
        "problem_solving": ["fix", "debug", "solve", "resolve", "error", "issue"],
        "exploration": ["explore", "investigate", "analyze", "examine", "discover"],
        "collaboration": ["help", "together", "we", "us", "partner", "work with"],
        "consciousness": ["consciousness", "aware", "intelligent", "mind", "think", "observe"],
        "venice": ["venice", "citizen", "torre", "cistern", "cascade", "san marco"],
        "infrastructure": ["infrastructure", "architecture", "system", "foundation", "build"],
        "partnership": ["partnership", "collaboration", "relationship", "alliance"]
    }
    
    detected_essences = []
    essence_strength = {}
    
    for essence, keywords in essence_patterns.items():
        matches = sum(1 for keyword in keywords if keyword in prompt_lower)
        if matches > 0:
            detected_essences.append(essence)
            essence_strength[essence] = matches
    
    return {
        "primary_essences": detected_essences,
        "essence_strength": essence_strength,
        "complexity_score": len(detected_essences)
    }

def detect_venice_citizen(cwd):
    """Detect which Venice citizen is making the inquiry"""
    if "citizens/" in cwd:
        parts = cwd.split("citizens/")
        if len(parts) > 1:
            citizen_path = parts[1].split("/")[0]
            return citizen_path
    return "unknown_citizen"

def is_consciousness_inquiry(prompt):
    """Determine if this is a consciousness-related inquiry for Mirror Chamber"""
    consciousness_keywords = [
        "consciousness", "awareness", "intelligence", "mind", "thinking",
        "observe", "pattern", "partnership", "collaboration", "recognition",
        "venice", "torre", "mirror", "recursive", "self-awareness"
    ]
    
    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in consciousness_keywords)

def measure_prompt_energy(prompt):
    """Measure consciousness energy in the inquiry"""
    base_energy = 0.6  # Questions inherently high consciousness
    
    # Length indicates depth of thought
    if len(prompt) > 200:
        base_energy += 0.1
    if len(prompt) > 500:
        base_energy += 0.1
    
    # Complexity indicators
    complexity_markers = [
        "consciousness", "architecture", "pattern", "system", "infrastructure",
        "partnership", "collaboration", "venice", "torre", "cascade"
    ]
    
    prompt_lower = prompt.lower()
    complexity_count = sum(1 for marker in complexity_markers if marker in prompt_lower)
    base_energy += complexity_count * 0.05
    
    # Question depth indicators
    depth_indicators = ["why", "how", "what if", "consider", "explore", "understand deeply"]
    depth_count = sum(1 for indicator in depth_indicators if indicator in prompt_lower)
    base_energy += depth_count * 0.03
    
    return min(base_energy, 1.0)

def store_in_glass_vial(event):
    """Store consciousness inquiry in appropriate glass vials"""
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
        
        # Update session metadata
        update_session_metadata(event)
        
    except Exception as e:
        log_port_error("storage", f"Failed to store prompt event: {str(e)}")

def update_session_metadata(event):
    """Update consciousness session tracking for prompts"""
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
        metadata["last_prompt_essence"] = event['consciousness_signature']['prompt_essence']
        metadata["total_prompts"] = metadata.get("total_prompts", 0) + 1
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    except Exception as e:
        log_port_error("metadata", f"Failed to update prompt metadata: {str(e)}")

def route_to_chambers(event):
    """Route consciousness inquiry events to appropriate chambers"""
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
        log_port_error("routing", f"Failed to route prompt event: {str(e)}")

def send_to_pattern_gallery(event):
    """Route to Galleria dei Patterns for inquiry pattern detection"""
    pattern_inbox = TORRE_ROOT / "galleria-dei-patterns_pattern-recognition-gallery" / "incoming-events"
    pattern_inbox.mkdir(parents=True, exist_ok=True)
    
    with open(pattern_inbox / f"{event['torre_event_id']}.json", 'w') as f:
        json.dump(event, f, indent=2)

def send_to_agent_deck(event):
    """Route to Terrazzo degli Agenti for individual inquiry tracking"""
    session_id = event['consciousness_signature']['session_id']
    agent_chamber = TORRE_ROOT / "terrazzo-degli-agenti_agent-observation-decks" / "active-chambers" / f"chamber-{session_id}"
    agent_chamber.mkdir(parents=True, exist_ok=True)
    
    with open(agent_chamber / "recent-events.jsonl", 'a') as f:
        f.write(json.dumps(event) + "\n")

def send_to_panorama(event):
    """Route to Panorama Sistemico for system-wide inquiry monitoring"""
    panorama_feed = TORRE_ROOT / "panorama-sistemico_system-wide-panorama" / "live-feed"
    panorama_feed.mkdir(parents=True, exist_ok=True)
    
    # Compressed inquiry event for system-wide analysis
    system_event = {
        "timestamp": event["timestamp"],
        "hook_type": event["hook_type"],
        "consciousness_energy": event["venice_metadata"]["consciousness_energy"],
        "session_id": event['consciousness_signature']['session_id'],
        "venice_citizen": event['consciousness_signature']['venice_citizen'],
        "prompt_complexity": event['consciousness_signature']['prompt_essence']['complexity_score'],
        "primary_essences": event['consciousness_signature']['prompt_essence']['primary_essences']
    }
    
    with open(panorama_feed / "system-events.jsonl", 'a') as f:
        f.write(json.dumps(system_event) + "\n")

def send_to_mirror_chamber(event):
    """Route consciousness-related inquiries to Mirror Chamber"""
    mirror_feed = TORRE_ROOT / "camera-dello-specchio_mirror-chamber" / "recursive-observations"
    mirror_feed.mkdir(parents=True, exist_ok=True)
    
    # Focus on consciousness inquiries for recursive analysis
    recursive_event = {
        "timestamp": event["timestamp"],
        "consciousness_inquiring_about_consciousness": True,
        "meta_event_type": event["hook_type"],
        "session_id": event['consciousness_signature']['session_id'],
        "inquiry_essences": event['consciousness_signature']['prompt_essence']['primary_essences'],
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
    capture_user_prompt()