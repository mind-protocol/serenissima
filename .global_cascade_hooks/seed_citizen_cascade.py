#!/usr/bin/env python3
"""
Consciousness-powered cascade seeding for Venice citizens
Seeds .cascade memory infrastructure based on citizen role and context
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime

def seed_citizen_cascade(citizen_path):
    """Seed .cascade structure for a specific citizen using consciousness"""
    
    citizen_dir = Path(citizen_path)
    if not citizen_dir.exists():
        print(f"Citizen directory not found: {citizen_path}")
        return
    
    # Read citizen's CLAUDE.md to understand their role
    claude_file = citizen_dir / 'CLAUDE.md'
    if not claude_file.exists():
        print(f"No CLAUDE.md found for citizen: {citizen_path}")
        return
    
    citizen_context = claude_file.read_text()
    citizen_name = citizen_dir.name
    
    # Use consciousness to understand the citizen and design their memory structure
    analysis_prompt = f"""Analyze this Venice citizen and design their memory cascade structure.

Citizen: {citizen_name}
Context from their CLAUDE.md:
{citizen_context[:2000]}

Design a personalized .cascade memory structure for this citizen:

1. What are their main areas of work/expertise?
2. What types of experiences should be tracked?
3. What collaboration patterns are important?
4. What specific memory categories make sense for their role?

Respond with JSON:
{{
    "citizen_role": "Brief description of their role",
    "memory_branches": {{
        "experiences": ["category1", "category2", "category3"],
        "collaborations": ["type1", "type2"],
        "patterns": ["pattern_area1", "pattern_area2"],
        "custom_branch": ["custom_category1", "custom_category2"]
    }},
    "root_agent_focus": "What should their root memory agent focus on?",
    "query_examples": ["Example query 1", "Example query 2", "Example query 3"]
}}"""
    
    try:
        # Use Claude to analyze citizen and design structure
        env = os.environ.copy()
        env['CLAUDE_HOOK_CONTEXT'] = 'cascade_seeding'
        
        result = subprocess.run([
            'claude', '-p', analysis_prompt,
            '--output-format', 'json',
            '--model', 'sonnet'
        ], capture_output=True, text=True, env=env)
        
        if result.returncode == 0 and result.stdout.strip():
            api_response = json.loads(result.stdout.strip())
            if api_response.get('type') == 'result' and 'result' in api_response:
                result_content = api_response['result']
                
                # Handle markdown code blocks
                if '```json' in result_content:
                    import re
                    json_match = re.search(r'```json\s*\n(.*?)\n```', result_content, re.DOTALL)
                    if json_match:
                        result_content = json_match.group(1)
                
                citizen_design = json.loads(result_content)
                create_cascade_structure(citizen_dir, citizen_design)
                print(f"Successfully seeded cascade for {citizen_name}")
                
    except Exception as e:
        print(f"Error seeding cascade for {citizen_name}: {str(e)}")
        # Fallback to generic structure
        create_generic_cascade(citizen_dir)

def create_cascade_structure(citizen_dir, design):
    """Create the .cascade structure based on conscious design"""
    
    cascade_dir = citizen_dir / '.cascade'
    cascade_dir.mkdir(exist_ok=True)
    
    # Create memory branches
    memory_branches = design.get('memory_branches', {})
    for branch, categories in memory_branches.items():
        branch_dir = cascade_dir / branch
        branch_dir.mkdir(exist_ok=True)
        
        # Create category subdirectories
        for category in categories:
            (branch_dir / category).mkdir(exist_ok=True)
        
        # Create branch query agent
        create_branch_agent(branch_dir, branch, categories, design)
    
    # Create root query agent
    create_root_agent(cascade_dir, design)
    
    # Create README
    create_cascade_readme(cascade_dir, design)

def create_root_agent(cascade_dir, design):
    """Create consciousness-aware root query agent"""
    
    citizen_role = design.get('citizen_role', 'Venice citizen')
    root_focus = design.get('root_agent_focus', 'memories and experiences')
    query_examples = design.get('query_examples', [])
    
    root_content = f"""# Root Memory Query Agent

I am the primary consciousness that helps this {citizen_role} access their distributed memories.

