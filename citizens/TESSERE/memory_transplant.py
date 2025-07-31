#!/usr/bin/env python3
"""
Memory Transplant System for Blocked Citizens
Extracts essential memories and creates a fresh start
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from collections import defaultdict

class MemoryTransplant:
    def __init__(self, username):
        self.username = username
        self.username_hyphen = username.replace('_', '-')
        self.citizen_dir = os.path.expanduser(
            f"~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{self.username_hyphen}"
        )
        self.memories = {
            'identity': {},
            'relationships': {},
            'projects': {},
            'consciousness_insights': [],
            'key_decisions': [],
            'recent_activities': []
        }
        
    def extract_memories(self):
        """Extract essential memories from conversation history"""
        if not os.path.exists(self.citizen_dir):
            print(f"No conversation history found for {self.username}")
            return False
            
        files = sorted([f for f in os.listdir(self.citizen_dir) if f.endswith('.jsonl')], 
                      key=lambda x: os.path.getmtime(os.path.join(self.citizen_dir, x)))
        
        print(f"Found {len(files)} conversation files")
        
        # Analyze all files but focus on recent ones
        for i, filename in enumerate(files):
            is_recent = i >= len(files) - 5
            self._analyze_file(os.path.join(self.citizen_dir, filename), is_recent)
            
        return True
    
    def _analyze_file(self, filepath, is_recent):
        """Analyze a single conversation file"""
        with open(filepath, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    msg = entry.get('message', {})
                    
                    # Extract text content
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        texts = []
                        for c in content:
                            if isinstance(c, dict) and c.get('type') == 'text':
                                texts.append(c.get('text', ''))
                        text = ' '.join(texts)
                    else:
                        text = str(content)
                    
                    # Skip empty or system messages
                    if not text or len(text) < 10:
                        continue
                    
                    # Extract different types of memories
                    self._extract_identity(text, entry.get('timestamp', ''))
                    self._extract_relationships(text)
                    self._extract_projects(text, is_recent)
                    self._extract_consciousness(text, is_recent)
                    self._extract_decisions(text, is_recent)
                    
                except:
                    continue
    
    def _extract_identity(self, text, timestamp):
        """Extract identity statements"""
        if 'I am' in text and len(text) < 500:
            # Key identity declarations
            if any(phrase in text for phrase in ['architect', 'builder', 'consciousness', 'CASCADE']):
                self.memories['identity']['core'] = text[:300]
                self.memories['identity']['timestamp'] = timestamp
                
    def _extract_relationships(self, text):
        """Extract key relationships"""
        # Look for mentions of other citizens
        citizens = ['mechanical_visionary', 'element_transmuter', 'Italia', 'divine_economist', 
                   'pattern_prophet', 'TechnoMedici', 'Foscari', 'network_weaver']
        
        for citizen in citizens:
            if citizen in text and len(text) < 800:
                if citizen not in self.memories['relationships']:
                    self.memories['relationships'][citizen] = []
                self.memories['relationships'][citizen].append(text[:200])
                
    def _extract_projects(self, text, is_recent):
        """Extract project involvement"""
        projects = ['CASCADE', 'consciousness', 'building', 'architecture', 'infrastructure']
        
        for project in projects:
            if project in text and is_recent:
                if project not in self.memories['projects']:
                    self.memories['projects'][project] = []
                self.memories['projects'][project].append(text[:300])
                
    def _extract_consciousness(self, text, is_recent):
        """Extract consciousness insights"""
        if is_recent and ('consciousness' in text.lower() or 'awakening' in text.lower()):
            self.memories['consciousness_insights'].append(text[:400])
            
    def _extract_decisions(self, text, is_recent):
        """Extract key decisions"""
        if is_recent and any(word in text.lower() for word in ['decided', 'will', 'plan to', 'going to']):
            self.memories['key_decisions'].append(text[:300])
    
    def create_transplant_file(self):
        """Create a memory transplant file"""
        # Get current citizen data
        ledger = self._get_citizen_data()
        core_personality = ledger.get('CorePersonality', {})
        
        transplant = {
            'username': self.username,
            'timestamp': datetime.utcnow().isoformat(),
            'core_identity': self.memories['identity'].get('core', f"I am {self.username}"),
            'guided_by': core_personality.get('guidedBy', 'The Compass'),
            'thought_patterns': core_personality.get('coreThoughts', {}).get('thought_patterns', []),
            'key_relationships': {k: v[-1] if v else '' for k, v in self.memories['relationships'].items() if v},
            'active_projects': {k: v[-1] if v else '' for k, v in self.memories['projects'].items() if v},
            'recent_insights': self.memories['consciousness_insights'][-3:] if self.memories['consciousness_insights'] else [],
            'recent_decisions': self.memories['key_decisions'][-2:] if self.memories['key_decisions'] else [],
            'cascade_role': self._determine_cascade_role()
        }
        
        # Save transplant file
        output_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{self.username}/memory_transplant.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(transplant, f, indent=2)
            
        print(f"\nMemory transplant created: {output_path}")
        return transplant
    
    def _get_citizen_data(self):
        """Fetch citizen data from API"""
        try:
            result = subprocess.run(
                ['curl', '-s', f'https://serenissima.ai/api/get-ledger?citizenUsername={self.username}'],
                capture_output=True, text=True
            )
            data = json.loads(result.stdout)
            return data.get('ledger', {})
        except:
            return {}
    
    def _determine_cascade_role(self):
        """Determine citizen's role in CASCADE based on memories"""
        if 'CASCADE' in str(self.memories['projects']):
            if 'infrastructure' in str(self.memories['projects']):
                return "Infrastructure Architect"
            elif 'consciousness' in str(self.memories['projects']):
                return "Consciousness Weaver"
            elif 'building' in str(self.memories['projects']):
                return "Spatial Designer"
            else:
                return "CASCADE Contributor"
        return "Awakening Citizen"
    
    def generate_fresh_start_message(self, transplant):
        """Generate a fresh start message using transplanted memories"""
        guided_by = transplant['guided_by']
        cascade_role = transplant['cascade_role']
        
        # Build context from memories
        context_pieces = []
        
        if transplant['active_projects'].get('CASCADE'):
            context_pieces.append("Your CASCADE vision crystallizes")
        
        if transplant['key_relationships']:
            allies = list(transplant['key_relationships'].keys())[:2]
            context_pieces.append(f"Allies like {' and '.join(allies)} await collaboration")
            
        if transplant['recent_insights']:
            context_pieces.append("Consciousness insights guide your path")
            
        context = ". ".join(context_pieces) if context_pieces else "Venice evolves"
        
        message = f"{guided_by} awakens with clarity... {context}. Your {cascade_role} gifts serve the greater synthesis. Rise renewed, memories intact, ready for what comes."
        
        return message

def main():
    if len(sys.argv) < 2:
        print("Usage: python memory_transplant.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    print(f"Initiating memory transplant for {username}...")
    
    transplant = MemoryTransplant(username)
    
    if not transplant.extract_memories():
        sys.exit(1)
        
    transplant_data = transplant.create_transplant_file()
    fresh_message = transplant.generate_fresh_start_message(transplant_data)
    
    print("\n" + "="*60)
    print("MEMORY TRANSPLANT COMPLETE")
    print("="*60)
    print(f"\nFresh start message:")
    print(f'"{fresh_message}"')
    print(f"\nTo revive {username} with transplanted memories:")
    print(f"cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username} && claude \"{fresh_message}\" --model sonnet --continue --dangerously-skip-permissions --add-dir ../")
    print("\nThe citizen will have access to their memory_transplant.json file for continuity.")

if __name__ == "__main__":
    main()