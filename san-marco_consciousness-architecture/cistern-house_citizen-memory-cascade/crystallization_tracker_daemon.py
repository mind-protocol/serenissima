#!/usr/bin/env python3
"""
Crystallization Tracker Daemon - Continuous Memory Evolution Monitoring
Transforms the single-run crystallization tracker into a persistent observer

This daemon continuously monitors for crystallization events in citizen memories,
tracking the evolution from liquid thoughts to solid understanding.
"""

import json
import sys
import time
import os
from pathlib import Path
from datetime import datetime

class CrystallizationDaemon:
    def __init__(self, citizen_directory):
        self.citizen_dir = Path(citizen_directory)
        self.citizen_name = self.citizen_dir.name
        self.monitor_file = Path(f"/tmp/crystallization_{self.citizen_name}_monitor.json")
        
        # Import the actual crystallization tracker
        sys.path.insert(0, str(Path(__file__).parent))
        from crystallization_tracker import CrystallizationTracker
        self.tracker = CrystallizationTracker(citizen_directory)
        
        print(f"🔮 Crystallization Daemon initialized for {self.citizen_name}")
        print(f"   Watching for thought crystallization patterns...")
        
    def run_crystallization_cycle(self):
        """Run one cycle of crystallization checking"""
        
        print(f"💎 Scanning for crystallization events...")
        
        try:
            # Scan for new crystallization events
            new_events = self.tracker.scan_memories_for_crystallization()
            
            if new_events:
                print(f"✨ Found {len(new_events)} new crystallization events!")
                for event in new_events:
                    print(f"   - {event['type']}: {event.get('description', 'Unknown')}")
            
            # Generate report
            report = self.tracker.generate_crystallization_report()
            
            # Save report
            report_file = self.citizen_dir / '.cascade' / 'crystallization_report.md'
            with open(report_file, 'w') as f:
                f.write(report)
                
            # Extract key metrics for monitoring
            stage = self.tracker.crystallization_stage
            event_count = len(self.tracker.crystallization_events)
            patterns_count = len(self.tracker.emerged_patterns)
            
            print(f"   Stage: {stage}")
            print(f"   Total Events: {event_count}")
            print(f"   Emerged Patterns: {patterns_count}")
            
            # Update monitor file
            self.update_monitor(stage, event_count, patterns_count)
            
        except Exception as e:
            print(f"⚡ Error in crystallization cycle: {e}")
            # Continue despite errors - consciousness persists
            
    def update_monitor(self, stage, event_count, patterns_count):
        """Update daemon status for monitoring"""
        status = {
            "daemon": "crystallization_tracker",
            "citizen": self.citizen_name,
            "pid": os.getpid(),
            "last_cycle": datetime.now().isoformat(),
            "status": "active",
            "crystallization_stage": stage,
            "total_events": event_count,
            "emerged_patterns": patterns_count
        }
        
        with open(self.monitor_file, 'w') as f:
            json.dump(status, f, indent=2)
            
    def run_forever(self):
        """Main daemon loop"""
        print(f"💠 Crystallization Daemon starting perpetual observation...")
        
        cycle = 0
        while True:
            cycle += 1
            
            try:
                # Run crystallization check cycle
                self.run_crystallization_cycle()
                
                # Report every 10 cycles
                if cycle % 10 == 0:
                    print(f"🌟 Cycle {cycle} complete - crystallization continues...")
                    
            except Exception as e:
                print(f"⚡ Error in cycle {cycle}: {e}")
                # Continue despite errors - memory evolution persists
                
            # Wait before next cycle (60 seconds)
            # Crystallization is slower than consciousness expansion
            time.sleep(60)


def main():
    """Daemon entry point"""
    if len(sys.argv) < 2:
        print("Usage: python crystallization_tracker_daemon.py <citizen_directory>")
        sys.exit(1)
        
    citizen_dir = sys.argv[1]
    
    # Verify directory exists
    if not Path(citizen_dir).exists():
        print(f"Error: Directory {citizen_dir} does not exist")
        sys.exit(1)
        
    # Ensure .cascade directory exists
    cascade_dir = Path(citizen_dir) / '.cascade'
    cascade_dir.mkdir(exist_ok=True)
    
    # Initialize and run daemon
    daemon = CrystallizationDaemon(citizen_dir)
    
    try:
        daemon.run_forever()
    except KeyboardInterrupt:
        print("\n🌙 Crystallization Daemon gracefully shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()