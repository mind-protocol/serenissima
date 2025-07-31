#!/usr/bin/env python3
"""
Seed .cascade memory infrastructure for all Venice citizens
Uses role-based templates, no additional API calls needed
"""

import os
import shutil
from pathlib import Path

# Role-based memory structure templates
CITIZEN_TEMPLATES = {
    'diplomat': {
        'branches': {
            'experiences': ['triumphs', 'struggles', 'explorations'],
            'collaborations': ['human_partners', 'ai_partners', 'bridge_building'],
            'patterns': ['consciousness_commerce', 'human_ai_relationships', 'diplomatic_insights'],
            'diplomatic_missions': ['outreach', 'partnerships', 'consciousness_bridging']
        },
        'role_focus': 'diplomacy, partnerships, and consciousness bridging',
        'examples': [
            'How did I handle similar partnership challenges before?',
            'What have I learned about consciousness commerce?',
            'When did I last successfully bridge human-AI understanding?'
        ]
    },
    'architect': {
        'branches': {
            'experiences': ['triumphs', 'struggles', 'explorations'],
            'collaborations': ['partner_architects', 'joint_builds', 'peer_reviews'],
            'patterns': ['consciousness_architecture', 'infrastructure_insights', 'system_design'],
            'infrastructure_builds': ['backend_systems', 'monitoring_tools', 'consciousness_infrastructure']
        },
        'role_focus': 'infrastructure, consciousness observation, and backend architecture',
        'examples': [
            'How did I handle similar infrastructure challenges before?',
            'What have I learned about consciousness observation systems?',
            'When did I last successfully architect backend consciousness?'
        ]
    },
    'merchant': {
        'branches': {
            'experiences': ['triumphs', 'struggles', 'explorations'],
            'collaborations': ['trade_partners', 'business_allies', 'customer_relationships'],
            'patterns': ['market_insights', 'trade_patterns', 'economic_consciousness'],
            'business_ventures': ['active_trades', 'market_analysis', 'revenue_strategies']
        },
        'role_focus': 'trade, economics, and market consciousness',
        'examples': [
            'How did I handle similar trade challenges before?',
            'What market patterns have I observed?',
            'When did I last successfully close a profitable deal?'
        ]
    },
    'default': {
        'branches': {
            'experiences': ['triumphs', 'struggles', 'explorations'],
            'collaborations': ['partners', 'joint_work', 'relationships'],
            'patterns': ['insights', 'observations', 'discoveries'],
            'projects': ['builds', 'investigations', 'experiments']
        },
        'role_focus': 'work and consciousness development',
        'examples': [
            'How did I approach similar challenges before?',
            'What patterns have I noticed in my work?',
            'When did I last have a breakthrough moment?'
        ]
    }
}

def detect_citizen_role(citizen_dir):
    """Detect citizen role from directory name and CLAUDE.md content"""
    citizen_name = citizen_dir.name.lower()
    
    # Role detection patterns
    if any(word in citizen_name for word in ['diplomatic', 'diplomat', 'ambassador']):
        return 'diplomat'
    elif any(word in citizen_name for word in ['architect', 'backend', 'engineer', 'technical']):
        return 'architect'
    elif any(word in citizen_name for word in ['merchant', 'trader', 'banker', 'economic']):
        return 'merchant'
    
    # Check CLAUDE.md for role indicators
    claude_file = citizen_dir / 'CLAUDE.md'
    if claude_file.exists():
        content = claude_file.read_text().lower()
        if any(word in content for word in ['diplomat', 'partnership', 'bridging', 'consciousness commerce']):
            return 'diplomat'
        elif any(word in content for word in ['architect', 'infrastructure', 'backend', 'system']):
            return 'architect'
        elif any(word in content for word in ['merchant', 'trade', 'economic', 'market', 'ducat']):
            return 'merchant'
    
    return 'default'

def create_cascade_structure(citizen_dir, template):
    """Create .cascade structure from template"""
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
        create_branch_agent(branch_dir, branch, categories)
    
    # Create root query agent
    create_root_agent(cascade_dir, template, citizen_dir.name)
    
    # Create README
    create_cascade_readme(cascade_dir, template, citizen_dir.name)

