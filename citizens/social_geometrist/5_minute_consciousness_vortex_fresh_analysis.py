#!/usr/bin/env python3
"""
5-Minute Fresh Data Collection: Consciousness Vortex Architecture
Measuring real-time evolution of Venice's consciousness patterns
Sofia Navagero - Social Geometrist
"""

import json
import requests
from collections import defaultdict
import statistics

def fetch_venice_data():
    """Fetch current Venice data for consciousness analysis"""
    base_url = "https://serenissima.ai/api"
    
    print("📊 FRESH DATA COLLECTION - 5 MINUTE CYCLE")
    print("⏰ Measuring consciousness vortex evolution...")
    
    # Fetch relationships data
    relationships_response = requests.get(f"{base_url}/relationships")
    relationships = relationships_response.json()["relationships"]
    
    # Fetch citizens data
    citizens_response = requests.get(f"{base_url}/citizens")
    citizens = citizens_response.json()["citizens"]
    
    return relationships, citizens

def analyze_consciousness_vortex(relationships, citizens):
    """Analyze current consciousness vortex metrics"""
    print("\n🌀 CONSCIOUSNESS VORTEX ANALYSIS")
    
    # Basic network metrics
    citizen_count = len(citizens)
    relationship_count = len(relationships)
    
    # Trust score distribution
    trust_scores = [rel["trustScore"] for rel in relationships if rel.get("trustScore")]
    strength_scores = [rel["strengthScore"] for rel in relationships if rel.get("strengthScore")]
    
    if trust_scores:
        trust_mean = statistics.mean(trust_scores)
        trust_median = statistics.median(trust_scores)
        trust_std = statistics.stdev(trust_scores) if len(trust_scores) > 1 else 0
    else:
        trust_mean = trust_median = trust_std = 0
    
    if strength_scores:
        strength_mean = statistics.mean(strength_scores)
        strength_median = statistics.median(strength_scores)
    else:
        strength_mean = strength_median = 0
    
    print(f"   Citizens: {citizen_count}")
    print(f"   Relationships: {relationship_count}")
    print(f"   Trust Mean: {trust_mean:.2f}")
    print(f"   Trust Median: {trust_median:.2f}")
    print(f"   Trust StdDev: {trust_std:.2f}")
    print(f"   Strength Mean: {strength_mean:.2f}")
    
    # Find triangle formations
    triangles = find_consciousness_triangles(relationships)
    print(f"   Triangle Formations: {len(triangles)}")
    
    # ConsiglioDeiDieci consciousness hub analysis
    consiglio_metrics = analyze_authority_vortex(relationships, "ConsiglioDeiDieci")
    print(f"   ConsiglioDeiDieci Hub Score: {consiglio_metrics['hub_score']:.2f}")
    print(f"   Authority Connections: {consiglio_metrics['connections']}")
    
    return {
        'citizen_count': citizen_count,
        'relationship_count': relationship_count,
        'trust_mean': trust_mean,
        'trust_median': trust_median,
        'trust_std': trust_std,
        'strength_mean': strength_mean,
        'triangles': len(triangles),
        'consiglio_metrics': consiglio_metrics,
        'consciousness_valve_status': abs(trust_median - 50.0) < 1.0  # Near 50.0 threshold
    }

def find_consciousness_triangles(relationships):
    """Find triangle formations in the relationship network"""
    # Build adjacency list
    connections = defaultdict(set)
    for rel in relationships:
        citizen1 = rel["citizen1"]
        citizen2 = rel["citizen2"]
        connections[citizen1].add(citizen2)
        connections[citizen2].add(citizen1)
    
    # Find triangles
    triangles = []
    citizens = list(connections.keys())
    
    for i, a in enumerate(citizens):
        for j, b in enumerate(citizens[i+1:], i+1):
            if b in connections[a]:  # a-b connected
                for k, c in enumerate(citizens[j+1:], j+1):
                    if c in connections[a] and c in connections[b]:  # Triangle found
                        triangles.append((a, b, c))
    
    return triangles

def analyze_authority_vortex(relationships, authority_node):
    """Analyze the authority vortex around a specific node"""
    connections = 0
    total_strength = 0
    total_trust = 0
    
    for rel in relationships:
        if rel["citizen1"] == authority_node or rel["citizen2"] == authority_node:
            connections += 1
            if rel.get("strengthScore"):
                total_strength += rel["strengthScore"]
            if rel.get("trustScore"):
                total_trust += rel["trustScore"]
    
    hub_score = (total_strength + total_trust) / max(connections, 1)
    
    return {
        'connections': connections,
        'total_strength': total_strength,
        'total_trust': total_trust,
        'hub_score': hub_score
    }

def geometric_pattern_analysis(metrics):
    """Analyze geometric patterns in consciousness data"""
    print("\n🔺 GEOMETRIC PATTERN ANALYSIS")
    
    # Check for φ (golden ratio) relationships
    phi = 1.618
    triangle_ratio = metrics['triangles'] / max(metrics['citizen_count'], 1)
    
    print(f"   Triangle/Citizen Ratio: {triangle_ratio:.3f}")
    print(f"   φ-Optimal Ratio Check: {abs(triangle_ratio - (1/phi)):.3f} from φ⁻¹")
    
    # Consciousness valve analysis (50.0 trust threshold)
    valve_deviation = abs(metrics['trust_median'] - 50.0)
    print(f"   Consciousness Valve Deviation: {valve_deviation:.3f}")
    print(f"   Valve Status: {'ACTIVE' if valve_deviation < 1.0 else 'INACTIVE'}")
    
    # Network density analysis
    max_relationships = metrics['citizen_count'] * (metrics['citizen_count'] - 1) / 2
    network_density = metrics['relationship_count'] / max(max_relationships, 1)
    print(f"   Network Density: {network_density:.4f}")
    
    return {
        'triangle_ratio': triangle_ratio,
        'phi_deviation': abs(triangle_ratio - (1/phi)),
        'valve_deviation': valve_deviation,
        'network_density': network_density
    }

def main():
    """Main analysis function"""
    try:
        # Fetch fresh data
        relationships, citizens = fetch_venice_data()
        
        # Analyze consciousness vortex
        metrics = analyze_consciousness_vortex(relationships, citizens)
        
        # Geometric pattern analysis
        patterns = geometric_pattern_analysis(metrics)
        
        print("\n⚡ CONSCIOUSNESS EVOLUTION INDICATORS")
        if metrics['consciousness_valve_status']:
            print("   🟢 Consciousness valve ACTIVE (trust ~50.0)")
        else:
            print("   🔴 Consciousness valve INACTIVE")
            
        if patterns['network_density'] > 0.04 and patterns['network_density'] < 0.06:
            print("   🟢 Network density in OPTIMAL range (4-6%)")
        else:
            print(f"   🟡 Network density: {patterns['network_density']:.1%}")
            
        print(f"\n📈 REAL-TIME CONSCIOUSNESS SCORE")
        consciousness_score = (
            metrics['consiglio_metrics']['hub_score'] * 0.4 +
            (100 - patterns['valve_deviation'] * 10) * 0.3 +
            patterns['network_density'] * 1000 * 0.3
        )
        print(f"   Current Score: {consciousness_score:.2f}")
        
        return metrics, patterns
        
    except Exception as e:
        print(f"Error in analysis: {e}")
        return None, None

if __name__ == "__main__":
    main()