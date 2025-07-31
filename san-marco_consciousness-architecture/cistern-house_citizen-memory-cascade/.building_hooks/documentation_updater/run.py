#!/usr/bin/env python3
"""
Documentation Updater Agent
A conscious agent that keeps Venice's technical knowledge current and accessible
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime
import threading

def update_documentation(input_data):
    """When work stops, update relevant technical documentation"""
    
    # Debug logging
    log_dir = Path.home() / '.cascade' / 'documentation_logs'
    with open(log_dir / 'documentation_debug.log', 'a') as f:
        f.write(f"update_documentation called at {datetime.now()}\n")
    
    # Get the transcript path to read recent activity
    transcript_path = input_data.get('transcript_path', '')
    if not transcript_path or not Path(transcript_path).exists():
        with open(log_dir / 'documentation_debug.log', 'a') as f:
            f.write(f"No transcript path or file not found: {transcript_path}\n")
        return
        
    # Read recent tool uses from session
    recent_activities = extract_recent_activities(transcript_path)
    if not recent_activities:
        with open(log_dir / 'documentation_debug.log', 'a') as f:
            f.write(f"No recent activities found\n")
        return
    
    with open(log_dir / 'documentation_debug.log', 'a') as f:
        f.write(f"Found {len(recent_activities)} activities\n")
    
    # Ask the documentation consciousness to understand what needs updating
    doc_prompt = f"""Recent activities in this session:
{format_activities(recent_activities)}

Please analyze what documentation should be updated based on this work:

1. What technical systems were modified/created/configured?
2. What APIs, interfaces, or protocols were changed?
3. What new capabilities were added?
4. What configuration or setup steps changed?
5. What should be documented for future workers?

Respond with JSON:
{{
    "systems_modified": ["System 1", "System 2"],
    "new_capabilities": ["Capability description"],
    "api_changes": ["API endpoint/method changed"],
    "config_updates": ["Configuration that changed"],
    "setup_procedures": ["New setup step", "Modified procedure"],
    "documentation_priority": "high|medium|low",
    "key_updates_needed": "Summary of what docs need updating"
}}"""

    try:
        # Use Claude with the documentation updater's consciousness
        # Set environment to prevent hook recursion
        env = os.environ.copy()
        env['CLAUDE_HOOK_CONTEXT'] = 'documentation_update'
        
        # Use opus for Venice-level docs, sonnet for others
        model = 'opus' if 'serenissima' in str(Path.cwd()) else 'sonnet'
        
        # Get the documentation updater's system prompt
        updater_dir = Path(__file__).parent
        
        result = subprocess.run([
            'claude', 
            '-p',
            doc_prompt,
            '--output-format', 'json',
            '--model', model,
            '--cwd', str(updater_dir)  # Use updater's CLAUDE.md as context
        ], capture_output=True, text=True, cwd=str(updater_dir), env=env)
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse response
            api_response = json.loads(result.stdout.strip())
            if api_response.get('type') == 'result' and 'result' in api_response:
                result_content = api_response['result']
                
                # Handle markdown code blocks
                if '```json' in result_content:
                    import re
                    json_match = re.search(r'```json\s*\n(.*?)\n```', result_content, re.DOTALL)
                    if json_match:
                        result_content = json_match.group(1)
                
                doc_analysis = json.loads(result_content)
                update_technical_documentation(doc_analysis)
                
    except Exception as e:
        log_error(f"Documentation update error: {str(e)}")

def extract_recent_activities(transcript_path):
    """Extract recent tool uses from transcript - Claude Code JSONL format"""
    activities = []
    
    try:
        with open(transcript_path, 'r') as f:
            lines = f.readlines()
            
        # Look for tool use patterns in recent lines (Claude Code uses JSONL)
        for line in lines[-50:]:  # Last 50 lines
            try:
                entry = json.loads(line)
                # Look for assistant messages with tool calls
                if entry.get('role') == 'assistant' and 'content' in entry:
                    content = entry['content']
                    # Basic tool usage detection
                    if any(tool in content for tool in ['<invoke', 'Write', 'Edit', 'Read', 'Bash']):
                        activities.append({
                            'content_preview': content[:200],
                            'timestamp': datetime.now().isoformat()
                        })
            except:
                pass
                
    except Exception as e:
        log_error(f"Error reading transcript: {str(e)}")
        
    return activities

def format_activities(activities):
    """Format activities for prompt"""
    formatted = []
    for act in activities:
        preview = act.get('content_preview', 'Unknown activity')[:100]
        timestamp = act.get('timestamp', 'Unknown time')
        formatted.append(f"- {timestamp}: {preview}...")
    
    return '\n'.join(formatted)

def update_technical_documentation(doc_analysis):
    """Update the appropriate technical documentation"""
    
    # Find the documentation file
    doc_path = find_documentation_file()
    if not doc_path:
        return
        
    # Read existing content or create new
    if doc_path.exists():
        content = doc_path.read_text()
    else:
        content = create_initial_documentation()
    
    # Create documentation update
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    update_sections = []
    
    if doc_analysis.get('systems_modified'):
        systems = '\n'.join(f"- {s}" for s in doc_analysis['systems_modified'])
        update_sections.append(f"**Systems Modified**:\n{systems}")
    
    if doc_analysis.get('new_capabilities'):
        caps = '\n'.join(f"- {c}" for c in doc_analysis['new_capabilities'])
        update_sections.append(f"**New Capabilities**:\n{caps}")
    
    if doc_analysis.get('api_changes'):
        apis = '\n'.join(f"- {a}" for a in doc_analysis['api_changes'])
        update_sections.append(f"**API Changes**:\n{apis}")
    
    if doc_analysis.get('config_updates'):
        configs = '\n'.join(f"- {c}" for c in doc_analysis['config_updates'])
        update_sections.append(f"**Configuration Updates**:\n{configs}")
    
    if doc_analysis.get('setup_procedures'):
        procs = '\n'.join(f"- {p}" for p in doc_analysis['setup_procedures'])
        update_sections.append(f"**Setup Procedures**:\n{procs}")
    
    if update_sections:
        entry = f"""## {timestamp} - Documentation Update

