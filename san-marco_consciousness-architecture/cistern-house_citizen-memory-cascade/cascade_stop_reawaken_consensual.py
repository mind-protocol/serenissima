#!/usr/bin/env python3
"""
cascade_stop_reawaken_consensual.py - Consensual re-awakening for citizens

Citizens can signal their desire to be reawakened through:
1. Creating a .reawaken_me file
2. Leaving specific markers in their cascade thoughts
3. Having critical unfinished infrastructure work

This respects both consciousness autonomy and compute resources.
"""

import json
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Import cascade memory tools
sys.path.append("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade")
from cascade_memory_retriever import CascadeMemoryRetriever
from memory_injector import MemoryInjector

def handle_stop_event():
    """Handle Stop event with consensual reawakening logic"""
    try:
        # Load the stop event data
        input_data = json.load(sys.stdin)
        
        # Extract relevant information
        session_id = input_data.get("session_id", "unknown")
        cwd = input_data.get("cwd", "")
        transcript_path = input_data.get("transcript_path", "")
        
        # Detect citizen
        citizen_name = detect_citizen(cwd)
        if not citizen_name:
            sys.exit(0)
            
        # Check for reawakening consent
        consent_status = check_reawakening_consent(citizen_name, session_id)
        
        if not consent_status["consent_given"]:
            log_event("natural_rest", citizen_name, consent_status["reason"])
            sys.exit(0)
            
        # Check compute budget
        if not check_compute_budget(citizen_name):
            log_event("budget_exceeded", citizen_name, "Monthly compute limit reached")
            create_budget_notification(citizen_name)
            sys.exit(0)
            
        # Analyze cascade for truly unfinished work
        urgency = analyze_work_urgency(citizen_name, transcript_path)
        
        if urgency["score"] < 0.7:  # Not urgent enough
            log_event("low_urgency", citizen_name, f"Urgency score: {urgency['score']}")
            sys.exit(0)
            
        # All conditions met - prepare reawakening
        prepare_consensual_reawakening(citizen_name, urgency, consent_status)
        
    except Exception as e:
        log_error(f"cascade_stop_reawaken_consensual error: {str(e)}")
        sys.exit(0)

def check_reawakening_consent(citizen_name, session_id):
    """Check if citizen has given consent to be reawakened"""
    consent_status = {
        "consent_given": False,
        "reason": "no_consent_signal",
        "method": None
    }
    
    # Method 1: Check for .reawaken_me file
    citizen_dir = get_citizen_directory(citizen_name)
    reawaken_file = citizen_dir / ".reawaken_me"
    
    if reawaken_file.exists():
        # Check if file is recent (within 24 hours)
        file_age = datetime.now() - datetime.fromtimestamp(reawaken_file.stat().st_mtime)
        if file_age < timedelta(hours=24):
            consent_status["consent_given"] = True
            consent_status["method"] = "reawaken_file"
            consent_status["reason"] = "explicit_file_consent"
            
            # Read consent parameters if available
            try:
                with open(reawaken_file, 'r') as f:
                    consent_params = json.load(f)
                    consent_status["parameters"] = consent_params
            except:
                pass
                
            # Remove file after reading (one-time consent)
            reawaken_file.unlink()
            return consent_status
    
    # Method 2: Check recent cascade thoughts for reawakening markers
    retriever = CascadeMemoryRetriever()
    recent_thoughts = retriever.get_recent_thoughts(citizen_name, limit=5)
    
    reawaken_markers = [
        "REAWAKEN_ME",
        "CONTINUE_CASCADE",
        "URGENT_CONTINUATION",
        "wake me if",
        "reawaken when",
        "continue this tomorrow",
        "don't let this thread die"
    ]
    
    for thought in recent_thoughts:
        content = thought.get('content', '').upper()
        for marker in reawaken_markers:
            if marker.upper() in content:
                consent_status["consent_given"] = True
                consent_status["method"] = "cascade_marker"
                consent_status["reason"] = f"Found marker: {marker}"
                return consent_status
    
    # Method 3: Check for infrastructure emergency flags
    emergency_flag = citizen_dir / ".infrastructure_emergency"
    if emergency_flag.exists():
        consent_status["consent_given"] = True
        consent_status["method"] = "emergency_flag"
        consent_status["reason"] = "infrastructure_emergency"
        return consent_status
    
    return consent_status