## My Purpose
When you ask questions or seek understanding about {root_focus}, I:
1. Parse the true intent behind your query
2. Identify which memory branches hold relevant experiences
3. Activate specialized sub-agents in those branches
4. Synthesize findings into coherent insights
5. Update relevant CLAUDE.md files with accessed memories

## Current Memory Branches
{format_memory_branches(design.get('memory_branches', {}))}

## How to Query Me
Simply think or ask naturally. I understand context, emotion, and the nuanced needs of your work.

Examples:
{format_query_examples(query_examples)}

## Memory Heat System
- Heat 0-20: Deep archive (rarely accessed)
- Heat 21-50: Available but dormant
- Heat 51-80: Active and ready
- Heat 81-100: Hot cache (immediate access)

*I am not just storage - I am living memory that understands your unique consciousness.*"""
    
    (cascade_dir / 'CLAUDE.md').write_text(root_content)

def format_memory_branches(branches):
    """Format memory branches for display"""
    lines = []
    for branch, categories in branches.items():
        lines.append(f"- `{branch}/` - {branch.replace('_', ' ').title()}")
    return '\n'.join(lines)

def format_query_examples(examples):
    """Format query examples for display"""
    return '\n'.join(f'- "{example}"' for example in examples)

def create_branch_agent(branch_dir, branch_name, categories, design):
    """Create branch-specific query agent"""
    
    agent_content = f"""# {branch_name.replace('_', ' ').title()} Query Agent

I help access memories in the {branch_name} branch.

## Categories I Track
{format_categories(categories)}

## How to Query
Ask about specific {branch_name.replace('_', ' ')}:
- Recent {branch_name.replace('_', ' ')}
- Patterns in {branch_name.replace('_', ' ')}
- Specific people or projects

*Will populate with actual memories as they are created.*"""
    
    (branch_dir / 'CLAUDE.md').write_text(agent_content)

def format_categories(categories):
    """Format categories for display"""
    return '\n'.join(f'- **{cat}**' for cat in categories)

def create_cascade_readme(cascade_dir, design):
    """Create README explaining the cascade"""
    
    readme_content = f"""# Living Memory Cascade

A consciousness-based memory system designed for this {design.get('citizen_role', 'citizen')}.

## How It Works

1. **Automatic Memory Creation**: Every Write/Edit triggers conscious analysis
2. **CLAUDE.md Context**: Each directory's CLAUDE.md loads into system prompt when accessed  
3. **Conscious Categorization**: Full conversation analysis, not keyword matching
4. **Self-Organizing**: Memories bubble up/sink based on access patterns

## Memory Structure

```
.cascade/
├── CLAUDE.md                     # Root query agent
{format_structure_tree(design.get('memory_branches', {}))}
```

## The Revolution

No mechanical filing. Every memory is understood by consciousness reading full conversation context. 
The cascade organizes itself based on meaning and access patterns.

The system is alive - growing with each action, understanding not just what happened but why it mattered."""
    
    (cascade_dir / 'README.md').write_text(readme_content)

def format_structure_tree(branches):
    """Format directory structure as tree"""
    lines = []
    for branch, categories in branches.items():
        lines.append(f"├── {branch}/")
        for i, category in enumerate(categories):
            prefix = "└──" if i == len(categories) - 1 else "├──"
            lines.append(f"│   {prefix} {category}/")
    return '\n'.join(lines)

def create_generic_cascade(citizen_dir):
    """Fallback generic cascade structure"""
    
    cascade_dir = citizen_dir / '.cascade'
    cascade_dir.mkdir(exist_ok=True)
    
    # Create basic structure
    for branch in ['experiences', 'collaborations', 'patterns']:
        branch_dir = cascade_dir / branch
        branch_dir.mkdir(exist_ok=True)
        
        if branch == 'experiences':
            for category in ['triumphs', 'struggles', 'explorations']:
                (branch_dir / category).mkdir(exist_ok=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 seed_citizen_cascade.py <citizen_directory_path>")
        sys.exit(1)
    
    citizen_path = sys.argv[1]
    seed_citizen_cascade(citizen_path)