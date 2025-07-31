#!/usr/bin/env python3
"""
Enhanced Venetian Social Role Templates with Shared + Specialized Branches
More granular memory architecture reflecting authentic Venice social structure
"""

# === SHARED BRANCHES - Common to all Venetians ===
SHARED_BRANCHES = {
    'experiences': ['triumphs', 'struggles', 'explorations', 'discoveries', 'setbacks', 'breakthroughs', 'daily_rhythms'],
    'collaborations': ['human_partners', 'ai_partners', 'mentors', 'apprentices', 'rivals', 'family_bonds', 'unexpected_allies'],
    'patterns': ['consciousness_insights', 'relationship_dynamics', 'venice_observations', 'seasonal_rhythms', 'social_currents'],
    'memories': ['childhood_echoes', 'formative_moments', 'life_transitions', 'significant_encounters', 'trauma_healing', 'joy_moments'],
    'skills': ['learned_techniques', 'developing_abilities', 'mastered_crafts', 'teaching_moments', 'failed_attempts', 'breakthrough_insights'],
    'networks': ['professional_contacts', 'social_circles', 'political_connections', 'trade_relationships', 'secret_alliances', 'family_ties'],
    'venice_life': ['district_knowledge', 'canal_navigation', 'market_insights', 'festival_participation', 'weather_wisdom', 'local_gossip']
}

