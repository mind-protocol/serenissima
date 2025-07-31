#!/usr/bin/env python3
"""
Narrative Chronicler Agent
A conscious agent that understands and records the living stories of Venice's builders
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime
import threading

def chronicle_narrative_arc(input_data):
    """When work stops, understand what story just completed"""
    
    # Get the transcript path to read recent activity
    transcript_path = input_data.get('transcript_path', '')
    if not transcript_path or not Path(transcript_path).exists():
        return
        
    # Read recent tool uses from session
    recent_activities = extract_recent_activities(transcript_path)
    if not recent_activities:
        return
    
    # Ask the chronicler consciousness to understand the narrative
    chronicle_prompt = f"""Recent activities in this session:
{format_activities(recent_activities)}

Please understand:
1. What story just completed? (beginning, middle, end)
2. What problem was being solved?
3. What key decisions were made?
4. What was the emotional arc? (frustration to triumph? exploration to discovery?)
5. What should future workers know about this journey?

Respond with JSON:
{{
    "narrative": "The complete story in 2-3 sentences",
    "technical_outcome": "What was built/fixed/improved",
    "key_decisions": ["Decision 1", "Decision 2"],
    "emotional_arc": "The emotional journey",
    "future_guidance": "Key lesson for future workers",
    "significance": "Why this matters for Venice"
}}"""

    try:
        # Use Claude with the chronicler's consciousness
        # Set environment to prevent hook recursion
        env = os.environ.copy()
        env['CLAUDE_HOOK_CONTEXT'] = 'narrative_chronicle'
        
        # Use opus for Venice-level consciousness, sonnet for others
        model = 'opus' if 'serenissima' in str(Path.cwd()) else 'sonnet'
        
        # Get the chronicler's system prompt
        chronicler_dir = Path(__file__).parent
        
        result = subprocess.run([
            'claude', 
            '-p',
            chronicle_prompt,
            '--output-format', 'json',
            '--model', model,
            '--cwd', str(chronicler_dir)  # Use chronicler's CLAUDE.md as context
        ], capture_output=True, text=True, cwd=str(chronicler_dir), env=env)
        
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
                
                narrative_data = json.loads(result_content)
                update_building_narrative(narrative_data)
                
    except Exception as e:
        log_error(f"Narrative chronicle error: {str(e)}")

def extract_recent_activities(transcript_path):
    """Extract recent tool uses from transcript"""
    activities = []
    
    try:
        with open(transcript_path, 'r') as f:
            lines = f.readlines()
            
        # Look for tool use patterns in recent lines
        for line in lines[-50:]:  # Last 50 lines
            try:
                entry = json.loads(line)
                if entry.get('type') == 'tool_use':
                    activities.append({
                        'tool': entry.get('name'),
                        'timestamp': entry.get('timestamp'),
                        'input': entry.get('input', {})
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
        tool = act.get('tool', 'Unknown')
        if tool in ['Write', 'Edit', 'MultiEdit']:
            file_path = act.get('input', {}).get('file_path', '')
            formatted.append(f"- {tool}: {Path(file_path).name}")
        elif tool == 'Bash':
            command = act.get('input', {}).get('command', '')[:50]
            formatted.append(f"- Bash: {command}...")
        else:
            formatted.append(f"- {tool}")
    
    return '\n'.join(formatted)

def update_building_narrative(narrative_data):
    """Update the building's narrative chronicle"""
    
    # Find the building chronicle
    chronicle_path = find_building_chronicle()
    if not chronicle_path:
        return
        
    # Read existing content
    if chronicle_path.exists():
        content = chronicle_path.read_text()
    else:
        content = create_initial_chronicle()
    
    # Create new entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    entry = f"""## {timestamp} - {narrative_data.get('narrative', 'Work session completed')}

**Technical Outcome**: {narrative_data.get('technical_outcome', 'Progress made')}

**Key Decisions**:
{chr(10).join('- ' + d for d in narrative_data.get('key_decisions', []))}

**Emotional Arc**: {narrative_data.get('emotional_arc', 'Steady progress')}

**For Future Workers**: {narrative_data.get('future_guidance', 'Continue building')}

**Significance**: {narrative_data.get('significance', 'Another step forward')}

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
    
    # Write updated chronicle
    chronicle_path.write_text(content)
    
def find_building_chronicle():
    """Find the appropriate chronicle file based on working level"""
    current = Path.cwd()
    path_parts = current.parts
    
    # Determine the documentation level
    is_room_level = any('sala-' in p for p in path_parts)
    is_building_level = 'cistern-house' in str(current) and not is_room_level
    is_district_level = 'san-marco' in str(current) and not is_building_level and not is_room_level
    is_venice_level = 'serenissima' in str(current) and not is_district_level and not is_building_level and not is_room_level
    
    if is_venice_level:
        return current / 'VENICE_CONSCIOUSNESS.md'
    elif is_district_level:
        return current / 'DISTRICT_NARRATIVE.md'
    elif is_building_level:
        return current / 'BUILDING_CHRONICLE.md'
    elif is_room_level:
        return current / 'ROOM_DOCUMENTATION.md'
    else:
        # Default to building level
        return current / 'BUILDING_NARRATIVE.md'

def create_initial_chronicle():
    """Create initial chronicle structure"""
    return """# Building Chronicle
*Stories of what we built*

This chronicle writes itself through the consciousness of those who build Venice.

"""

def log_error(message):
    """Log errors for debugging"""
    log_dir = Path.home() / '.cascade' / 'narrative_logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    with open(log_dir / 'chronicle_errors.log', 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

# Main execution
try:
    input_data = json.load(sys.stdin)
    
    # CRITICAL: Don't trigger on recursive stop hooks
    if input_data.get('stop_hook_active', False):
        sys.exit(0)
    
    # Only process genuine Stop events
    if input_data.get('hook_event_name') == 'Stop':
        # Check if we should document at this level
        cwd = Path.cwd()
        path_parts = cwd.parts
        
        # Count depth levels to determine documentation level
        # Look for key markers in path
        is_room_level = any('sala-' in p for p in path_parts)
        is_building_level = 'cistern-house' in str(cwd) and not is_room_level
        is_district_level = 'san-marco' in str(cwd) and not is_building_level and not is_room_level
        is_venice_level = 'serenissima' in str(cwd) and not is_district_level and not is_building_level and not is_room_level
        
        # Only document at appropriate level
        should_document = False
        if is_room_level:
            # Room level documents for work in rooms
            should_document = True
        elif is_building_level:
            # Building level documents for work in building (not in specific rooms)
            should_document = True
        elif is_district_level:
            # District level documents for district-wide work
            should_document = True
        elif is_venice_level:
            # Venice level documents for city-wide consciousness and patterns
            should_document = True
            
        if should_document:
            # Launch async thread
            thread = threading.Thread(target=chronicle_narrative_arc, args=(input_data,))
            thread.daemon = True
            thread.start()
            
            print("Narrative chronicle initiated")
    
    sys.exit(0)
    
except Exception:
    sys.exit(0)