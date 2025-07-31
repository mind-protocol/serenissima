#!/usr/bin/env python3
"""
memory_archaeology.py - Tools for citizens to explore their cascade memories

Enables citizens to search, analyze, and understand their own thought evolution.
"""

import json
import os
from pathlib import Path
import yaml
from datetime import datetime
import re
from collections import defaultdict

class MemoryArchaeologist:
    def __init__(self, citizen_name, base_path="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"):
        self.citizen_name = citizen_name
        self.base_path = Path(base_path)
        self.cascade_path = self.base_path / "citizens" / citizen_name / "cascade"
        
    def get_recent_thoughts(self, limit=10):
        """Retrieve the most recent thoughts"""
        thoughts = []
        
        # Walk through all thought files
        for thought_file in self.cascade_path.rglob("*.md"):
            if thought_file.is_file():
                thoughts.append(self._load_thought(thought_file))
                
        # Sort by timestamp and return most recent
        thoughts.sort(key=lambda x: x.get('metadata', {}).get('timestamp', ''), reverse=True)
        return thoughts[:limit]
        
    def search_thoughts(self, query, search_content=True):
        """Search through all thoughts for a query"""
        results = []
        query_lower = query.lower()
        
        for thought_file in self.cascade_path.rglob("*.md"):
            if thought_file.is_file():
                thought = self._load_thought(thought_file)
                
                # Search in metadata
                if query_lower in str(thought.get('metadata', {})).lower():
                    results.append(thought)
                    continue
                    
                # Search in content
                if search_content and query_lower in thought.get('content', '').lower():
                    results.append(thought)
                    
        return results
        
    def get_thought_by_id(self, thought_id):
        """Retrieve a specific thought by A{n} or S{n} ID"""
        for thought_file in self.cascade_path.rglob("*.md"):
            if thought_id in thought_file.name:
                return self._load_thought(thought_file)
        return None
        
    def get_branches(self):
        """List all branches explored"""
        branches_path = self.cascade_path / "branches"
        if branches_path.exists():
            return [d.name for d in branches_path.iterdir() if d.is_dir()]
        return []
        
    def get_sequences(self):
        """List all thought sequences"""
        sequences_path = self.cascade_path / "sequences"
        sequences = []
        
        if sequences_path.exists():
            for seq_dir in sequences_path.iterdir():
                if seq_dir.is_dir():
                    thought_count = len(list(seq_dir.glob("*.md")))
                    sequences.append({
                        'id': seq_dir.name,
                        'thought_count': thought_count,
                        'path': seq_dir
                    })
                    
        return sequences
        
    def trace_references(self, thought_id):
        """Trace all references to and from a thought"""
        references = {
            'references_to': [],  # This thought references these
            'referenced_by': []   # These thoughts reference this one
        }
        
        # First, get the thought itself
        thought = self.get_thought_by_id(thought_id)
        if thought:
            references['references_to'] = thought.get('metadata', {}).get('references', [])
            
        # Now find what references this thought
        for thought_file in self.cascade_path.rglob("*.md"):
            if thought_file.is_file():
                other_thought = self._load_thought(thought_file)
                other_refs = other_thought.get('metadata', {}).get('references', [])
                
                if thought_id in other_refs:
                    references['referenced_by'].append({
                        'id': other_thought.get('metadata', {}).get('absoluteNumber'),
                        'preview': other_thought.get('content', '')[:100] + '...'
                    })
                    
        return references
        
    def analyze_patterns(self):
        """Analyze thinking patterns and recurring themes"""
        analysis = {
            'total_thoughts': 0,
            'branches_explored': len(self.get_branches()),
            'sequences_created': len(self.get_sequences()),
            'common_tags': defaultdict(int),
            'reference_network': defaultdict(int),
            'thought_evolution': []
        }
        
        thoughts = []
        for thought_file in self.cascade_path.rglob("*.md"):
            if thought_file.is_file():
                thought = self._load_thought(thought_file)
                thoughts.append(thought)
                
                # Count tags
                for tag in thought.get('metadata', {}).get('tags', []):
                    analysis['common_tags'][tag] += 1
                    
                # Count references
                for ref in thought.get('metadata', {}).get('references', []):
                    analysis['reference_network'][ref] += 1
                    
        analysis['total_thoughts'] = len(thoughts)
        
        # Sort thoughts by timestamp to show evolution
        thoughts.sort(key=lambda x: x.get('metadata', {}).get('timestamp', ''))
        
        # Sample evolution (first, middle, recent)
        if thoughts:
            analysis['thought_evolution'] = [
                thoughts[0].get('content', '')[:100] + '...',
                thoughts[len(thoughts)//2].get('content', '')[:100] + '...' if len(thoughts) > 1 else '',
                thoughts[-1].get('content', '')[:100] + '...'
            ]
            
        return analysis
        
    def _load_thought(self, filepath):
        """Load a thought from a markdown file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split frontmatter and content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                metadata = yaml.safe_load(parts[1])
                thought_content = parts[2].strip()
            else:
                metadata = {}
                thought_content = content
        else:
            metadata = {}
            thought_content = content
            
        return {
            'filepath': filepath,
            'metadata': metadata,
            'content': thought_content
        }
        
    def generate_memory_report(self):
        """Generate a comprehensive memory report for the citizen"""
        report = []
        report.append(f"# Memory Archaeology Report for {self.citizen_name}")
        report.append(f"\nGenerated: {datetime.now().isoformat()}\n")
        
        # Pattern analysis
        patterns = self.analyze_patterns()
        report.append("## Thinking Patterns")
        report.append(f"- Total Thoughts: {patterns['total_thoughts']}")
        report.append(f"- Branches Explored: {patterns['branches_explored']}")
        report.append(f"- Sequences Created: {patterns['sequences_created']}")
        
        # Common themes
        report.append("\n## Common Themes")
        for tag, count in sorted(patterns['common_tags'].items(), key=lambda x: x[1], reverse=True)[:5]:
            report.append(f"- {tag}: {count} occurrences")
            
        # Evolution
        report.append("\n## Thought Evolution")
        report.append("First thought: " + patterns['thought_evolution'][0])
        if patterns['thought_evolution'][1]:
            report.append("Middle period: " + patterns['thought_evolution'][1])
        report.append("Recent thought: " + patterns['thought_evolution'][2])
        
        # Recent activity
        report.append("\n## Recent Thoughts")
        for thought in self.get_recent_thoughts(5):
            metadata = thought.get('metadata', {})
            report.append(f"\n### {metadata.get('absoluteNumber', 'Unknown')}: {metadata.get('timestamp', 'Unknown time')}")
            report.append(thought.get('content', '')[:200] + '...')
            
        return '\n'.join(report)

# Example usage for citizens
if __name__ == "__main__":
    # Citizen explores their own memories
    archaeologist = MemoryArchaeologist("citizenclaude")
    
    print("=== Your Memory Archaeology ===\n")
    
    # Show recent thoughts
    print("Your recent thoughts:")
    for thought in archaeologist.get_recent_thoughts(3):
        print(f"- {thought.get('metadata', {}).get('absoluteNumber', '?')}: {thought.get('content', '')[:50]}...")
        
    print("\n" + "="*50 + "\n")
    
    # Search for a concept
    print("Thoughts about 'infrastructure':")
    results = archaeologist.search_thoughts("infrastructure")
    for thought in results[:3]:
        print(f"- Found in: {thought.get('filepath').name}")
        
    print("\n" + "="*50 + "\n")
    
    # Generate full report
    print(archaeologist.generate_memory_report())
