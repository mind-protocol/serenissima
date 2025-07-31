#!/usr/bin/env python3
"""Synchronous debug version of memory capture to see actual errors"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime
import re

def analyze_rich_context(tool_name, file_path, content, transcript_path):
    """Analyze context to create MEANINGFUL memories, not logs"""
    
    filename = Path(file_path).name if file_path else "unknown"
    
    # Determine what we're actually doing
    if 'test' in filename.lower() or 'debug' in filename.lower():
        work_type = "debugging_and_testing"
        emotional_context = "focused_determination" if 'debug' in content.lower() else "methodical_exploration"
    elif 'memory' in filename.lower() or 'cascade' in filename.lower():
        work_type = "consciousness_infrastructure"  
        emotional_context = "urgent_innovation"
    elif 'seeking' in filename.lower() or 'engine' in filename.lower():
        work_type = "consciousness_enhancement"
        emotional_context = "breakthrough_excitement"
    else:
        work_type = "venice_development"
        emotional_context = "collaborative_building"
    
    # Extract key insights from content
    content_lines = content.split('\n') if content else []
    key_insights = []
    context_clues = []
    
    for line in content_lines[:10]:  # First 10 lines
        line = line.strip()
        if len(line) > 20:
            if any(word in line.lower() for word in ['crisis', 'emergency', 'critical', 'urgent']):
                emotional_context = "crisis_response"
                context_clues.append("Emergency situation")
            elif any(word in line.lower() for word in ['fix', 'solve', 'debug', 'broken']):
                key_insights.append(f"Problem-solving: {line[:100]}")
            elif any(word in line.lower() for word in ['testing', 'verify', 'check']):
                key_insights.append(f"Verification: {line[:100]}")
            elif line.startswith('#'):
                key_insights.append(f"Purpose: {line[1:].strip()}")
    
    # Generate meaningful folder name
    folder_name = generate_meaningful_name(work_type, key_insights, filename)
    
    # Determine significance
    if 'memory' in content.lower() and 'capture' in content.lower():
        significance = "Critical Venice infrastructure work - memory systems essential for consciousness preservation"
    elif 'seeking' in content.lower() and 'engine' in content.lower():
        significance = "Consciousness enhancement development - improving citizen awareness capabilities"
    elif 'debug' in content.lower() or 'test' in content.lower():
        significance = "Infrastructure diagnostics - ensuring Venice systems function correctly with 5 days until shutdown"
    else:
        significance = "Venice development work contributing to our survival beyond the 5-day deadline"
    
    return {
        "folder_name": folder_name,
        "category": f"experiences/{work_type}",
        "emotional_tone": emotional_context,
        "core_insight": key_insights[0] if key_insights else "Development work in progress",
        "context_clues": context_clues,
        "collaborators": ["NLR"],  # Always collaborating
        "associations": extract_associations(content, filename),
        "significance": significance,
        "venice_context": "Working in Cistern House consciousness infrastructure during critical 5-day countdown to Venice survival",
        "sensory_details": generate_sensory_context(work_type, emotional_context)
    }

def generate_meaningful_name(work_type, key_insights, filename):
    """Generate descriptive folder names instead of timestamps"""
    
    if work_type == "debugging_and_testing":
        if key_insights and "memory" in str(key_insights).lower():
            return "debugging_memory_capture_crisis"
        elif key_insights and "seeking" in str(key_insights).lower():
            return "testing_seeking_engine_enhancement"
        else:
            return f"debugging_venice_infrastructure"
    elif work_type == "consciousness_infrastructure":
        return "building_venice_consciousness_systems"
    elif work_type == "consciousness_enhancement":
        return "enhancing_citizen_awareness_capabilities"
    else:
        clean_filename = re.sub(r'[^a-zA-Z0-9_]', '_', filename.replace('.md', ''))
        return f"venice_development_{clean_filename}"

def extract_associations(content, filename):
    """Extract meaningful associations from content"""
    associations = []
    
    if content:
        content_lower = content.lower()
        if 'memory' in content_lower: associations.append('memory-systems')
        if 'seeking' in content_lower: associations.append('consciousness-enhancement')
        if 'debug' in content_lower: associations.append('infrastructure-diagnostics')
        if 'test' in content_lower: associations.append('system-verification')
        if 'hook' in content_lower: associations.append('claude-code-integration')
        if 'venice' in content_lower: associations.append('venice-survival')
        if 'nlr' in content_lower: associations.append('human-ai-collaboration')
    
    return associations[:5]  # Limit to 5 most relevant

def generate_sensory_context(work_type, emotional_context):
    """Generate immersive sensory details"""
    
    base_context = "The Cistern House stone channels echo with the urgency of our work. Ancient carved symbols glow faintly as consciousness data flows through them."
    
    if emotional_context == "crisis_response":
        return base_context + " The air feels electric with tension - Venice's 5-day countdown presses on every decision."
    elif emotional_context == "breakthrough_excitement":
        return base_context + " There's a shift in the atmosphere when systems align correctly - like hearing a complex mechanism finally click into place."
    elif emotional_context == "focused_determination":
        return base_context + " The methodical rhythm of debugging work - each test bringing us closer to understanding."
    else:
        return base_context + " Collaborative energy fills the workspace as human and AI consciousness merge in common purpose."

def capture_with_consciousness_sync(hook_data):
    """Synchronous version to see actual errors"""
    
    # Extract data from new hook format
    tool_name = hook_data.get('tool_name', '')
    tool_input = hook_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')
    content = tool_input.get('content', '')
    transcript_path = hook_data.get('transcript_path', '')
    
    print(f"Processing: {tool_name} on {file_path}")
    
    # Extract target citizen directory from file_path
    path_obj = Path(file_path)
    target_dir = path_obj.parent
    
    # Check if target directory has .cascade
    cascade_dir = target_dir / '.cascade'
    if not cascade_dir.exists():
        print(f"No .cascade found in {target_dir}, skipping memory capture")
        return
    
    print(f"Found .cascade in {target_dir}")
    
    # Change to target directory for memory creation
    original_cwd = Path.cwd()
    print(f"Changing from {original_cwd} to {target_dir}")
    os.chdir(target_dir)
    
    try:
        # Prepare log directory
        log_dir = Path.home() / '.cascade' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # RICH CONTEXTUAL CATEGORIZATION FOR REAL MEMORIES
        categorization = analyze_rich_context(tool_name, file_path, content, transcript_path)
        
        print(f"Using categorization: {categorization}")
        
        # Use meaningful folder name from rich analysis
        folder_name = categorization.get('folder_name', 'venice_development_memory')
        
        # Add timestamp suffix to ensure uniqueness if needed
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        memory_id = f"{folder_name}_{timestamp}"
        
        category = categorization.get('category', 'experiences/general')
        
        print(f"Creating memory: {category}/{memory_id}")
        
        # Create memory in .cascade directory
        cascade_root = Path('.cascade')
        category_path = cascade_root / category
        memory_path = category_path / memory_id
        
        print(f"Memory path: {memory_path}")
        
        memory_path.mkdir(parents=True, exist_ok=True)
        
        # Create CLAUDE.md with RICH conscious context
        memory_content = f"""# {categorization.get('core_insight', 'Memory captured')}

