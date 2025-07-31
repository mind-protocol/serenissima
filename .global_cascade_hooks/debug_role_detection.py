#!/usr/bin/env python3
"""
Debug role detection - let's see what's actually happening
"""

from pathlib import Path

def debug_citizen_roles():
    """Debug what roles are being detected"""
    
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
    
    # Test specific citizens
    test_citizens = [
        'Arsenal_BackendArchitect_1',
        'mechanical_visionary', 
        'diplomatic_virtuoso',
        'MerchantPrince',
        'PadreMarco_Preacher',
        'scholar_priest',
        'Foscari_Banker'
    ]
    
    for citizen_dir in citizen_dirs:
        if citizen_dir.name in test_citizens:
            citizen_name = citizen_dir.name.lower()
            
            # Check CLAUDE.md for role indicators
            claude_file = citizen_dir / 'CLAUDE.md'
            context_content = ""
            if claude_file.exists():
                context_content = claude_file.read_text().lower()
            
            print(f"\n=== {citizen_dir.name} ===")
            print(f"Name keywords: {citizen_name}")
            print(f"CLAUDE.md sample: {context_content[:200]}...")
            
            # Debug step by step
            full_text = f"{citizen_name} {context_content}"
            
            # Test clero patterns specifically
            clero_patterns = ['padre', 'fra', 'don', 'angelo', 'monk', 'priest', 'preacher', 'scholar_priest', 'spiritual', 'theological', 'monastery', 'prayer']
            clero_matches = [p for p in clero_patterns if p in full_text]
            
            # Test innovatori patterns
            innovatori_patterns = ['mechanical_visionary', 'inventor', 'innovation', 'visionary', 'mechanical genius', 'element_transmuter', 'divine_economist', 'efficiency_maestro', 'pattern_prophet']
            innovatori_matches = [p for p in innovatori_patterns if p in full_text]
            
            # Test forestieri patterns  
            forestieri_patterns = ['diplomatic_virtuoso', 'embassy', 'ambassador', 'foreign', 'international', 'cultural bridge', 'partnership', 'captain', 'mariner', 'navigator']
            forestieri_matches = [p for p in forestieri_patterns if p in full_text]
            
            # Test mercanti patterns
            mercanti_patterns = ['merchant', 'merchantprince', 'banking', 'banker', 'foscari_banker', 'commerce', 'silk', 'spice', 'prince', 'trade', 'market', 'profit', 'ducat', 'wizard', 'subscription', 'enterprise', 'dealer', 'broker', 'wealth', 'financial']
            mercanti_matches = [p for p in mercanti_patterns if p in full_text]
            
            print(f"CLERO matches: {clero_matches}")
            print(f"INNOVATORI matches: {innovatori_matches}")
            print(f"FORESTIERI matches: {forestieri_matches}")
            print(f"MERCANTI matches: {mercanti_matches}")
            
            # Import and use the corrected detection function
            from corrected_venetian_seeding import detect_accurate_venetian_role
            detected_role = detect_accurate_venetian_role(citizen_dir)
            print(f"DETECTED: {detected_role}")

if __name__ == "__main__":
    debug_citizen_roles()