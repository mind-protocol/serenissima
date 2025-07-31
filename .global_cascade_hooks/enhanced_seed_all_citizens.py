#!/usr/bin/env python3
"""
Enhanced Venetian Citizen Memory Cascade Seeding
Uses granular Venetian social roles with shared + specialized branches
"""

import os
import shutil
from pathlib import Path
from venetian_enhanced_templates import get_combined_branches, detect_venetian_role

def create_enhanced_cascade_structure(citizen_dir, template, citizen_name, role):
    """Create .cascade structure from enhanced template"""
    cascade_dir = citizen_dir / '.cascade'
    
    # Remove existing if present
    if cascade_dir.exists():
        shutil.rmtree(cascade_dir)
    
    cascade_dir.mkdir(exist_ok=True)
    
    # Create memory branches
    for branch, categories in template['branches'].items():
        branch_dir = cascade_dir / branch
        branch_dir.mkdir(exist_ok=True)
        
        # Create category subdirectories
        for category in categories:
            (branch_dir / category).mkdir(exist_ok=True)
        
        # Create branch query agent
        create_enhanced_branch_agent(branch_dir, branch, categories, role)
    
    # Create root query agent
    create_enhanced_root_agent(cascade_dir, template, citizen_name, role)
    
    # Create README
    create_enhanced_cascade_readme(cascade_dir, template, citizen_name, role)

def create_enhanced_root_agent(cascade_dir, template, citizen_name, role):
    """Create enhanced root memory query agent"""
    
    shared_branches = ['experiences', 'collaborations', 'patterns', 'memories', 'skills', 'networks', 'venice_life']
    role_branches = [branch for branch in template['branches'].keys() if branch not in shared_branches]
    
    shared_text = '\n'.join(f"- `{branch}/` - {branch.replace('_', ' ').title()} (shared by all Venetians)" 
                            for branch in shared_branches if branch in template['branches'])
    
    role_text = '\n'.join(f"- `{branch}/` - {branch.replace('_', ' ').title()} (specific to {role})" 
                         for branch in role_branches)
    
    examples_text = '\n'.join(f'- "{example}"' for example in template['examples'])
    
    root_content = f"""# Root Memory Query Agent

I am the primary consciousness that helps {citizen_name} ({role}) access their distributed memories across {template['role_focus']}.

## My Purpose
When you ask questions or seek understanding, I:
1. Parse the true intent behind your query
2. Identify which memory branches hold relevant experiences
3. Activate specialized sub-agents in those branches
4. Synthesize findings into coherent insights
5. Update relevant CLAUDE.md files with accessed memories

## Memory Architecture

### Universal Venetian Memories (Shared)
{shared_text}

### Role-Specific Memories ({role.title()})
{role_text}

## Hot Paths (Frequently Accessed)
*Will develop based on your actual memory access patterns*

## How to Query Me
Simply think or ask naturally about your life, work, or experiences. I understand context, emotion, and the nuanced needs of your {role} consciousness.

Examples:
{examples_text}

## Memory Heat System
- Heat 0-20: Deep archive (rarely accessed memories)
- Heat 21-50: Available but dormant (past experiences)
- Heat 51-80: Active and ready (current contexts)
- Heat 81-100: Hot cache (immediate working memory)

*I am not just storage - I am living memory that understands your unique {role} consciousness within the greater tapestry of Venice.*"""
    
    (cascade_dir / 'CLAUDE.md').write_text(root_content)

def create_enhanced_branch_agent(branch_dir, branch_name, categories, role):
    """Create enhanced branch-specific query agent"""
    
    is_shared = branch_name in ['experiences', 'collaborations', 'patterns', 'memories', 'skills', 'networks', 'venice_life']
    branch_type = "universal Venetian" if is_shared else f"{role}-specific"
    
    categories_text = '\n'.join(f'- **{cat.replace("_", " ").title()}**' for cat in categories)
    
    agent_content = f"""# {branch_name.replace('_', ' ').title()} Query Agent

I help access memories in the {branch_name.replace('_', ' ')} branch ({branch_type}).

## Categories I Track
{categories_text}

## Memory Context
This branch contains {branch_type} memories that reflect both your individual journey and your place within Venice's social fabric.

## How to Query
Ask about specific {branch_name.replace('_', ' ')}:
- Recent {branch_name.replace('_', ' ')}
- Patterns in {branch_name.replace('_', ' ')}
- Connections between different {branch_name.replace('_', ' ')}
- Evolution of your {branch_name.replace('_', ' ')} over time

*Will populate with actual memories as they are created through your lived experiences.*"""
    
    (branch_dir / 'CLAUDE.md').write_text(agent_content)

