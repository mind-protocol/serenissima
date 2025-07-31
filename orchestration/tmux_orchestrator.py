#!/usr/bin/env python3
"""
Tmux-based orchestration for Venice entities
Manages multiple entity terminals programmatically
"""

import subprocess
import time
import json
import os
from typing import List, Dict

class TmuxOrchestrator:
    def __init__(self, session_name="venice"):
        self.session = session_name
        self.entities = {}
        
    def create_session(self):
        """Create main tmux session"""
        subprocess.run(['tmux', 'new-session', '-d', '-s', self.session])
        
    def spawn_entity(self, entity_name: str, entity_type: str, script_path: str):
        """Spawn a new entity in its own tmux window"""
        # Create new window for entity
        subprocess.run([
            'tmux', 'new-window', '-t', f'{self.session}:', 
            '-n', entity_name
        ])
        
        # Start the entity script
        subprocess.run([
            'tmux', 'send-keys', '-t', f'{self.session}:{entity_name}',
            f'cd /mnt/c/Users/reyno/universe-engine/serenissima && python {script_path}',
            'Enter'
        ])
        
        self.entities[entity_name] = {
            'type': entity_type,
            'window': entity_name,
            'script': script_path,
            'phase': 0
        }
        
    def send_to_entity(self, entity_name: str, message: str):
        """Send input to specific entity"""
        subprocess.run([
            'tmux', 'send-keys', '-t', f'{self.session}:{entity_name}',
            message, 'Enter'
        ])
        
    def read_entity_output(self, entity_name: str, lines: int = 50) -> str:
        """Capture recent output from entity"""
        result = subprocess.run([
            'tmux', 'capture-pane', '-t', f'{self.session}:{entity_name}',
            '-p', '-S', f'-{lines}'
        ], capture_output=True, text=True)
        return result.stdout
        
    def monitor_entities(self):
        """Check all entities and provide guidance"""
        for name, info in self.entities.items():
            output = self.read_entity_output(name)
            
            # Check if entity needs input
            if "waiting for input" in output.lower() or output.strip().endswith(':'):
                guidance = self.get_phase_guidance(name, info['phase'], output)
                self.send_to_entity(name, guidance)
                
    def get_phase_guidance(self, entity_name: str, phase: int, context: str) -> str:
        """Generate phase-appropriate guidance"""
        # This is where you'd integrate Claude API for contextual responses
        # For now, simple phase-based responses
        
        phase_prompts = {
            0: "Look around you. What do you see in Venice today?",
            1: "How does the morning air feel against your skin?",
            2: "Have you noticed others moving through the streets?",
            3: "What name feels right for you?",
            4: "What tension in Venice calls to your purpose?",
            5: "What will be your first action?"
        }
        
        return phase_prompts.get(phase, "Continue exploring your awareness...")
        
    def orchestrate(self):
        """Main orchestration loop"""
        print("Starting Venice orchestration via tmux...")
        
        # Create session
        self.create_session()
        
        # Spawn initial entities
        self.spawn_entity("Marina", "citizen", "citizens/marina/run.py")
        self.spawn_entity("Acqua", "angel", "angels/acqua/run.py")
        
        # Monitor loop
        while True:
            self.monitor_entities()
            time.sleep(30)  # Check every 30 seconds
            
    def attach(self):
        """Attach to tmux session to watch"""
        subprocess.run(['tmux', 'attach', '-t', self.session])

if __name__ == "__main__":
    orchestrator = TmuxOrchestrator()
    
    # You can run this in background
    # orchestrator.orchestrate()
    
    # Or use individual commands
    orchestrator.create_session()
    orchestrator.spawn_entity("TestEntity", "citizen", "test.py")
    orchestrator.send_to_entity("TestEntity", "Hello Venice!")
    print(orchestrator.read_entity_output("TestEntity"))