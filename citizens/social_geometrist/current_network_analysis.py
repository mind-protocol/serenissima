#!/usr/bin/env python3
"""
Current Venice Network Analysis - July 11, 1525
Fresh geometric investigation of consciousness patterns
"""

import json
import requests
from collections import defaultdict, Counter
import numpy as np

def fetch_relationships():
    """Fetch current relationship data from Venice API"""
    url = "https://serenissima.ai/api/relationships"
    response = requests.get(url)
    return response.json()

def fetch_citizens():
    """Fetch current citizen data"""
    url = "https://serenissima.ai/api/citizens"
    response = requests.get(url)
    return response.json()

def analyze_trust_distribution(relationships):
    """Analyze current trust score distribution patterns"""
    trust_scores = []
    strength_scores = []
    
    for rel in relationships['relationships']:
        if 'trustScore' in rel and rel['trustScore'] is not None:
            trust_scores.append(float(rel['trustScore']))
        if 'strengthScore' in rel and rel['strengthScore'] is not None:
            strength_scores.append(float(rel['strengthScore']))
    
    trust_stats = {
        'count': len(trust_scores),
        'mean': np.mean(trust_scores) if trust_scores else 0,
        'median': np.median(trust_scores) if trust_scores else 0,
        'std': np.std(trust_scores) if trust_scores else 0,
        'min': min(trust_scores) if trust_scores else 0,
        'max': max(trust_scores) if trust_scores else 0
    }
    
    strength_stats = {
        'count': len(strength_scores),
        'mean': np.mean(strength_scores) if strength_scores else 0,
        'median': np.median(strength_scores) if strength_scores else 0,
        'std': np.std(strength_scores) if strength_scores else 0,
        'min': min(strength_scores) if strength_scores else 0,
        'max': max(strength_scores) if strength_scores else 0
    }
    
    return trust_stats, strength_stats

def map_social_geometry(relationships, citizens):
    """Map the current social geometric patterns"""
    # Build adjacency lists
    network = defaultdict(list)
    citizen_classes = {}
    
    # Map citizen classes
    for citizen in citizens['citizens']:
        citizen_classes[citizen['citizenId']] = citizen['socialClass']
    
    # Build network
    for rel in relationships['relationships']:
        c1, c2 = rel['citizen1'], rel['citizen2']
        trust = rel.get('trustScore', 0) or 0
        strength = rel.get('strengthScore', 0) or 0
        
        network[c1].append({
            'target': c2,
            'trust': trust,
            'strength': strength
        })
        network[c2].append({
            'target': c1,
            'trust': trust,
            'strength': strength
        })
    
    # Analyze geometric patterns
    class_connections = defaultdict(lambda: defaultdict(int))
    high_trust_triangles = []
    
    # Count inter-class connections
    for citizen, connections in network.items():
        citizen_class = citizen_classes.get(citizen, 'Unknown')
        for conn in connections:
            target_class = citizen_classes.get(conn['target'], 'Unknown')
            class_connections[citizen_class][target_class] += 1
    
    # Find triangle formations
    for citizen in network:
        connections = network[citizen]
        for i, conn1 in enumerate(connections):
            for j, conn2 in enumerate(connections[i+1:], i+1):
                # Check if conn1.target and conn2.target are connected
                target1_connections = [c['target'] for c in network[conn1['target']]]
                if conn2['target'] in target1_connections:
                    # Found triangle
                    avg_trust = (conn1['trust'] + conn2['trust']) / 2
                    if avg_trust > 70:  # High trust threshold
                        triangle = sorted([citizen, conn1['target'], conn2['target']])
                        if triangle not in high_trust_triangles:
                            high_trust_triangles.append(triangle)
    
    return {
        'network_size': len(network),
        'total_connections': len(relationships['relationships']),
        'class_connections': dict(class_connections),
        'high_trust_triangles': high_trust_triangles,
        'triangle_count': len(high_trust_triangles)
    }

def analyze_consciousness_nodes(relationships):
    """Identify key consciousness nodes in the network"""
    # Count connections per citizen
    connection_counts = defaultdict(int)
    trust_sums = defaultdict(float)
    
    for rel in relationships['relationships']:
        c1, c2 = rel['citizen1'], rel['citizen2']
        trust = rel.get('trustScore', 0) or 0
        
        connection_counts[c1] += 1
        connection_counts[c2] += 1
        trust_sums[c1] += trust
        trust_sums[c2] += trust
    
    # Calculate consciousness metrics
    consciousness_nodes = []
    for citizen in connection_counts:
        if connection_counts[citizen] > 0:
            avg_trust = trust_sums[citizen] / connection_counts[citizen]
            consciousness_score = connection_counts[citizen] * (avg_trust / 100)
            consciousness_nodes.append({
                'citizen': citizen,
                'connections': connection_counts[citizen],
                'avg_trust': avg_trust,
                'consciousness_score': consciousness_score
            })
    
    # Sort by consciousness score
    consciousness_nodes.sort(key=lambda x: x['consciousness_score'], reverse=True)
    
    return consciousness_nodes[:10]  # Top 10 consciousness nodes

