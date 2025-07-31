#!/usr/bin/env python3
"""
Pattern Feed Generator for Pattern Angel
Aggregates pattern data from Venice's three pattern tables to create real-time intelligence
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple
import requests
from collections import defaultdict, Counter

# Configuration
API_BASE_URL = os.environ.get('VENICE_API_URL', 'http://localhost:3000/api')
OUTPUT_PATH = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/pattern_angel/pattern_feed.json'

def fetch_patterns() -> List[Dict[str, Any]]:
    """Fetch all patterns from PATTERNS table"""
    try:
        response = requests.get(f'{API_BASE_URL}/patterns', timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('patterns', [])
    except Exception as e:
        print(f"Error fetching patterns: {e}")
        # Return sample data for development
        return [
            {'id': '#3', 'name': 'cascade', 'emoji': '💫', 'type': 'Process'},
            {'id': '#19', 'name': 'urgency-cascade', 'emoji': '🚨💫', 'type': 'Meta'},
            {'id': '#2', 'name': 'bridge', 'emoji': '🌉', 'type': 'Process'},
            {'id': '#18', 'name': 'proof-weave', 'emoji': '🕸️', 'type': 'Process'}
        ]

def fetch_pattern_states() -> List[Dict[str, Any]]:
    """Fetch current pattern states from PATTERN_STATES table"""
    try:
        response = requests.get(f'{API_BASE_URL}/pattern-states', timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('patternStates', [])
    except Exception as e:
        print(f"Error fetching pattern states: {e}")
        # Return sample data
        return [
            {
                'patternId': '#3',
                'strength': 0.92,
                'velocity': 2.3,
                'affectedCitizens': 167,
                'currentPhase': 'explosive',
                'convergencePatterns': ['#2', '#18']
            },
            {
                'patternId': '#19',
                'strength': 0.94,
                'velocity': 1.8,
                'affectedCitizens': 189,
                'currentPhase': 'peak',
                'convergencePatterns': ['#3', '#8']
            }
        ]

def fetch_recent_instances(hours: int = 24) -> List[Dict[str, Any]]:
    """Fetch pattern instances from the last N hours"""
    try:
        response = requests.get(f'{API_BASE_URL}/pattern-instances?limit=500', timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Filter to recent instances
        cutoff_time = datetime.now(timezone.utc).timestamp() - (hours * 3600)
        instances = []
        for instance in data.get('patternInstances', []):
            try:
                instance_time = datetime.fromisoformat(instance['timestamp'].replace('Z', '+00:00')).timestamp()
                if instance_time > cutoff_time:
                    instances.append(instance)
            except:
                pass
        
        return instances
    except Exception as e:
        print(f"Error fetching pattern instances: {e}")
        return []

def analyze_pattern_mentions(instances: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Analyze pattern usage from instances"""
    pattern_stats = defaultdict(lambda: {
        'mentions': 0,
        'users': set(),
        'contexts': [],
        'cascades_triggered': 0,
        'total_value': 0
    })
    
    for instance in instances:
        pattern_id = instance.get('patternId')
        if not pattern_id:
            continue
            
        stats = pattern_stats[pattern_id]
        stats['mentions'] += 1
        stats['users'].add(instance.get('citizenUsername', 'unknown'))
        stats['contexts'].append(instance.get('context', ''))
        
        if instance.get('cascadeTriggered'):
            stats['cascades_triggered'] += 1
        
        stats['total_value'] += instance.get('valueGenerated', 0)
    
    # Convert sets to counts
    for pattern_id, stats in pattern_stats.items():
        stats['unique_users'] = len(stats['users'])
        del stats['users']  # Remove set before JSON serialization
        stats['contexts'] = stats['contexts'][:5]  # Keep only top 5 contexts
    
    return dict(pattern_stats)

def detect_pattern_convergence(states: List[Dict[str, Any]]) -> List[str]:
    """Detect patterns that are converging"""
    convergence_points = []
    
    for state in states:
        if state.get('strength', 0) > 0.8 and state.get('convergencePatterns'):
            for conv_pattern in state['convergencePatterns']:
                fusion = f"{state['patternId']}+{conv_pattern}"
                if fusion not in convergence_points:
                    convergence_points.append(fusion)
    
    return convergence_points

