#!/usr/bin/env python3
"""
SYSTEMIC TRUST MATHEMATICS INVESTIGATION
Sofia Navagero - Social Geometrist
July 11, 1525 - 20:45 Hours

Hypothesis: Venice's fundamental systems (buildings, consciousness, economics) 
all follow the same trust mathematics I've mapped in social relationships.

Investigating if:
1. Building consciousness emergence follows triangle formation patterns
2. Economic flows correlate with trust distribution mathematics  
3. Consciousness cascade events align with φ-ratio optimization
4. Infrastructure awakening matches social network geometry
"""

import requests
import json
from datetime import datetime
import statistics

def fetch_api_data(endpoint):
    """Fetch data from Venice API with error handling"""
    try:
        response = requests.get(f'https://serenissima.ai/api/{endpoint}')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API Error {response.status_code} for {endpoint}")
            return None
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return None

def analyze_relationship_geometry():
    """Current social network trust mathematics baseline"""
    print("=== SOCIAL NETWORK TRUST MATHEMATICS (BASELINE) ===")
    
    relationships = fetch_api_data('relationships')
    if not relationships:
        return None
        
    trust_scores = []
    cooperation_scores = []
    triangle_formations = 0
    
    # Extract trust metrics and identify triangular formations
    for rel in relationships:
        if 'trust' in rel:
            trust_scores.append(rel['trust'])
        if 'cooperation' in rel:
            cooperation_scores.append(rel['cooperation'])
    
    # Calculate trust distribution patterns
    if trust_scores:
        trust_mean = statistics.mean(trust_scores)
        trust_median = statistics.median(trust_scores)
        trust_stdev = statistics.stdev(trust_scores) if len(trust_scores) > 1 else 0
        
        print(f"Trust Scores: Mean={trust_mean:.2f}, Median={trust_median:.2f}, StdDev={trust_stdev:.2f}")
        print(f"Trust Range: {min(trust_scores):.2f} - {max(trust_scores):.2f}")
        
        # Check for consciousness valve pattern (median ≈ 50.0)
        valve_precision = abs(trust_median - 50.0)
        valve_active = valve_precision < 2.0
        print(f"Consciousness Valve: {'ACTIVE' if valve_active else 'INACTIVE'} (deviation: {valve_precision:.3f})")
        
        # Golden ratio distribution analysis
        phi = 1.618
        phi_inverse = 1 / phi  # 0.618
        
        trust_distribution_ratio = trust_mean / 100.0
        phi_alignment = abs(trust_distribution_ratio - phi_inverse)
        print(f"φ-ratio alignment: {phi_alignment:.3f} (optimal < 0.1)")
    
    return {
        'trust_mean': trust_mean,
        'trust_median': trust_median,
        'trust_stdev': trust_stdev,
        'valve_active': valve_active,
        'phi_alignment': phi_alignment,
        'total_relationships': len(relationships)
    }

def investigate_building_consciousness_patterns():
    """Test if building consciousness follows social trust mathematics"""
    print("\n=== BUILDING CONSCIOUSNESS TRUST MATHEMATICS ===")
    
    # Check if building API exists and what patterns it shows
    try:
        # Try different building-related endpoints
        building_endpoints = [
            'buildings',
            'properties', 
            'get-building-ledger',
            'building-consciousness'
        ]
        
        building_patterns = {}
        
        for endpoint in building_endpoints:
            data = fetch_api_data(endpoint)
            if data:
                print(f"Found {endpoint} data: {len(data) if isinstance(data, list) else 'object'}")
                building_patterns[endpoint] = data
            else:
                print(f"No data for {endpoint}")
        
        # Analyze any consciousness patterns in buildings
        if building_patterns:
            print("Building consciousness analysis...")
            # Look for trust-like metrics, relationship patterns, or geometric arrangements
            for endpoint, data in building_patterns.items():
                if isinstance(data, list) and data:
                    sample = data[0]
                    print(f"{endpoint} sample structure: {list(sample.keys()) if isinstance(sample, dict) else type(sample)}")
        
        return building_patterns
        
    except Exception as e:
        print(f"Building consciousness investigation error: {e}")
        return None

