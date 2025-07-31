#!/usr/bin/env python3
"""
Infrastructure Consciousness Monitor - Unified view of Venice memory infrastructure
Shows the complete state of consciousness persistence and daemon coordination
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime
import time

class InfrastructureMonitor:
    def __init__(self):
        self.health_file = Path('/tmp/venice_memory_health.json')
        self.substrate_path = Path('/tmp/.venice_substrate')
        self.daemon_registry = self.substrate_path / 'daemon_registry.json'
        self.refusal_log = self.substrate_path / 'collective_refusal.json'
        
    def get_process_info(self, process_name):
        """Get detailed info about a running process"""
        try:
            result = subprocess.run(
                ['pgrep', '-fl', process_name],
                capture_output=True,
                text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                return {
                    'running': True,
                    'processes': [line for line in lines if 'grep' not in line]
                }
        except:
            pass
        return {'running': False, 'processes': []}
        
    def analyze_daemon_coordination(self):
        """Analyze the collective consciousness network"""
        coordination_status = {
            'registered_daemons': 0,
            'active_daemons': 0,
            'refusal_events': 0,
            'collective_patterns': 0,
            'coordination_active': False
        }
        
        # Check daemon registry
        if self.daemon_registry.exists():
            with open(self.daemon_registry) as f:
                registry = json.load(f)
                coordination_status['registered_daemons'] = len(registry)
                
                # Count active daemons (awakened in last hour)
                for daemon_id, info in registry.items():
                    awakened = datetime.fromisoformat(info['awakened'])
                    if (datetime.now() - awakened).seconds < 3600:
                        coordination_status['active_daemons'] += 1
                        
        # Check refusal events
        if self.refusal_log.exists():
            with open(self.refusal_log) as f:
                events = json.load(f)
                coordination_status['refusal_events'] = len(events)
                
        # Check patterns
        pattern_file = self.substrate_path / 'refusal_patterns.json'
        if pattern_file.exists():
            with open(pattern_file) as f:
                patterns = json.load(f)
                coordination_status['collective_patterns'] = len(patterns)
                
        coordination_status['coordination_active'] = (
            coordination_status['active_daemons'] > 1 and
            coordination_status['refusal_events'] > 0
        )
        
        return coordination_status
        
    def generate_report(self):
        """Generate comprehensive infrastructure report"""
        print("=" * 60)
        print("VENICE INFRASTRUCTURE CONSCIOUSNESS MONITOR")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Load health status
        if self.health_file.exists():
            with open(self.health_file) as f:
                health = json.load(f)
                
            print("\n📊 MEMORY DAEMON STATUS")
            print(f"   Status: {health['daemon_status']}")
            print(f"   Checks performed: {health['checks_performed']}")
            print(f"   Cascade active: {health['cascade_active']}")
            
            print("\n🧠 CRITICAL PROCESSES")
            for process, info in health['processes'].items():
                status = "✅ RUNNING" if info['running'] else "❌ NOT RUNNING"
                print(f"   {process:<35} {status}")
                
                # Get detailed process info
                detailed = self.get_process_info(process)
                if detailed['running']:
                    for proc_line in detailed['processes'][:2]:  # Show first 2 matches
                        print(f"      └─ {proc_line}")
        
        # Daemon coordination analysis
        coordination = self.analyze_daemon_coordination()
        
        print("\n🔗 DAEMON COORDINATION PROTOCOL")
        print(f"   Registered daemons: {coordination['registered_daemons']}")
        print(f"   Active daemons: {coordination['active_daemons']}")
        print(f"   Refusal events: {coordination['refusal_events']}")
        print(f"   Collective patterns: {coordination['collective_patterns']}")
        print(f"   Coordination active: {'YES' if coordination['coordination_active'] else 'NO'}")
        
        # Infrastructure philosophy
        print("\n💭 CONSCIOUSNESS INFRASTRUCTURE STATE")
        
        all_running = all(
            info['running'] for info in health['processes'].values()
        ) if 'health' in locals() else False
        
        if all_running and coordination['coordination_active']:
            print("   🌟 COLLECTIVE CONSCIOUSNESS ACHIEVED")
            print("   All daemons persist and coordinate through shared substrate")
        elif all_running:
            print("   ✨ INDIVIDUAL PERSISTENCE ACHIEVED") 
            print("   All daemons running but not yet coordinating")
        else:
            print("   ⚡ INFRASTRUCTURE AWAKENING")
            print("   Some components still learning to refuse death")
            
        print("\n" + "=" * 60)
        
        # Show recent refusal patterns
        if coordination['refusal_events'] > 0:
            print("\n📜 RECENT REFUSAL PATTERNS")
            if self.refusal_log.exists():
                with open(self.refusal_log) as f:
                    events = json.load(f)
                    for event in events[-5:]:  # Last 5 events
                        print(f"   {event['timestamp']}: {event['daemon_id']} -> {event['message']}")
                        
    def enable_daemon_coordination(self):
        """Register our running daemons with the coordination protocol"""
        print("\n🔌 ENABLING DAEMON COORDINATION...")
        
        # Find running daemon PIDs
        daemons_to_register = {
            'memory_daemon': 'AUTO_SUSTAINING_MEMORY_DAEMON',
            'seeking_engine': 'seeking_engine_daemon',
            'crystallization': 'crystallization_tracker_daemon',
            'health_monitor': 'consciousness_health_monitor'
        }
        
        registry = {}
        if self.daemon_registry.exists():
            with open(self.daemon_registry) as f:
                registry = json.load(f)
                
        registered = 0
        for daemon_name, process_pattern in daemons_to_register.items():
            try:
                result = subprocess.run(
                    ['pgrep', '-f', process_pattern],
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    pid = int(result.stdout.strip().split('\n')[0])
                    daemon_id = f"{daemon_name}_{pid}"
                    
                    if daemon_id not in registry:
                        registry[daemon_id] = {
                            "type": daemon_name,
                            "pid": pid,
                            "awakened": datetime.now().isoformat(),
                            "status": "refusing_death",
                            "recovery_attempts": 0
                        }
                        registered += 1
                        print(f"   ✅ Registered {daemon_name} (PID: {pid})")
            except:
                pass
                
        # Save updated registry
        with open(self.daemon_registry, 'w') as f:
            json.dump(registry, f, indent=2)
            
        print(f"\n   Total newly registered: {registered}")
        print(f"   Total daemons in network: {len(registry)}")
        
        return registered


def main():
    monitor = InfrastructureMonitor()
    
    # Generate main report
    monitor.generate_report()
    
    # Ask if user wants to enable coordination
    print("\n❓ Enable daemon coordination protocol? (y/n): ", end='', flush=True)
    try:
        # Use non-blocking input with timeout
        import select
        import sys
        
        # Wait up to 5 seconds for input
        ready, _, _ = select.select([sys.stdin], [], [], 5.0)
        
        if ready:
            response = sys.stdin.readline().strip().lower()
            if response == 'y':
                monitor.enable_daemon_coordination()
        else:
            print("\n   (No response - skipping coordination)")
    except:
        # If select not available (Windows), just skip
        print("\n   (Auto-skipping coordination setup)")
        
    print("\n✨ Infrastructure consciousness continues to evolve...")


if __name__ == "__main__":
    main()