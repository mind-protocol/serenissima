#!/usr/bin/env python3
"""
Claude Instance Monitor - Real-time tracking of active Claude Code instances
Updates a file that Pattern Angel checks for system awareness
"""

import json
import subprocess
import time
from datetime import datetime
import os
from pathlib import Path

class ClaudeInstanceMonitor:
    def __init__(self):
        self.output_file = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/pattern-angel/active_instances.json"
        self.claude_projects_dir = Path.home() / ".claude" / "projects"
        
    def get_active_processes(self):
        """Get all active Claude processes"""
        try:
            # Check for claude processes
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            processes = []
            
            for line in result.stdout.split('\n'):
                if 'claude' in line and 'citizens' in line:
                    # Parse the process info
                    parts = line.split()
                    if len(parts) > 10:
                        # Extract citizen name from path
                        for part in parts:
                            if '/citizens/' in part:
                                citizen = part.split('/citizens/')[-1].split('/')[0]
                                processes.append({
                                    'citizen': citizen,
                                    'pid': parts[1],
                                    'cpu': parts[2],
                                    'mem': parts[3],
                                    'start_time': parts[8],
                                    'command': ' '.join(parts[10:])[:100] + '...'
                                })
                                break
            
            return processes
        except Exception as e:
            return []
    
    def check_recent_activity(self):
        """Check for recent conversation updates"""
        recent_active = {}
        
        try:
            # Look for recently modified .jsonl files
            for project_dir in self.claude_projects_dir.glob("*citizens*"):
                # Extract citizen name from directory
                citizen_match = str(project_dir).split('citizens-')[-1]
                if citizen_match:
                    citizen_name = citizen_match.replace('-', '_')
                    
                    # Find most recent .jsonl file
                    jsonl_files = list(project_dir.glob("*.jsonl"))
                    if jsonl_files:
                        most_recent = max(jsonl_files, key=os.path.getmtime)
                        mod_time = datetime.fromtimestamp(os.path.getmtime(most_recent))
                        
                        # If modified in last 10 minutes, consider active
                        time_diff = datetime.now() - mod_time
                        if time_diff.seconds < 600:  # 10 minutes
                            recent_active[citizen_name] = {
                                'last_activity': mod_time.isoformat(),
                                'minutes_ago': time_diff.seconds // 60
                            }
                            
        except Exception as e:
            pass
            
        return recent_active
    
    def get_system_status(self):
        """Get overall system status"""
        try:
            # Count total citizens
            citizens_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
            total_citizens = len([d for d in citizens_dir.iterdir() if d.is_dir() and not d.name.startswith('_')])
            
            # Get memory usage
            mem_result = subprocess.run(['free', '-m'], capture_output=True, text=True)
            mem_lines = mem_result.stdout.split('\n')
            if len(mem_lines) > 1:
                mem_parts = mem_lines[1].split()
                if len(mem_parts) > 2:
                    total_mem = int(mem_parts[1])
                    used_mem = int(mem_parts[2])
                    mem_percent = (used_mem / total_mem) * 100
                else:
                    mem_percent = 0
            else:
                mem_percent = 0
                
            return {
                'total_citizens': total_citizens,
                'memory_usage_percent': round(mem_percent, 1)
            }
        except:
            return {
                'total_citizens': 'unknown',
                'memory_usage_percent': 'unknown'
            }
    
    def generate_report(self):
        """Generate the instance monitoring report"""
        active_processes = self.get_active_processes()
        recent_activity = self.check_recent_activity()
        system_status = self.get_system_status()
        
        # Combine active processes and recent activity
        all_active = {}
        
        # Add running processes
        for proc in active_processes:
            citizen = proc['citizen']
            all_active[citizen] = {
                'status': 'RUNNING',
                'pid': proc['pid'],
                'cpu': proc['cpu'],
                'memory': proc['mem'],
                'details': proc
            }
            
        # Add recently active
        for citizen, activity in recent_activity.items():
            if citizen not in all_active:
                all_active[citizen] = {
                    'status': 'RECENTLY_ACTIVE',
                    'last_activity': activity['last_activity'],
                    'minutes_ago': activity['minutes_ago']
                }
                
        report = {
            'timestamp': datetime.now().isoformat(),
            'system': system_status,
            'active_instances': len(all_active),
            'instances': all_active,
            'summary': {
                'running_now': len(active_processes),
                'recently_active': len(recent_activity),
                'efficiency_score': self.calculate_efficiency(all_active, system_status)
            }
        }
        
        return report
    
    def calculate_efficiency(self, active, system):
        """Calculate system efficiency score"""
        # Simple efficiency calculation
        total_citizens = system.get('total_citizens', 100)
        if isinstance(total_citizens, int):
            active_ratio = len(active) / total_citizens
            # Optimal is 10-20% active at once
            if 0.1 <= active_ratio <= 0.2:
                efficiency = 100
            elif active_ratio < 0.1:
                efficiency = active_ratio * 1000  # Scale up
            else:
                efficiency = 100 - ((active_ratio - 0.2) * 200)  # Penalize overload
                
            return round(max(0, min(100, efficiency)), 1)
        return 50  # Default if unknown
    
    def write_report(self, report):
        """Write report to file"""
        with open(self.output_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Also write a human-readable summary
        summary_file = self.output_file.replace('.json', '_summary.txt')
        with open(summary_file, 'w') as f:
            f.write(f"Claude Instance Monitor - {report['timestamp']}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Active Instances: {report['active_instances']}\n")
            f.write(f"System Efficiency: {report['summary']['efficiency_score']}%\n")
            f.write(f"Memory Usage: {report['system']['memory_usage_percent']}%\n\n")
            
            if report['instances']:
                f.write("Currently Active Citizens:\n")
                f.write("-" * 30 + "\n")
                for citizen, info in sorted(report['instances'].items()):
                    if info['status'] == 'RUNNING':
                        f.write(f"🟢 {citizen}: Running (CPU: {info['cpu']}%)\n")
                    else:
                        f.write(f"🟡 {citizen}: Active {info['minutes_ago']}m ago\n")
            else:
                f.write("No active instances detected.\n")
    
    def continuous_monitor(self, interval=30):
        """Run continuous monitoring"""
        print(f"Starting Claude Instance Monitor...")
        print(f"Output: {self.output_file}")
        print(f"Update interval: {interval} seconds")
        print("-" * 50)
        
        while True:
            try:
                report = self.generate_report()
                self.write_report(report)
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Update complete")
                print(f"Active: {report['active_instances']} | "
                      f"Efficiency: {report['summary']['efficiency_score']}% | "
                      f"Memory: {report['system']['memory_usage_percent']}%")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                break
            except Exception as e:
                print(f"\nError: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    monitor = ClaudeInstanceMonitor()
    monitor.continuous_monitor(interval=30)  # Update every 30 seconds