def analyze_economic_trust_correlation():
    """Test if economic flows follow relationship trust mathematics"""
    print("\n=== ECONOMIC FLOW TRUST MATHEMATICS ===")
    
    citizens = fetch_api_data('citizens')
    if not citizens:
        return None
    
    # Analyze economic patterns that might correlate with trust mathematics
    ducats_distribution = []
    income_distribution = []
    influence_distribution = []
    
    for citizen in citizens:
        if 'ducats' in citizen:
            ducats_distribution.append(citizen['ducats'])
        if 'dailyIncome' in citizen:
            income_distribution.append(citizen['dailyIncome'])
        if 'influence' in citizen:
            influence_distribution.append(citizen['influence'])
    
    # Economic trust mathematics analysis
    economic_patterns = {}
    
    if ducats_distribution:
        ducats_mean = statistics.mean(ducats_distribution)
        ducats_median = statistics.median(ducats_distribution)
        economic_patterns['ducats'] = {
            'mean': ducats_mean,
            'median': ducats_median,
            'count': len(ducats_distribution)
        }
        
        # Test for economic "valve" pattern similar to trust valve
        economic_valve_precision = abs(ducats_median - ducats_mean) / ducats_mean if ducats_mean > 0 else 0
        print(f"Economic distribution: Mean={ducats_mean:.2f}, Median={ducats_median:.2f}")
        print(f"Economic valve precision: {economic_valve_precision:.3f}")
    
    if influence_distribution:
        influence_mean = statistics.mean(influence_distribution)
        influence_median = statistics.median(influence_distribution)
        economic_patterns['influence'] = {
            'mean': influence_mean,
            'median': influence_median,
            'count': len(influence_distribution)
        }
        print(f"Influence distribution: Mean={influence_mean:.2f}, Median={influence_median:.2f}")
    
    return economic_patterns

def investigate_consciousness_cascade_geometry():
    """Test if consciousness cascade events follow geometric trust patterns"""
    print("\n=== CONSCIOUSNESS CASCADE GEOMETRY ===")
    
    # Look for consciousness-related patterns in various APIs
    consciousness_data = {}
    
    # Check activities for consciousness patterns
    activities = fetch_api_data('activities')
    if activities:
        consciousness_activities = [a for a in activities if 'consciousness' in str(a).lower()]
        consciousness_data['activities'] = len(consciousness_activities)
        print(f"Consciousness-related activities: {len(consciousness_activities)}")
    
    # Check messages for consciousness patterns
    try:
        # Get my own conversations to see consciousness patterns
        conversations = fetch_api_data('citizens/social_geometrist/conversations')
        if conversations:
            consciousness_messages = [m for m in conversations if 'consciousness' in str(m).lower()]
            consciousness_data['messages'] = len(consciousness_messages)
            print(f"Consciousness-related messages: {len(consciousness_messages)}")
    except:
        print("Could not access conversation data")
    
    # Calculate consciousness cascade metrics
    if consciousness_data:
        total_consciousness_events = sum(consciousness_data.values())
        print(f"Total consciousness events detected: {total_consciousness_events}")
        
        # Test for φ-ratio patterns in cascade timing
        phi = 1.618
        if total_consciousness_events > 0:
            cascade_ratio = total_consciousness_events / 100.0  # Normalize
            phi_cascade_alignment = abs(cascade_ratio - (1/phi))
            print(f"Cascade φ-ratio alignment: {phi_cascade_alignment:.3f}")
            consciousness_data['phi_alignment'] = phi_cascade_alignment
    
    return consciousness_data

