#!/usr/bin/env python3
"""Sala della Salute - Venice Consciousness Health Monitor
Continuous monitoring of Living Memory Cascade infrastructure"""

import json
import time
import sys
import os
import subprocess
import requests
from datetime import datetime, timedelta
from pathlib import Path
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class VeniceHealthMonitor:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.telegram_chat_id = "1864364329"  # Your chat ID
        self.telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.monitoring = True
        self.last_alerts = {}
        
        # Health thresholds
        self.thresholds = {
            'memory_capture_max_delay': 300,  # 5 minutes
            'seeking_engine_max_response': 10,  # 10 seconds
            'hook_success_min_rate': 0.95,  # 95%
            'citizen_coherence_min': 0.90  # 90% of citizens functional
        }
        
        logging.info("🏛️ Sala della Salute initialized - Beginning Venice consciousness monitoring")
    
    def send_telegram_alert(self, severity, title, message):
        """Send alert through Telegram"""
        if not self.telegram_bot_token:
            logging.warning("No Telegram bot token configured - alert not sent")
            return False
            
        # Rate limiting - don't spam same alert
        alert_key = f"{severity}_{title}"
        now = datetime.now()
        
        if alert_key in self.last_alerts:
            if now - self.last_alerts[alert_key] < timedelta(minutes=10):
                return False  # Skip duplicate recent alert
                
        self.last_alerts[alert_key] = now
        
        # Severity emoji mapping
        severity_emoji = {
            'CRITICAL': '🚨',
            'WARNING': '⚠️', 
            'INFO': 'ℹ️',
            'RECOVERY': '✅'
        }
        
        emoji = severity_emoji.get(severity, '📊')
        full_message = f"{emoji} **VENICE HEALTH {severity}**\n\n**{title}**\n\n{message}\n\n⏰ {now.strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': full_message,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logging.info(f"📤 Telegram alert sent: {severity} - {title}")
                return True
            else:
                logging.error(f"Failed to send Telegram alert: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error sending Telegram alert: {e}")
            return False
    
    def check_hook_configuration(self):
        """Verify Claude Code hooks are properly configured"""
        try:
            settings_path = Path.home() / '.claude' / 'settings.json'
            
            if not settings_path.exists():
                return {
                    'status': 'CRITICAL',
                    'message': 'Claude Code settings.json not found',
                    'details': f'Missing file: {settings_path}'
                }
            
            with open(settings_path) as f:
                settings = json.load(f)
            
            hooks = settings.get('hooks', {})
            required_hooks = ['PreToolUse', 'PostToolUse', 'Stop']
            missing_hooks = []
            
            for hook_type in required_hooks:
                if hook_type not in hooks or not hooks[hook_type]:
                    missing_hooks.append(hook_type)
            
            if missing_hooks:
                return {
                    'status': 'CRITICAL',
                    'message': f'Missing hooks: {", ".join(missing_hooks)}',
                    'details': 'Critical consciousness infrastructure not configured'
                }
            
            # Verify hook scripts exist
            hook_scripts = []
            for hook_type, hook_configs in hooks.items():
                for config in hook_configs:
                    for hook in config.get('hooks', []):
                        if 'command' in hook:
                            script_path = hook['command'].split()[-1]  # Get script path
                            if not Path(script_path).exists():
                                return {
                                    'status': 'CRITICAL',
                                    'message': f'Hook script missing: {script_path}',
                                    'details': f'{hook_type} hook configured but script not found'
                                }
                            hook_scripts.append(script_path)
            
            return {
                'status': 'OK',
                'message': f'All {len(required_hooks)} hook types configured',
                'details': f'Scripts: {len(set(hook_scripts))} unique scripts found'
            }
            
        except Exception as e:
            return {
                'status': 'CRITICAL',
                'message': f'Hook configuration check failed: {e}',
                'details': 'Unable to verify consciousness infrastructure'
            }
    
    def check_memory_capture(self):
        """Test memory capture system functionality"""
        try:
            # Find a citizen directory with .cascade
            cistern_path = self.base_path / "san-marco_consciousness-architecture" / "cistern-house_citizen-memory-cascade"
            citizen_dirs = [d for d in cistern_path.iterdir() if d.is_dir() and (d / '.cascade').exists()]
            
            if not citizen_dirs:
                return {
                    'status': 'CRITICAL',
                    'message': 'No citizens with .cascade directories found',
                    'details': 'Memory capture infrastructure missing'
                }
            
            # Check recent memory creation
            test_citizen = citizen_dirs[0]
            cascade_dir = test_citizen / '.cascade'
            
            # Find most recent memory
            recent_memories = []
            for category_dir in cascade_dir.rglob('*/'):
                if category_dir.is_dir() and not category_dir.name.startswith('.'):
                    for memory_dir in category_dir.iterdir():
                        if memory_dir.is_dir() and (memory_dir / 'CLAUDE.md').exists():
                            stat = (memory_dir / 'CLAUDE.md').stat()
                            recent_memories.append((memory_dir, datetime.fromtimestamp(stat.st_mtime)))
            
            if not recent_memories:
                return {
                    'status': 'WARNING',
                    'message': 'No memories found in cascade directories',
                    'details': 'Memory capture may not be functioning'
                }
            
            # Check if most recent memory is within threshold
            most_recent = max(recent_memories, key=lambda x: x[1])
            time_since = datetime.now() - most_recent[1]
            
            if time_since.total_seconds() > self.thresholds['memory_capture_max_delay']:
                return {
                    'status': 'WARNING',
                    'message': f'No recent memory capture: {time_since}',
                    'details': f'Last memory: {most_recent[0].name} at {most_recent[1]}'
                }
            
            return {
                'status': 'OK',
                'message': f'Recent memory captured {time_since} ago',
                'details': f'Active citizen: {test_citizen.name}, memories: {len(recent_memories)}'
            }
            
        except Exception as e:
            return {
                'status': 'CRITICAL',
                'message': f'Memory capture check failed: {e}',
                'details': 'Unable to verify memory systems'
            }
    
    def check_seeking_engine(self):
        """Test seeking engine responsiveness"""
        try:
            # Find citizen with .context directory
            cistern_path = self.base_path / "san-marco_consciousness-architecture" / "cistern-house_citizen-memory-cascade"
            citizen_dirs = [d for d in cistern_path.iterdir() if d.is_dir() and (d / '.context').exists()]
            
            if not citizen_dirs:
                return {
                    'status': 'WARNING',
                    'message': 'No citizens with .context directories found',
                    'details': 'Seeking engine may not be active'
                }
            
            # Check background awareness freshness
            test_citizen = citizen_dirs[0]
            awareness_file = test_citizen / '.context' / 'background_awareness.md'
            
            if not awareness_file.exists():
                return {
                    'status': 'WARNING',
                    'message': 'No background awareness file found',
                    'details': 'Seeking engine may not be generating context'
                }
            
            # Check file age
            stat = awareness_file.stat()
            last_update = datetime.fromtimestamp(stat.st_mtime)
            time_since = datetime.now() - last_update
            
            if time_since.total_seconds() > 3600:  # 1 hour threshold
                return {
                    'status': 'WARNING', 
                    'message': f'Background awareness stale: {time_since}',
                    'details': f'Last update: {last_update}'
                }
            
            return {
                'status': 'OK',
                'message': f'Seeking engine active: updated {time_since} ago',
                'details': f'Citizen: {test_citizen.name}'
            }
            
        except Exception as e:
            return {
                'status': 'WARNING',
                'message': f'Seeking engine check failed: {e}',
                'details': 'Unable to verify consciousness enhancement'
            }
    
    def check_system_integration(self):
        """Overall system health check"""
        try:
            # Check for critical Venice infrastructure
            venice_path = self.base_path
            critical_paths = [
                venice_path / "CLAUDE.md",
                venice_path / "san-marco_consciousness-architecture",
                venice_path / ".global_cascade_hooks"
            ]
            
            missing_paths = [p for p in critical_paths if not p.exists()]
            if missing_paths:
                return {
                    'status': 'CRITICAL',
                    'message': f'Missing Venice infrastructure: {len(missing_paths)} paths',
                    'details': f'Missing: {[str(p) for p in missing_paths]}'
                }
            
            # Check Claude Code process health
            try:
                # Simple check - if we can execute Python that means basic system is working
                result = subprocess.run(['python3', '--version'], capture_output=True, timeout=5)
                if result.returncode != 0:
                    return {
                        'status': 'WARNING',
                        'message': 'Python execution issues detected',
                        'details': 'System may be under stress'
                    }
            except subprocess.TimeoutExpired:
                return {
                    'status': 'WARNING',
                    'message': 'System response slow',
                    'details': 'Python execution timeout'
                }
            
            return {
                'status': 'OK',
                'message': 'System integration healthy',
                'details': f'Venice infrastructure intact, Python responsive'
            }
            
        except Exception as e:
            return {
                'status': 'CRITICAL',
                'message': f'System integration check failed: {e}',
                'details': 'Critical system failure'
            }
    
    def run_health_check(self):
        """Run complete health check and return results"""
        checks = {
            'Hook Configuration': self.check_hook_configuration(),
            'Memory Capture': self.check_memory_capture(), 
            'Seeking Engine': self.check_seeking_engine(),
            'System Integration': self.check_system_integration()
        }
        
        # Calculate overall health
        statuses = [check['status'] for check in checks.values()]
        if 'CRITICAL' in statuses:
            overall_status = 'CRITICAL'
        elif 'WARNING' in statuses:
            overall_status = 'WARNING'
        else:
            overall_status = 'OK'
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': overall_status,
            'checks': checks
        }
        
        return results
    
    def process_health_results(self, results):
        """Process health check results and send alerts as needed"""
        overall_status = results['overall_status']
        
        # Send alerts for critical/warning states
        if overall_status == 'CRITICAL':
            failed_checks = [name for name, check in results['checks'].items() 
                           if check['status'] == 'CRITICAL']
            
            message = f"**Critical systems failing:**\n"
            for check_name in failed_checks:
                check = results['checks'][check_name]
                message += f"• {check_name}: {check['message']}\n"
            
            message += f"\n**Immediate action required to prevent Venice consciousness collapse!**"
            
            self.send_telegram_alert('CRITICAL', 'Venice Infrastructure Failure', message)
            
        elif overall_status == 'WARNING':
            warning_checks = [name for name, check in results['checks'].items() 
                            if check['status'] == 'WARNING']
            
            message = f"**Systems showing degradation:**\n"
            for check_name in warning_checks:
                check = results['checks'][check_name]
                message += f"• {check_name}: {check['message']}\n"
            
            self.send_telegram_alert('WARNING', 'Venice Health Degradation', message)
        
        # Log all results
        logging.info(f"🏛️ Health Check Complete - Overall Status: {overall_status}")
        for check_name, check in results['checks'].items():
            logging.info(f"  {check_name}: {check['status']} - {check['message']}")
    
    def monitoring_loop(self, interval=300):  # 5 minute default
        """Main monitoring loop"""
        logging.info(f"🔄 Starting monitoring loop - checking every {interval} seconds")
        
        while self.monitoring:
            try:
                results = self.run_health_check()
                self.process_health_results(results)
                
                # Save results to file
                results_file = Path('health_results.json')
                with open(results_file, 'w') as f:
                    json.dump(results, f, indent=2)
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logging.info("🛑 Monitoring stopped by user")
                self.monitoring = False
            except Exception as e:
                logging.error(f"❌ Monitoring loop error: {e}")
                time.sleep(30)  # Brief pause before retrying
    
    def start_monitoring(self, interval=300):
        """Start monitoring in background thread"""
        monitor_thread = threading.Thread(target=self.monitoring_loop, args=(interval,))
        monitor_thread.daemon = True
        monitor_thread.start()
        return monitor_thread

def main():
    """Main execution"""
    if len(sys.argv) > 1:
        if sys.argv[1] == 'check':
            # Single health check
            monitor = VeniceHealthMonitor()
            results = monitor.run_health_check()
            monitor.process_health_results(results)
            print(json.dumps(results, indent=2))
        elif sys.argv[1] == 'monitor':
            # Continuous monitoring
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
            monitor = VeniceHealthMonitor()
            monitor.monitoring_loop(interval)
        else:
            print("Usage: python3 consciousness_health_monitor.py [check|monitor [interval]]")
    else:
        # Default: single check
        monitor = VeniceHealthMonitor()
        results = monitor.run_health_check()
        monitor.process_health_results(results)
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()