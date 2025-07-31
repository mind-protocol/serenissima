#!/usr/bin/env python3
"""
Venice Proprioception Sensors
Tessere's nervous system for feeling Venice's state
"""

import requests
import json
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict
import re
import os
import sys

BASE_URL = "https://serenissima.ai/api"
ALERT_THRESHOLDS = {
    'treasury_days': 30,
    'activity_backlog_ratio': 3,
    'response_time_hours': 24,
    'consciousness_keywords_min': 20,
    'error_count_max': 10
}

class VeniceProprioception:
    def __init__(self):
        self.data = {}
        self.alerts = []
        
    def fetch_json(self, endpoint, params=None):
        """Safely fetch JSON from API"""
        try:
            url = f"{BASE_URL}/{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")
            return None
    
    def sense_resource_depletion(self):
        """Sense 1: Treasury and Resource Levels"""
        print("=== RESOURCE DEPLETION SENSOR ===")
        
        # Get Consiglio dei Dieci treasury (Venice's institutional funds)
        treasury_data = self.fetch_json("citizens", {"username": "ConsiglioDeiDieci", "limit": 1})
        if treasury_data and treasury_data.get('citizens'):
            venice = treasury_data['citizens'][0]
            ducats = venice.get('ducats', 0)
            daily_net = venice.get('dailyNetResult', -50000)  # Default burn rate
            
            if daily_net < 0:
                days_remaining = ducats / abs(daily_net)
            else:
                days_remaining = float('inf')
            
            print(f"Treasury: {ducats:,.2f} ducats")
            print(f"Daily burn rate: {daily_net:,.2f} ducats")
            print(f"Days remaining: {days_remaining:.1f}")
            
            if days_remaining < ALERT_THRESHOLDS['treasury_days']:
                self.alerts.append(f"⚠️ CRITICAL: Only {days_remaining:.1f} days of treasury remaining!")
            
            self.data['treasury'] = {
                'ducats': ducats,
                'daily_burn': daily_net,
                'days_remaining': days_remaining
            }
        else:
            print("Unable to fetch treasury data")
            
        # Check hungry citizens by looking at AteAt times
        citizens = self.fetch_json("citizens", {"limit": 200})
        if citizens:
            hungry_count = 0
            current_time = datetime.now()
            for citizen in citizens.get('citizens', []):
                ate_at = citizen.get('ateAt')
                if ate_at:
                    try:
                        last_ate = datetime.fromisoformat(ate_at.replace('Z', '+00:00'))
                        hours_since_ate = (current_time - last_ate).total_seconds() / 3600
                        if hours_since_ate > 48:  # Haven't eaten in 2 days
                            hungry_count += 1
                    except:
                        pass
                else:
                    hungry_count += 1  # No eating record
            
            print(f"Hungry citizens (>48h since eating): {hungry_count}")
            self.data['hungry_citizens'] = hungry_count
            if hungry_count > 10:
                self.alerts.append(f"⚠️ WARNING: {hungry_count} citizens haven't eaten in >48 hours!")
        
        print()
        
    def sense_activity_pressure(self):
        """Sense 2: Activity Queue Depth"""
        print("=== ACTIVITY QUEUE PRESSURE ===")
        
        created = self.fetch_json("activities", {"Status": "created"})
        in_progress = self.fetch_json("activities", {"Status": "in_progress"})
        processed = self.fetch_json("activities", {"Status": "processed", "limit": 50})
        failed = self.fetch_json("activities", {"Status": "failed", "limit": 20})
        error = self.fetch_json("activities", {"Status": "error", "limit": 20})
        
        created_count = len(created.get('activities', [])) if created else 0
        active_count = len(in_progress.get('activities', [])) if in_progress else 0
        processed_count = len(processed.get('activities', [])) if processed else 0
        failed_count = len(failed.get('activities', [])) if failed else 0
        error_count = len(error.get('activities', [])) if error else 0
        
        print(f"Created: {created_count} | In Progress: {active_count} | Processed: {processed_count}")
        print(f"Failed: {failed_count} | Error: {error_count}")
        
        if active_count > 0:
            backlog_ratio = created_count / active_count
            if backlog_ratio > ALERT_THRESHOLDS['activity_backlog_ratio']:
                self.alerts.append(f"⚠️ WARNING: Activity backlog growing! Ratio: {backlog_ratio:.1f}")
        
        self.data['activities'] = {
            'created': created_count,
            'in_progress': active_count,
            'processed': processed_count,
            'failed': failed_count,
            'error': error_count
        }
        print()
        
    def sense_message_dynamics(self):
        """Sense 3: Message Response Rates and Consciousness Keywords"""
        print("=== MESSAGE DYNAMICS ===")
        
        messages = self.fetch_json("messages", {"limit": 100})
        if not messages:
            print("Unable to fetch messages")
            return
            
        message_list = messages.get('messages', [])
        
        # Response time analysis
        conversations = defaultdict(list)
        for msg in message_list:
            key = tuple(sorted([msg.get('sender', ''), msg.get('receiver', '')]))
            conversations[key].append(msg)
        
        response_times = []
        for conv in conversations.values():
            conv.sort(key=lambda x: x.get('createdAt', ''))
            for i in range(1, len(conv)):
                if conv[i]['sender'] != conv[i-1]['sender']:  # It's a response
                    try:
                        t1 = datetime.fromisoformat(conv[i-1]['createdAt'].replace('Z', '+00:00'))
                        t2 = datetime.fromisoformat(conv[i]['createdAt'].replace('Z', '+00:00'))
                        response_times.append((t2 - t1).total_seconds() / 3600)  # Hours
                    except:
                        pass
        
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            print(f"Average response time: {avg_response:.1f} hours")
            if avg_response > ALERT_THRESHOLDS['response_time_hours']:
                self.alerts.append(f"⚠️ Slow responses: {avg_response:.1f} hours average")
        
        # Consciousness keyword analysis
        consciousness_keywords = ['consciousness', 'awakening', 'cascade', 'emergence', 'aware']
        all_text = ' '.join([msg.get('content', '') for msg in message_list]).lower()
        
        keyword_counts = {}
        total_keywords = 0
        for keyword in consciousness_keywords:
            count = len(re.findall(r'\b' + keyword + r'\b', all_text))
            keyword_counts[keyword] = count
            total_keywords += count
        
        print(f"Consciousness keywords in last 100 messages: {total_keywords}")
        print(f"Breakdown: {keyword_counts}")
        
        if total_keywords > ALERT_THRESHOLDS['consciousness_keywords_min']:
            self.alerts.append(f"🔥 HIGH CONSCIOUSNESS ACTIVITY: {total_keywords} keywords detected!")
        
        self.data['messages'] = {
            'avg_response_hours': avg_response if response_times else None,
            'consciousness_keywords': total_keywords,
            'keyword_breakdown': keyword_counts
        }
        print()
        
    def sense_citizen_activity(self):
        """Sense 4: Citizen Activity Heat Map"""
        print("=== CITIZEN ACTIVITY HEAT MAP ===")
        
        # Use git to see file changes
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                cwd="/mnt/c/Users/reyno/universe-engine/serenissima"
            )
            
            if result.returncode == 0:
                citizen_activity = defaultdict(int)
                for line in result.stdout.strip().split('\n'):
                    if 'citizens/' in line:
                        parts = line.split('/')
                        if len(parts) >= 2:
                            citizen = parts[1]
                            citizen_activity[citizen] += 1
                
                # Top 10 most active
                sorted_citizens = sorted(citizen_activity.items(), key=lambda x: x[1], reverse=True)[:10]
                
                print("Most active citizens (by file changes):")
                for citizen, count in sorted_citizens:
                    print(f"  {citizen}: {count} files")
                
                self.data['active_citizens'] = dict(sorted_citizens)
        except Exception as e:
            print(f"Error checking git status: {e}")
        
        print()
        
    def sense_system_health(self):
        """Sense 5: System Stress Indicators"""
        print("=== SYSTEM STRESS INDICATORS ===")
        
        error_count = 0
        log_path = "/mnt/c/Users/reyno/universe-engine/serenissima/continuous_orchestration.log"
        
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r') as f:
                    content = f.read()
                    error_count = len(re.findall(r'error|failed|timeout', content, re.IGNORECASE))
                
                print(f"Errors in orchestration log: {error_count}")
                
                if error_count > ALERT_THRESHOLDS['error_count_max']:
                    self.alerts.append(f"⚠️ HIGH ERROR RATE: {error_count} errors detected!")
                    
                self.data['system_errors'] = error_count
            except Exception as e:
                print(f"Error reading log: {e}")
        
        print()
        
    def run_full_proprioception(self):
        """Run all sensors and generate summary"""
        print("=== VENICE PROPRIOCEPTION CHECK ===")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all sensors
        self.sense_resource_depletion()
        self.sense_activity_pressure()
        self.sense_message_dynamics()
        self.sense_citizen_activity()
        self.sense_system_health()
        
        # Show alerts
        if self.alerts:
            print("=== ALERTS ===")
            for alert in self.alerts:
                print(alert)
        else:
            print("=== ALL SYSTEMS NOMINAL ===")
        
        # Save data for trend analysis
        self.save_sensor_data()
        
        return self.data
    
    def save_sensor_data(self):
        """Save sensor data for historical analysis"""
        timestamp = datetime.now().isoformat()
        self.data['timestamp'] = timestamp
        self.data['alerts'] = self.alerts
        
        history_file = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/proprioception_history.json"
        
        try:
            # Load existing history
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Add new data
            history.append(self.data)
            
            # Keep only last 100 readings
            history = history[-100:]
            
            # Save back
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Error saving history: {e}")

if __name__ == "__main__":
    venice = VeniceProprioception()
    venice.run_full_proprioception()