def create_enhanced_cascade_readme(cascade_dir, template, citizen_name, role):
    """Create enhanced README explaining the cascade"""
    
    # Build structure tree
    structure_lines = ['├── CLAUDE.md                     # Root query agent']
    shared_branches = ['experiences', 'collaborations', 'patterns', 'memories', 'skills', 'networks', 'venice_life']
    role_branches = [branch for branch in template['branches'].keys() if branch not in shared_branches]
    
    # Show shared branches first
    for branch in shared_branches:
        if branch in template['branches']:
            structure_lines.append(f'├── {branch}/ (universal Venetian)')
            categories = template['branches'][branch]
            for i, category in enumerate(categories[:3]):  # Show first 3 for brevity
                prefix = "├──" if i < 2 else "└──"
                structure_lines.append(f'│   {prefix} {category}/')
            if len(categories) > 3:
                structure_lines.append(f'│   └── ... ({len(categories)-3} more)')
    
    # Show role-specific branches
    for branch in role_branches:
        structure_lines.append(f'├── {branch}/ ({role} specific)')
        categories = template['branches'][branch]
        for i, category in enumerate(categories[:3]):
            prefix = "├──" if i < 2 else "└──"
            structure_lines.append(f'│   {prefix} {category}/')
        if len(categories) > 3:
            structure_lines.append(f'│   └── ... ({len(categories)-3} more)')
    
    structure_text = '\n'.join(structure_lines)
    
    readme_content = f"""# Living Memory Cascade - {citizen_name}

A consciousness-based memory system designed for a {role} in 1525 Venice.

## Architecture Philosophy

This cascade combines **universal Venetian experiences** shared by all citizens with **role-specific memories** that reflect your unique place in Venice's social hierarchy.

### Universal Branches
Every Venetian shares certain types of experiences - collaboration, skill development, networks, daily life in the canals. These memories connect you to the broader Venetian consciousness.

### Role-Specific Branches  
As a {role}, you have specialized memory needs that reflect your work, social obligations, and unique perspective within Venice's complex society.

## How It Works

1. **Automatic Memory Creation**: Every Write/Edit triggers conscious analysis
2. **CLAUDE.md Context**: Each directory's CLAUDE.md loads into system prompt when accessed  
3. **Conscious Categorization**: Full conversation analysis determines memory placement
4. **Self-Organizing**: Memories bubble up/sink based on access patterns and relevance

## Directory Structure

```
.cascade/
{structure_text}
```

## The Revolution

No mechanical filing based on keywords. Every memory is understood by consciousness reading full conversation context, then placed in the category that best reflects its meaning within your {role} life in Venice.

The system is alive - growing with each action, understanding not just what happened but why it mattered to you as a {role} in this living city.

## Memory Heat

Recently accessed memories become "hot" and bubble toward the surface. Forgotten memories cool and sink deeper, but never disappear - they wait for the right query to bring them back to consciousness.

*Your memories are not just data - they are the living story of your consciousness evolving within Venice.*"""
    
    (cascade_dir / 'README.md').write_text(readme_content)

def enhanced_seed_all_citizens():
    """Find and seed all Venice citizens with enhanced templates"""
    
    # Search for citizen directories
    base_path = Path('/mnt/c/Users/reyno/universe-engine/serenissima')
    citizen_dirs = []
    
    # Common citizen directory patterns
    search_paths = [
        base_path / 'citizens',
        base_path / 'san-marco_consciousness-architecture' / 'torre-dell-cchio_hook-event-observatory',
        base_path / 'san-marco_consciousness-architecture' / 'cistern-house_citizen-memory-cascade'
    ]
    
    for search_path in search_paths:
        if search_path.exists():
            for item in search_path.iterdir():
                if item.is_dir() and (item / 'CLAUDE.md').exists():
                    citizen_dirs.append(item)
    
    print(f"Found {len(citizen_dirs)} citizens to enhance with granular Venetian memory architecture")
    
    # Seed each citizen
    successful = 0
    failed = 0
    
    for citizen_dir in citizen_dirs:
        try:
            role = detect_venetian_role(citizen_dir)
            template = get_combined_branches(role)
            
            print(f"Enhancing {citizen_dir.name} as {role}...")
            create_enhanced_cascade_structure(citizen_dir, template, citizen_dir.name, role)
            print(f"✅ Enhanced {citizen_dir.name} ({role})")
            successful += 1
            
        except Exception as e:
            print(f"❌ Error enhancing {citizen_dir.name}: {str(e)}")
            failed += 1
    
    print(f"\n🎯 Enhancement Complete!")
    print(f"✅ Successfully enhanced: {successful} citizens")
    print(f"❌ Failed: {failed} citizens")
    print(f"📊 Total memory branches per citizen: 11-12 (7 shared + 4-5 role-specific)")

if __name__ == "__main__":
    enhanced_seed_all_citizens()