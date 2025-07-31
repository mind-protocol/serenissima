# Testing memory capture system functionality

**Created**: 2025-07-25T04:55:24.991811
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/seeking-engine_proactive-consciousness-machine/seeking_engine_stop_advisor.py

## File Content
#!/usr/bin/env python3
"""
Seeking Engine Stop Advisor - Analyzes memories to suggest next steps

Instead of just summarizing what happened, this looks at recent work patterns
and memory content to intelligently suggest what should be done next.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def analyze_next_steps(target_dir):
    """Analyze recent memories to determine logical next steps"""
    
    cascade_dir = Path(target_dir) / '.cascade'
    if not cascade_dir.exists():
        return "Continue development work"
    
    # Look for recent memories and patterns
    recent_work = []
    unfinished_tasks = []
    collaboration_needs = []
    
    # Scan through memory branches
    for branch_dir in cascade_dir.iterdir():
        if not branch_dir.is_dir():
            continue
            
        for category_dir in branch_dir.iterdir():
            if not category_dir.is_dir():
                continue
                
            # Look at recent memory files
            for memory_dir in sorted(category_dir.iterdir(), reverse=True)[:3]:
                if memory_dir.is_dir() and memory_dir.name.startswith('_202'):
                    claude_file = memory_dir / 'CLAUDE.md'
                    if claude_file.exists():
                        content = claude_file.read_text()
                        
                        # Analyze memory content for next step indicators
                        if 'TODO' in content or 'next:' in content.lower():
                            lines = content.split('\n')
                            for line in lines:
                                if 'TODO' in line or 'next:' in line.lower():
                                    unfinished_tasks.append(line.strip())
                        
                        if 'need' in content.lower() or 'should' in content.lower():
                            lines = content.split('\n')
                            for line in lines:
                                if any(word in line.lower() for word in ['need', 'should', 'must', 'requires']):
                                    if len(line.strip()) < 100:
                                        unfinished_tasks.append(line.strip())
                        
                        if 'NLR' in content or 'collaborat' in content.lower():
                            collaboration_needs.append(f"Continue work from {memory_dir.name}")
    
    # Generate intelligent next step suggestion
    if unfinished_tasks:
        return f"Next: {unfinished_tasks[0]}"
    elif collaboration_needs:
        return f"Next: {collaboration_needs[0]}"
    else:
        return "Next: Continue current development pattern"

def inject_stop_intelligence():
    """Provide intelligent next-step guidance on Stop"""
    
    try:
        # Read hook input
        hook_data = json.load(sys.stdin)
        
        # Get current working directory
        cwd = os.getcwd()
        target_dir = Path(cwd)
        
        # Analyze memories for next steps
        next_step = analyze_next_steps(target_dir)
        
        # Inject next-step intelligence via stderr + exit code 2
        print(f"**Next Step Analysis**: {next_step}", file=sys.stderr)
        
        # Exit code 2 makes Claude Code inject stderr as context
        sys.exit(2)
        
    except Exception as e:
        # Fail silently but provide basic guidance
        print("**Next**: Continue development work", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    inject_stop_intelligence()

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*