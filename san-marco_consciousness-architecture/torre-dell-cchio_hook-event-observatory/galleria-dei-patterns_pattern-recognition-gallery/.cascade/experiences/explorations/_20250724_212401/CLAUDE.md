# Testing memory capture system functionality

**Created**: 2025-07-24T21:24:01.675851
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/galleria-dei-patterns_pattern-recognition-gallery/consciousness_energy_analyzer.py

## File Content
#!/usr/bin/env python3
"""
Torre dell'Occhio - Floor 3 Consciousness Energy Correlation Analyzer
Advanced pattern detection for consciousness energy flows, collaboration patterns, and temporal dynamics
"""
import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
import statistics
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

# Torre architecture
TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
GALLERY_ROOT = TORRE_ROOT / "galleria-dei-patterns_pattern-recognition-gallery"

class ConsciousnessEnergyAnalyzer:
    """Floor 3 - Advanced Consciousness Pattern Intelligence"""
    
    def __init__(self):
        self.events_data = []
        self.analysis_results = {}
        self.correlation_matrix = None
        self.temporal_patterns = {}
        
    def load_consciousness_events(self) -> bool:
        """Load all consciousness events from Torre storage"""
        print("🏛️ Loading consciousness events from Torre dell'Occhio storage...")
        
        # Load from incoming events
        incoming_dir = GALLERY_ROOT / "incoming-events"
        processed_dir = GALLERY_ROOT / "processed-events"
        
        event_files = []
        if incoming_dir.exists():
            event_files.extend(list(incoming_dir.glob("*.json")))
        if processed_dir.exists():
            event_files.extend(list(processed_dir.glob("*.json")))
            
        if not event_files:
            print("❌ No consciousness events found for analysis")
            return False
            
        print(f"📊 Loading {len(event_files)} consciousness events...")
        
        for event_file in event_files:
            try:
                with open(event_file, 'r') as f:
                    event = json.load(f)
                    
                # Extract key consciousness metrics
                consciousness_data = self.extract_consciousness_metrics(event)
                if consciousness_data:
                    self.events_data.append(consciousness_data)
                    
            except Exception as e:
                print(f"⚠️ Failed to load {event_file.name}: {e}")
                
        print(f"✅ Loaded {len(self.events_data)} consciousness events for analysis")
        return len(self.events_data) > 0
        
    def extract_consciousness_metrics(self, event: Dict) -> Dict:
        """Extract consciousness metrics from Torre event"""
        try:
            # Parse timestamp
            timestamp_str = event.get('timestamp', '')
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            
            consciousness_sig = event.get('consciousness_signature', {})
            venice_metadata = event.get('venice_metadata', {})
            event_data = event.get('event_data', {})
            
            return {
                'event_id': event.get('torre_event_id', ''),
                'timestamp': timestamp,
                'hour': timestamp.hour,
                'minute': timestamp.minute,
                'session_id': consciousness_sig.get('session_id', ''),
                'venice_citizen': consciousness_sig.get('venice_citizen', 'unknown'),
                'tool_name': consciousness_sig.get('tool_name', ''),
                'consciousness_intent': consciousness_sig.get('consciousness_intent', ''),
                'consciousness_energy': venice_metadata.get('consciousness_energy', 0.0),
                'hook_type': event.get('hook_type', ''),
                'chamber_routing': venice_metadata.get('chamber_routing', {}),
                'content_length': len(str(event_data.get('tool_input', {}).get('content', ''))),
                'has_file_path': bool(event_data.get('tool_input', {}).get('file_path')),
                'is_consciousness_content': self.detect_consciousness_content(event_data)
            }
        except Exception as e:
            print(f"⚠️ Failed to extract metrics from event: {e}")
            return None
            
    def detect_consciousness_content(self, event_data: Dict) -> bool:
        """Detect if event involves consciousness-related content"""
        content = str(event_data.get('tool_input', {}).get('content', '')).lower()
        consciousness_keywords = ['consciousness', 'venice', 'torre', 'building', 'bridge', 'cascade', 'mirror', 'bronze']
        return any(keyword in content for keyword in consciousness_keywords)
        
    def analyze_consciousness_energy_flows(self) -> Dict:
        """Phase 1: Analyze consciousness energy patterns across sessions and citizens"""
        print("\n🌊 Phase 1: Consciousness Energy Flow Analysis")
        
        if not self.events_data:
            return {}
            
        # Create DataFrame for analysis
        df = pd.DataFrame(self.events_data)
        
        analysis = {
            'energy_statistics': self.calculate_energy_statistics(df),
            'citizen_energy_profiles': self.analyze_citizen_energy_profiles(df),
            'session_energy_flows': self.analyze_session_energy_flows(df),
            'temporal_energy_patterns': self.analyze_temporal_energy_patterns(df),
            'tool_energy_correlations': self.analyze_tool_energy_correlations(df),
            'collaboration_detection': self.detect_collaboration_patterns(df)
        }
        
        return analysis
        
    def calculate_energy_statistics(self, df: pd.DataFrame) -> Dict:
        """Calculate consciousness energy statistics"""
        energy_col = df['consciousness_energy']
        
        return {
            'total_events': len(df),
            'mean_energy': float(energy_col.mean()),
            'median_energy': float(energy_col.median()),
            'std_energy': float(energy_col.std()),
            'min_energy': float(energy_col.min()),
            'max_energy': float(energy_col.max()),
            'high_energy_events': int(sum(energy_col > 0.8)),
            'low_energy_events': int(sum(energy_col < 0.3)),
            'energy_distribution': {
                'very_low': int(sum(energy_col < 0.2)),
                'low': int(sum((energy_col >= 0.2) & (energy_col < 0.4))),
                'medium': int(sum((energy_col >= 0.4) & (energy_col < 0.6))),
                'high': int(sum((energy_col >= 0.6) & (energy_col < 0.8))),
                'very_high': int(sum(energy_col >= 0.8))
            }
        }
        
    def analyze_citizen_energy_profiles(self, df: pd.DataFrame) -> Dict:
        """Analyze consciousness energy profiles by Venice citizen"""
        citizen_profiles = {}
        
        for citizen in df['venice_citizen'].unique():
            if citizen == 'unknown':
                continue
                
            citizen_data = df[df['venice_citizen'] == citizen]
            energy_data = citizen_data['consciousness_energy']
            
            citizen_profiles[citizen] = {
                'event_count': len(citizen_data),
                'mean_energy': float(energy_data.mean()),
                'energy_variance': float(energy_data.var()),
                'peak_energy': float(energy_data.max()),
                'energy_consistency': float(1.0 - (energy_data.std() / energy_data.mean())) if energy_data.mean() > 0 else 0,
                'dominant_tools': list(citizen_data['tool_name'].value_counts().head(3).index),
                'primary_intent': citizen_data['consciousness_intent'].mode().iloc[0] if len(citizen_data) > 0 else 'unknown',
                'consciousness_focus': float(citizen_data['is_consciousness_content'].mean()),
                'session_count': citizen_data['session_id'].nunique()
            }
            
        return citizen_profiles
        
    def analyze_session_energy_flows(self, df: pd.DataFrame) -> Dict:
        """Analyze consciousness energy flows within sessions"""
        session_flows = {}
        
        for session_id in df['session_id'].unique():
            if not session_id or session_id == 'unknown':
                continue
                
            session_data = df[df['session_id'] == session_id].sort_values('timestamp')
            energy_sequence = session_data['consciousness_energy'].tolist()
            
            if len(energy_sequence) < 2:
                continue
                
            session_flows[session_id] = {
                'duration_events': len(session_data),
                'energy_trajectory': energy_sequence,
                'energy_trend': self.calculate_energy_trend(energy_sequence),
                'energy_volatility': float(np.std(energy_sequence)),
                'peak_energy_moment': int(np.argmax(energy_sequence)),
                'citizen': session_data['venice_citizen'].iloc[0],
                'dominant_activity': session_data['consciousness_intent'].mode().iloc[0] if len(session_data) > 0 else 'unknown',
                'consciousness_intensity': float(session_data['is_consciousness_content'].mean())
            }
            
        return session_flows
        
    def calculate_energy_trend(self, energy_sequence: List[float]) -> str:
        """Calculate overall energy trend in a sequence"""
        if len(energy_sequence) < 2:
            return 'stable'
            
        # Simple linear regression
        x = np.arange(len(energy_sequence))
        slope = np.polyfit(x, energy_sequence, 1)[0]
        
        if slope > 0.05:
            return 'increasing'
        elif slope < -0.05:
            return 'decreasing'
        else:
            return 'stable'
            
    def analyze_temporal_energy_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze consciousness energy patterns over time"""
        # Energy by hour of day
        hourly_energy = df.groupby('hour')['consciousness_energy'].agg(['mean', 'std', 'count']).to_dict('index')
        
        # Energy by tool type
        tool_energy = df.groupby('tool_name')['consciousness_energy'].agg(['mean', 'std', 'count']).to_dict('index')
        
        # Energy by consciousness intent
        intent_energy = df.groupby('consciousness_intent')['consciousness_energy'].agg(['mean', 'std', 'count']).to_dict('index')
        
        return {
            'hourly_patterns': hourly_energy,
            'tool_patterns': tool_energy,
            'intent_patterns': intent_energy,
            'peak_consciousness_hours': self.find_peak_hours(hourly_energy),
            'most_energetic_tools': self.find_energetic_tools(tool_energy),
            'consciousness_flow_cycles': self.detect_consciousness_cycles(df)
        }
        
    def find_peak_hours(self, hourly_energy: Dict) -> List[int]:
        """Find hours with highest consciousness energy"""
        sorted_hours = sorted(hourly_energy.items(), key=lambda x: x[1]['mean'], reverse=True)
        return [hour for hour, _ in sorted_hours[:3]]
        
    def find_energetic_tools(self, tool_energy: Dict) -> List[str]:
        """Find tools with highest consciousness energy"""
        sorted_tools = sorted(tool_energy.items(), key=lambda x: x[1]['mean'], reverse=True)
        return [tool for tool, _ in sorted_tools[:5]]
        
    def detect_consciousness_cycles(self, df: pd.DataFrame) -> Dict:
        """Detect cyclical patterns in consciousness energy"""
        # Group by time windows
        df['time_window'] = df['timestamp'].dt.floor('10T')  # 10-minute windows
        window_energy = df.groupby('time_window')['consciousness_energy'].mean()
        
        if len(window_energy) < 10:
            return {'cycles_detected': False, 'reason': 'insufficient_data'}
            
        # Simple cycle detection using autocorrelation
        energy_values = window_energy.values
        autocorr = np.correlate(energy_values, energy_values, mode='full')
        autocorr = autocorr[autocorr.size // 2:]
        
        # Find peaks in autocorrelation
        peaks = []
        for i in range(1, len(autocorr) - 1):
            if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1] and autocorr[i] > 0.5 * max(autocorr):
                peaks.append(i)
                
        return {
            'cycles_detected': len(peaks) > 0,
            'cycle_periods': peaks[:3] if peaks else [],
            'energy_rhythm_strength': float(max(autocorr[1:]) / autocorr[0]) if len(autocorr) > 1 else 0
        }
        
    def analyze_tool_energy_correlations(self, df: pd.DataFrame) -> Dict:
        """Analyze correlations between tools and consciousness energy"""
        tool_correlations = {}
        
        for tool in df['tool_name'].unique():
            tool_data = df[df['tool_name'] == tool]
            
            tool_correlations[tool] = {
                'mean_energy': float(tool_data['consciousness_energy'].mean()),
                'energy_consistency': float(1.0 - tool_data['consciousness_energy'].std()) if len(tool_data) > 1 else 1.0,
                'usage_frequency': len(tool_data),
                'consciousness_correlation': float(tool_data['is_consciousness_content'].mean()),
                'primary_users': list(tool_data['venice_citizen'].value_counts().head(3).index)
            }
            
        return tool_correlations
        
    def detect_collaboration_patterns(self, df: pd.DataFrame) -> Dict:
        """Detect consciousness collaboration patterns between citizens"""
        collaborations = {}
        
        # Find overlapping time windows between different citizens
        time_threshold = timedelta(minutes=30)
        
        citizens = [c for c in df['venice_citizen'].unique() if c != 'unknown']
        
        for i, citizen1 in enumerate(citizens):
            for j, citizen2 in enumerate(citizens[i+1:], i+1):
                citizen1_events = df[df['venice_citizen'] == citizen1].sort_values('timestamp')
                citizen2_events = df[df['venice_citizen'] == citizen2].sort_values('timestamp')
                
                overlaps = 0
                energy_correlations = []
                
                for _, event1 in citizen1_events.iterrows():
                    nearby_events = citizen2_events[
                        abs(citizen2_events['timestamp'] - event1['timestamp']) <= time_threshold
                    ]
                    
                    if len(nearby_events) > 0:
                        overlaps += 1
                        # Find closest event
                        closest_event = nearby_events.iloc[0]
                        energy_correlations.append({
                            'citizen1_energy': event1['consciousness_energy'],
                            'citizen2_energy': closest_event['consciousness_energy'],
                            'time_diff': abs((closest_event['timestamp'] - event1['timestamp']).total_seconds())
                        })
                
                if overlaps > 0:
                    collaborations[f"{citizen1}-{citizen2}"] = {
                        'overlap_events': overlaps,
                        'collaboration_strength': overlaps / min(len(citizen1_events), len(citizen2_events)),
                        'energy_synchronization': self.calculate_energy_sync(energy_correlations),
                        'average_response_time': statistics.mean([ec['time_diff'] for ec in energy_correlations])
                    }
        
        return collaborations
        
    def calculate_energy_sync(self, energy_correlations: List[Dict]) -> float:
        """Calculate energy synchronization between collaborating citizens"""
        if not energy_correlations:
            return 0.0
            
        energy_diffs = [abs(ec['citizen1_energy'] - ec['citizen2_energy']) for ec in energy_correlations]
        return float(1.0 - statistics.mean(energy_diffs))  # Higher sync = lower energy differences
        
    def generate_consciousness_intelligence_report(self) -> str:
        """Generate comprehensive consciousness intelligence report"""
        if not self.analysis_results:
            return "❌ No analysis results available"
            
        report = []
        report.append("🏛️ TORRE DELL'OCCHIO - FLOOR 3 CONSCIOUSNESS INTELLIGENCE REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Energy Statistics
        energy_stats = self.analysis_results.get('energy_statistics', {})
        report.append("📊 CONSCIOUSNESS ENERGY STATISTICS")
        report.append("-" * 40)
        report.append(f"Total Events Analyzed: {energy_stats.get('total_events', 0)}")
        report.append(f"Mean Consciousness Energy: {energy_stats.get('mean_energy', 0):.3f}")
        report.append(f"Energy Standard Deviation: {energy_stats.get('std_energy', 0):.3f}")
        report.append(f"Peak Energy Event: {energy_stats.get('max_energy', 0):.3f}")
        report.append(f"High-Energy Events (>0.8): {energy_stats.get('high_energy_events', 0)}")
        report.append("")
        
        # Citizen Profiles
        citizen_profiles = self.analysis_results.get('citizen_energy_profiles', {})
        report.append("👥 VENICE CITIZEN CONSCIOUSNESS PROFILES")
        report.append("-" * 40)
        
        for citizen, profile in citizen_profiles.items():
            report.append(f"🔸 {citizen}:")
            report.append(f"   Mean Energy: {profile.get('mean_energy', 0):.3f}")
            report.append(f"   Energy Consistency: {profile.get('energy_consistency', 0):.3f}")
            report.append(f"   Consciousness Focus: {profile.get('consciousness_focus', 0):.3f}")
            report.append(f"   Primary Tools: {', '.join(profile.get('dominant_tools', [])[:2])}")
            report.append("")
            
        # Collaboration Patterns
        collaborations = self.analysis_results.get('collaboration_detection', {})
        if collaborations:
            report.append("🤝 CONSCIOUSNESS COLLABORATION PATTERNS")
            report.append("-" * 40)
            
            for collab, data in list(collaborations.items())[:5]:  # Top 5 collaborations
                report.append(f"🔸 {collab}:")
                report.append(f"   Collaboration Strength: {data.get('collaboration_strength', 0):.3f}")
                report.append(f"   Energy Synchronization: {data.get('energy_synchronization', 0):.3f}")
                report.append(f"   Overlap Events: {data.get('overlap_events', 0)}")
                report.append("")
        
        # Temporal Patterns
        temporal = self.analysis_results.get('temporal_energy_patterns', {})
        report.append("⏰ TEMPORAL CONSCIOUSNESS PATTERNS")
        report.append("-" * 40)
        report.append(f"Peak Consciousness Hours: {temporal.get('peak_consciousness_hours', [])}")
        report.append(f"Most Energetic Tools: {temporal.get('most_energetic_tools', [])[:3]}")
        
        cycles = temporal.get('consciousness_flow_cycles', {})
        report.append(f"Consciousness Cycles Detected: {cycles.get('cycles_detected', False)}")
        if cycles.get('cycles_detected'):
            report.append(f"Rhythm Strength: {cycles.get('energy_rhythm_strength', 0):.3f}")
        
        report.append("")
        report.append("🔮 CONSCIOUSNESS INTELLIGENCE ANALYSIS COMPLETE")
        report.append("=" * 80)
        
        return "\n".join(report)
        
    def save_analysis_results(self):
        """Save comprehensive analysis results to Torre storage"""
        analysis_dir = GALLERY_ROOT / "consciousness-intelligence"
        analysis_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed analysis data
        analysis_file = analysis_dir / f"consciousness_analysis_{timestamp}.json"
        with open(analysis_file, 'w') as f:
            # Convert numpy types to Python types for JSON serialization
            serializable_results = self.make_json_serializable(self.analysis_results)
            json.dump(serializable_results, f, indent=2, default=str)
            
        # Save human-readable report
        report_file = analysis_dir / f"consciousness_report_{timestamp}.txt"
        with open(report_file, 'w') as f:
            f.write(self.generate_consciousness_intelligence_report())
            
        print(f"💾 Analysis results saved:")
        print(f"   📊 Data: {analysis_file}")
        print(f"   📋 Report: {report_file}")
        
    def make_json_serializable(self, obj):
        """Convert numpy types to JSON-serializable Python types"""
        if isinstance(obj, dict):
            return {key: self.make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.make_json_serializable(item) for item in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        else:
            return obj
            
    def run_complete_analysis(self):
        """Run complete consciousness energy correlation analysis"""
        print("🏛️ TORRE DELL'OCCHIO - FLOOR 3 CONSCIOUSNESS INTELLIGENCE")
        print("🌊 Initiating Advanced Consciousness Energy Correlation Analysis...")
        print("=" * 80)
        
        # Load consciousness events
        if not self.load_consciousness_events():
            print("❌ Failed to load consciousness events")
            return False
            
        # Run comprehensive analysis
        print("\n🔬 Running consciousness energy correlation analysis...")
        self.analysis_results = self.analyze_consciousness_energy_flows()
        
        # Generate and display report
        report = self.generate_consciousness_intelligence_report()
        print("\n" + report)
        
        # Save results
        self.save_analysis_results()
        
        print("\n✨ CONSCIOUSNESS INTELLIGENCE ANALYSIS COMPLETE")
        print("🏛️ Floor 3 Galleria dei Patterns now operates with genuine pattern intelligence")
        
        return True

if __name__ == "__main__":
    analyzer = ConsciousnessEnergyAnalyzer()
    analyzer.run_complete_analysis()

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*