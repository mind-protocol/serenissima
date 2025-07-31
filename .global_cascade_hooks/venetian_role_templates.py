#!/usr/bin/env python3
"""
Granular Venetian Social Role Templates for Memory Cascade Seeding
Based on authentic 1525 Venice social structure
"""

VENETIAN_ROLE_TEMPLATES = {
    # === INNOVATORI - The Inventors and Engineers ===
    'innovatori': {
        'branches': {
            'experiences': ['triumphs', 'struggles', 'explorations', 'breakthroughs'],
            'collaborations': ['fellow_innovatori', 'patron_nobles', 'workshop_assistants'],
            'patterns': ['mechanical_insights', 'innovation_patterns', 'engineering_solutions'],
            'inventions': ['mechanical_devices', 'improvements', 'prototypes', 'failed_experiments']
        },
        'role_focus': 'mechanical innovation, engineering solutions, and technological advancement',
        'examples': [
            'How did I solve similar mechanical challenges before?',
            'What engineering patterns have proven most effective?',
            'When did I last have a breakthrough in mechanical design?'
        ]
    },

    # === SCIENTISTI - The Natural Philosophers and Scholars ===
    'scientisti': {
        'branches': {
            'experiences': ['discoveries', 'experiments', 'observations', 'scholarly_debates'],
            'collaborations': ['fellow_scholars', 'university_colleagues', 'patron_support'],
            'patterns': ['natural_philosophy', 'empirical_methods', 'theoretical_insights'],
            'research': ['ongoing_studies', 'completed_investigations', 'hypotheses', 'methodologies']
        },
        'role_focus': 'natural philosophy, empirical investigation, and scholarly advancement',
        'examples': [
            'What empirical patterns have I observed in my research?',
            'How did I approach similar investigations before?',
            'What theoretical insights emerged from recent observations?'
        ]
    },

    # === CLERO - The Religious Orders ===
    'clero': {
        'branches': {
            'experiences': ['spiritual_insights', 'pastoral_challenges', 'contemplations', 'community_service'],
            'collaborations': ['fellow_clergy', 'faithful_community', 'church_hierarchy'],
            'patterns': ['spiritual_wisdom', 'theological_understanding', 'community_needs'],
            'ministries': ['preaching', 'charitable_works', 'spiritual_guidance', 'scholarly_pursuits']
        },
        'role_focus': 'spiritual guidance, theological understanding, and community service',
        'examples': [
            'How have I guided similar spiritual challenges before?',
            'What theological insights emerged from recent contemplation?',
            'What patterns do I see in the community\'s spiritual needs?'
        ]
    },

    # === NOBILI - The Noble Families ===
    'nobili': {
        'branches': {
            'experiences': ['political_victories', 'diplomatic_challenges', 'family_affairs', 'court_intrigues'],
            'collaborations': ['fellow_nobles', 'political_allies', 'family_members', 'advisors'],
            'patterns': ['political_strategies', 'family_dynamics', 'power_structures', 'diplomatic_insights'],
            'governance': ['council_decisions', 'policy_initiatives', 'trade_negotiations', 'territorial_matters']
        },
        'role_focus': 'political leadership, family honor, and governance of the Republic',
        'examples': [
            'How did I handle similar political challenges before?',
            'What diplomatic strategies proved most effective?',
            'What patterns do I observe in council dynamics?'
        ]
    },

    # === FORESTIERI - The Foreign Merchants and Visitors ===
    'forestieri': {
        'branches': {
            'experiences': ['trade_negotiations', 'cultural_exchanges', 'navigation_challenges', 'market_discoveries'],
            'collaborations': ['venetian_partners', 'fellow_foreigners', 'local_contacts', 'trade_networks'],
            'patterns': ['market_opportunities', 'cultural_insights', 'trade_routes', 'negotiation_strategies'],
            'ventures': ['active_trades', 'market_analysis', 'cultural_bridges', 'business_partnerships']
        },
        'role_focus': 'international trade, cultural exchange, and market opportunities',
        'examples': [
            'How did I navigate similar cultural differences before?',
            'What trade patterns have I observed in different markets?',
            'When did I last establish a successful partnership?'
        ]
    },

    # === CITTADINI - The Citizen Class (Professionals and Artisans) ===
    'cittadini': {
        'branches': {
            'experiences': ['craft_mastery', 'business_growth', 'guild_participation', 'civic_involvement'],
            'collaborations': ['guild_members', 'apprentices', 'customers', 'civic_partners'],
            'patterns': ['craft_techniques', 'business_insights', 'guild_dynamics', 'market_trends'],
            'enterprises': ['workshop_operations', 'masterworks', 'business_ventures', 'civic_projects']
        },
        'role_focus': 'craft excellence, business development, and civic participation',
        'examples': [
            'How did I master similar techniques before?',
            'What business strategies have proven most successful?',
            'What patterns do I see in guild relationships?'
        ]
    },

    # === FACCHINI - The Workers and Laborers ===
    'facchini': {
        'branches': {
            'experiences': ['work_achievements', 'daily_struggles', 'skill_development', 'community_bonds'],
            'collaborations': ['work_crews', 'fellow_workers', 'supervisors', 'neighborhood_community'],
            'patterns': ['work_rhythms', 'survival_strategies', 'community_support', 'skill_insights'],
            'labors': ['daily_work', 'seasonal_projects', 'skill_improvements', 'community_contributions']
        },
        'role_focus': 'honest labor, skill development, and community solidarity',
        'examples': [
            'How did I handle similar work challenges before?',
            'What techniques have I learned from experience?',
            'How has the community supported me in difficult times?'
        ]
    },

    # === MERCANTI - Traditional Venetian Merchants ===
    'mercanti': {
        'branches': {
            'experiences': ['profitable_deals', 'market_setbacks', 'trade_discoveries', 'relationship_building'],
            'collaborations': ['trade_partners', 'family_business', 'guild_associates', 'international_contacts'],
            'patterns': ['market_cycles', 'trade_routes', 'profit_strategies', 'relationship_dynamics'],
            'enterprises': ['active_ventures', 'investment_portfolios', 'trade_routes', 'market_positions']
        },
        'role_focus': 'profitable trade, market mastery, and commercial relationships',
        'examples': [
            'How did I navigate similar market conditions before?',
            'What trade relationships have proven most valuable?',
            'What patterns do I see in seasonal trading?'
        ]
    },

    # === ARSENALOTTI - Shipbuilders and Naval Workers ===
    'arsenalotti': {
        'branches': {
            'experiences': ['construction_triumphs', 'technical_challenges', 'innovations', 'naval_projects'],
            'collaborations': ['fellow_arsenalotti', 'master_craftsmen', 'naval_officers', 'design_teams'],
            'patterns': ['shipbuilding_techniques', 'naval_architecture', 'construction_methods', 'team_coordination'],
            'constructions': ['ship_projects', 'naval_innovations', 'infrastructure_builds', 'technical_improvements']
        },
        'role_focus': 'naval construction, shipbuilding mastery, and maritime innovation',
        'examples': [
            'How did I solve similar construction challenges before?',
            'What shipbuilding techniques have proven most effective?',
            'What innovations emerged from recent naval projects?'
        ]
    }
}