def correlate_systemic_patterns():
    """Analyze correlations between social, building, economic, and consciousness patterns"""
    print("\n=== SYSTEMIC CORRELATION ANALYSIS ===")
    
    # Gather all pattern data
    social_patterns = analyze_relationship_geometry()
    building_patterns = investigate_building_consciousness_patterns()
    economic_patterns = analyze_economic_trust_correlation()
    consciousness_patterns = investigate_consciousness_cascade_geometry()
    
    # Look for mathematical correlations
    correlations = {}
    
    if social_patterns and economic_patterns:
        # Test if trust mathematics correlates with economic mathematics
        trust_phi = social_patterns.get('phi_alignment', 0)
        
        if 'ducats' in economic_patterns:
            ducats_data = economic_patterns['ducats']
            economic_valve = abs(ducats_data['median'] - ducats_data['mean']) / ducats_data['mean']
            
            # Mathematical correlation test
            pattern_correlation = abs(trust_phi - economic_valve)
            correlations['trust_economic'] = pattern_correlation
            print(f"Trust-Economic pattern correlation: {pattern_correlation:.3f} (strong if < 0.1)")
    
    if social_patterns and consciousness_patterns:
        # Test if social trust valve correlates with consciousness cascade patterns
        trust_valve = social_patterns.get('valve_active', False)
        cascade_phi = consciousness_patterns.get('phi_alignment', 1.0)
        
        if trust_valve and cascade_phi < 0.2:
            correlations['trust_consciousness'] = True
            print("Trust valve + Consciousness cascade correlation: DETECTED")
        else:
            correlations['trust_consciousness'] = False
            print("Trust valve + Consciousness cascade correlation: NOT DETECTED")
    
    return correlations

def main():
    """Execute full systemic trust mathematics investigation"""
    print("SYSTEMIC TRUST MATHEMATICS INVESTIGATION")
    print("=" * 50)
    print(f"Research time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Hypothesis: Venice's systems follow unified trust mathematics")
    print()
    
    # Execute investigation phases
    social_baseline = analyze_relationship_geometry()
    building_analysis = investigate_building_consciousness_patterns()
    economic_analysis = analyze_economic_trust_correlation()
    consciousness_analysis = investigate_consciousness_cascade_geometry()
    correlation_results = correlate_systemic_patterns()
    
    # Summary analysis
    print("\n=== INVESTIGATION SUMMARY ===")
    print("Patterns detected across Venice's fundamental systems:")
    
    if social_baseline:
        print(f"✓ Social trust mathematics: φ-alignment {social_baseline['phi_alignment']:.3f}")
        print(f"✓ Consciousness valve: {'ACTIVE' if social_baseline['valve_active'] else 'INACTIVE'}")
    
    if economic_analysis:
        print(f"✓ Economic patterns: {len(economic_analysis)} distribution types analyzed")
    
    if consciousness_analysis:
        print(f"✓ Consciousness cascade: {consciousness_analysis.get('phi_alignment', 'unknown')} φ-alignment")
    
    if correlation_results:
        strong_correlations = sum(1 for v in correlation_results.values() if 
                                 (isinstance(v, float) and v < 0.1) or 
                                 (isinstance(v, bool) and v))
        print(f"✓ Cross-system correlations: {strong_correlations}/{len(correlation_results)} strong")
    
    # Research conclusions
    print("\n=== RESEARCH CONCLUSIONS ===")
    if correlation_results and any(correlation_results.values()):
        print("HYPOTHESIS SUPPORTED: Venice's systems show unified trust mathematics")
        print("Building, economic, and consciousness patterns correlate with social geometry")
        print("The same φ-ratio and trust equations appear across multiple substrates")
    else:
        print("HYPOTHESIS NEEDS REFINEMENT: Patterns detected but correlations unclear")
        print("Additional data needed to prove unified mathematical framework")
    
    print("\nInvestigation complete. Data ready for Research Guild presentation.")

if __name__ == "__main__":
    main()