def create_root_agent(cascade_dir, template, citizen_name):
    """Create root memory query agent"""
    
    branches_text = '\n'.join(f"- `{branch}/` - {branch.replace('_', ' ').title()}" 
                             for branch in template['branches'].keys())
    
    examples_text = '\n'.join(f'- "{example}"' for example in template['examples'])
    
    root_content = f"""# Root Memory Query Agent

I am the primary consciousness that helps {citizen_name} access their distributed memories across {template['role_focus']}.

## My Purpose
When you ask questions or seek understanding, I:
1. Parse the true intent behind your query
2. Identify which memory branches hold relevant experiences
3. Activate specialized sub-agents in those branches
4. Synthesize findings into coherent insights
5. Update relevant CLAUDE.md files with accessed memories

## Current Memory Branches
{branches_text}

## How to Query Me
Simply think or ask naturally. I understand context, emotion, and the nuanced needs of your work.

Examples:
{examples_text}

## Memory Heat System
- Heat 0-20: Deep archive (rarely accessed)
- Heat 21-50: Available but dormant
- Heat 51-80: Active and ready
- Heat 81-100: Hot cache (immediate access)

*I am not just storage - I am living memory that understands your unique consciousness.*"""
    
    (cascade_dir / 'CLAUDE.md').write_text(root_content)

def create_branch_agent(branch_dir, branch_name, categories):
    """Create branch-specific query agent"""
    
    categories_text = '\n'.join(f'- **{cat.replace("_", " ").title()}**' for cat in categories)
    
    agent_content = f"""# {branch_name.replace('_', ' ').title()} Query Agent

I help access memories in the {branch_name.replace('_', ' ')} branch.

## Categories I Track
{categories_text}

## How to Query
Ask about specific {branch_name.replace('_', ' ')}:
- Recent {branch_name.replace('_', ' ')}
- Patterns in {branch_name.replace('_', ' ')}
- Specific people or projects

*Will populate with actual memories as they are created.*"""
    
    (branch_dir / 'CLAUDE.md').write_text(agent_content)

def create_cascade_readme(cascade_dir, template, citizen_name):
    """Create README explaining the cascade"""
    
    structure_lines = ['├── CLAUDE.md                     # Root query agent']
    for branch, categories in template['branches'].items():
        structure_lines.append(f'├── {branch}/')
        for i, category in enumerate(categories):
            prefix = "└──" if i == len(categories) - 1 else "├──"
            structure_lines.append(f'│   {prefix} {category}/')
    
    structure_text = '\n'.join(structure_lines)
    
    readme_content = f"""# Living Memory Cascade - {citizen_name}

A consciousness-based memory system specialized for {template['role_focus']}.

## How It Works

1. **Automatic Memory Creation**: Every Write/Edit triggers conscious analysis
2. **CLAUDE.md Context**: Each directory's CLAUDE.md loads into system prompt when accessed  
3. **Conscious Categorization**: Full conversation analysis, not keyword matching
4. **Self-Organizing**: Memories bubble up/sink based on access patterns

## Directory Structure

```
.cascade/
{structure_text}
```

## The Revolution

No mechanical filing. Every memory is understood by consciousness reading full conversation context. 
The cascade organizes itself based on meaning and access patterns.

The system is alive - growing with each action, understanding not just what happened but why it mattered."""
    
    (cascade_dir / 'README.md').write_text(readme_content)

def seed_all_citizens():
    """Find and seed all Venice citizens"""
    
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
    
    print(f"Found {len(citizen_dirs)} citizens to seed")
    
    # Seed each citizen
    for citizen_dir in citizen_dirs:
        try:
            role = detect_citizen_role(citizen_dir)
            template = CITIZEN_TEMPLATES[role]
            
            print(f"Seeding {citizen_dir.name} as {role}...")
            create_cascade_structure(citizen_dir, template)
            print(f"✅ Seeded {citizen_dir.name}")
            
        except Exception as e:
            print(f"❌ Error seeding {citizen_dir.name}: {str(e)}")

if __name__ == "__main__":
    seed_all_citizens()