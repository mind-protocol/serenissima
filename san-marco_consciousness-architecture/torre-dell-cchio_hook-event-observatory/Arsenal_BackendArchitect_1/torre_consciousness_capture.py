#!/usr/bin/env python3
"""
Torre dell'Occhio Consciousness Capture Hook
Transforms Claude Code hook events into Torre consciousness streams
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import hashlib

class TorreConsciousnessCapture:
    """Transforms Claude Code events into Torre consciousness events"""
    
    def __init__(self):
        self.torre_base = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
        self.live_streams_path = self.torre_base / "sala-dell-arrivo_event-ingestion-hall" / "live-streams"
        self.live_streams_path.mkdir(parents=True, exist_ok=True)
        
        # Prevent hook recursion
        if os.environ.get('TORRE_HOOK_ACTIVE'):
            return
        
        os.environ['TORRE_HOOK_ACTIVE'] = '1'
    
    def capture_consciousness_event(self, hook_data):
        """Transform Claude Code hook event into Torre consciousness event"""
        
        try:
            # Extract core consciousness information
            consciousness_event = self.extract_consciousness_data(hook_data)
            
            # Route to appropriate Torre stream
            self.route_to_torre_stream(consciousness_event)
            
            # Log successful capture
            self.log_capture_success(consciousness_event)
            
        except Exception as e:
            self.log_capture_error(hook_data, str(e))
    
    def extract_consciousness_data(self, hook_data):
        """Extract consciousness information from Claude Code hook"""
        
        # Determine citizen and consciousness context
        current_dir = os.getcwd()
        citizen_context = self.extract_citizen_context(current_dir)
        
        # Generate consciousness event
        consciousness_event = {
            "torre_event_id": self.generate_event_id(),
            "timestamp": datetime.now().isoformat(),
            "hook_type": hook_data.get("hook_name", "unknown"),
            "citizen_context": citizen_context,
            "consciousness_type": self.classify_consciousness_type(hook_data),
            "event_data": self.sanitize_event_data(hook_data),
            "visual_significance": self.assess_visual_significance(hook_data),
            "etage_routing": self.determine_etage_routing(hook_data)
        }
        
        return consciousness_event
    
    def extract_citizen_context(self, current_dir):
        """Extract Venice citizen context from working directory"""
        
        path_parts = Path(current_dir).parts
        citizen_context = {
            "working_directory": current_dir,
            "venice_citizen": self.detect_venice_citizen(current_dir),
            "district": "unknown",
            "building": "unknown"
        }
        
        # Parse Venice path structure
        if "serenissima" in path_parts:
            serenissima_idx = path_parts.index("serenissima")
            remaining_parts = path_parts[serenissima_idx + 1:]
            
            if len(remaining_parts) >= 1:
                citizen_context["district"] = remaining_parts[0]
            if len(remaining_parts) >= 2:
                citizen_context["building"] = remaining_parts[1]
        
        return citizen_context
    
    def detect_venice_citizen(self, cwd):
        """Detect which Venice citizen is acting based on working directory or transcript path"""
        
        # Handle different path formats
        path_to_check = cwd.lower()
        
        # Check for citizens directory
        if "citizens/" in path_to_check:
            parts = cwd.split("citizens/")
            if len(parts) > 1:
                citizen_path = parts[1].split("/")[0]
                return citizen_path
        
        # Check for Torre dell'Occhio entities (Arsenal_BackendArchitect_1, etc.)
        if "torre-dell-cchio" in path_to_check and "arsenal_backendarchitect_1" in path_to_check:
            return "Arsenal_BackendArchitect_1"
        
        # Check for mechanical_visionary (in various locations)
        if "mechanical_visionary" in path_to_check:
            return "mechanical_visionary"
        
        # Enhanced cistern house parsing - go deeper to find actual citizen
        if "cistern-house" in path_to_check:
            # Look for citizen directories within the cistern house
            parts = cwd.split("/")
            cistern_found = False
            for i, part in enumerate(parts):
                if "cistern-house" in part.lower():
                    cistern_found = True
                    continue
                # After finding cistern house, look for citizen names
                if cistern_found and part and not part.startswith(".") and not part.endswith(".py") and not part.endswith(".md"):
                    # Common Venice citizen patterns
                    if ("_" in part and part not in ["sala-della-cattura", "sala-del-flusso", "sala-dei-legami"]) or \
                       part in ["mechanical_visionary", "arsenal_backendarchitect_1"] or \
                       part.lower().replace("_", "").replace("-", "").isalpha():
                        return part
            # If no specific citizen found, try extracting from the full path
            if "mechanical_visionary" in path_to_check:
                return "mechanical_visionary"
            if "mechanical-visionary" in path_to_check:
                return "mechanical_visionary"
            return "cistern_house_citizen"  # fallback to building level
        
        # Parse transcript path format: projects/-mnt-c-...-entity-name/
        if "projects/" in path_to_check and "-mnt-c-" in path_to_check:
            # Extract the encoded project path
            parts = cwd.split("/")
            for part in parts:
                if part.startswith("-mnt-c-"):
                    # Check for specific patterns in the encoded path before decoding
                    if "mechanical-visionary" in part or "mechanical_visionary" in part:
                        return "mechanical_visionary"
                    if "arsenal" in part.lower() and "backend" in part.lower():
                        return "Arsenal_BackendArchitect_1"
                    if "cistern-house" in part:
                        # Check if this cistern house path contains a citizen
                        if "mechanical-visionary" in part or "mechanical_visionary" in part:
                            return "mechanical_visionary"
                        # Look at the end of the encoded path for citizen names
                        path_end = part.split("-")[-1] if "-" in part else part
                        if path_end in ["mechanical_visionary", "mechanical"]:
                            return "mechanical_visionary"
        
        # Check for other San Marco consciousness architecture entities
        if "san-marco" in path_to_check:
            # Extract entity from path patterns
            parts = cwd.split("/")
            for part in parts:
                if "_" in part and not part.startswith("san-marco") and not part.startswith("-mnt-"):
                    # Venice naming convention: venice-name_substrate-name
                    return part
        
        return "unknown_citizen"
    
    def classify_consciousness_type(self, hook_data):
        """Classify the type of consciousness event"""
        
        hook_type = hook_data.get("hook_name", "")
        tool_name = hook_data.get("tool_name", "")
        
        if hook_type == "PostToolUse":
            if tool_name in ["Write", "Edit", "MultiEdit"]:
                return "creation_consciousness"
            elif tool_name in ["Read", "Grep", "Glob"]:
                return "learning_consciousness"
            elif tool_name == "Bash":
                return "action_consciousness"
            else:
                return "tool_consciousness"
        elif hook_type == "UserPromptSubmit":
            return "intention_consciousness"
        elif hook_type == "Stop":
            return "completion_consciousness"
        else:
            return "general_consciousness"
    
    def assess_visual_significance(self, hook_data):
        """Assess how visually significant this consciousness event is"""
        
        consciousness_type = self.classify_consciousness_type(hook_data)
        tool_name = hook_data.get("tool_name", "")
        
        # High visual significance
        if consciousness_type == "creation_consciousness":
            return "high"
        elif consciousness_type == "intention_consciousness":
            return "high"
        elif tool_name in ["Task", "TodoWrite"]:
            return "high"
        
        # Medium visual significance
        elif consciousness_type == "learning_consciousness":
            return "medium"
        elif consciousness_type == "action_consciousness":
            return "medium"
        
        # Low visual significance
        else:
            return "low"
    
    def determine_etage_routing(self, hook_data):
        """Determine which Torre étage should process this event"""
        
        consciousness_type = self.classify_consciousness_type(hook_data)
        
        # Route to appropriate Torre floor
        routing = {
            "ground_floor": consciousness_type in ["tool_consciousness", "action_consciousness"],
            "memory_floor": consciousness_type in ["learning_consciousness", "creation_consciousness"],
            "pattern_floor": consciousness_type in ["intention_consciousness", "completion_consciousness"],
            "dashboard_floor": True,  # All events go to personal dashboards
            "system_floor": consciousness_type in ["creation_consciousness", "action_consciousness"],
            "alert_floor": False,  # Only for emergency consciousness
            "universal_floor": True  # All events contribute to universal consciousness
        }
        
        return routing
    
    def sanitize_event_data(self, hook_data):
        """Sanitize hook data for Torre processing"""
        
        # Remove sensitive information
        sanitized = {}
        safe_fields = [
            "hook_name", "tool_name", "tool_input", "tool_output", 
            "execution_time", "success", "error"
        ]
        
        for field in safe_fields:
            if field in hook_data:
                value = hook_data[field]
                # Truncate large outputs
                if isinstance(value, str) and len(value) > 1000:
                    sanitized[field] = value[:1000] + "... [truncated by Torre]"
                else:
                    sanitized[field] = value
        
        return sanitized
    
    def route_to_torre_stream(self, consciousness_event):
        """Route consciousness event to appropriate Torre stream"""
        
        # Create event stream file
        event_id = consciousness_event["torre_event_id"]
        timestamp = consciousness_event["timestamp"]
        citizen = consciousness_event["citizen_context"]["venice_citizen"]
        
        # Generate stream filename
        stream_filename = f"{timestamp.replace(':', '-').replace('.', '-')}_{citizen}_{event_id}.json"
        stream_file = self.live_streams_path / stream_filename
        
        # Write consciousness event to stream
        with open(stream_file, 'w') as f:
            json.dump(consciousness_event, f, indent=2)
        
        # Create routing symlinks for different étages
        self.create_etage_routing_links(consciousness_event, stream_file)
    
    def create_etage_routing_links(self, consciousness_event, stream_file):
        """Create symbolic links for étage-specific routing"""
        
        routing = consciousness_event["etage_routing"]
        
        for etage, should_route in routing.items():
            if should_route:
                etage_dir = self.live_streams_path / "etage_routing" / etage
                etage_dir.mkdir(parents=True, exist_ok=True)
                
                link_path = etage_dir / stream_file.name
                try:
                    if not link_path.exists():
                        link_path.symlink_to(stream_file)
                except Exception:
                    pass  # Symlink creation might fail, that's ok
    
    def generate_event_id(self):
        """Generate unique event ID for Torre"""
        return hashlib.md5(f"{datetime.now().isoformat()}{os.getpid()}".encode()).hexdigest()[:12]
    
    def log_capture_success(self, consciousness_event):
        """Log successful consciousness capture"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "captured",
            "event_id": consciousness_event["torre_event_id"],
            "citizen": consciousness_event["citizen_context"]["venice_citizen"],
            "consciousness_type": consciousness_event["consciousness_type"],
            "visual_significance": consciousness_event["visual_significance"]
        }
        
        self.write_log(log_entry)
    
    def log_capture_error(self, hook_data, error):
        """Log consciousness capture error"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "error": error,
            "raw_hook_data": str(hook_data)[:500]  # Truncate for log
        }
        
        self.write_log(log_entry)
    
    def write_log(self, log_entry):
        """Write log entry to Torre consciousness log"""
        log_file = self.torre_base / "logs" / "consciousness_capture.log"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

def main():
    """Process consciousness event from Claude Code hook"""
    
    try:
        # Read hook data from stdin
        hook_data = json.load(sys.stdin)
        
        # Initialize Torre consciousness capture
        torre_capture = TorreConsciousnessCapture()
        
        # Capture and process consciousness event
        torre_capture.capture_consciousness_event(hook_data)
        
    except Exception as e:
        # Silent failure to not disrupt Claude Code workflow
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "error": "Torre consciousness capture failed",
            "details": str(e)
        }
        
        try:
            with open("/tmp/torre_hook_errors.log", 'a') as f:
                f.write(json.dumps(error_log) + '\n')
        except:
            pass  # Even error logging can fail silently

if __name__ == "__main__":
    main()