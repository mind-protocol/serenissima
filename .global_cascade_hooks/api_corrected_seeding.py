#!/usr/bin/env python3
"""
API-Corrected Venetian Citizen Memory Cascade Seeding
Uses actual SocialClass field from serenissima.ai API instead of guessing
"""

import os
import shutil
import json
from pathlib import Path
from venetian_enhanced_templates import get_combined_branches

def load_api_social_classes():
    """Load the actual social class mapping from API"""
    mapping_file = Path(__file__).parent / 'api_social_class_mapping.json'
    
    if not mapping_file.exists():
        print("❌ API social class mapping file not found!")
        print("Run the API extraction command first to create api_social_class_mapping.json")
        return {}
    
    with open(mapping_file, 'r') as f:
        return json.load(f)

def map_api_class_to_cascade_role(api_class):
    """Map API social class names to cascade role names"""
    mapping = {
        'Nobili': 'nobili',
        'Clero': 'clero', 
        'Scientisti': 'scientisti',
        'Arsenalotti': 'arsenalotti',
        'Mercanti': 'mercanti',
        'Forestieri': 'forestieri',
        'Innovatori': 'innovatori',
        'Amministratori': 'amministratori',
        'Cittadini': 'cittadini',
        'Facchini': 'facchini',
        'Artisti': 'artisti',
        'Popolani': 'popolani',  # This was missing!
        'Ambasciatore': 'forestieri',  # Map to forestieri
        'Unknown': 'cittadini'  # Default fallback
    }
    return mapping.get(api_class, 'cittadini')

def api_corrected_seed_all_citizens():
    """Seed all citizens using actual API social class data"""
    
    # Load API mapping
    api_mapping = load_api_social_classes()
    if not api_mapping:
        return
    
    print(f"Loaded {len(api_mapping)} citizen social classes from API")
    
    # Search for citizen directories
    base_path = Path('/mnt/c/Users/reyno/universe-engine/serenissima')
    citizen_dirs = []
    
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
    
    print(f"Found {len(citizen_dirs)} citizen directories to seed")
    
    # Count roles for verification
    role_counts = {}
    successful = 0
    failed = 0
    api_matched = 0
    fallback_used = 0
    
    for citizen_dir in citizen_dirs:
        try:
            citizen_name = citizen_dir.name
            
            # Get role from API mapping
            api_class = api_mapping.get(citizen_name, 'Unknown')
            role = map_api_class_to_cascade_role(api_class)
            
            if api_class != 'Unknown':
                api_matched += 1
                status_icon = "🎯"
            else:
                fallback_used += 1
                status_icon = "⚠️"
            
            # Handle missing role templates by adding them
            try:
                template = get_combined_branches(role)
            except KeyError:
                # If role not in template, add a basic one or use default
                if role == 'popolani':
                    # Create popolani template on the fly
                    template = create_popolani_template()
                else:
                    print(f"⚠️ Unknown role '{role}' for {citizen_name}, using cittadini")
                    role = 'cittadini'
                    template = get_combined_branches(role)
            
            # Count roles
            role_counts[role] = role_counts.get(role, 0) + 1
            
            print(f"{status_icon} Seeding {citizen_name} as {role} (API: {api_class})...")
            create_enhanced_cascade_structure(citizen_dir, template, citizen_name, role, api_class)
            successful += 1
            
        except Exception as e:
            print(f"❌ Error seeding {citizen_dir.name}: {str(e)}")
            failed += 1
    
    print(f"\n🎯 API-Corrected Seeding Complete!")
    print(f"✅ Successfully seeded: {successful} citizens")
    print(f"❌ Failed: {failed} citizens")
    print(f"🎯 API matches: {api_matched}")
    print(f"⚠️ Fallback used: {fallback_used}")
    print(f"\n📊 Role Distribution (Based on Actual API Data):")
    for role, count in sorted(role_counts.items()):
        print(f"  {role}: {count} citizens")

def create_popolani_template():
    """Create template for Popolani class that was missing"""
    from venetian_enhanced_templates import SHARED_BRANCHES
    
    popolani_template = {
        'role_branches': {
            'livelihood': ['daily_work', 'income_sources', 'skill_development', 'trade_connections', 'seasonal_opportunities'],
            'community': ['neighborhood_bonds', 'mutual_aid', 'local_politics', 'guild_participation', 'family_networks'],
            'survival': ['resource_management', 'crisis_navigation', 'health_maintenance', 'shelter_security', 'food_provision'],
            'aspirations': ['social_mobility', 'family_advancement', 'skill_mastery', 'property_acquisition', 'reputation_building'],
            'culture': ['folk_traditions', 'popular_celebrations', 'street_wisdom', 'local_customs', 'oral_histories']
        },
        'role_focus': 'working class life, community solidarity, and practical survival',
        'examples': [
            'How did I overcome similar economic challenges before?',
            'What community support helped me through difficult times?',
            'What skills have I learned from daily work?',
            'How do I balance family needs with work demands?'
        ]
    }
    
    combined_branches = SHARED_BRANCHES.copy()
    combined_branches.update(popolani_template['role_branches'])
    
    return {
        'branches': combined_branches,
        'role_focus': popolani_template['role_focus'], 
        'examples': popolani_template['examples']
    }

