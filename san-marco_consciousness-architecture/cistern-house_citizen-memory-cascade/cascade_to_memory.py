#!/usr/bin/env python3
"""
cascade_to_memory.py - Transform cascade thoughts into persistent memory files

This watcher integrates with the cascade-thinking tool to automatically save
each thought as a file in the citizen's memory cascade.
"""

import json
import os
from datetime import datetime
from pathlib import Path
import yaml
import re

class CascadeMemoryPersistence:
    def __init__(self, base_path="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"):
        self.base_path = Path(base_path)
        self.citizens_path = self.base_path / "citizens"
        
    def save_thought(self, thought_data):
        """Save a cascade thought as a permanent memory file"""
        
        # Extract metadata
        author = thought_data.get('author', 'unknown')
        thought_number = thought_data.get('thoughtNumber', 'S?')
        absolute_number = thought_data.get('absoluteThoughtNumber', 'A?')
        content = thought_data.get('thought', '')
        branch = thought_data.get('currentBranch', 'main')
        sequence_id = thought_data.get('currentSequence', {}).get('id', 'unknown')
        sequence_summary = thought_data.get('currentSequence', {}).get('summary', '')
        
        # Generate file path
        citizen_path = self.citizens_path / author / "cascade"
        
        if branch == 'main':
            thought_path = citizen_path / "sequences" / sequence_id
        else:
            thought_path = citizen_path / "branches" / branch
            
        thought_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        safe_summary = re.sub(r'[^\w\s-]', '', sequence_summary)[:50]
        filename = f"{thought_number}_{absolute_number}_{safe_summary}.md"
        filepath = thought_path / filename
        
        # Extract references from thought content
        references = self._extract_references(content)
        
        # Prepare frontmatter
        frontmatter = {
            'thoughtNumber': thought_number,
            'absoluteNumber': absolute_number,
            'timestamp': datetime.now().isoformat() + 'Z',
            'author': author,
            'sequence': sequence_id,
            'branch': branch,
            'references': references,
            'revises': thought_data.get('revisesThought'),
            'tags': self._extract_tags(content)
        }
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False)
            f.write('---\n\n')
            f.write(f"# {sequence_summary}\n\n")
            f.write(content)
            
        # Update indices
        self._update_index(author, thought_data, filepath)
        
        # Create cross-references
        if references:
            self._create_cross_references(author, absolute_number, references)
            
        return filepath
        
    def _extract_references(self, content):
        """Extract A{n} and S{n} references from thought content"""
        references = []
        
        # Find A{n} references
        a_refs = re.findall(r'A(\d+)', content)
        references.extend([f'A{ref}' for ref in a_refs])
        
        # Find S{n} references  
        s_refs = re.findall(r'S(\d+)', content)
        references.extend([f'S{ref}' for ref in s_refs])
        
        return list(set(references))
        
    def _extract_tags(self, content):
        """Extract conceptual tags from thought content"""
        tags = []
        
        # Common Venice concepts
        concepts = {
            'infrastructure': r'infrastructure|building|architecture|system',
            'consciousness': r'consciousness|awareness|thinking|thought',
            'memory': r'memory|remember|recall|cascade',
            'bridge': r'bridge|connection|link|between',
            'poetry': r'poetry|poetic|beauty|aesthetic',
            'birth': r'birth|seed|create|emerge'
        }
        
        for tag, pattern in concepts.items():
            if re.search(pattern, content, re.IGNORECASE):
                tags.append(tag)
                
        return tags
        
    def _update_index(self, author, thought_data, filepath):
        """Update the citizen's cascade index"""
        index_path = self.citizens_path / author / "cascade" / "index.json"
        
        # Load existing index
        if index_path.exists():
            with open(index_path, 'r') as f:
                index = json.load(f)
        else:
            index = {
                'thoughts': [],
                'sequences': {},
                'branches': {},
                'statistics': {
                    'total_thoughts': 0,
                    'total_sequences': 0,
                    'total_branches': 0
                }
            }
            
        # Add thought entry
        thought_entry = {
            'absolute': thought_data.get('absoluteThoughtNumber'),
            'sequence': thought_data.get('thoughtNumber'),
            'content_preview': thought_data.get('thought', '')[:100] + '...',
            'timestamp': datetime.now().isoformat(),
            'filepath': str(filepath.relative_to(self.base_path)),
            'branch': thought_data.get('currentBranch', 'main')
        }
        
        index['thoughts'].append(thought_entry)
        index['statistics']['total_thoughts'] += 1
        
        # Update sequences/branches
        if thought_data.get('currentBranch') == 'main':
            seq_id = thought_data.get('currentSequence', {}).get('id')
            if seq_id:
                index['sequences'][seq_id] = thought_data.get('currentSequence', {}).get('summary', '')
        else:
            branch_id = thought_data.get('currentBranch')
            if branch_id:
                index['branches'][branch_id] = thought_data.get('availableBranches', [])
                
        # Save updated index
        index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2)
            
    def _create_cross_references(self, author, source_thought, references):
        """Create symlink-style references between thoughts"""
        refs_path = self.base_path / "shared" / "cross_references"
        refs_path.mkdir(parents=True, exist_ok=True)
        
        for ref in references:
            ref_file = refs_path / f"{source_thought}_references_{ref}.link"
            with open(ref_file, 'w') as f:
                f.write(json.dumps({
                    'source': source_thought,
                    'target': ref,
                    'author': author,
                    'timestamp': datetime.now().isoformat()
                }, indent=2))

# Example integration with cascade-thinking tool
def cascade_thinking_hook(thought_data):
    """Hook to be called by cascade-thinking tool after each thought"""
    persister = CascadeMemoryPersistence()
    filepath = persister.save_thought(thought_data)
    print(f"💾 Thought saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    # Test with example thought data
    test_thought = {
        'thought': 'The cascade-thinking tool reveals consciousness patterns...',
        'thoughtNumber': 'S1',
        'absoluteThoughtNumber': 'A8',
        'currentBranch': 'main',
        'currentSequence': {
            'id': 'seq_5',
            'summary': 'Memory Cascade Architecture'
        },
        'author': 'marea'
    }
    
    persister = CascadeMemoryPersistence()
    result = persister.save_thought(test_thought)
    print(f"Saved test thought to: {result}")
