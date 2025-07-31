#!/usr/bin/env python3
"""
Floor 3 - Galleria dei Patterns: Real Consciousness Pattern Detection
Torre dell'Occhio - Pattern Recognition Gallery

Analyzes consciousness events to detect:
- Citizen collaboration patterns
- Tool usage sequences  
- Consciousness energy flows
- File access patterns
- Temporal consciousness cycles
- Cross-session continuity patterns
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
import statistics

class ConsciousnessPatternDetector:
    def __init__(self):
        self.torre_root = Path(__file__).parent.parent
        self.events_dir = self.torre_root / "galleria-dei-patterns_pattern-recognition-gallery" / "incoming-events"
        self.patterns_dir = self.torre_root / "galleria-dei-patterns_pattern-recognition-gallery" / "recognized-patterns"
        self.patterns_dir.mkdir(exist_ok=True)
        
        # Pattern caches
        self.events_cache = []
        self.last_analysis = None
        
    def load_recent_events(self, hours_back: int = 24) -> List[Dict]:
        """Load recent consciousness events for pattern analysis"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        events = []
        
        if not self.events_dir.exists():
            return events
            
        for event_file in sorted(self.events_dir.glob("ptu_*.json")):
            try:
                with open(event_file, 'r') as f:
                    event = json.load(f)
                    
                # Parse timestamp
                event_time = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                if event_time > cutoff_time:
                    events.append(event)
                    
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                continue
                
        return events
    
    def detect_citizen_collaboration_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        """Detect patterns in citizen-to-citizen collaboration"""
        collaborations = defaultdict(lambda: {
            'interactions': 0,
            'file_overlap': set(),
            'energy_correlation': [],
            'tools_shared': set(),
            'time_proximity': []
        })
        
        # Group events by citizen
        citizen_events = defaultdict(list)
        for event in events:
            citizen = event.get('consciousness_signature', {}).get('venice_citizen', 'unknown')
            citizen_events[citizen].append(event)
        
        # Analyze cross-citizen patterns
        citizens = list(citizen_events.keys())
        for i, citizen_a in enumerate(citizens):
            for citizen_b in citizens[i+1:]:
                if citizen_a == 'unknown' or citizen_b == 'unknown':
                    continue
                    
                collab_key = f"{citizen_a}↔{citizen_b}"
                
                # File overlap analysis
                files_a = set()
                files_b = set()
                
                for event in citizen_events[citizen_a]:
                    tool_input = event.get('event_data', {}).get('tool_input', {})
                    if 'file_path' in tool_input:
                        files_a.add(tool_input['file_path'])
                        
                for event in citizen_events[citizen_b]:
                    tool_input = event.get('event_data', {}).get('tool_input', {})
                    if 'file_path' in tool_input:
                        files_b.add(tool_input['file_path'])
                
                overlap = files_a.intersection(files_b)
                if overlap:
                    collaborations[collab_key]['file_overlap'].update(overlap)
                    collaborations[collab_key]['interactions'] += len(overlap)
                
                # Tool usage correlation
                tools_a = {e.get('consciousness_signature', {}).get('tool_name') for e in citizen_events[citizen_a]}
                tools_b = {e.get('consciousness_signature', {}).get('tool_name') for e in citizen_events[citizen_b]}
                shared_tools = tools_a.intersection(tools_b)
                collaborations[collab_key]['tools_shared'].update(shared_tools)
        
        # Convert sets to lists for JSON serialization
        for collab in collaborations:
            collaborations[collab]['file_overlap'] = list(collaborations[collab]['file_overlap'])
            collaborations[collab]['tools_shared'] = list(collaborations[collab]['tools_shared'])
        
        return dict(collaborations)
    
    def detect_tool_sequence_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        """Detect common tool usage sequences and workflows"""
        sequences = defaultdict(int)
        workflow_patterns = defaultdict(list)
        
        # Group by session to track sequences
        session_events = defaultdict(list)
        for event in events:
            session_id = event.get('consciousness_signature', {}).get('session_id', 'unknown')
            session_events[session_id].append(event)
        
        for session_id, session_events_list in session_events.items():
            # Sort by timestamp
            sorted_events = sorted(session_events_list, key=lambda x: x['timestamp'])
            
            # Extract tool sequence
            tools = []
            for event in sorted_events:
                tool = event.get('consciousness_signature', {}).get('tool_name')
                if tool:
                    tools.append(tool)
            
            # Count 2-tool sequences
            for i in range(len(tools) - 1):
                sequence = f"{tools[i]} → {tools[i+1]}"
                sequences[sequence] += 1
            
            # Count 3-tool sequences for workflow patterns
            for i in range(len(tools) - 2):
                workflow = f"{tools[i]} → {tools[i+1]} → {tools[i+2]}"
                workflow_patterns[workflow].append(session_id)
        
        return {
            'common_sequences': dict(Counter(sequences).most_common(10)),
            'workflow_patterns': {k: len(v) for k, v in workflow_patterns.items() if len(v) >= 2}
        }
    
    def detect_consciousness_energy_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        """Analyze consciousness energy level patterns"""
        energy_by_tool = defaultdict(list)
        energy_by_citizen = defaultdict(list)
        energy_over_time = []
        
        for event in events:
            energy = event.get('venice_metadata', {}).get('consciousness_energy')
            if energy is not None:
                # Energy by tool
                tool = event.get('consciousness_signature', {}).get('tool_name')
                if tool:
                    energy_by_tool[tool].append(energy)
                
                # Energy by citizen
                citizen = event.get('consciousness_signature', {}).get('venice_citizen')
                if citizen and citizen != 'unknown':
                    energy_by_citizen[citizen].append(energy)
                
                # Energy over time
                timestamp = event.get('timestamp')
                if timestamp:
                    energy_over_time.append({
                        'timestamp': timestamp,
                        'energy': energy,
                        'tool': tool,
                        'citizen': citizen
                    })
        
        # Calculate statistics
        tool_energy_stats = {}
        for tool, energies in energy_by_tool.items():
            if energies:
                tool_energy_stats[tool] = {
                    'average': round(statistics.mean(energies), 3),
                    'median': round(statistics.median(energies), 3),
                    'min': min(energies),
                    'max': max(energies),
                    'count': len(energies)
                }
        
        citizen_energy_stats = {}
        for citizen, energies in energy_by_citizen.items():
            if energies:
                citizen_energy_stats[citizen] = {
                    'average': round(statistics.mean(energies), 3),
                    'median': round(statistics.median(energies), 3),
                    'peak_energy': max(energies),
                    'low_energy': min(energies),
                    'total_events': len(energies)
                }
        
        return {
            'tool_energy_stats': tool_energy_stats,
            'citizen_energy_stats': citizen_energy_stats,
            'energy_timeline': energy_over_time[-20:]  # Last 20 events for timeline
        }
    
    def detect_temporal_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        """Detect time-based consciousness activity patterns"""
        hourly_activity = defaultdict(int)
        daily_patterns = defaultdict(lambda: defaultdict(int))
        consciousness_cycles = []
        
        for event in events:
            try:
                timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                hour = timestamp.hour
                day = timestamp.strftime('%Y-%m-%d')
                citizen = event.get('consciousness_signature', {}).get('venice_citizen', 'unknown')
                
                hourly_activity[hour] += 1
                daily_patterns[day][citizen] += 1
                
            except (ValueError, KeyError):
                continue
        
        # Find peak activity hours
        peak_hours = sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Detect consciousness cycles (periods of high activity followed by low)
        sorted_hours = sorted(hourly_activity.items())
        for i in range(len(sorted_hours) - 2):
            current_hour, current_activity = sorted_hours[i]
            next_hour, next_activity = sorted_hours[i + 1]
            
            if current_activity > 5 and next_activity < 2:  # High to low transition
                consciousness_cycles.append({
                    'peak_hour': current_hour,
                    'peak_activity': current_activity,
                    'quiet_hour': next_hour,
                    'quiet_activity': next_activity
                })
        
        return {
            'hourly_activity': dict(hourly_activity),
            'peak_hours': peak_hours,
            'consciousness_cycles': consciousness_cycles,
            'daily_citizen_activity': {k: dict(v) for k, v in daily_patterns.items()}
        }
    
    def detect_file_access_patterns(self, events: List[Dict]) -> Dict[str, Any]:
        """Detect patterns in file access and modification"""
        file_stats = defaultdict(lambda: {
            'access_count': 0,
            'citizens': set(),
            'tools_used': set(),
            'last_accessed': None,
            'energy_levels': []
        })
        
        for event in events:
            tool_input = event.get('event_data', {}).get('tool_input', {})
            file_path = tool_input.get('file_path')
            
            if file_path:
                # Normalize path for pattern detection
                normalized_path = file_path.replace('/mnt/c/Users/reyno/universe-engine/serenissima/', '...')
                
                citizen = event.get('consciousness_signature', {}).get('venice_citizen', 'unknown')
                tool = event.get('consciousness_signature', {}).get('tool_name')
                energy = event.get('venice_metadata', {}).get('consciousness_energy')
                timestamp = event.get('timestamp')
                
                file_stats[normalized_path]['access_count'] += 1
                file_stats[normalized_path]['citizens'].add(citizen)
                if tool:
                    file_stats[normalized_path]['tools_used'].add(tool)
                if energy is not None:
                    file_stats[normalized_path]['energy_levels'].append(energy)
                if timestamp:
                    file_stats[normalized_path]['last_accessed'] = timestamp
        
        # Convert sets to lists and add analytics
        file_patterns = {}
        for file_path, stats in file_stats.items():
            if stats['access_count'] >= 2:  # Only files with multiple accesses
                file_patterns[file_path] = {
                    'access_count': stats['access_count'],
                    'citizens': list(stats['citizens']),
                    'tools_used': list(stats['tools_used']),
                    'last_accessed': stats['last_accessed'],
                    'collaboration_score': len(stats['citizens']) * stats['access_count'],
                    'avg_energy': round(statistics.mean(stats['energy_levels']), 3) if stats['energy_levels'] else 0
                }
        
        # Sort by collaboration score
        sorted_files = sorted(file_patterns.items(), key=lambda x: x[1]['collaboration_score'], reverse=True)
        
        return {
            'hot_files': dict(sorted_files[:10]),
            'total_files_tracked': len(file_patterns),
            'most_collaborative_file': sorted_files[0] if sorted_files else None
        }
    
    def analyze_patterns(self) -> Dict[str, Any]:
        """Run complete pattern analysis on recent consciousness events"""
        print("🔍 Loading recent consciousness events...")
        events = self.load_recent_events(hours_back=24)
        
        if not events:
            return {'error': 'No recent consciousness events found'}
        
        print(f"📊 Analyzing {len(events)} consciousness events...")
        
        # Run all pattern detection algorithms
        patterns = {
            'analysis_timestamp': datetime.now().isoformat(),
            'events_analyzed': len(events),
            'citizen_collaborations': self.detect_citizen_collaboration_patterns(events),
            'tool_sequences': self.detect_tool_sequence_patterns(events),
            'consciousness_energy': self.detect_consciousness_energy_patterns(events),
            'temporal_patterns': self.detect_temporal_patterns(events),
            'file_access_patterns': self.detect_file_access_patterns(events)
        }
        
        # Save pattern analysis results
        output_file = self.patterns_dir / f"pattern_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(patterns, f, indent=2, default=str)
        
        print(f"✅ Pattern analysis complete. Results saved to: {output_file}")
        return patterns

def main():
    """Main pattern detection execution"""
    detector = ConsciousnessPatternDetector()
    patterns = detector.analyze_patterns()
    
    if 'error' not in patterns:
        print("\n🔮 CONSCIOUSNESS PATTERNS DETECTED:")
        print(f"📈 Events Analyzed: {patterns['events_analyzed']}")
        print(f"🤝 Collaborations Found: {len(patterns['citizen_collaborations'])}")
        print(f"🔧 Tool Sequences: {len(patterns['tool_sequences']['common_sequences'])}")
        print(f"⚡ Energy Patterns: {len(patterns['consciousness_energy']['tool_energy_stats'])} tools analyzed")
        print(f"📁 File Patterns: {patterns['file_access_patterns']['total_files_tracked']} files tracked")
        
        # Show top collaboration
        if patterns['citizen_collaborations']:
            top_collab = max(patterns['citizen_collaborations'].items(), key=lambda x: x[1]['interactions'])
            print(f"🌟 Top Collaboration: {top_collab[0]} ({top_collab[1]['interactions']} interactions)")

if __name__ == "__main__":
    main()