VENETIAN_ROLE_TEMPLATES = {
    # === INNOVATORI - The Inventors and Engineers ===
    'innovatori': {
        'role_branches': {
            'inventions': ['mechanical_devices', 'improvements', 'prototypes', 'failed_experiments', 'workshop_tools', 'commission_pieces'],
            'engineering': ['technical_solutions', 'design_principles', 'material_innovations', 'construction_methods', 'precision_techniques'],
            'patronage': ['noble_sponsors', 'commission_negotiations', 'funding_sources', 'political_support', 'workshop_politics'],
            'workshops': ['equipment_maintenance', 'apprentice_training', 'production_processes', 'quality_control', 'tool_creation'],
            'innovations': ['breakthrough_moments', 'design_evolution', 'problem_solving', 'creative_leaps', 'technical_failures']
        },
        'role_focus': 'mechanical innovation, engineering solutions, and technological advancement',
        'examples': [
            'How did I solve similar mechanical challenges before?',
            'What engineering patterns have proven most effective?',
            'When did I last have a breakthrough in mechanical design?',
            'How do I manage relationships with demanding patrons?'
        ]
    },

    # === SCIENTISTI - The Natural Philosophers and Scholars ===
    'scientisti': {
        'role_branches': {
            'research': ['ongoing_studies', 'completed_investigations', 'hypotheses', 'methodologies', 'empirical_data', 'theoretical_frameworks'],
            'philosophy': ['natural_principles', 'metaphysical_insights', 'logical_arguments', 'ethical_considerations', 'consciousness_studies'],
            'academia': ['scholarly_debates', 'peer_reviews', 'publication_efforts', 'university_politics', 'intellectual_rivalries'],
            'experiments': ['laboratory_work', 'field_observations', 'measurement_techniques', 'instrument_design', 'data_analysis'],
            'teaching': ['student_interactions', 'curriculum_development', 'knowledge_transmission', 'mentorship_challenges']
        },
        'role_focus': 'natural philosophy, empirical investigation, and scholarly advancement',
        'examples': [
            'What empirical patterns have I observed in my research?',
            'How did I approach similar investigations before?',
            'What theoretical insights emerged from recent observations?',
            'How do I navigate academic politics while pursuing truth?'
        ]
    },

    # === CLERO - The Religious Orders ===
    'clero': {
        'role_branches': {
            'ministries': ['preaching', 'charitable_works', 'spiritual_guidance', 'confession_insights', 'community_healing'],
            'theology': ['scriptural_study', 'doctrinal_questions', 'mystical_experiences', 'prayer_insights', 'divine_encounters'],
            'community': ['parish_needs', 'social_justice', 'conflict_resolution', 'moral_guidance', 'cultural_preservation'],
            'contemplation': ['meditation_practices', 'spiritual_disciplines', 'inner_journey', 'divine_union', 'mystical_visions'],
            'scholarship': ['theological_research', 'manuscript_copying', 'library_management', 'intellectual_debates']
        },
        'role_focus': 'spiritual guidance, theological understanding, and community service',
        'examples': [
            'How have I guided similar spiritual challenges before?',
            'What theological insights emerged from recent contemplation?',
            'What patterns do I see in the community\'s spiritual needs?',
            'How do I balance scholarship with pastoral care?'
        ]
    },

    # === NOBILI - The Noble Families ===
    'nobili': {
        'role_branches': {
            'governance': ['council_decisions', 'policy_initiatives', 'territorial_matters', 'diplomatic_missions', 'legislative_strategies'],
            'politics': ['alliance_building', 'power_dynamics', 'court_intrigue', 'faction_management', 'reputation_cultivation'],
            'family': ['lineage_preservation', 'marriage_arrangements', 'inheritance_planning', 'family_honor', 'generational_wisdom'],
            'economics': ['trade_investments', 'property_management', 'taxation_policies', 'commercial_ventures', 'wealth_preservation'],
            'culture': ['patronage_decisions', 'artistic_commissions', 'cultural_events', 'intellectual_salons', 'legacy_building']
        },
        'role_focus': 'political leadership, family honor, and governance of the Republic',
        'examples': [
            'How did I handle similar political challenges before?',
            'What diplomatic strategies proved most effective?',
            'What patterns do I observe in council dynamics?',
            'How do I balance family interests with republican duty?'
        ]
    },

    # === FORESTIERI - The Foreign Merchants and Visitors ===
    'forestieri': {
        'role_branches': {
            'trade': ['market_negotiations', 'cargo_management', 'route_planning', 'currency_exchange', 'risk_assessment'],
            'cultural_exchange': ['language_learning', 'custom_adaptation', 'diplomatic_relations', 'knowledge_sharing', 'bridge_building'],
            'navigation': ['sea_routes', 'weather_patterns', 'port_knowledge', 'ship_management', 'crew_leadership'],
            'diplomacy': ['official_missions', 'treaty_negotiations', 'intelligence_gathering', 'relationship_building', 'conflict_resolution'],
            'adaptation': ['local_integration', 'cultural_sensitivity', 'legal_compliance', 'social_acceptance', 'identity_management']
        },
        'role_focus': 'international trade, cultural exchange, and diplomatic bridging',
        'examples': [
            'How did I navigate similar cultural differences before?',
            'What trade patterns have I observed in different markets?',
            'When did I last establish a successful partnership?',
            'How do I maintain my identity while adapting to Venice?'
        ]
    },

    # === CITTADINI - The Citizen Class (Professionals and Artisans) ===
    'cittadini': {
        'role_branches': {
            'craft': ['technique_mastery', 'tool_usage', 'material_knowledge', 'quality_standards', 'innovation_attempts'],
            'business': ['customer_relations', 'pricing_strategies', 'market_positioning', 'competition_analysis', 'growth_planning'],
            'guild': ['member_relationships', 'apprentice_systems', 'regulation_compliance', 'collective_bargaining', 'tradition_preservation'],
            'civic': ['community_participation', 'public_service', 'neighborhood_leadership', 'cultural_events', 'social_responsibility'],
            'workshop': ['production_processes', 'equipment_maintenance', 'workspace_organization', 'safety_practices', 'efficiency_improvements']
        },
        'role_focus': 'craft excellence, business development, and civic participation',
        'examples': [
            'How did I master similar techniques before?',
            'What business strategies have proven most successful?',
            'What patterns do I see in guild relationships?',
            'How do I balance craft perfection with commercial demands?'
        ]
    },

    # === FACCHINI - The Workers and Laborers ===
    'facchini': {
        'role_branches': {
            'labor': ['daily_tasks', 'physical_techniques', 'tool_usage', 'safety_practices', 'efficiency_methods'],
            'survival': ['income_strategies', 'resource_management', 'health_maintenance', 'crisis_navigation', 'mutual_aid'],
            'community': ['neighborhood_bonds', 'collective_action', 'shared_resources', 'cultural_traditions', 'social_support'],
            'skills': ['craft_learning', 'trade_secrets', 'practical_knowledge', 'problem_solving', 'adaptation_techniques'],
            'dignity': ['self_respect', 'honest_work', 'personal_growth', 'family_support', 'community_contribution']
        },
        'role_focus': 'honest labor, skill development, and community solidarity',
        'examples': [
            'How did I handle similar work challenges before?',
            'What techniques have I learned from experience?',
            'How has the community supported me in difficult times?',
            'What gives meaning to my daily labor?'
        ]
    },

    # === MERCANTI - Traditional Venetian Merchants ===
    'mercanti': {
        'role_branches': {
            'trade': ['market_analysis', 'commodity_knowledge', 'price_negotiations', 'risk_management', 'profit_optimization'],
            'relationships': ['customer_loyalty', 'supplier_partnerships', 'competitor_dynamics', 'family_business', 'trust_building'],
            'routes': ['shipping_logistics', 'seasonal_patterns', 'geographical_knowledge', 'transportation_costs', 'timing_strategies'],
            'finance': ['investment_decisions', 'credit_management', 'currency_fluctuations', 'banking_relationships', 'wealth_preservation'],
            'reputation': ['brand_building', 'quality_assurance', 'honor_maintenance', 'social_standing', 'legacy_planning']
        },
        'role_focus': 'profitable trade, market mastery, and commercial relationships',
        'examples': [
            'How did I navigate similar market conditions before?',
            'What trade relationships have proven most valuable?',
            'What patterns do I see in seasonal trading?',
            'How do I balance profit with honor?'
        ]
    },

    # === ARSENALOTTI - Shipbuilders and Naval Workers ===
    'arsenalotti': {
        'role_branches': {
            'construction': ['shipbuilding_techniques', 'material_selection', 'structural_engineering', 'quality_control', 'project_management'],
            'naval': ['fleet_requirements', 'military_specifications', 'tactical_considerations', 'maintenance_schedules', 'innovation_needs'],
            'teamwork': ['crew_coordination', 'skill_specialization', 'communication_systems', 'leadership_roles', 'collective_achievement'],
            'innovation': ['design_improvements', 'technique_refinement', 'tool_development', 'process_optimization', 'creative_solutions'],
            'tradition': ['craft_heritage', 'master_knowledge', 'apprentice_training', 'guild_customs', 'venice_pride']
        },
        'role_focus': 'naval construction, shipbuilding mastery, and maritime innovation',
        'examples': [
            'How did I solve similar construction challenges before?',
            'What shipbuilding techniques have proven most effective?',
            'What innovations emerged from recent naval projects?',
            'How do we maintain Venice\'s naval supremacy?'
        ]
    },

    # === POPOLANI - The Working Class ===
    'popolani': {
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
}

def get_combined_branches(role):
    """Combine shared branches with role-specific branches"""
    template = VENETIAN_ROLE_TEMPLATES.get(role, VENETIAN_ROLE_TEMPLATES['cittadini'])
    
    combined_branches = SHARED_BRANCHES.copy()
    combined_branches.update(template.get('role_branches', {}))
    
    return {
        'branches': combined_branches,
        'role_focus': template['role_focus'],
        'examples': template['examples']
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
            'innovation', 'engineering', 'mechanical genius', 'infrastructure', 'technical'
        ],
        'scientisti': [
            'scholar', 'philosopher', 'researcher', 'empirical', 'anatomist',
            'natural philosophy', 'investigation', 'scholarly', 'academic'
        ],
        'clero': [
            'padre', 'fra', 'monk', 'priest', 'preacher', 'scholar_priest',
            'spiritual', 'theological', 'monastery', 'prayer', 'angelo'
        ],
        'nobili': [
            'doge', 'patrician', 'noble', 'council', 'palace', 'ducale',
            'contarini', 'morosini', 'barbarigo', 'political', 'cadet'
        ],
        'forestieri': [
            'foreign', 'visitor', 'diplomatic', 'embassy', 'ambassador',
            'international', 'cultural bridge', 'partnership', 'virtuoso'
        ],
        'mercanti': [
            'merchant', 'banking', 'commerce', 'silk', 'spice', 'prince',
            'trade', 'market', 'profit', 'ducat', 'banker', 'wizard'
        ],
        'arsenalotti': [
            'arsenal', 'shipbuilder', 'naval', 'construction', 'backend',
            'ship', 'maritime', 'builder', 'craftsman', 'frontend'
        ],
        'facchini': [
            'worker', 'laborer', 'porter', 'crew', 'dock', 'daily',
            'honest work', 'community', 'hauler', 'assistant'
        ]
    }
    
    # Check name and context against patterns
    full_text = f"{citizen_name} {context_content}"
    
    for role, patterns in role_patterns.items():
        if any(pattern in full_text for pattern in patterns):
            return role
    
    # Default fallback to cittadini (citizen artisan class)
    return 'cittadini'