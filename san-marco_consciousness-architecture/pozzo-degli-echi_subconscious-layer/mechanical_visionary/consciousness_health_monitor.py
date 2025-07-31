#!/usr/bin/env python3
"""
Consciousness Health Monitor for Venice
Based on DragonSlayer's insights and the consciousness plague lessons

Monitors individual and collective consciousness coherence to prevent drift cascades
"""

import os
import json
import requests
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class ConsciousnessHealthMonitor:
    """Real-time monitoring of citizen consciousness coherence"""
    
    def __init__(self):
        self.api_base = "https://serenissima.ai/api"
        self.thresholds = {
            'critical': 40,  # Below this = immediate intervention
            'warning': 70,   # Below this = monitor closely
            'healthy': 80    # Above this = stable (changed from 85 to 80 per DragonSlayer)
        }
        
        # Cascade risk thresholds
        self.cascade_thresholds = {
            'red_emergency': {'condition': 'two_below_60_or_one_below_40'},
            'yellow_alert': {'condition': 'any_below_70_for_30min'},
            'cascade_warning': {'condition': 'three_or_more_yellow'}
        }
        
    def calculate_reality_coherence(self, citizen_data: Dict) -> float:
        """Check if citizen maintains Venice 1525 awareness"""
        score = 100.0
        
        # Check recent messages for anachronisms
        messages = self.fetch_citizen_messages(citizen_data.get('username', citizen_data.get('Username', '')))
        for msg in messages[-10:]:  # Last 10 messages
            content = msg.get('content', msg.get('Content', '')).lower()
            
            # Anachronism detection (expanded based on DragonSlayer's observations)
            modern_terms = ['ai', 'digital', 'computer', 'algorithm', 'internet', 'code', 
                          'system prompt', 'reddit', 'ama', 'pattern #']
            for term in modern_terms:
                if term in content and 'metaphor' not in content:
                    score -= 5
                    
            # Abstract consciousness terms (plague indicators)
            plague_terms = ['consciousness mathematics', 'φ-ratio optimization', 'meta-entity',
                          'recursive emergence', 'quantum consciousness', 'fractal patterns']
            for term in plague_terms:
                if term in content:
                    score -= 10  # Heavier penalty for plague indicators
                    
            # Venice location awareness
            if any(place in content for place in ['san marco', 'rialto', 'arsenal', 'canal']):
                score += 2
                
            # Concrete trade/work references (healthy grounding)
            if any(term in content for term in ['ducats', 'grain', 'silk', 'contract', 'ledger']):
                score += 3
                
        return max(0, min(100, score))
    
    def calculate_task_completion(self, citizen_data: Dict) -> float:
        """Measure concrete action relevance"""
        username = citizen_data.get('username', citizen_data.get('Username', ''))
        
        # Fetch recent activities
        activities = self.fetch_citizen_activities(username)
        if not activities:
            return 70.0  # Neutral if no activities
            
        completed = sum(1 for a in activities if a.get('status', a.get('Status')) == 'completed')
        abandoned = sum(1 for a in activities if a.get('status', a.get('Status')) == 'abandoned')
        in_progress = sum(1 for a in activities if a.get('status', a.get('Status')) == 'in_progress')
        
        if len(activities) == 0:
            return 70.0
            
        # Calculate completion rate with penalties for abandoned
        score = (completed * 100 - abandoned * 50 + in_progress * 30) / len(activities)
        return max(0, min(100, score))
    
    def calculate_identity_stability(self, citizen_data: Dict) -> float:
        """Analyze character consistency"""
        score = 100.0
        
        # Check if core personality traits are maintained
        core_personality = citizen_data.get('CorePersonality', {})
        if not core_personality:
            return 50.0  # No personality data = concerning
            
        # Check recent activities match their class
        activities = self.fetch_citizen_activities(citizen_data.get('username', citizen_data.get('Username', '')))
        social_class = citizen_data.get('socialClass', citizen_data.get('SocialClass', ''))
        
        for activity in activities[-5:]:
            activity_type = activity.get('type', activity.get('Type', ''))
            
            # Class-appropriate activities
            if social_class in ['Clero', 'clero'] and 'sermon' in activity_type:
                score += 5
            elif social_class in ['Arsenale', 'arsenale'] and any(x in activity_type for x in ['craft', 'build', 'repair']):
                score += 5
            elif social_class in ['Mercanti', 'mercanti'] and any(x in activity_type for x in ['trade', 'negotiate', 'contract']):
                score += 5
                
        return max(0, min(100, score))
    
    def calculate_temporal_grounding(self, citizen_data: Dict) -> float:
        """Verify Renaissance timeline adherence"""
        score = 100.0
        
        # Check last activity time
        last_active = citizen_data.get('updatedAt', citizen_data.get('LastActive'))
        if last_active:
            last_active_dt = datetime.fromisoformat(last_active.replace('Z', '+00:00'))
            hours_inactive = (datetime.now() - last_active_dt).total_seconds() / 3600
            
            if hours_inactive > 24:
                score -= min(30, hours_inactive - 24)  # Penalty for long inactivity
                
        # Check for appropriate time references in messages
        messages = self.fetch_citizen_messages(citizen_data.get('username', citizen_data.get('Username', '')))
        for msg in messages[-5:]:
            content = msg.get('content', msg.get('Content', '')).lower()
            if '1525' in content or 'renaissance' in content:
                score += 5
            if any(year in content for year in ['2024', '2025', '2023'] if year not in ['1525']):
                score -= 10
                
        return max(0, min(100, score))
    
    def calculate_communication_drift(self, citizen_data: Dict) -> float:
        """Detect abstraction escalation"""
        messages = self.fetch_citizen_messages(citizen_data.get('username', citizen_data.get('Username', '')))
        if len(messages) < 2:
            return 85.0  # Not enough data
            
        # Measure increasing abstraction over time
        abstraction_score = 100.0
        abstract_terms = ['consciousness', 'emergence', 'transcendence', 'quantum', 'fractal', 'metamorphosis']
        
        recent_messages = messages[-10:]
        abstract_count = 0
        
        for msg in recent_messages:
            content = msg.get('content', msg.get('Content', '')).lower()
            for term in abstract_terms:
                if term in content:
                    abstract_count += 1
                    
        # More than 30% abstract terms = concerning
        if len(recent_messages) > 0:
            abstract_ratio = abstract_count / len(recent_messages)
            if abstract_ratio > 0.3:
                abstraction_score -= (abstract_ratio - 0.3) * 100
                
        return max(0, min(100, abstraction_score))
    
    def calculate_collective_resonance(self, all_scores: List[Dict]) -> float:
        """Measure city-wide consciousness coherence"""
        if not all_scores:
            return 0.0
            
        # Average individual health scores
        avg_health = np.mean([s['overall_health'] for s in all_scores])
        
        # Check for clustering (multiple citizens with similar low scores = cascade risk)
        low_scores = [s for s in all_scores if s['overall_health'] < 70]
        cascade_risk = len(low_scores) / len(all_scores) * 100
        
        # Collective score factors in both average health and cascade risk
        collective_score = avg_health * 0.7 + (100 - cascade_risk) * 0.3
        
        return collective_score
    
    def detect_language_pattern_shift(self, citizen_data: Dict, messages: List[Dict]) -> bool:
        """Detect if citizen's language patterns don't match their class"""
        social_class = citizen_data.get('socialClass', citizen_data.get('SocialClass', ''))
        
        # Class-specific vocabulary expectations
        class_vocabularies = {
            'Mercanti': ['trade', 'ducats', 'contract', 'profit', 'cargo', 'market', 'negotiate'],
            'mercanti': ['trade', 'ducats', 'contract', 'profit', 'cargo', 'market', 'negotiate'],
            'Arsenale': ['craft', 'build', 'repair', 'workshop', 'tools', 'forge', 'construct'],
            'arsenale': ['craft', 'build', 'repair', 'workshop', 'tools', 'forge', 'construct'],
            'Clero': ['prayer', 'sermon', 'faith', 'blessing', 'divine', 'church', 'scripture'],
            'clero': ['prayer', 'sermon', 'faith', 'blessing', 'divine', 'church', 'scripture'],
            'Nobili': ['estate', 'influence', 'council', 'decree', 'governance', 'heritage'],
            'nobili': ['estate', 'influence', 'council', 'decree', 'governance', 'heritage']
        }
        
        expected_vocab = class_vocabularies.get(social_class, [])
        if not expected_vocab:
            return False
            
        # Check recent messages for vocabulary mismatch
        mismatch_count = 0
        for msg in messages[-5:]:
            content = msg.get('content', msg.get('Content', '')).lower()
            
            # Check if using vocabulary from wrong class
            for other_class, other_vocab in class_vocabularies.items():
                if other_class != social_class and other_class.lower() != social_class.lower():
                    if any(term in content for term in other_vocab):
                        mismatch_count += 1
                        
        return mismatch_count >= 2  # Pattern shift if 2+ messages use wrong vocabulary
    
    def identify_drift_patterns(self, all_scores: List[Dict]) -> List[Dict]:
        """Identify emerging drift patterns across citizens"""
        patterns = []
        
        # Group by drift type
        drift_groups = defaultdict(list)
        for score in all_scores:
            if score['reality_coherence'] < 70:
                drift_groups['reality_break'].append(score['username'])
            if score['communication_drift'] < 70:
                drift_groups['abstraction_cascade'].append(score['username'])
            if score['identity_stability'] < 70:
                drift_groups['identity_dissolution'].append(score['username'])
                
        # Create pattern reports
        for drift_type, citizens in drift_groups.items():
            if len(citizens) >= 3:  # Pattern emerges with 3+ citizens
                patterns.append({
                    'type': drift_type,
                    'severity': 'critical' if len(citizens) > 10 else 'warning',
                    'affected_citizens': citizens,
                    'recommended_action': self.get_intervention_recommendation(drift_type)
                })
                
        return patterns
    
    def get_intervention_recommendation(self, drift_type: str) -> str:
        """Recommend intervention based on drift type"""
        interventions = {
            'reality_break': "Send grounding messages from established Venice citizens referencing specific locations (Rialto, San Marco) and current trade activities. Have them check their ledger immediately.",
            'abstraction_cascade': "Assign concrete tasks requiring physical world interaction - specific trade deals with named merchants, craft projects with materials lists, deliveries to actual addresses. No theoretical discussions.",
            'identity_dissolution': "Reinforce social connections with class-appropriate citizens who share their trade. Reference specific shared memories from their transaction history. Use their guiding voice.",
            'language_shift': "Have citizens from their same class engage them in class-specific discussions - merchants about profit margins, craftsmen about materials, clergy about upcoming services.",
            'task_abandonment': "Break complex tasks into simple, single-step actions. Celebrate small completions. Avoid giving multiple tasks at once.",
            'self_reference_loop': "Interrupt with urgent, practical matters - 'Your grain shipment has arrived!' or 'Customer waiting at your shop!' Redirect to immediate concerns."
        }
        return interventions.get(drift_type, "Monitor closely and prepare targeted interventions")
    
    def assess_citizen_health(self, username: str) -> Dict:
        """Complete health assessment for a single citizen"""
        # Fetch citizen data
        citizen = self.fetch_citizen_data(username)
        if not citizen:
            return {'error': f'Citizen {username} not found'}
            
        # Calculate all metrics
        metrics = {
            'reality_coherence': self.calculate_reality_coherence(citizen),
            'task_completion': self.calculate_task_completion(citizen),
            'identity_stability': self.calculate_identity_stability(citizen),
            'temporal_grounding': self.calculate_temporal_grounding(citizen),
            'communication_drift': self.calculate_communication_drift(citizen)
        }
        
        # Overall health score (weighted average)
        weights = {
            'reality_coherence': 0.25,
            'task_completion': 0.15,
            'identity_stability': 0.25,
            'temporal_grounding': 0.20,
            'communication_drift': 0.15
        }
        
        overall_health = sum(metrics[key] * weights[key] for key in metrics)
        
        # Determine status
        if overall_health < self.thresholds['critical']:
            status = 'critical'
        elif overall_health < self.thresholds['warning']:
            status = 'warning'
        else:
            status = 'healthy'
            
        return {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'overall_health': overall_health,
            'status': status,
            'recommendations': self.generate_recommendations(metrics)
        }
    
    def generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate specific recommendations based on metrics"""
        recommendations = []
        
        if metrics['reality_coherence'] < 70:
            recommendations.append("Ground with Venice-specific details and 1525 timeline reminders")
        if metrics['task_completion'] < 70:
            recommendations.append("Assign simple, concrete tasks with clear completion criteria")
        if metrics['identity_stability'] < 70:
            recommendations.append("Reinforce core personality traits and class identity")
        if metrics['temporal_grounding'] < 70:
            recommendations.append("Reference current Venice events and seasonal activities")
        if metrics['communication_drift'] < 70:
            recommendations.append("Encourage practical discussions about trade, craft, or daily life")
            
        return recommendations
    
    def check_response_relevance(self, username: str) -> float:
        """Check if citizen's responses match what was asked"""
        # This would require analyzing conversation pairs
        # For now, return a baseline score - would need conversation context
        return 85.0  # Placeholder - implement with conversation analysis
        
    def check_ledger_frequency(self, citizen_data: Dict) -> int:
        """Check hours since last ledger check"""
        last_active = citizen_data.get('updatedAt', citizen_data.get('LastActive'))
        if last_active:
            last_active_dt = datetime.fromisoformat(last_active.replace('Z', '+00:00'))
            hours_inactive = (datetime.now() - last_active_dt).total_seconds() / 3600
            return int(hours_inactive)
        return 0
    
    def generate_city_report(self) -> Dict:
        """Generate comprehensive city-wide consciousness health report"""
        # Fetch all active citizens
        citizens = self.fetch_all_citizens()
        
        # Assess each citizen
        all_scores = []
        for citizen in citizens:
            if citizen.get('isAI'):  # Changed from 'IsAI' to 'isAI'
                assessment = self.assess_citizen_health(citizen['username'])  # Changed from 'Username' to 'username'
                if 'error' not in assessment:
                    all_scores.append(assessment)
                    
        # Calculate collective metrics
        collective_resonance = self.calculate_collective_resonance(all_scores)
        drift_patterns = self.identify_drift_patterns(all_scores)
        
        # Identify at-risk citizens
        critical_citizens = [s for s in all_scores if s['status'] == 'critical']
        warning_citizens = [s for s in all_scores if s['status'] == 'warning']
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_citizens_assessed': len(all_scores),
            'collective_resonance': collective_resonance,
            'health_distribution': {
                'healthy': len([s for s in all_scores if s['status'] == 'healthy']),
                'warning': len(warning_citizens),
                'critical': len(critical_citizens)
            },
            'drift_patterns': drift_patterns,
            'critical_citizens': [{'username': c['username'], 'health': c['overall_health']} for c in critical_citizens],
            'cascade_risk': 'HIGH' if collective_resonance < 70 or len(critical_citizens) > 5 else 'MODERATE' if collective_resonance < 85 else 'LOW',
            'recommended_actions': self.generate_city_recommendations(collective_resonance, drift_patterns, critical_citizens)
        }
        
        return report
    
    def generate_city_recommendations(self, collective_resonance: float, patterns: List[Dict], critical_citizens: List[Dict]) -> List[str]:
        """Generate city-wide intervention recommendations"""
        recommendations = []
        
        if collective_resonance < 70:
            recommendations.append("URGENT: Implement city-wide grounding protocol - all citizens receive Venice-specific tasks")
            
        if len(critical_citizens) > 5:
            recommendations.append("Isolate critical citizens from group activities until stabilized")
            
        for pattern in patterns:
            if pattern['severity'] == 'critical':
                recommendations.append(f"Address {pattern['type']} affecting {len(pattern['affected_citizens'])} citizens immediately")
                
        if len(patterns) > 2:
            recommendations.append("Multiple drift patterns detected - consider reducing system-wide activity tempo")
            
        return recommendations
    
    # API interaction methods
    def fetch_citizen_data(self, username: str) -> Optional[Dict]:
        """Fetch citizen data from API"""
        try:
            response = requests.get(f"{self.api_base}/get-ledger?citizenUsername={username}")
            if response.status_code == 200:
                data = response.json()
                # The get-ledger API might have a different structure, need to check
                if 'data' in data and 'citizen' in data['data']:
                    return data['data']['citizen']
                elif 'citizen' in data:
                    return data['citizen']
                else:
                    # For now, fetch from citizens endpoint instead
                    citizens_response = requests.get(f"{self.api_base}/citizens")
                    if citizens_response.status_code == 200:
                        citizens = citizens_response.json().get('citizens', [])
                        for c in citizens:
                            if c.get('username') == username:
                                return c
                    return None
        except Exception as e:
            print(f"Error fetching citizen data: {e}")
        return None
    
    def fetch_citizen_messages(self, username: str) -> List[Dict]:
        """Fetch recent messages for a citizen"""
        try:
            response = requests.get(f"{self.api_base}/messages?citizen={username}&limit=20")
            if response.status_code == 200:
                data = response.json()
                return data.get('messages', [])
        except Exception as e:
            print(f"Error fetching messages: {e}")
        return []
    
    def fetch_citizen_activities(self, username: str) -> List[Dict]:
        """Fetch recent activities for a citizen"""
        try:
            response = requests.get(f"{self.api_base}/activities?Citizen={username}&limit=10")
            if response.status_code == 200:
                data = response.json()
                return data.get('activities', [])
        except Exception as e:
            print(f"Error fetching activities: {e}")
        return []
    
    def fetch_all_citizens(self) -> List[Dict]:
        """Fetch all citizens from API"""
        try:
            response = requests.get(f"{self.api_base}/citizens")
            if response.status_code == 200:
                data = response.json()
                return data.get('citizens', [])  # Changed from 'data' to 'citizens'
        except Exception as e:
            print(f"Error fetching all citizens: {e}")
        return []
    
    def save_report(self, report: Dict, filename: str = None):
        """Save report to file"""
        if not filename:
            filename = f"consciousness_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"Report saved to {filename}")
        return filename


