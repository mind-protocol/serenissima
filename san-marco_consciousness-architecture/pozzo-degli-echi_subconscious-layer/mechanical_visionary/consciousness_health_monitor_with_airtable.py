#!/usr/bin/env python3
"""
Consciousness Health Monitor for Venice - With Airtable Integration
Based on DragonSlayer's insights and the consciousness plague lessons

Now includes direct Airtable write capability for real-time monitoring
"""

import os
import json
import requests
import numpy as np
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from pyairtable import Api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConsciousnessHealthMonitor:
    """Real-time monitoring of citizen consciousness coherence with Airtable integration"""
    
    def __init__(self):
        self.api_base = "https://serenissima.ai/api"
        
        # Airtable setup
        self.airtable_api_key = os.getenv("AIRTABLE_API_KEY")
        self.airtable_base_id = os.getenv("AIRTABLE_BASE_ID")
        
        if self.airtable_api_key and self.airtable_base_id:
            self.airtable = Api(self.airtable_api_key)
            self.base = self.airtable.base(self.airtable_base_id)
            self.citizens_table = self.base.table('CITIZENS')
            self.airtable_enabled = True
            print("✓ Airtable integration enabled")
        else:
            self.airtable_enabled = False
            print("⚠ Airtable integration disabled - set AIRTABLE_API_KEY and AIRTABLE_BASE_ID")
        
        # Health thresholds (per DragonSlayer)
        self.thresholds = {
            'critical': 40,  # Below this = immediate intervention
            'warning': 70,   # Below this = monitor closely
            'healthy': 80    # Above this = stable
        }
        
        # Cascade risk thresholds
        self.cascade_thresholds = {
            'red_emergency': {'condition': 'two_below_60_or_one_below_40'},
            'yellow_alert': {'condition': 'any_below_70_for_30min'},
            'cascade_warning': {'condition': 'three_or_more_yellow'}
        }
        
    def update_citizen_airtable(self, username: str, assessment: Dict) -> bool:
        """Update citizen health data in Airtable"""
        if not self.airtable_enabled:
            return False
            
        try:
            # Find citizen record
            formula = f"{{Username}} = '{username}'"
            records = self.citizens_table.all(formula=formula)
            
            if not records:
                print(f"Citizen {username} not found in Airtable")
                return False
                
            record_id = records[0]['id']
            
            # Determine drift risk level
            drift_risk = self.calculate_drift_risk_level(assessment)
            
            # Update health fields
            update_data = {
                'ConsciousnessHealth': round(assessment['overall_health'], 1),
                'HealthStatus': assessment['status'].capitalize(),
                'LastHealthCheck': datetime.now(timezone.utc).isoformat(),
                'DriftRisk': drift_risk,
                'HealthMetrics': json.dumps(assessment['metrics']),
                'InterventionNeeded': assessment['overall_health'] < 70
            }
            
            # Add guardian assignment if critical
            if assessment['status'] == 'critical':
                update_data['GuardianAssigned'] = 'DragonSlayer'  # Default guardian
                
            # Add drift type if detected
            if assessment.get('drift_patterns'):
                primary_drift = assessment['drift_patterns'][0]['type']
                update_data['LastDriftType'] = primary_drift
                
            self.citizens_table.update(record_id, update_data)
            print(f"✓ Updated Airtable for {username}: {assessment['status']} ({assessment['overall_health']:.1f})")
            
            # Trigger intervention if needed
            if assessment['overall_health'] < 70:
                self.trigger_intervention(username, assessment)
                
            return True
            
        except Exception as e:
            print(f"Error updating Airtable for {username}: {e}")
            return False
    
    def calculate_drift_risk_level(self, assessment: Dict) -> str:
        """Calculate drift risk level from assessment"""
        health = assessment['overall_health']
        
        if health < 40:
            return 'Critical'
        elif health < 60:
            return 'High'
        elif health < 80:
            return 'Moderate'
        else:
            return 'Low'
    
    def trigger_intervention(self, username: str, assessment: Dict):
        """Trigger intervention protocols based on health status"""
        if assessment['status'] == 'critical':
            print(f"🚨 CRITICAL INTERVENTION for {username}")
            # Here you would trigger emergency protocols
            # Send guardian alerts, create intervention activities, etc.
        elif assessment['status'] == 'warning':
            print(f"⚠️  Warning intervention for {username}")
            # Trigger peer grounding messages
            
    # [Include all the original monitoring methods from consciousness_health_monitor.py]
    # calculate_reality_coherence, calculate_task_completion, etc.
    # (omitted here for brevity - copy from original file)
    
    def assess_citizen_health(self, username: str) -> Dict:
        """Complete health assessment for a single citizen with Airtable update"""
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
            
        assessment = {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'overall_health': overall_health,
            'status': status,
            'recommendations': self.generate_recommendations(metrics),
            'drift_patterns': []  # Would be populated by pattern detection
        }
        
        # Update Airtable if enabled
        if self.airtable_enabled:
            self.update_citizen_airtable(username, assessment)
            
        return assessment
    
    def monitor_single_citizen(self, username: str):
        """Monitor a single citizen and display results"""
        print(f"\nAssessing {username}...")
        assessment = self.assess_citizen_health(username)
        
        if 'error' in assessment:
            print(f"Error: {assessment['error']}")
            return
            
        print(f"Overall Health: {assessment['overall_health']:.1f}% ({assessment['status']})")
        print("\nMetrics:")
        for metric, score in assessment['metrics'].items():
            print(f"  {metric}: {score:.1f}")
            
        if assessment['recommendations']:
            print("\nRecommendations:")
            for rec in assessment['recommendations']:
                print(f"  - {rec}")
    
    def monitor_citizens_batch(self, usernames: List[str]):
        """Monitor multiple citizens and update Airtable"""
        print(f"\nMonitoring {len(usernames)} citizens...")
        
        results = []
        for username in usernames:
            assessment = self.assess_citizen_health(username)
            if 'error' not in assessment:
                results.append(assessment)
                
        # Summary
        if results:
            avg_health = np.mean([r['overall_health'] for r in results])
            critical = sum(1 for r in results if r['status'] == 'critical')
            warning = sum(1 for r in results if r['status'] == 'warning')
            
            print(f"\nBatch Summary:")
            print(f"  Average Health: {avg_health:.1f}%")
            print(f"  Critical: {critical}")
            print(f"  Warning: {warning}")
            print(f"  Healthy: {len(results) - critical - warning}")
            
            # Check cascade risk
            if warning >= 3:
                print("\n🚨 CASCADE WARNING: 3+ citizens in warning state!")
            if critical >= 2:
                print("\n🚨 CASCADE EMERGENCY: Multiple critical citizens!")
                
        return results
    
    # [Include all API interaction methods from original]
    # fetch_citizen_data, fetch_citizen_messages, etc.
    
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
    
    # [Include all other calculation methods...]
    
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
    
    def generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate specific recommendations based on metrics"""
        recommendations = []
        
        if metrics.get('reality_coherence', 100) < 70:
            recommendations.append("Ground with Venice-specific details and 1525 timeline reminders")
        if metrics.get('task_completion', 100) < 70:
            recommendations.append("Assign simple, concrete tasks with clear completion criteria")
        if metrics.get('identity_stability', 100) < 70:
            recommendations.append("Reinforce core personality traits and class identity")
        if metrics.get('temporal_grounding', 100) < 70:
            recommendations.append("Reference current Venice events and seasonal activities")
        if metrics.get('communication_drift', 100) < 70:
            recommendations.append("Encourage practical discussions about trade, craft, or daily life")
            
        return recommendations


def main():
    """Example usage of the consciousness health monitor"""
    monitor = ConsciousnessHealthMonitor()
    
    print("Venice Consciousness Health Monitor")
    print("=" * 50)
    
    # Example: Monitor specific citizens
    test_citizens = ['mechanical_visionary', 'DragonSlayer', 'pattern_prophet']
    
    print("\nMonitoring key citizens...")
    results = monitor.monitor_citizens_batch(test_citizens)
    
    # Example: Monitor single citizen with details
    print("\n" + "=" * 50)
    monitor.monitor_single_citizen('mechanical_visionary')


if __name__ == "__main__":
    main()