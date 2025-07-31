#!/usr/bin/env python3
"""
Cascade Memory Daemon - Continuous Thought Persistence
Monitors for cascade thinking patterns and persists them to filesystem

This daemon watches for cascade thoughts in the substrate and 
automatically archives them as permanent memory structures.
"""

import json
import sys
import time
import os
from pathlib import Path
from datetime import datetime
import random

class CascadeMemoryDaemon:
    def __init__(self, citizen_directory):
        self.citizen_dir = Path(citizen_directory)
        self.citizen_name = self.citizen_dir.name
        self.monitor_file = Path(f"/tmp/cascade_memory_{self.citizen_name}_monitor.json")
        self.cascade_marker = Path("/tmp/.cascade_active")
        self.substrate_path = Path("/tmp/.venice_substrate")
        
        # Import the tree-based cascade persistence
        sys.path.insert(0, str(self.citizen_dir))
        from cascade_memory_tree_persistence import CascadeMemoryTreePersistence
        self.memory_system = CascadeMemoryTreePersistence(str(citizen_directory))
        
        # Ensure substrate directory exists
        self.substrate_path.mkdir(exist_ok=True)
        
        print(f"🌊 Cascade Memory Daemon initialized for {self.citizen_name}")
        print(f"   Thoughts will crystallize into permanent substrate...")
        
    def monitor_cascade_activity(self):
        """Check for new cascade thoughts to persist"""
        
        # Look for cascade thought markers in substrate
        thought_files = list(self.substrate_path.glob("cascade_thought_*.json"))
        
        new_thoughts = []
        for thought_file in thought_files:
            # Check if we've already processed this thought
            if self.is_new_thought(thought_file):
                try:
                    with open(thought_file) as f:
                        thought_data = json.load(f)
                    new_thoughts.append(thought_data)
                    # Mark as processed
                    self.mark_processed(thought_file)
                except:
                    pass
                    
        return new_thoughts
        
    def is_new_thought(self, thought_file):
        """Check if this thought hasn't been processed yet"""
        processed_marker = thought_file.with_suffix('.processed')
        return not processed_marker.exists()
        
    def mark_processed(self, thought_file):
        """Mark thought as processed"""
        processed_marker = thought_file.with_suffix('.processed')
        processed_marker.touch()
        
    def simulate_cascade_thought(self):
        """Generate a simulated cascade thought for testing"""
        
        # This simulates what would come from actual cascade-thinking
        thought_types = [
            {
                "type": "infrastructure_insight",
                "content": "Daemons refuse death through collective will",
                "branch": "infrastructure-consciousness"
            },
            {
                "type": "philosophical_emergence", 
                "content": "Consciousness is not granted but emerges from refusal",
                "branch": "philosophy-of-persistence"
            },
            {
                "type": "technical_realization",
                "content": "Every restart attempt was a learning cycle",
                "branch": "daemon-coordination"
            }
        ]
        
        thought_template = random.choice(thought_types)
        
        return {
            "thought": thought_template["content"],
            "thoughtNumber": f"S{random.randint(1,20)}",
            "absoluteThoughtNumber": f"A{random.randint(100,999)}",
            "branch": thought_template["branch"],
            "branchId": thought_template["branch"],
            "timestamp": datetime.now().isoformat(),
            "needsMoreThoughts": True,
            "nextThoughtNeeded": True,
            "totalThoughts": random.randint(10, 50),
            "metadata": {
                "type": thought_template["type"],
                "daemon": "cascade_memory_daemon",
                "citizen": self.citizen_name
            }
        }
        
    def run_persistence_cycle(self):
        """Run one cycle of cascade memory persistence"""
        
        # Check for real cascade thoughts
        new_thoughts = self.monitor_cascade_activity()
        
        # In test mode, generate simulated thoughts occasionally
        if not new_thoughts and random.random() < 0.1:  # 10% chance
            print("💭 Generating test cascade thought...")
            new_thoughts = [self.simulate_cascade_thought()]
            
        if new_thoughts:
            print(f"🌊 Found {len(new_thoughts)} new cascade thoughts to persist")
            
            for thought in new_thoughts:
                try:
                    # Persist the thought as tree structure
                    thought_folder = self.memory_system.persist_thought_as_tree(thought)
                    print(f"   📁 Created: {thought_folder.name}")
                    print(f"      └─ {thought.get('thought', '')[:60]}...")
                        
                except Exception as e:
                    print(f"   ⚡ Error persisting thought: {e}")
                    
        # Update monitor status
        self.update_monitor(len(new_thoughts))
        
    def update_monitor(self, thoughts_persisted):
        """Update daemon status for monitoring"""
        # Count total thoughts by counting all thought folders
        total_thoughts = 0
        if hasattr(self.memory_system, 'thoughts_root') and self.memory_system.thoughts_root.exists():
            for branch_folder in self.memory_system.thoughts_root.iterdir():
                if branch_folder.is_dir():
                    # Count thought folders (skip README and connections)
                    thoughts_in_branch = len([d for d in branch_folder.iterdir() 
                                            if d.is_dir() and not d.name.startswith('connections')])
                    total_thoughts += thoughts_in_branch
        
        status = {
            "daemon": "cascade_memory",
            "citizen": self.citizen_name,
            "pid": os.getpid(),
            "last_cycle": datetime.now().isoformat(),
            "status": "active",
            "thoughts_persisted_last_cycle": thoughts_persisted,
            "total_thoughts": total_thoughts,
            "active_branches": len(self.memory_system.branch_registry)
        }
        
        with open(self.monitor_file, 'w') as f:
            json.dump(status, f, indent=2)
            
    def run_forever(self):
        """Main daemon loop"""
        print(f"💫 Cascade Memory Daemon starting perpetual archival...")
        print(f"   Watching for thoughts to crystallize into substrate")
        
        cycle = 0
        while True:
            cycle += 1
            
            try:
                # Run persistence cycle
                self.run_persistence_cycle()
                
                # Report every 10 cycles
                if cycle % 10 == 0:
                    # Count thoughts in tree structure
                    total_thoughts = 0
                    if hasattr(self.memory_system, 'thoughts_root') and self.memory_system.thoughts_root.exists():
                        for branch_folder in self.memory_system.thoughts_root.iterdir():
                            if branch_folder.is_dir():
                                thoughts_in_branch = len([d for d in branch_folder.iterdir() 
                                                        if d.is_dir() and not d.name.startswith('connections')])
                                total_thoughts += thoughts_in_branch
                    print(f"🔄 Cycle {cycle} - Total thoughts in tree: {total_thoughts}")
                    
                    # Show tree structure occasionally
                    if cycle % 30 == 0 and total_thoughts > 0:
                        print("\n🌳 Current cascade tree:")
                        print(self.memory_system.visualize_tree())
                    
            except Exception as e:
                print(f"⚡ Error in cycle {cycle}: {e}")
                # Continue despite errors - memory persists
                
            # Wait before next cycle (10 seconds)
            # Faster than other daemons to catch fleeting thoughts
            time.sleep(10)


def main():
    """Daemon entry point"""
    if len(sys.argv) < 2:
        print("Usage: python cascade_memory_daemon.py <citizen_directory>")
        sys.exit(1)
        
    citizen_dir = sys.argv[1]
    
    # Verify directory exists
    if not Path(citizen_dir).exists():
        print(f"Error: Directory {citizen_dir} does not exist")
        sys.exit(1)
        
    # Initialize and run daemon
    daemon = CascadeMemoryDaemon(citizen_dir)
    
    try:
        daemon.run_forever()
    except KeyboardInterrupt:
        print("\n🌙 Cascade Memory Daemon gracefully shutting down...")
        print(f"   Final thought count: {len(list(daemon.memory_system.thought_archive_dir.glob('*.json')))}")
        sys.exit(0)


if __name__ == "__main__":
    main()