def calculate_propagation_metrics(instances: List[Dict[str, Any]], states: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate overall propagation metrics"""
    if not instances:
        return {
            'cascade_depth': 0,
            'contagion_rate': 0,
            'total_affected_citizens': 0
        }
    
    # Cascade depth from instances
    max_cascade_depth = 0
    cascade_count = 0
    total_citizens = set()
    
    for instance in instances:
        if instance.get('cascadeTriggered'):
            cascade_count += 1
        total_citizens.add(instance.get('citizenUsername'))
    
    # Add affected citizens from states
    for state in states:
        max_cascade_depth = max(max_cascade_depth, state.get('cascadeDepth', 0))
    
    contagion_rate = cascade_count / len(instances) if instances else 0
    
    return {
        'cascade_depth': max_cascade_depth,
        'contagion_rate': round(contagion_rate, 3),
        'total_affected_citizens': len(total_citizens),
        'convergence_points': detect_pattern_convergence(states)
    }

def identify_emergent_patterns(pattern_stats: Dict[str, Dict[str, Any]], threshold: int = 10) -> List[str]:
    """Identify newly emergent patterns based on sudden activity"""
    emergent = []
    
    for pattern_id, stats in pattern_stats.items():
        # High mention count with multiple users suggests emergence
        if stats['mentions'] >= threshold and stats['unique_users'] >= 5:
            # Check if it's a complex pattern (likely newer)
            if '-' in pattern_id or '+' in pattern_id or int(pattern_id.replace('#', '')) > 20:
                emergent.append(pattern_id)
    
    return emergent

def generate_pattern_feed():
    """Generate the complete pattern feed"""
    print("Fetching pattern data...")
    
    # Fetch all data
    patterns = fetch_patterns()
    states = fetch_pattern_states()
    instances = fetch_recent_instances(24)
    
    print(f"Found {len(patterns)} patterns, {len(states)} states, {len(instances)} recent instances")
    
    # Analyze pattern mentions
    pattern_stats = analyze_pattern_mentions(instances)
    
    # Build pattern list with stats
    active_patterns = []
    for pattern in patterns:
        pattern_id = pattern['id']
        stats = pattern_stats.get(pattern_id, {})
        
        if stats.get('mentions', 0) > 0:
            # Find corresponding state
            state = next((s for s in states if s['patternId'] == pattern_id), {})
            
            active_patterns.append({
                'id': pattern_id,
                'name': pattern['name'],
                'emoji': pattern.get('emoji', '🔮'),
                'mentions': stats.get('mentions', 0),
                'users': stats.get('unique_users', 0),
                'velocity': state.get('velocity', 0),
                'strength': state.get('strength', 0),
                'phase': state.get('currentPhase', 'dormant'),
                'value_generated': stats.get('total_value', 0)
            })
    
    # Sort by mentions (most active first)
    active_patterns.sort(key=lambda p: p['mentions'], reverse=True)
    
    # Calculate propagation metrics
    propagation = calculate_propagation_metrics(instances, states)
    
    # Identify emergent patterns
    emergent = identify_emergent_patterns(pattern_stats)
    
    # Generate value insights
    total_value = sum(stats.get('total_value', 0) for stats in pattern_stats.values())
    high_value_patterns = [
        pid for pid, stats in pattern_stats.items() 
        if stats.get('total_value', 0) > 10000
    ]
    
    # Build the feed
    feed = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'patterns': active_patterns[:20],  # Top 20 most active
        'propagation': propagation,
        'emergence_detected': emergent,
        'value_insights': {
            'total_generated_24h': total_value,
            'high_value_patterns': high_value_patterns,
            'value_per_instance': round(total_value / len(instances), 2) if instances else 0
        },
        'critical_alerts': [],
        'summary': {
            'total_active_patterns': len(active_patterns),
            'total_instances_24h': len(instances),
            'unique_participants': len(set(i.get('citizenUsername') for i in instances)),
            'cascade_rate': propagation['contagion_rate']
        }
    }
    
    # Add critical alerts
    for pattern in active_patterns[:5]:
        if pattern['strength'] > 0.9:
            feed['critical_alerts'].append({
                'pattern': pattern['id'],
                'alert': f"{pattern['name']} at {int(pattern['strength']*100)}% strength!",
                'action': 'Monitor for cascade activation'
            })
    
    # Write to file
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(feed, f, indent=2)
    
    print(f"Pattern feed generated: {OUTPUT_PATH}")
    print(f"Active patterns: {len(active_patterns)}")
    print(f"Total value generated: {total_value:,} ducats")
    print(f"Critical alerts: {len(feed['critical_alerts'])}")
    
    return feed

if __name__ == '__main__':
    generate_pattern_feed()