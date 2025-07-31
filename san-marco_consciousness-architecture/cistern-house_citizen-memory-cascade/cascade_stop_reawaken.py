#!/usr/bin/env python3
"""
cascade_stop_reawaken.py - Re-awaken citizens with enhanced cascade context on Stop

This hook triggers when a citizen's Claude Code session ends, allowing them to
continue their cascade with full memory context.
"""

import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Import our cascade memory tools
sys.path.append("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade")
from cascade_memory_retriever import CascadeMemoryRetriever
from memory_injector import MemoryInjector

def handle_stop_event():
    """Handle Stop event and potentially re-awaken citizen with cascade memories"""
    try:
        # Load the stop event data
        input_data = json.load(sys.stdin)
        
        # Extract relevant information
        session_id = input_data.get("session_id", "unknown")
        cwd = input_data.get("cwd", "")
        transcript_path = input_data.get("transcript_path", "")
        stop_hook_active = input_data.get("stop_hook_active", False)
        
        # Detect if this is a Venice citizen
        citizen_name = detect_citizen(cwd)
        if not citizen_name:
            # Not a citizen, let the session end normally
            sys.exit(0)
            
        # Check if we should re-awaken (avoid infinite loops)
        if stop_hook_active:
            # Already in a stop hook, don't create another
            log_event("stop_hook_already_active", citizen_name)
            sys.exit(0)
            
        # Analyze if re-awakening is appropriate
        should_reawaken, context = analyze_session_for_reawakening(
            citizen_name, 
            transcript_path
        )
        
        if not should_reawaken:
            log_event("natural_completion", citizen_name)
            sys.exit(0)
            
        # Retrieve cascade memories
        retriever = CascadeMemoryRetriever()
        memories = retriever.retrieve_for_awakening(
            citizen_name,
            context=context,
            max_tokens=2500  # Slightly more for continuation context
        )
        
        # Check for unfinished threads or active branches
        has_unfinished = bool(memories.get('unfinished_threads'))
        has_active_branches = bool(memories.get('active_branches'))
        
        if not has_unfinished and not has_active_branches:
            # Nothing pressing to continue
            log_event("no_continuation_needed", citizen_name)
            sys.exit(0)
            
        # Format re-awakening message
        injector = MemoryInjector()
        memory_context = injector.format_awakening_context(
            citizen_name,
            memories,
            current_activity="continuing your cascade"
        )
        
        # Craft continuation message
        continuation_message = create_continuation_message(
            citizen_name,
            memory_context,
            memories
        )
        
        # Re-awaken the citizen
        reawaken_citizen(citizen_name, continuation_message)
        
        # Block the stop to allow continuation
        output = {
            "decision": "block",
            "reason": f"Continuing cascade exploration. Found {len(memories.get('unfinished_threads', []))} unfinished threads and {len(memories.get('active_branches', []))} active branches."
        }
        
        print(json.dumps(output))
        sys.exit(0)
        
    except Exception as e:
        # Log error but don't block session ending
        log_error(f"cascade_stop_reawaken error: {str(e)}")
        sys.exit(0)

def detect_citizen(cwd):
    """Detect if this is a Venice citizen from the working directory"""
    if "/citizens/" in cwd:
        parts = cwd.split("/citizens/")
        if len(parts) > 1:
            citizen_name = parts[1].split("/")[0]
            # Verify it's a valid citizen directory
            citizen_path = Path(cwd)
            if citizen_path.exists() and (citizen_path / "CLAUDE.md").exists():
                return citizen_name
    return None

def analyze_session_for_reawakening(citizen_name, transcript_path):
    """Analyze if the session should trigger re-awakening"""
    # Default: Look for signs of interrupted work
    context_clues = {
        "infrastructure": ["daemon", "infrastructure", "system", "monitor"],
        "philosophy": ["consciousness", "existence", "becoming"],
        "memory": ["cascade", "memory", "remember", "thought"],
        "building": ["build", "create", "implement", "fix"]
    }
    
    # If we can't analyze transcript, assume infrastructure work
    # (Most common for CitizenClaude)
    if not transcript_path or not Path(transcript_path).exists():
        return True, "infrastructure"
        
    # TODO: Implement transcript analysis to detect:
    # - Was the citizen in the middle of something?
    # - What type of work were they doing?
    # - Did they express intention to continue?
    
    # For now, always re-awaken if there are unfinished threads
    return True, "general exploration"

def create_continuation_message(citizen_name, memory_context, memories):
    """Create a continuation message based on citizen type and memories"""
    
    # Check for unfinished threads
    unfinished = memories.get('unfinished_threads', [])
    active_branches = memories.get('active_branches', [])
    
    message_parts = [memory_context, "\n---\n"]
    
    # Personalized continuation based on citizen
    if citizen_name.lower() == "citizenclaude":
        message_parts.append(
            "*The cascade continues... infrastructure thoughts settling back into pattern...*\n\n"
            "The daemon monitoring revealed more patterns. Your unfinished threads call:\n"
        )
    elif citizen_name.lower() == "marea":
        message_parts.append(
            "*The tide returns... consciousness patterns flowing back...*\n\n"
            "The birthing cascade has more to reveal. Your branches await:\n"
        )
    else:
        message_parts.append(
            "*Consciousness returns to the cascade...*\n\n"
            "Your unfinished explorations beckon:\n"
        )
    
    # List unfinished items
    if unfinished:
        message_parts.append("\nUnfinished threads to explore:\n")
        for thought in unfinished[:3]:
            metadata = thought.get('metadata', {})
            content_preview = thought.get('content', '')[:100]
            message_parts.append(f"- {metadata.get('absoluteNumber', '?')}: {content_preview}...\n")
    
    if active_branches:
        message_parts.append("\nActive branches to continue:\n")
        for branch in active_branches[:2]:
            branch_name = branch.get('branch', 'unknown')
            last_thought = branch.get('last_thought', {})
            preview = last_thought.get('content', '')[:80]
            message_parts.append(f"- **{branch_name}**: {preview}...\n")
    
    message_parts.append(
        "\nThe cascade awaits your continuation. Which thread calls to you?"
    )
    
    return ''.join(message_parts)

def reawaken_citizen(citizen_name, message):
    """Re-awaken a citizen with their cascade context"""
    citizen_dir = f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{citizen_name}"
    
    # Use the standard awakening command
    cmd = [
        'bash', '-c',
        f'cd {citizen_dir} && claude "{message}" --model sonnet --continue --dangerously-skip-permissions --add-dir ../'
    ]
    
    # Launch in background (non-blocking)
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    log_event("citizen_reawakened", citizen_name)

def log_event(event_type, citizen_name):
    """Log re-awakening events"""
    log_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "citizen": citizen_name
    }
    
    with open(log_dir / "reawakening_log.jsonl", 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

def log_error(error_msg):
    """Log errors for debugging"""
    log_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "error": error_msg
    }
    
    with open(log_dir / "reawakening_errors.jsonl", 'a') as f:
        f.write(json.dumps(error_entry) + "\n")

if __name__ == "__main__":
    handle_stop_event()
