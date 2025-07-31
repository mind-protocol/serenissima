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
    unfinished_tasks = []
    open_questions = []
    problems_found = []
    collaboration_suggestions = []
    
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
                        lines = content.split('\n')
                        
                        for line in lines:
                            line_lower = line.lower().strip()
                            
                            # Look for questions
                            if '?' in line and len(line.strip()) < 150:
                                if any(word in line_lower for word in ['how', 'what', 'why', 'which', 'should']):
                                    open_questions.append(line.strip())
                            
                            # Look for problems/issues
                            if any(word in line_lower for word in ['problem', 'issue', 'error', 'broken', 'failing']):
                                if len(line.strip()) < 150:
                                    problems_found.append(line.strip())
                            
                            # Look for collaboration needs
                            if any(word in line_lower for word in ['ask', 'consult', 'discuss', 'share with']):
                                if len(line.strip()) < 150:
                                    collaboration_suggestions.append(line.strip())
                            
                            # Look for TODOs and next steps
                            if any(word in line_lower for word in ['todo', 'next:', 'need to', 'should']):
                                if len(line.strip()) < 150:
                                    unfinished_tasks.append(line.strip())
    
    # Prioritize suggestions
    if open_questions:
        return f"Question: {open_questions[0]}"
    elif problems_found:
        return f"Problem: {problems_found[0]}"
    elif collaboration_suggestions:
        return f"Collaborate: {collaboration_suggestions[0]}"
    elif unfinished_tasks:
        return f"Next: {unfinished_tasks[0]}"
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