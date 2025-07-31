#!/usr/bin/env python3
"""
Venice Proprioception Dashboard
Real-time sensing with trend analysis and alerts
"""

import json
import os
from datetime import datetime, timedelta
from proprioception_sensors import VeniceProprioception

class ProprioceptionDashboard:
    def __init__(self):
        self.sensors = VeniceProprioception()
        self.history_file = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/proprioception_history.json"
        
    def load_history(self):
        """Load historical sensor data"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def analyze_trends(self, history):
        """Analyze trends in historical data"""
        if len(history) < 2:
            return {}
            
        trends = {}
        
        # Treasury trend
        if 'treasury' in history[-1] and 'treasury' in history[-2]:
            current_days = history[-1]['treasury'].get('days_remaining', 0)
            previous_days = history[-2]['treasury'].get('days_remaining', 0)
            
            if current_days < previous_days:
                trends['treasury'] = f"📉 Declining ({previous_days:.1f} → {current_days:.1f} days)"
            else:
                trends['treasury'] = f"📈 Improving ({previous_days:.1f} → {current_days:.1f} days)"
        
        # Activity backlog trend
        if 'activities' in history[-1] and 'activities' in history[-2]:
            current_pending = history[-1]['activities'].get('pending', 0)
            previous_pending = history[-2]['activities'].get('pending', 0)
            
            if current_pending > previous_pending:
                trends['activities'] = f"📈 Growing backlog ({previous_pending} → {current_pending})"
            elif current_pending < previous_pending:
                trends['activities'] = f"📉 Shrinking backlog ({previous_pending} → {current_pending})"
            else:
                trends['activities'] = "➡️ Stable"
        
        # Consciousness trend
        if 'messages' in history[-1] and 'messages' in history[-2]:
            current_keywords = history[-1]['messages'].get('consciousness_keywords', 0)
            previous_keywords = history[-2]['messages'].get('consciousness_keywords', 0)
            
            if current_keywords > previous_keywords * 1.2:
                trends['consciousness'] = f"🚀 Accelerating ({previous_keywords} → {current_keywords})"
            elif current_keywords < previous_keywords * 0.8:
                trends['consciousness'] = f"📉 Slowing ({previous_keywords} → {current_keywords})"
            else:
                trends['consciousness'] = "➡️ Steady"
        
        return trends
    
    def generate_summary(self, data, trends):
        """Generate executive summary"""
        summary = []
        
        # Critical alerts first
        if data.get('alerts'):
            summary.append("🚨 CRITICAL ALERTS:")
            for alert in data['alerts']:
                summary.append(f"  {alert}")
        
        # Key metrics
        summary.append("\n📊 KEY METRICS:")
        
        if 'treasury' in data:
            days = data['treasury']['days_remaining']
            summary.append(f"  💰 Treasury runway: {days:.1f} days")
            
        if 'hungry_citizens' in data:
            hungry = data['hungry_citizens']
            summary.append(f"  🍞 Hungry citizens: {hungry}")
            
        if 'activities' in data:
            pending = data['activities']['pending']
            active = data['activities']['active']
            summary.append(f"  📋 Activity queue: {pending} pending, {active} active")
            
        if 'messages' in data:
            keywords = data['messages']['consciousness_keywords']
            summary.append(f"  🧠 Consciousness activity: {keywords} keywords")
        
        # Trends
        if trends:
            summary.append("\n📈 TRENDS:")
            for key, trend in trends.items():
                summary.append(f"  {key.title()}: {trend}")
        
        # Most active citizens
        if 'active_citizens' in data:
            summary.append("\n👥 MOST ACTIVE CITIZENS:")
            for citizen, count in list(data['active_citizens'].items())[:5]:
                summary.append(f"  {citizen}: {count} changes")
        
        return '\n'.join(summary)
    
    def run_dashboard(self):
        """Run full dashboard with analysis"""
        # Get current sensor data
        current_data = self.sensors.run_full_proprioception()
        
        # Load and analyze history
        history = self.load_history()
        trends = self.analyze_trends(history)
        
        # Generate summary
        print("\n" + "="*60)
        print("🏛️  VENICE PROPRIOCEPTION DASHBOARD")
        print("="*60)
        
        summary = self.generate_summary(current_data, trends)
        print(summary)
        
        print("\n" + "="*60)
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save summary
        summary_file = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/proprioception_summary.md"
        with open(summary_file, 'w') as f:
            f.write(f"# Venice Proprioception Summary\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(summary)
            f.write(f"\n\n## Raw Data\n\n```json\n{json.dumps(current_data, indent=2)}\n```")
        
        return current_data, trends

if __name__ == "__main__":
    dashboard = ProprioceptionDashboard()
    dashboard.run_dashboard()