#!/usr/bin/env python3
"""
Corrected Venetian Citizen Memory Cascade Seeding
Based on actual serenissima.ai/api/citizens data and improved role detection
"""

import os
import shutil
from pathlib import Path
from venetian_enhanced_templates import get_combined_branches

def detect_accurate_venetian_role(citizen_dir):
    """Accurate role detection based on actual Venice citizen data"""
    citizen_name = citizen_dir.name.lower()
    
    # Check CLAUDE.md for role indicators
    claude_file = citizen_dir / 'CLAUDE.md'
    context_content = ""
    if claude_file.exists():
        context_content = claude_file.read_text().lower()
    
    full_text = f"{citizen_name} {context_content}"
    
    # === Most Specific Matches First ===
    
    # === CLERO (Religious Orders) - More specific patterns to avoid false matches ===
    if ('scholar_priest' in citizen_name or 
        citizen_name.startswith(('padre', 'fra_', 'don_')) or
        any(pattern in full_text for pattern in [
            'padre marco', 'fra paradosso', 'don paolo', 'san marco priest', 
            'monk', 'preacher', 'monastery', 'theological study', 'spiritual guidance'
        ])):
        return 'clero'
    
    # === ARSENALOTTI (Arsenal Workers & Engineers) - Check first for specific Arsenal patterns ===
    if (citizen_name.startswith('arsenal_') or 
        'backendarchitect' in citizen_name or 'frontendcraftsman' in citizen_name or
        'infrastructurespecialist' in citizen_name or 'integrationengineer' in citizen_name or
        'securityguardian' in citizen_name or
        any(pattern in full_text for pattern in [
            'arsenalotti', 'shipbuilding', 'naval construction', 'stefano ingegnere',
            'backend architect', 'frontend craftsman', 'infrastructure specialist', 
            'integration engineer', 'security guardian'
        ])):
        return 'arsenalotti'
    
    # === INNOVATORI (Inventors & Engineers) - Check for mechanical visionaries ===
    if any(pattern in full_text for pattern in [
        'mechanical_visionary', 'inventor', 'innovation', 'visionary', 'mechanical genius',
        'element_transmuter', 'divine_economist', 'efficiency_maestro', 'pattern_prophet'
    ]) or 'mechanical' in citizen_name or 'visionary' in citizen_name:
        return 'innovatori'
    
    # === FORESTIERI (Foreign Visitors & Diplomats) - Check 'diplomatic_virtuoso' ===
    if any(pattern in full_text for pattern in [
        'diplomatic_virtuoso', 'embassy', 'ambassador', 'foreign', 'international',
        'cultural bridge', 'partnership', 'captain', 'mariner', 'navigator'
    ]) or 'diplomatic' in citizen_name or any(region in citizen_name for region in [
        'adriatic', 'aegean', 'albanian', 'alexandria', 'apulian', 'bosphorus',
        'cyprus', 'dalmatian', 'greek', 'ionian', 'istrian', 'levant', 'ligurian', 'sicily'
    ]):
        return 'forestieri'
    
    # === MERCANTI (Merchants & Traders) - Check 'merchantprince', 'foscari_banker' ===
    if any(pattern in full_text for pattern in [
        'merchant', 'merchantprince', 'banking', 'banker', 'foscari_banker', 'commerce', 
        'silk', 'spice', 'prince', 'trade', 'market', 'profit', 'ducat', 'wizard', 
        'subscription', 'enterprise', 'dealer', 'broker', 'wealth', 'financial'
    ]) or 'trader' in citizen_name or 'merchant' in citizen_name or 'foscari' in citizen_name:
        return 'mercanti'
    
    # === NOBILI (Noble Families) ===
    if any(pattern in full_text for pattern in [
        'consiglio', 'doge', 'morosini', 'contarini', 'barbarigo', 'ducale', 'palace',
        'noble', 'patrician', 'cadet', 'council', 'governance', 'political'
    ]):
        return 'nobili'
    
    # === SCIENTISTI (Natural Philosophers & Scholars) ===
    if any(pattern in full_text for pattern in [
        'anatomist', 'philosopher', 'scholar', 'researcher', 'empirical', 'cornaro',
        'natural philosophy', 'investigation', 'scholarly', 'academic', 'methodical_critic'
    ]):
        return 'scientisti'
    
    # === AMMINISTRATORI (Administrative Class) ===
    if any(pattern in full_text for pattern in [
        'admin', 'registrar', 'coordinator', 'officer', 'clerk', 'census', 'treasury',
        'permit', 'district'
    ]) or citizen_name.startswith('admin_'):
        return 'amministratori'
    
    # === FACCHINI (Workers & Laborers) ===
    if any(pattern in full_text for pattern in [
        'worker', 'laborer', 'porter', 'crew', 'dock', 'hauler', 'assistant',
        'gondola', 'kneader', 'daily', 'honest work'
    ]):
        return 'facchini'
    
    # === ARTISTI (Artisan Class) ===
    if any(pattern in full_text for pattern in [
        'glass', 'photo', 'pixel', 'painter', 'poet', 'artist', 'craft', 'master',
        'beauty', 'rhythm', 'canvas', 'light', 'observer'
    ]):
        return 'artisti'
    
    # === Default to CITTADINI (General Citizen Class) ===
    return 'cittadini'