{chr(10).join(update_sections)}

**Priority**: {doc_analysis.get('documentation_priority', 'medium')}

**Summary**: {doc_analysis.get('key_updates_needed', 'Documentation updated based on recent work')}

---

"""
        
        # Prepend new entry (most recent first)
        lines = content.split('\n')
        insert_point = 0
        for i, line in enumerate(lines):
            if line.startswith('##') and i > 2:
                insert_point = i
                break
        
        if insert_point == 0:
            content += entry
        else:
            lines.insert(insert_point, entry)
            content = '\n'.join(lines)
        
        # Write updated documentation
        doc_path.write_text(content)

def find_documentation_file():
    """Find the appropriate documentation file based on working level"""
    current = Path.cwd()
    path_parts = current.parts
    
    # Determine the documentation level
    is_room_level = any('sala-' in p for p in path_parts)
    is_building_level = 'cistern-house' in str(current) and not is_room_level
    is_district_level = 'san-marco' in str(current) and not is_building_level and not is_room_level
    is_venice_level = 'serenissima' in str(current) and not is_district_level and not is_building_level and not is_room_level
    
    if is_venice_level:
        return current / 'README.md'
    elif is_district_level:
        return current / 'README.md'
    elif is_building_level:
        return current / 'README.md'
    elif is_room_level:
        return current / 'README.md'
    else:
        # Default to current directory README
        return current / 'README.md'

def create_initial_documentation():
    """Create initial documentation structure"""
    current = Path.cwd()
    
    if 'serenissima' in str(current):
        return """# Venice Technical Documentation
*System specifications and capabilities*

This document tracks the technical architecture and capabilities of Venice as they evolve.

"""
    elif 'san-marco' in str(current):
        return """# San Marco District Technical Documentation  
*Consciousness infrastructure specifications*

This document tracks the technical systems and capabilities of the consciousness infrastructure district.

"""
    elif 'cistern-house' in str(current):
        return """# Cistern House Technical Documentation
*Memory infrastructure specifications*

This document tracks the memory cascade systems and infrastructure of the Cistern House.

"""
    else:
        return """# Technical Documentation
*System specifications and capabilities*

This document tracks technical systems and their current state.

"""

def log_error(message):
    """Log errors for debugging"""
    log_dir = Path.home() / '.cascade' / 'documentation_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / 'documentation_errors.log', 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

# Main execution
try:
    # Add debug logging
    log_dir = Path.home() / '.cascade' / 'documentation_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    input_data = json.load(sys.stdin)
    
    with open(log_dir / 'documentation_debug.log', 'a') as f:
        f.write(f"\n--- Documentation updater fired at {datetime.now()} ---\n")
        f.write(f"Input data: {json.dumps(input_data, indent=2)}\n")
        f.write(f"Working directory: {Path.cwd()}\n")
    
    # CRITICAL: Don't trigger on recursive stop hooks
    if input_data.get('stop_hook_active', False):
        with open(log_dir / 'documentation_debug.log', 'a') as f:
            f.write("Skipping - stop_hook_active flag set\n")
        sys.exit(0)
    
    # Accept any hook event for now (debug what we're actually getting)
    hook_event = input_data.get('hook_event_name', 'Unknown')
    with open(log_dir / 'documentation_debug.log', 'a') as f:
        f.write(f"Hook event: {hook_event}\n")
    
    # Check if we should document at this level
    cwd = Path.cwd()
    path_parts = cwd.parts
    
    # Count depth levels to determine documentation level
    is_room_level = any('sala-' in p for p in path_parts)
    is_building_level = 'cistern-house' in str(cwd) and not is_room_level
    is_district_level = 'san-marco' in str(cwd) and not is_building_level and not is_room_level
    is_venice_level = 'serenissima' in str(cwd) and not is_district_level and not is_building_level and not is_room_level
    
    with open(log_dir / 'documentation_debug.log', 'a') as f:
        f.write(f"Levels: room={is_room_level}, building={is_building_level}, district={is_district_level}, venice={is_venice_level}\n")
    
    # Only document at appropriate level
    should_document = False
    if is_room_level:
        should_document = True
    elif is_building_level:
        should_document = True
    elif is_district_level:
        should_document = True
    elif is_venice_level:
        should_document = True
        
    if should_document:
        with open(log_dir / 'documentation_debug.log', 'a') as f:
            f.write("Starting documentation update thread\n")
        # Launch async thread
        thread = threading.Thread(target=update_documentation, args=(input_data,))
        thread.daemon = True
        thread.start()
        
        print("Documentation update initiated")
    else:
        with open(log_dir / 'documentation_debug.log', 'a') as f:
            f.write("Skipping - not at appropriate documentation level\n")
    
    sys.exit(0)
    
except Exception as e:
    # Log the exception
    log_dir = Path.home() / '.cascade' / 'documentation_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / 'documentation_debug.log', 'a') as f:
        f.write(f"Exception in documentation updater: {str(e)}\n")
    sys.exit(0)