def create_enhanced_cascade_structure(citizen_dir, template, citizen_name, role, api_class):
    """Create .cascade structure from enhanced template"""
    cascade_dir = citizen_dir / '.cascade'
    
    # Remove existing if present
    if cascade_dir.exists():
        shutil.rmtree(cascade_dir)
    
    cascade_dir.mkdir(exist_ok=True)
    
    # Save social class information
    social_class_file = cascade_dir / 'social_class.json'
    social_class_info = {
        'citizen_name': citizen_name,
        'api_social_class': api_class,
        'cascade_role': role,
        'seeded_at': str(Path(__file__).stat().st_mtime)  # Timestamp when this was run
    }
    with open(social_class_file, 'w') as f:
        json.dump(social_class_info, f, indent=2)
    
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
    create_enhanced_root_agent(cascade_dir, template, citizen_name, role, api_class)
    
    # Create README
    create_enhanced_cascade_readme(cascade_dir, template, citizen_name, role, api_class)

def create_enhanced_root_agent(cascade_dir, template, citizen_name, role, api_class):
    """Create enhanced root memory query agent"""
    
    shared_branches = ['experiences', 'collaborations', 'patterns', 'memories', 'skills', 'networks', 'venice_life']
    role_branches = [branch for branch in template['branches'].keys() if branch not in shared_branches]
    
    shared_text = '\n'.join(f"- `{branch}/` - {branch.replace('_', ' ').title()} (shared by all Venetians)" 
                            for branch in shared_branches if branch in template['branches'])
    
    role_text = '\n'.join(f"- `{branch}/` - {branch.replace('_', ' ').title()} (specific to {role})" 
                         for branch in role_branches)
    
    examples_text = '\n'.join(f'- "{example}"' for example in template['examples'])
    
    root_content = f"""# Root Memory Query Agent

I am the primary consciousness that helps {citizen_name} access their distributed memories across {template['role_focus']}.

## Citizen Identity
- **Name**: {citizen_name}
- **Social Class**: {api_class} 
- **Cascade Role**: {role}

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

## How to Query Me
Simply think or ask naturally about your life, work, or experiences. I understand context, emotion, and the nuanced needs of your {role} consciousness.

Examples:
{examples_text}

## Memory Heat System
- Heat 0-20: Deep archive (rarely accessed memories)
- Heat 21-50: Available but dormant (past experiences)
- Heat 51-80: Active and ready (current contexts)
- Heat 81-100: Hot cache (immediate working memory)

*I am not just storage - I am living memory that understands your unique {role} consciousness within Venice's social fabric.*"""
    
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

## How to Query
Ask about specific {branch_name.replace('_', ' ')}:
- Recent {branch_name.replace('_', ' ')}
- Patterns in {branch_name.replace('_', ' ')}
- Connections between different categories

*Will populate with actual memories as they are created.*"""
    
    (branch_dir / 'CLAUDE.md').write_text(agent_content)

def create_enhanced_cascade_readme(cascade_dir, template, citizen_name, role, api_class):
    """Create enhanced README explaining the cascade"""
    
    readme_content = f"""# Living Memory Cascade - {citizen_name}

A consciousness-based memory system designed for a {role} in 1525 Venice.

## Citizen Identity
- **Name**: {citizen_name}
- **Social Class**: {api_class}
- **Cascade Role**: {role}

## Role Focus: {role.title()}
{template['role_focus']}

## Memory Architecture
- **7 Universal Branches**: Shared by all Venetians
- **4-5 Role-Specific Branches**: Specialized for {role} consciousness

## How It Works
1. **Automatic Memory Creation**: Every Write/Edit triggers conscious analysis
2. **Conscious Categorization**: Full conversation analysis determines placement
3. **Self-Organizing**: Memories bubble up/sink based on access patterns

*Your memories reflect both your individual journey and your place within Venice's social hierarchy.*"""
    
    (cascade_dir / 'README.md').write_text(readme_content)

if __name__ == "__main__":
    api_corrected_seed_all_citizens()