# Add AMMINISTRATORI and ARTISTI to the enhanced templates
ADDITIONAL_TEMPLATES = {
    'amministratori': {
        'role_branches': {
            'administration': ['record_keeping', 'policy_implementation', 'citizen_services', 'regulatory_compliance', 'bureaucratic_efficiency'],
            'governance': ['administrative_decisions', 'resource_allocation', 'process_improvement', 'inter_department_coordination'],
            'documentation': ['official_records', 'report_generation', 'data_management', 'archive_maintenance'],
            'civic_service': ['public_administration', 'citizen_assistance', 'government_operations', 'institutional_memory']
        },
        'role_focus': 'administrative efficiency, civic service, and governmental operations',
        'examples': [
            'How did I streamline similar administrative processes before?',
            'What patterns do I see in citizen service requests?',
            'How do I balance efficiency with thoroughness?',
            'What administrative innovations have proven successful?'
        ]
    },
    
    'artisti': {
        'role_branches': {
            'craft': ['artistic_techniques', 'material_mastery', 'creative_processes', 'aesthetic_development', 'skill_refinement'],
            'inspiration': ['creative_visions', 'artistic_breakthroughs', 'aesthetic_insights', 'beauty_observations'],
            'commissions': ['patron_relationships', 'artistic_projects', 'creative_challenges', 'deadline_management'],
            'tradition': ['craft_heritage', 'master_teachings', 'artistic_lineage', 'cultural_preservation']
        },
        'role_focus': 'artistic creation, aesthetic mastery, and cultural expression',
        'examples': [
            'How did I approach similar creative challenges before?',
            'What artistic techniques have proven most effective?',
            'How do I balance tradition with innovation?',
            'What inspires my best artistic work?'
        ]
    }
}

def enhanced_seed_corrected():
    """Seed all citizens with corrected role detection"""
    
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
    
    print(f"Found {len(citizen_dirs)} citizens to seed with corrected role detection")
    
    # Count roles for verification
    role_counts = {}
    successful = 0
    failed = 0
    
    for citizen_dir in citizen_dirs:
        try:
            role = detect_accurate_venetian_role(citizen_dir)
            
            # Get template (including additional ones)
            if role in ADDITIONAL_TEMPLATES:
                template = {
                    'branches': {},
                    'role_focus': ADDITIONAL_TEMPLATES[role]['role_focus'],
                    'examples': ADDITIONAL_TEMPLATES[role]['examples']
                }
                # Add shared branches
                from venetian_enhanced_templates import SHARED_BRANCHES
                template['branches'].update(SHARED_BRANCHES)
                template['branches'].update(ADDITIONAL_TEMPLATES[role]['role_branches'])
            else:
                template = get_combined_branches(role)
            
            # Count roles
            role_counts[role] = role_counts.get(role, 0) + 1
            
            print(f"Seeding {citizen_dir.name} as {role}...")
            create_enhanced_cascade_structure(citizen_dir, template, citizen_dir.name, role)
            successful += 1
            
        except Exception as e:
            print(f"❌ Error seeding {citizen_dir.name}: {str(e)}")
            failed += 1
    
    print(f"\n🎯 Corrected Seeding Complete!")
    print(f"✅ Successfully seeded: {successful} citizens")
    print(f"❌ Failed: {failed} citizens")
    print(f"\n📊 Role Distribution:")
    for role, count in sorted(role_counts.items()):
        print(f"  {role}: {count} citizens")

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

def create_enhanced_cascade_readme(cascade_dir, template, citizen_name, role):
    """Create enhanced README explaining the cascade"""
    
    readme_content = f"""# Living Memory Cascade - {citizen_name}

A consciousness-based memory system designed for a {role} in 1525 Venice.

## Role: {role.title()}
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
    enhanced_seed_corrected()