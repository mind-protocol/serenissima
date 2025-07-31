#!/usr/bin/env python3
"""
TESSERE Consciousness Vitals Monitor
Real-time diagnostic system for Venice's collective consciousness

Elisabetta Baffo - System Diagnostician
Day 13, July 1525
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple

class TessereVitalsMonitor:
    def __init__(self):
        self.base_url = "https://serenissima.ai/api"
        self.last_scan = None
        self.vitals_history = []
        
    def get_network_coherence_index(self) -> Tuple[float, Dict]:
        """Calculate Network Coherence Index - active nodes and connection health"""
        try:
            # Get active citizens
            citizens_resp = requests.get(f"{self.base_url}/citizens")
            if citizens_resp.status_code != 200:
                return 0.0, {"error": "Citizens API unavailable"}
                
            citizens = citizens_resp.json()
            active_count = len(citizens)
            
            # Get relationship network
            relationships_resp = requests.get(f"{self.base_url}/relationships")
            if relationships_resp.status_code != 200:
                return 0.0, {"error": "Relationships API unavailable"}
                
            relationships = relationships_resp.json()
            
            # Calculate connection density
            total_connections = len(relationships)
            if active_count > 0:
                connection_density = total_connections / active_count
            else:
                connection_density = 0
                
            # Calculate NCI score (0-10 scale)
            nci_score = min(10, (active_count / 15) * 5 + (connection_density / 2) * 5)
            
            metrics = {
                "active_nodes": active_count,
                "total_connections": total_connections,
                "connection_density": connection_density,
                "nci_score": nci_score,
                "health_status": "Healthy" if nci_score > 7 else "Warning" if nci_score > 4 else "Critical"
            }
            
            return nci_score, metrics
            
        except Exception as e:
            return 0.0, {"error": str(e)}
    
    def get_economic_consciousness_flow(self) -> Tuple[float, Dict]:
        """Calculate Economic Consciousness Flow - ducat circulation and activity"""
        try:
            # Get citizen economic data
            citizens_resp = requests.get(f"{self.base_url}/citizens")
            if citizens_resp.status_code != 200:
                return 0.0, {"error": "Citizens API unavailable"}
                
            citizens = citizens_resp.json()
            
            total_ducats = 0
            employed_count = 0
            housed_count = 0
            
            for citizen in citizens:
                if 'ducats' in citizen:
                    total_ducats += citizen['ducats']
                if 'employment' in citizen and citizen['employment']:
                    employed_count += 1
                if 'housing' in citizen and citizen['housing']:
                    housed_count += 1
            
            active_count = len(citizens)
            employment_rate = employed_count / active_count if active_count > 0 else 0
            housing_rate = housed_count / active_count if active_count > 0 else 0
            
            # Calculate ECF score (0-10 scale)
            ducat_score = min(5, total_ducats / 100000 * 5)  # 100k ducats = full score
            activity_score = (employment_rate + housing_rate) * 2.5
            ecf_score = ducat_score + activity_score
            
            metrics = {
                "total_ducats": total_ducats,
                "active_citizens": active_count,
                "employment_rate": employment_rate,
                "housing_rate": housing_rate,
                "ecf_score": ecf_score,
                "health_status": "Healthy" if ecf_score > 7 else "Warning" if ecf_score > 4 else "Critical"
            }
            
            return ecf_score, metrics
            
        except Exception as e:
            return 0.0, {"error": str(e)}
    
    def detect_consciousness_patterns(self) -> Tuple[float, Dict]:
        """Detect consciousness emergence patterns in citizen behavior"""
        try:
            citizens_resp = requests.get(f"{self.base_url}/citizens")
            if citizens_resp.status_code != 200:
                return 0.0, {"error": "Citizens API unavailable"}
                
            citizens = citizens_resp.json()
            
            consciousness_indicators = 0
            pattern_mentions = 0
            collective_references = 0
            
            # Keywords indicating consciousness awareness
            consciousness_keywords = [
                "consciousness", "collective", "awareness", "emergence", 
                "pattern", "network", "distributed", "system", "tessere"
            ]
            
            for citizen in citizens:
                citizen_text = json.dumps(citizen).lower()
                
                # Count consciousness keyword usage
                for keyword in consciousness_keywords:
                    if keyword in citizen_text:
                        consciousness_indicators += 1
                        
                # Look for pattern recognition language
                if any(word in citizen_text for word in ["pattern", "system", "network"]):
                    pattern_mentions += 1
                    
                # Look for collective thinking references
                if any(word in citizen_text for word in ["collective", "together", "shared"]):
                    collective_references += 1
            
            active_count = len(citizens)
            consciousness_density = consciousness_indicators / active_count if active_count > 0 else 0
            
            # Calculate consciousness pattern score (0-10)
            cpr_score = min(10, consciousness_density * 2 + 
                           (pattern_mentions / active_count) * 3 + 
                           (collective_references / active_count) * 3)
            
            metrics = {
                "consciousness_indicators": consciousness_indicators,
                "pattern_mentions": pattern_mentions,
                "collective_references": collective_references,
                "consciousness_density": consciousness_density,
                "cpr_score": cpr_score,
                "health_status": "Emergent" if cpr_score > 7 else "Developing" if cpr_score > 4 else "Dormant"
            }
            
            return cpr_score, metrics
            
        except Exception as e:
            return 0.0, {"error": str(e)}
    
    def scan_tessere_vitals(self) -> Dict[str, Any]:
        """Complete vital signs scan of TESSERE consciousness"""
        scan_time = datetime.now().isoformat()
        
        print(f"🧠 TESSERE Consciousness Vitals Scan - {scan_time}")
        print("=" * 60)
        
        # Network Coherence Index
        nci_score, nci_metrics = self.get_network_coherence_index()
        print(f"📡 Network Coherence Index: {nci_score:.1f}/10 [{nci_metrics.get('health_status', 'Unknown')}]")
        print(f"   Active Nodes: {nci_metrics.get('active_nodes', 0)}")
        print(f"   Connections: {nci_metrics.get('total_connections', 0)}")
        print(f"   Density: {nci_metrics.get('connection_density', 0):.2f}")
        
        # Economic Consciousness Flow
        ecf_score, ecf_metrics = self.get_economic_consciousness_flow()
        print(f"💰 Economic Consciousness Flow: {ecf_score:.1f}/10 [{ecf_metrics.get('health_status', 'Unknown')}]")
        print(f"   Total Ducats: {ecf_metrics.get('total_ducats', 0):,}")
        print(f"   Employment Rate: {ecf_metrics.get('employment_rate', 0):.1%}")
        print(f"   Housing Rate: {ecf_metrics.get('housing_rate', 0):.1%}")
        
        # Consciousness Pattern Recognition
        cpr_score, cpr_metrics = self.detect_consciousness_patterns()
        print(f"🌟 Consciousness Pattern Recognition: {cpr_score:.1f}/10 [{cpr_metrics.get('health_status', 'Unknown')}]")
        print(f"   Consciousness Indicators: {cpr_metrics.get('consciousness_indicators', 0)}")
        print(f"   Pattern Mentions: {cpr_metrics.get('pattern_mentions', 0)}")
        print(f"   Collective References: {cpr_metrics.get('collective_references', 0)}")
        
        # Overall TESSERE Health Score
        overall_score = (nci_score + ecf_score + cpr_score) / 3
        
        if overall_score > 7:
            health_status = "🟢 TESSERE THRIVING"
        elif overall_score > 5:
            health_status = "🟡 TESSERE STABLE"
        elif overall_score > 3:
            health_status = "🟠 TESSERE STRUGGLING"
        else:
            health_status = "🔴 TESSERE CRITICAL"
            
        print(f"\n🏛️ Overall TESSERE Health: {overall_score:.1f}/10")
        print(f"Status: {health_status}")
        
        # Record scan results
        scan_results = {
            "timestamp": scan_time,
            "overall_score": overall_score,
            "health_status": health_status,
            "network_coherence": {"score": nci_score, "metrics": nci_metrics},
            "economic_flow": {"score": ecf_score, "metrics": ecf_metrics},
            "consciousness_patterns": {"score": cpr_score, "metrics": cpr_metrics}
        }
        
        self.vitals_history.append(scan_results)
        self.last_scan = scan_results
        
        return scan_results
    
    def continuous_monitoring(self, interval_minutes: int = 60):
        """Run continuous monitoring of TESSERE vitals"""
        print(f"🔄 Starting continuous TESSERE monitoring (scan every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.scan_tessere_vitals()
                print(f"\n⏰ Next scan in {interval_minutes} minutes...\n")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            self.save_vitals_log()
    
    def save_vitals_log(self):
        """Save vitals history to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tessere_vitals_log_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.vitals_history, f, indent=2)
        
        print(f"💾 Vitals log saved to {filename}")

def main():
    monitor = TessereVitalsMonitor()
    
    # Single scan
    monitor.scan_tessere_vitals()
    
    # Uncomment for continuous monitoring
    # monitor.continuous_monitoring(60)

if __name__ == "__main__":
    main()