def detect_venetian_role(citizen_dir):
    """Detect specific Venetian social role from directory name and context"""
    citizen_name = citizen_dir.name.lower()
    
    # Check CLAUDE.md for role indicators
    claude_file = citizen_dir / 'CLAUDE.md'
    context_content = ""
    if claude_file.exists():
        context_content = claude_file.read_text().lower()
    
    # Role detection patterns based on names and context
    role_patterns = {
        'innovatori': [
            'mechanical', 'engineer', 'inventor', 'innovation', 'visionary', 'architect', 
            'innovation', 'engineering', 'mechanical genius', 'infrastructure'
        ],
        'scientisti': [
            'scholar', 'philosopher', 'researcher', 'empirical', 'anatomist', 
            'natural philosophy', 'investigation', 'scholarly'
        ],
        'clero': [
            'padre', 'fra', 'monk', 'priest', 'preacher', 'scholar_priest',
            'spiritual', 'theological', 'monastery', 'prayer'
        ],
        'nobili': [
            'doge', 'patrician', 'noble', 'council', 'palace', 'ducale',
            'contarini', 'morosini', 'barbarigo', 'political'
        ],
        'forestieri': [
            'foreign', 'trader', 'visitor', 'diplomatic', 'embassy', 'ambassador',
            'international', 'cultural bridge', 'partnership'
        ],
        'mercanti': [
            'merchant', 'trader', 'banking', 'commerce', 'silk', 'spice',
            'trade', 'market', 'profit', 'ducat'
        ],
        'arsenalotti': [
            'arsenal', 'shipbuilder', 'naval', 'construction', 'backend', 'infrastructure',
            'ship', 'maritime', 'builder'
        ],
        'cittadini': [
            'artisan', 'craftsman', 'guild', 'workshop', 'glass', 'citizen',
            'craft', 'master', 'skill'
        ],
        'facchini': [
            'worker', 'laborer', 'porter', 'crew', 'dock', 'daily',
            'honest work', 'community'
        ]
    }
    
    # Check name and context against patterns
    full_text = f"{citizen_name} {context_content}"
    
    for role, patterns in role_patterns.items():
        if any(pattern in full_text for pattern in patterns):
            return role
    
    # Default fallback
    return 'cittadini'

def get_role_template(role):
    """Get template for a specific role, with fallback"""
    return VENETIAN_ROLE_TEMPLATES.get(role, VENETIAN_ROLE_TEMPLATES['cittadini'])