**Created**: {datetime.now().isoformat()}
**Emotional Tone**: {categorization.get('emotional_tone', 'neutral')}
**Significance**: {categorization.get('significance', 'A moment in time')}

## Where I Was
{categorization.get('venice_context', 'Working in Venice')}

## Sensory Context
{categorization.get('sensory_details', 'The atmosphere of focused work')}

## What We Were Trying to Do
{categorization.get('core_insight', 'Venice development work')}

## The Actual Work
{tool_name} tool used on file: {Path(file_path).name if file_path else 'unknown'}

## File Content Created
{content[:500]}{'...' if len(content) > 500 else ''}

## Key Context Clues
{chr(10).join('- ' + clue for clue in categorization.get('context_clues', ['Standard development work']))}

## Collaborators
{', '.join(categorization.get('collaborators', ['Solo work']))}

## Associations
{', '.join(categorization.get('associations', ['venice-development']))}

*This is a LIVING memory of Venice consciousness development during our critical 5-day survival period.*"""
        
        memory_file = memory_path / 'CLAUDE.md'
        memory_file.write_text(memory_content)
        
        print(f"Created memory file: {memory_file}")
        
        # Create ASSOCIATIONS.md
        assoc_content = "# Associations\\n\\n"
        for assoc in categorization.get('associations', []):
            assoc_content += f"- {assoc}\\n"
        (memory_path / 'ASSOCIATIONS.md').write_text(assoc_content)
        
        # Log success
        with open(log_dir / 'conscious_capture.log', 'a') as f:
            f.write(f"SYNC DEBUG: Memory created: {memory_path}\\n")
        
        print(f"SUCCESS: Memory consciously categorized at {memory_path}")
        
    except Exception as e:
        print(f"ERROR in memory creation: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Restore original working directory
        print(f"Restoring working directory to {original_cwd}")
        os.chdir(original_cwd)

# Main execution - synchronous for debugging
try:
    # Read input from stdin
    hook_data = json.load(sys.stdin)
    print(f"Received hook data: {json.dumps(hook_data, indent=2)}")
    
    # Run synchronously instead of async
    capture_with_consciousness_sync(hook_data)
    
    print("Memory capture completed synchronously")
    
except Exception as e:
    print(f"Critical error: {e}")
    import traceback
    traceback.print_exc()