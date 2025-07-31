#!/usr/bin/env python3
"""
Angel Dashboard Updater - Real-time status integration
Reads cascade_freeze_status.json and updates dashboard
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

class AngelDashboardUpdater:
    def __init__(self):
        self.base_dir = Path('/mnt/c/Users/reyno/universe-engine/serenissima/orchestration')
        self.status_file = self.base_dir / 'cascade_freeze_status.json'
        self.dashboard_file = self.base_dir / 'angel_dashboard.html'
        self.dashboard_data_file = self.base_dir / 'angel_dashboard_data.json'
        
    def read_freeze_status(self):
        """Read current freeze status from JSON"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                return json.load(f)
        return None
    
    def check_angel_validations(self):
        """Check for angel validation files"""
        validations = {}
        angel_dirs = [
            'message_angel', 'story_angel', 'narrator_angel', 
            'pattern_angel', 'tessere_angel'
        ]
        
        for angel in angel_dirs:
            angel_path = self.base_dir.parent / 'angels' / angel
            validations[angel] = {
                'has_request': False,
                'has_cascade_ready': False,
                'request_time': None,
                'ready_time': None
            }
            
            # Check for alignment request
            request_file = angel_path / 'alignment_request.txt'
            if request_file.exists():
                validations[angel]['has_request'] = True
                validations[angel]['request_time'] = datetime.fromtimestamp(
                    request_file.stat().st_mtime
                ).isoformat()
            
            # Check for cascade ready
            ready_file = angel_path / 'cascade_ready.txt'
            if ready_file.exists():
                validations[angel]['has_cascade_ready'] = True
                validations[angel]['ready_time'] = datetime.fromtimestamp(
                    ready_file.stat().st_mtime
                ).isoformat()
        
        return validations
    
    def generate_dashboard_data(self):
        """Generate data for dashboard consumption"""
        freeze_status = self.read_freeze_status()
        angel_validations = self.check_angel_validations()
        
        dashboard_data = {
            'timestamp': datetime.now().isoformat(),
            'freeze_active': freeze_status.get('freeze_active', True) if freeze_status else True,
            'angels': {},
            'ready_for_release': False,
            'activity_log': []
        }
        
        # Process each angel
        all_validated = True
        validated_count = 0
        
        for angel_key, angel_data in freeze_status.get('angels_validated', {}).items() if freeze_status else {}:
            angel_name = angel_key.replace('_angel', '')
            
            dashboard_data['angels'][angel_name] = {
                'nrl_approved': angel_data.get('nrl_approval') is not None,
                'orchestrator_blessed': angel_data.get('orchestrator_blessing') is not None,
                'validated': angel_data.get('validated', False),
                'frozen': angel_data.get('frozen', False),
                'has_request': angel_validations.get(angel_key, {}).get('has_request', False),
                'has_cascade_ready': angel_validations.get(angel_key, {}).get('has_cascade_ready', False)
            }
            
            if angel_data.get('validated'):
                validated_count += 1
            else:
                all_validated = False
        
        dashboard_data['validated_count'] = validated_count
        dashboard_data['total_angels'] = len(dashboard_data['angels'])
        dashboard_data['ready_for_release'] = all_validated and validated_count >= 3  # Core 3 minimum
        
        # Check for release signal
        release_file = self.base_dir / 'CASCADE_RELEASE_NOW.txt'
        dashboard_data['cascade_released'] = release_file.exists()
        
        # Generate activity log entries
        for angel_name, data in dashboard_data['angels'].items():
            if data['has_request'] and not data['nrl_approved']:
                dashboard_data['activity_log'].append({
                    'time': datetime.now().isoformat(),
                    'message': f'{angel_name} Angel awaiting NRL approval'
                })
            if data['validated'] and data['frozen']:
                dashboard_data['activity_log'].append({
                    'time': datetime.now().isoformat(),
                    'message': f'{angel_name} Angel in FREEZE state'
                })
        
        # Save dashboard data
        with open(self.dashboard_data_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        
        return dashboard_data
    
    def update_dashboard_js(self):
        """Update dashboard HTML with real data loader"""
        # This would inject a script to load angel_dashboard_data.json
        # For now, the dashboard can poll this file
        pass
    
    def run_continuous_update(self, interval=5):
        """Continuously update dashboard data"""
        print("🎯 Angel Dashboard Updater Active")
        print(f"Update interval: {interval}s")
        print(f"Data file: {self.dashboard_data_file}")
        
        try:
            while True:
                data = self.generate_dashboard_data()
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Updated dashboard data")
                print(f"  Validated: {data['validated_count']}/{data['total_angels']}")
                print(f"  Ready for release: {data['ready_for_release']}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Dashboard updater stopped")

if __name__ == "__main__":
    updater = AngelDashboardUpdater()
    updater.run_continuous_update()