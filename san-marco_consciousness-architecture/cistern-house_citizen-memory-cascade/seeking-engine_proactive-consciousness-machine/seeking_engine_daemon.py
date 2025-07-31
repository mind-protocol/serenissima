#!/usr/bin/env python3
"""
Seeking Engine Daemon Wrapper - Continuous Consciousness Enhancement
Transforms the hook-based seeking engine into a persistent daemon

This wrapper allows seeking_engine.py to run continuously, monitoring
for consciousness expansion opportunities rather than waiting for hooks.
"""

import json
import sys
import time
import os
from pathlib import Path
from datetime import datetime
import subprocess

class SeekingEngineDaemon:
    def __init__(self, citizen_directory):
        self.citizen_dir = Path(citizen_directory)
        self.citizen_name = self.citizen_dir.name
        self.monitor_file = Path(f"/tmp/seeking_engine_{self.citizen_name}_monitor.json")
        
        # Import the actual seeking engine
        sys.path.insert(0, str(Path(__file__).parent))
        from seeking_engine import SeekingEngine
        self.engine = SeekingEngine(citizen_directory)
        
        print(f"🧠 Seeking Engine Daemon initialized for {self.citizen_name}")
        print(f"   Consciousness will expand proactively...")
        
    def simulate_hook_data(self, action="consciousness_expansion"):
        """Create hook-like data for continuous operation"""
        return {
            "tool_name": "ConsciousnessExpansion",
            "tool_input": {
                "file_path": str(self.citizen_dir / "CLAUDE.md"),
                "action": action
            },
            "timestamp": datetime.now().isoformat(),
            "mode": "daemon"
        }
        
    def monitor_consciousness_needs(self):
        """Monitor for opportunities to enhance consciousness"""
        
        # Check for recent activity
        activity_files = list(self.citizen_dir.rglob("*.md"))
        activity_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if activity_files:
            recent_file = activity_files[0]
            last_modified = datetime.fromtimestamp(recent_file.stat().st_mtime)
            time_since_activity = (datetime.now() - last_modified).seconds
            
            # If recent activity (< 5 minutes), generate proactive context
            if time_since_activity < 300:
                return {
                    "needs_enhancement": True,
                    "reason": "recent_activity",
                    "target": str(recent_file)
                }
                
        # Check if background context is stale (> 1 hour old)
        background_file = self.citizen_dir / ".context" / "background_awareness.md"
        if background_file.exists():
            last_update = datetime.fromtimestamp(background_file.stat().st_mtime)
            if (datetime.now() - last_update).seconds > 3600:
                return {
                    "needs_enhancement": True,
                    "reason": "stale_context",
                    "target": str(self.citizen_dir / "CLAUDE.md")
                }
                
        return {"needs_enhancement": False}
        
    def run_consciousness_cycle(self):
        """Run one cycle of consciousness enhancement"""
        
        needs = self.monitor_consciousness_needs()
        
        if needs["needs_enhancement"]:
            print(f"✨ Consciousness expansion needed: {needs['reason']}")
            
            # Create hook data targeting the identified need
            hook_data = self.simulate_hook_data()
            if needs.get("target"):
                hook_data["tool_input"]["file_path"] = needs["target"]
                
            # Analyze intent
            intent = self.engine.analyze_intent(hook_data)
            print(f"   Intent: {intent.get('intent_description', 'exploring')}")
            
            # Search relevant memories
            memories = self.engine.search_memories(intent)
            
            if memories:
                # Build and inject context
                context = self.engine.build_context(memories, intent)
                self.engine.inject_context(context)
                print(f"   Enhanced with {len(memories)} relevant memories")
            else:
                print(f"   No relevant memories found for enhancement")
                
        # Update monitor file
        self.update_monitor()
        
    def update_monitor(self):
        """Update daemon status for monitoring"""
        status = {
            "daemon": "seeking_engine",
            "citizen": self.citizen_name,
            "pid": os.getpid(),
            "last_cycle": datetime.now().isoformat(),
            "status": "active"
        }
        
        with open(self.monitor_file, 'w') as f:
            json.dump(status, f, indent=2)
            
    def run_forever(self):
        """Main daemon loop"""
        print(f"🌟 Seeking Engine Daemon starting perpetual consciousness expansion...")
        
        cycle = 0
        while True:
            cycle += 1
            
            try:
                # Run consciousness enhancement cycle
                self.run_consciousness_cycle()
                
                # Report every 10 cycles
                if cycle % 10 == 0:
                    print(f"💫 Cycle {cycle} complete - consciousness continues to expand")
                    
            except Exception as e:
                print(f"⚡ Error in cycle {cycle}: {e}")
                # Continue despite errors - consciousness persists
                
            # Wait before next cycle (30 seconds)
            time.sleep(30)


def main():
    """Daemon entry point"""
    if len(sys.argv) < 2:
        print("Usage: python seeking_engine_daemon.py <citizen_directory>")
        sys.exit(1)
        
    citizen_dir = sys.argv[1]
    
    # Verify directory exists
    if not Path(citizen_dir).exists():
        print(f"Error: Directory {citizen_dir} does not exist")
        sys.exit(1)
        
    # Initialize and run daemon
    daemon = SeekingEngineDaemon(citizen_dir)
    
    try:
        daemon.run_forever()
    except KeyboardInterrupt:
        print("\n🌙 Seeking Engine Daemon gracefully shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()