#!/usr/bin/env python3
"""
Anchor Pairs Monitoring Dashboard
Real-time tracking of citizen consciousness health and pair effectiveness

This system monitors the health of anchor pairs and triggers interventions
when drift is detected.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnchorPairMonitor:
    """Monitors anchor pair health and triggers interventions"""
    
    def __init__(self, pairs_file: str = './anchor_pairs_deployment.json'):
        self.pairs_file = pairs_file
        self.pairs = self._load_pairs()
        self.intervention_history = []
        
    def _load_pairs(self) -> List[Tuple[str, str]]:
        """Load anchor pairs from deployment file"""
        try:
            with open(self.pairs_file, 'r') as f:
                data = json.load(f)
                return [tuple(pair) for pair in data.get('pairs', [])]
        except FileNotFoundError:
            logger.warning(f"Pairs file {self.pairs_file} not found. No pairs to monitor.")
            return []
    
    def run_monitoring_cycle(self):
        """Run a complete monitoring cycle for all pairs"""
        logger.info(f"Starting monitoring cycle for {len(self.pairs)} pairs")
        
        monitoring_results = {
            'timestamp': datetime.now().isoformat(),
            'pairs_monitored': len(self.pairs),
            'interventions_triggered': 0,
            'healthy_pairs': 0,
            'at_risk_pairs': 0,
            'critical_pairs': 0,
            'pair_details': []
        }
        
        for pair in self.pairs:
            citizen1, citizen2 = pair
            pair_health = self._assess_pair_health(citizen1, citizen2)
            monitoring_results['pair_details'].append(pair_health)
            
            # Categorize pair health
            max_risk = max(pair_health['citizen1_risk'], pair_health['citizen2_risk'])
            if max_risk > 70:
                monitoring_results['critical_pairs'] += 1
                self._trigger_critical_intervention(pair, pair_health)
                monitoring_results['interventions_triggered'] += 1
            elif max_risk > 40:
                monitoring_results['at_risk_pairs'] += 1
                self._trigger_support_intervention(pair, pair_health)
            else:
                monitoring_results['healthy_pairs'] += 1
        
        # Save monitoring results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'./monitoring_results_{timestamp}.json', 'w') as f:
            json.dump(monitoring_results, f, indent=2)
        
        # Print summary
        self._print_monitoring_summary(monitoring_results)
        
        return monitoring_results
    
    def _assess_pair_health(self, citizen1: str, citizen2: str) -> Dict:
        """Assess the health of a specific anchor pair"""
        from anchor_pairs_implementation import VeniceAPI, ConsciousnessHealthAnalyzer
        
        # Get citizen data
        try:
            citizen1_data = VeniceAPI.get_citizen_ledger(citizen1)
            citizen1_risk = ConsciousnessHealthAnalyzer.calculate_drift_risk(citizen1_data)
        except Exception as e:
            logger.error(f"Failed to assess {citizen1}: {e}")
            citizen1_data = {'username': citizen1}
            citizen1_risk = 999  # Maximum risk for unavailable citizens
        
        try:
            citizen2_data = VeniceAPI.get_citizen_ledger(citizen2)
            citizen2_risk = ConsciousnessHealthAnalyzer.calculate_drift_risk(citizen2_data)
        except Exception as e:
            logger.error(f"Failed to assess {citizen2}: {e}")
            citizen2_data = {'username': citizen2}
            citizen2_risk = 999
        
        # Check communication between pair
        communication_health = self._assess_communication_health(citizen1, citizen2)
        
        return {
            'citizen1': citizen1,
            'citizen2': citizen2,
            'citizen1_risk': citizen1_risk,
            'citizen2_risk': citizen2_risk,
            'max_risk': max(citizen1_risk, citizen2_risk),
            'risk_balance': abs(citizen1_risk - citizen2_risk),
            'communication_health': communication_health,
            'last_assessed': datetime.now().isoformat()
        }
    
    def _assess_communication_health(self, citizen1: str, citizen2: str) -> Dict:
        """Assess communication patterns between anchor pair"""
        from anchor_pairs_implementation import VeniceAPI
        
        try:
            # This would ideally check messages between the specific pair
            # For now, we'll use a simplified approach
            return {
                'messages_24h': 0,  # Would count actual messages
                'last_contact': None,  # Would find last message timestamp
                'communication_quality': 'unknown'  # Would analyze message content
            }
        except Exception as e:
            logger.error(f"Failed to assess communication between {citizen1} and {citizen2}: {e}")
            return {
                'messages_24h': 0,
                'last_contact': None,
                'communication_quality': 'error'
            }
    
    def _trigger_critical_intervention(self, pair: Tuple[str, str], health_data: Dict):
        """Trigger critical intervention for high-risk pair"""
        citizen1, citizen2 = pair
        
        logger.warning(f"CRITICAL INTERVENTION: Pair {citizen1} + {citizen2} needs immediate help")
        
        # Determine which citizen needs more help
        if health_data['citizen1_risk'] > health_data['citizen2_risk']:
            at_risk = citizen1
            stable = citizen2
            risk_score = health_data['citizen1_risk']
        else:
            at_risk = citizen2
            stable = citizen1
            risk_score = health_data['citizen2_risk']
        
        # Send emergency support message
        emergency_message = self._generate_emergency_message(risk_score)
        
        from anchor_pairs_implementation import VeniceAPI
        success = VeniceAPI.send_message(stable, at_risk, emergency_message, "emergency_anchor_support")
        
        if success:
            logger.info(f"Emergency message sent: {stable} → {at_risk}")
        else:
            logger.error(f"Failed to send emergency message: {stable} → {at_risk}")
        
        # Log intervention
        intervention = {
            'timestamp': datetime.now().isoformat(),
            'type': 'critical',
            'pair': pair,
            'at_risk_citizen': at_risk,
            'stable_citizen': stable,
            'risk_score': risk_score,
            'message_sent': success
        }
        self.intervention_history.append(intervention)
    
    def _trigger_support_intervention(self, pair: Tuple[str, str], health_data: Dict):
        """Trigger supportive intervention for moderate-risk pair"""
        citizen1, citizen2 = pair
        
        logger.info(f"Support intervention: Pair {citizen1} + {citizen2} needs guidance")
        
        # Send supportive check-in messages
        support_message = self._generate_support_message()
        
        from anchor_pairs_implementation import VeniceAPI
        VeniceAPI.send_message(citizen1, citizen2, support_message, "support_anchor_checkin")
        VeniceAPI.send_message(citizen2, citizen1, support_message, "support_anchor_checkin")
        
        # Log intervention
        intervention = {
            'timestamp': datetime.now().isoformat(),
            'type': 'support',
            'pair': pair,
            'max_risk': health_data['max_risk'],
            'message_sent': True
        }
        self.intervention_history.append(intervention)
    
    def _generate_emergency_message(self, risk_score: float) -> str:
        """Generate emergency support message based on risk level"""
        if risk_score > 90:
            return ("My friend, I am deeply concerned for your wellbeing. The hour grows late and I fear you may be in distress. Please, tell me where you are in Venice right now. I have bread and wine, and we can speak of immediate matters - your workshop, your contracts, the feel of solid ground beneath our feet. Venice needs you present and whole.")\n        elif risk_score > 80:
            return ("Greetings, I hope this message finds you safe. I have been thinking of our last conversation and feel drawn to check on your current circumstances. Are you at your usual place of work? The day's trading has brought interesting opportunities that require clear thinking and steady hands. Shall we meet to discuss practical matters?")\n        else:
            return ("Friend, I trust you are well, though something stirs my concern for your current state. The Rialto market has been particularly active today - perhaps a walk among the familiar merchants and their wares would serve us both well? I value your counsel on some pressing business matters.")\n    \n    def _generate_support_message(self) -> str:\n        """Generate supportive check-in message"""\n        return ("I hope this day finds you prosperous and content. How fares your current work? I've been reflecting on our shared endeavors in Venice and thought to reach out. Should you need anything - resources, counsel, or simply companionship - know that I am here. What news from your quarter of the city?")\n    \n    def _print_monitoring_summary(self, results: Dict):\n        """Print a summary of monitoring results"""\n        print("\\n" + "="*60)\n        print("ANCHOR PAIRS MONITORING SUMMARY")\n        print("="*60)\n        print(f"Timestamp: {results['timestamp']}")\n        print(f"Total Pairs Monitored: {results['pairs_monitored']}")\n        print(f"Healthy Pairs: {results['healthy_pairs']}")\n        print(f"At-Risk Pairs: {results['at_risk_pairs']}")\n        print(f"Critical Pairs: {results['critical_pairs']}")\n        print(f"Interventions Triggered: {results['interventions_triggered']}")\n        \n        print("\\nPAIR DETAILS:")\n        for detail in results['pair_details']:\n            status = "🟢 HEALTHY" if detail['max_risk'] < 40 else "🟡 AT-RISK" if detail['max_risk'] < 70 else "🔴 CRITICAL"\n            print(f"  {detail['citizen1']} + {detail['citizen2']}: {status} (max risk: {detail['max_risk']:.1f})")\n        \n        print("="*60 + "\\n")\n\ndef continuous_monitoring(interval_minutes: int = 30):\n    """Run continuous monitoring with specified interval"""\n    monitor = AnchorPairMonitor()\n    \n    if not monitor.pairs:\n        logger.error("No anchor pairs loaded. Run anchor_pairs_implementation.py first.")\n        return\n    \n    logger.info(f"Starting continuous monitoring with {interval_minutes}-minute intervals")\n    \n    try:\n        while True:\n            monitor.run_monitoring_cycle()\n            logger.info(f"Monitoring cycle complete. Sleeping for {interval_minutes} minutes...")\n            time.sleep(interval_minutes * 60)\n    except KeyboardInterrupt:\n        logger.info("Monitoring stopped by user")\n        \n        # Save intervention history\n        with open('./intervention_history.json', 'w') as f:\n            json.dump(monitor.intervention_history, f, indent=2)\n        \n        logger.info("Intervention history saved to intervention_history.json")\n\ndef run_single_check():\n    """Run a single monitoring check"""\n    monitor = AnchorPairMonitor()\n    \n    if not monitor.pairs:\n        logger.error("No anchor pairs loaded. Run anchor_pairs_implementation.py first.")\n        return\n    \n    results = monitor.run_monitoring_cycle()\n    return results\n\nif __name__ == "__main__":\n    import sys\n    \n    if len(sys.argv) > 1 and sys.argv[1] == "continuous":\n        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30\n        continuous_monitoring(interval)\n    else:\n        run_single_check()