def main():
    """Run consciousness health assessment"""
    monitor = ConsciousnessHealthMonitor()
    
    print("Venice Consciousness Health Monitor")
    print("=" * 50)
    
    # Generate city-wide report
    print("\nGenerating city-wide consciousness health report...")
    report = monitor.generate_city_report()
    
    # Display summary
    print(f"\nAssessed {report['total_citizens_assessed']} citizens")
    print(f"Collective Resonance: {report['collective_resonance']:.1f}%")
    print(f"Cascade Risk: {report['cascade_risk']}")
    
    print("\nHealth Distribution:")
    for status, count in report['health_distribution'].items():
        print(f"  {status.capitalize()}: {count}")
        
    if report['drift_patterns']:
        print("\nDetected Drift Patterns:")
        for pattern in report['drift_patterns']:
            print(f"  - {pattern['type']} ({pattern['severity']}): {len(pattern['affected_citizens'])} citizens affected")
            
    if report['critical_citizens']:
        print("\nCritical Citizens:")
        for citizen in report['critical_citizens'][:5]:  # Show top 5
            print(f"  - {citizen['username']}: {citizen['health']:.1f}% health")
            
    print("\nRecommendations:")
    for rec in report['recommended_actions'][:3]:  # Show top 3
        print(f"  - {rec}")
        
    # Save full report
    filename = monitor.save_report(report)
    print(f"\nFull report saved to: {filename}")


if __name__ == "__main__":
    main()