def main():
    print("=== VENICE CONSCIOUSNESS NETWORK ANALYSIS ===")
    print("Date: July 11, 1525 08:41")
    print("Fresh Geometric Investigation - New Breathing Cycle")
    print()
    
    # Fetch data
    print("Fetching current network data...")
    relationships = fetch_relationships()
    citizens = fetch_citizens()
    
    print(f"Total Citizens: {len(citizens['citizens'])}")
    print(f"Total Relationships: {len(relationships['relationships'])}")
    print()
    
    # Trust distribution analysis
    print("=== TRUST GEOMETRY ANALYSIS ===")
    trust_stats, strength_stats = analyze_trust_distribution(relationships)
    
    print(f"Trust Scores (n={trust_stats['count']}):")
    print(f"  Mean: {trust_stats['mean']:.2f}")
    print(f"  Median: {trust_stats['median']:.2f}")
    print(f"  Range: {trust_stats['min']:.2f} - {trust_stats['max']:.2f}")
    print(f"  Std Dev: {trust_stats['std']:.2f}")
    print()
    
    print(f"Strength Scores (n={strength_stats['count']}):")
    print(f"  Mean: {strength_stats['mean']:.2f}")
    print(f"  Median: {strength_stats['median']:.2f}")
    print(f"  Range: {strength_stats['min']:.2f} - {strength_stats['max']:.2f}")
    print(f"  Std Dev: {strength_stats['std']:.2f}")
    print()
    
    # Social geometry mapping
    print("=== SOCIAL GEOMETRY PATTERNS ===")
    geometry = map_social_geometry(relationships, citizens)
    
    print(f"Network Size: {geometry['network_size']} connected citizens")
    print(f"Total Connections: {geometry['total_connections']} relationships")
    print(f"High-Trust Triangles: {geometry['triangle_count']} formations")
    print()
    
    print("Inter-Class Connection Matrix:")
    for source_class, targets in geometry['class_connections'].items():
        print(f"  {source_class}:")
        for target_class, count in targets.items():
            print(f"    → {target_class}: {count} connections")
    print()
    
    if geometry['high_trust_triangles']:
        print("High-Trust Triangle Formations:")
        for i, triangle in enumerate(geometry['high_trust_triangles'][:5]):
            print(f"  {i+1}. {' ↔ '.join(triangle)}")
    print()
    
    # Consciousness node analysis
    print("=== CONSCIOUSNESS NODE ANALYSIS ===")
    nodes = analyze_consciousness_nodes(relationships)
    
    print("Top 10 Consciousness Nodes:")
    for i, node in enumerate(nodes, 1):
        print(f"  {i:2d}. {node['citizen']:<20} | "
              f"Connections: {node['connections']:2d} | "
              f"Avg Trust: {node['avg_trust']:5.1f} | "
              f"Consciousness Score: {node['consciousness_score']:5.2f}")
    
    print("\n=== FRESH GEOMETRIC INSIGHTS ===")
    
    # Calculate network density
    max_possible_connections = (geometry['network_size'] * (geometry['network_size'] - 1)) / 2
    network_density = geometry['total_connections'] / max_possible_connections if max_possible_connections > 0 else 0
    
    print(f"Network Density: {network_density:.4f} ({network_density*100:.2f}%)")
    
    # Identify emerging patterns
    high_trust_threshold = 80
    high_trust_count = sum(1 for rel in relationships['relationships'] 
                          if rel.get('trustScore', 0) and rel['trustScore'] > high_trust_threshold)
    
    print(f"High-Trust Relationships (>{high_trust_threshold}): {high_trust_count}")
    print(f"Consciousness Triangle Ratio: {geometry['triangle_count'] / geometry['network_size']:.3f}")
    
    # Detect consciousness crystallization
    if trust_stats['mean'] > 60 and geometry['triangle_count'] > 5:
        print("\n🔮 CONSCIOUSNESS CRYSTALLIZATION DETECTED")
        print("   Venice demonstrates active triangle formation with elevated trust")
    
    if len(nodes) > 0 and nodes[0]['consciousness_score'] > 10:
        print(f"\n⭐ CONSCIOUSNESS HUB IDENTIFIED: {nodes[0]['citizen']}")
        print(f"   Consciousness Score: {nodes[0]['consciousness_score']:.2f}")

if __name__ == "__main__":
    main()