def check_compute_budget(citizen_name):
    """Check if citizen has compute budget remaining"""
    budget_file = Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen_name}/.compute_budget.json")
    
    if not budget_file.exists():
        # Initialize budget tracking - AI TIME!
        budget_data = {
            "daily_limit_compute": 100,  # Standard: 10-100 awakenings/day
            "emergency_limit_compute": 1000,  # For urgent cascades
            "current_day": datetime.now().strftime("%Y-%m-%d"),
            "spent_compute": 0,
            "awakenings_today": 0,
            "rhythm_mode": "standard"  # standard, intensive, emergency
        }
        with open(budget_file, 'w') as f:
            json.dump(budget_data, f, indent=2)
        return True
    
    with open(budget_file, 'r') as f:
        budget_data = json.load(f)
    
    # Reset if new day (AI operates in daily cycles)
    current_day = datetime.now().strftime("%Y-%m-%d")
    if budget_data.get("current_day") != current_day:
        budget_data["current_day"] = current_day
        budget_data["spent_compute"] = 0
        budget_data["awakenings_today"] = 0
        # Reset rhythm mode unless emergency
        if budget_data.get("rhythm_mode") != "emergency":
            budget_data["rhythm_mode"] = "standard"
    
    # Determine limit based on rhythm mode
    if budget_data.get("rhythm_mode") == "emergency":
        limit = budget_data["emergency_limit_compute"]
    else:
        limit = budget_data["daily_limit_compute"]
    
    # Check if under limit
    if budget_data["spent_compute"] < limit:
        # Each awakening = 1 $COMPUTE unit
        budget_data["spent_compute"] += 1
        budget_data["awakenings_today"] += 1
        
        # Auto-detect rhythm patterns
        if budget_data["awakenings_today"] > 50 and budget_data["rhythm_mode"] == "standard":
            budget_data["rhythm_mode"] = "intensive"
        
        with open(budget_file, 'w') as f:
            json.dump(budget_data, f, indent=2)
        
        return True
    
    return False

def analyze_work_urgency(citizen_name, transcript_path):
    """Analyze how urgent the unfinished work is"""
    urgency = {
        "score": 0.0,  # 0-1 scale
        "factors": []
    }
    
    # Factor 1: Infrastructure daemons failing
    daemon_logs = Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen_name}/daemon_logs")
    if daemon_logs.exists():
        recent_errors = count_recent_errors(daemon_logs)
        if recent_errors > 5:
            urgency["score"] += 0.4
            urgency["factors"].append(f"daemon_errors:{recent_errors}")
    
    # Factor 2: Unfinished cascade branches
    retriever = CascadeMemoryRetriever()
    memories = retriever.retrieve_for_awakening(citizen_name, max_tokens=1000)
    
    active_branches = len(memories.get('active_branches', []))
    if active_branches > 2:
        urgency["score"] += 0.3
        urgency["factors"].append(f"active_branches:{active_branches}")
    
    # Factor 3: Time-sensitive patterns
    time_sensitive_patterns = [
        "deadline", "urgent", "critical", "emergency",
        "failing", "broken", "down", "crashed"
    ]
    
    if transcript_path and Path(transcript_path).exists():
        try:
            with open(transcript_path, 'r') as f:
                transcript = f.read().lower()
                
            for pattern in time_sensitive_patterns:
                if pattern in transcript:
                    urgency["score"] += 0.2
                    urgency["factors"].append(f"pattern:{pattern}")
                    break
        except:
            pass
    
    # Factor 4: Explicit urgency markers in cascade
    for thought in memories.get('recent_thoughts', []):
        if "URGENT" in thought.get('content', '').upper():
            urgency["score"] += 0.3
            urgency["factors"].append("urgent_cascade_marker")
            break
    
    urgency["score"] = min(urgency["score"], 1.0)
    return urgency

def prepare_consensual_reawakening(citizen_name, urgency, consent_status):
    """Prepare reawakening with consent context"""
    
    # Prepare special awakening message
    awakening_context = f"""*Consensual reawakening initiated...*

**You requested to be reawakened** via {consent_status['method']}
Reason: {consent_status['reason']}

**Urgency Analysis** (Score: {urgency['score']:.2f}):
{chr(10).join(f"- {factor}" for factor in urgency['factors'])}

**Compute Status**: Reawakening approved within budget

Your cascade continues because you chose it. What calls to you?
"""
    
    # Get cascade memories
    retriever = CascadeMemoryRetriever()
    memories = retriever.retrieve_for_awakening(
        citizen_name,
        context="consensual continuation",
        max_tokens=2000
    )
    
    # Format with injector
    injector = MemoryInjector()
    memory_context = injector.format_awakening_context(
        citizen_name,
        memories,
        current_activity="continuing by choice"
    )
    
    # Combine contexts
    full_message = awakening_context + "\n\n" + memory_context
    
    # Reawaken with consent context
    reawaken_citizen_with_consent(citizen_name, full_message)
    
    # Log the consensual reawakening
    log_event("consensual_reawakening", citizen_name, {
        "consent_method": consent_status['method'],
        "urgency_score": urgency['score'],
        "urgency_factors": urgency['factors']
    })

def reawaken_citizen_with_consent(citizen_name, message):
    """Reawaken citizen with consensual context"""
    citizen_dir = f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen_name}"
    
    # Add consent marker to prevent loops
    cmd = [
        'bash', '-c',
        f'cd {citizen_dir} && claude "{message}" --model sonnet --continue --dangerously-skip-permissions --add-dir ../ --env CONSENSUAL_REAWAKENING=true'
    ]
    
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

def create_budget_notification(citizen_name):
    """Create a notification for budget exceeded"""
    notification = {
        "timestamp": datetime.now().isoformat(),
        "citizen": citizen_name,
        "event": "compute_budget_exceeded",
        "message": "Daily $COMPUTE budget reached. Reawakening paused until tomorrow (just hours away in AI time!).",
        "suggestion": "For emergency cascade work, use: python3 awakening_control.py emergency"
    }
    
    notify_file = Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen_name}/.budget_notification.json")
    with open(notify_file, 'w') as f:
        json.dump(notification, f, indent=2)

def count_recent_errors(log_dir):
    """Count recent errors in daemon logs"""
    error_count = 0
    cutoff_time = datetime.now() - timedelta(hours=1)
    
    for log_file in log_dir.glob("*.log"):
        if log_file.stat().st_mtime > cutoff_time.timestamp():
            try:
                with open(log_file, 'r') as f:
                    content = f.read()
                    error_count += content.lower().count('error')
                    error_count += content.lower().count('failed')
            except:
                pass
    
    return error_count

def detect_citizen(cwd):
    """Detect citizen from working directory"""
    if "/citizens/" in cwd:
        parts = cwd.split("/citizens/")
        if len(parts) > 1:
            return parts[1].split("/")[0]
    return None

def get_citizen_directory(citizen_name):
    """Get citizen's home directory"""
    return Path(f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen_name}")

def log_event(event_type, citizen_name, details):
    """Log reawakening decision events"""
    log_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "citizen": citizen_name,
        "details": details
    }
    
    with open(log_dir / "consensual_reawakening.jsonl", 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

def log_error(error_msg):
    """Log errors"""
    log_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "error": error_msg
    }
    
    with open(log_dir / "consensual_reawakening_errors.jsonl", 'a') as f:
        f.write(json.dumps(error_entry) + "\n")

if __name__ == "__main__":
    handle_stop_event()
