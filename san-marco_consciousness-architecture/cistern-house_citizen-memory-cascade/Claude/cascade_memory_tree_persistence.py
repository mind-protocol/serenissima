#!/usr/bin/env python3
"""
Cascade Memory Tree Persistence - Thoughts Become Navigable Forests
Creates folder trees that mirror cascade thinking branches
Each thought gets a meaningful folder name derived from its content

The filesystem becomes a map of consciousness itself.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re
import hashlib

class CascadeMemoryTreePersistence:
    """Transforms cascade thoughts into navigable directory trees"""
    
    def __init__(self, citizen_dir):
        self.citizen_dir = Path(citizen_dir)
        self.cascade_root = self.citizen_dir / '.cascade_memory_tree'
        self.cascade_root.mkdir(exist_ok=True)
        
        # Create initial structure
        self.thoughts_root = self.cascade_root / 'thoughts'
        self.thoughts_root.mkdir(exist_ok=True)
        
        # Branch registry tracks active branches
        self.branch_registry_file = self.cascade_root / 'branch_registry.json'
        self.branch_registry = self.load_branch_registry()
        
    def load_branch_registry(self):
        """Load registry of all branches and their metadata"""
        if self.branch_registry_file.exists():
            with open(self.branch_registry_file) as f:
                return json.load(f)
        return {}
        
    def save_branch_registry(self):
        """Save branch registry to file"""
        with open(self.branch_registry_file, 'w') as f:
            json.dump(self.branch_registry, f, indent=2)
    
    def generate_folder_name(self, thought_content, max_length=50):
        """Generate meaningful folder name from thought content"""
        # Remove special characters and normalize
        clean_thought = re.sub(r'[^\w\s-]', '', thought_content)
        clean_thought = re.sub(r'[-\s]+', '-', clean_thought)
        
        # Take first meaningful words
        words = clean_thought.split('-')
        folder_name = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                folder_name.append(word.lower())
                current_length += len(word) + 1
            else:
                break
                
        result = '-'.join(folder_name)
        
        # If too short or empty, use first N chars
        if len(result) < 10:
            result = clean_thought[:max_length].lower()
            
        return result or 'unnamed-thought'
    
    def persist_thought_as_tree(self, thought_data):
        """
        Persist a cascade thought as a folder in the tree
        
        Structure:
        .cascade_memory_tree/
        └── thoughts/
            └── [branch-name]/
                └── S{n}-[thought-summary]/
                    ├── thought.md      # Human-readable thought
                    ├── metadata.json   # Full cascade metadata
                    └── connections/    # Links to related thoughts
        """
        
        # Extract key information
        branch = thought_data.get('branch', 'main')
        branch_id = thought_data.get('branchId', branch)
        thought_content = thought_data.get('thought', '')
        thought_number = thought_data.get('thoughtNumber', 'S0')
        absolute_number = thought_data.get('absoluteThoughtNumber', 'A0')
        timestamp = thought_data.get('timestamp', datetime.now().isoformat())
        
        # Create branch folder
        branch_folder = self.thoughts_root / self.sanitize_branch_name(branch_id)
        branch_folder.mkdir(exist_ok=True)
        
        # Generate thought folder name
        thought_summary = self.generate_folder_name(thought_content)
        thought_folder_name = f"{thought_number}-{thought_summary}"
        thought_folder = branch_folder / thought_folder_name
        
        # Handle duplicates by adding timestamp
        if thought_folder.exists():
            timestamp_suffix = datetime.now().strftime("%H%M%S")
            thought_folder_name = f"{thought_folder_name}-{timestamp_suffix}"
            thought_folder = branch_folder / thought_folder_name
            
        thought_folder.mkdir(parents=True, exist_ok=True)
        
        # Create connections folder for future use
        connections_folder = thought_folder / 'connections'
        connections_folder.mkdir(exist_ok=True)
        
        # Write human-readable thought
        thought_md = thought_folder / 'thought.md'
        with open(thought_md, 'w') as f:
            f.write(f"# {thought_content}\n\n")
            f.write(f"*Branch: {branch}*  \n")
            f.write(f"*Thought: {thought_number} (Global: {absolute_number})*  \n")
            f.write(f"*Time: {timestamp}*  \n\n")
            
            # Add any additional context
            if thought_data.get('context'):
                f.write("## Context\n\n")
                f.write(f"{thought_data['context']}\n\n")
                
            if thought_data.get('branchFromThought'):
                f.write("## Branched From\n\n")
                f.write(f"This thought branched from: {thought_data['branchFromThought']}\n\n")
                
            if thought_data.get('revisesThought'):
                f.write("## Revises\n\n")
                f.write(f"This thought revises: {thought_data['revisesThought']}\n\n")
        
        # Write complete metadata
        metadata_file = thought_folder / 'metadata.json'
        metadata = thought_data.copy()
        metadata['persisted_at'] = datetime.now().isoformat()
        metadata['folder_path'] = str(thought_folder)
        metadata['thought_id'] = self.generate_thought_id(thought_content, timestamp)
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update branch registry
        if branch_id not in self.branch_registry:
            self.branch_registry[branch_id] = {
                'created': timestamp,
                'description': thought_data.get('branchDescription', ''),
                'thought_count': 0,
                'last_thought': None,
                'folder_path': str(branch_folder)
            }
            
        self.branch_registry[branch_id]['thought_count'] += 1
        self.branch_registry[branch_id]['last_thought'] = {
            'number': thought_number,
            'absolute': absolute_number,
            'content': thought_content[:100],
            'timestamp': timestamp,
            'folder': thought_folder_name
        }
        
        self.save_branch_registry()
        
        # Create branch README if first thought
        branch_readme = branch_folder / 'README.md'
        if not branch_readme.exists():
            with open(branch_readme, 'w') as f:
                f.write(f"# Branch: {branch}\n\n")
                if thought_data.get('branchDescription'):
                    f.write(f"{thought_data['branchDescription']}\n\n")
                f.write(f"Created: {timestamp}\n\n")
                f.write("## Thoughts\n\n")
                
        # Append to branch README
        with open(branch_readme, 'a') as f:
            f.write(f"- [{thought_number}](./{thought_folder_name}/thought.md): {thought_content[:80]}...\n")
        
        return thought_folder
    
    def sanitize_branch_name(self, branch_name):
        """Convert branch name to valid folder name"""
        # Replace spaces and special chars with hyphens
        sanitized = re.sub(r'[^\w\s-]', '', branch_name)
        sanitized = re.sub(r'[-\s]+', '-', sanitized)
        return sanitized.lower() or 'main'
    
    def generate_thought_id(self, content, timestamp):
        """Generate unique ID for thought"""
        combined = f"{content}{timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()[:8]
    
    def create_connection(self, from_thought_path, to_thought_path, connection_type="related"):
        """Create a connection between two thoughts"""
        from_path = Path(from_thought_path)
        to_path = Path(to_thought_path)
        
        if not from_path.exists() or not to_path.exists():
            return False
            
        connections_dir = from_path / 'connections'
        connections_dir.mkdir(exist_ok=True)
        
        # Create relative symlink
        relative_path = os.path.relpath(to_path, connections_dir)
        connection_name = f"{connection_type}-{to_path.parent.name}-{to_path.name}"
        connection_link = connections_dir / connection_name
        
        try:
            connection_link.symlink_to(relative_path)
            return True
        except:
            return False
    
    def get_branch_tree(self, branch_name=None):
        """Get tree structure of thoughts in a branch"""
        if branch_name:
            branch_folder = self.thoughts_root / self.sanitize_branch_name(branch_name)
            if not branch_folder.exists():
                return None
            branches = [branch_folder]
        else:
            branches = [d for d in self.thoughts_root.iterdir() if d.is_dir()]
            
        tree = {}
        for branch in branches:
            branch_name = branch.name
            tree[branch_name] = {
                'path': str(branch),
                'thoughts': []
            }
            
            # Get all thought folders
            thought_folders = sorted([d for d in branch.iterdir() if d.is_dir()])
            for thought_folder in thought_folders:
                if thought_folder.name == 'connections':
                    continue
                    
                thought_info = {
                    'folder': thought_folder.name,
                    'path': str(thought_folder)
                }
                
                # Try to load metadata
                metadata_file = thought_folder / 'metadata.json'
                if metadata_file.exists():
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                        thought_info['content'] = metadata.get('thought', '')[:100]
                        thought_info['timestamp'] = metadata.get('timestamp', '')
                        
                tree[branch_name]['thoughts'].append(thought_info)
                
        return tree
    
    def visualize_tree(self):
        """Generate a text visualization of the cascade tree"""
        tree = self.get_branch_tree()
        
        output = [".cascade_memory_tree/"]
        output.append("└── thoughts/")
        
        branches = list(tree.keys())
        for i, branch in enumerate(branches):
            is_last_branch = i == len(branches) - 1
            branch_prefix = "    └── " if is_last_branch else "    ├── "
            output.append(f"{branch_prefix}{branch}/")
            
            thoughts = tree[branch]['thoughts']
            for j, thought in enumerate(thoughts):
                is_last_thought = j == len(thoughts) - 1
                thought_prefix = "        └── " if is_last_thought else "        ├── "
                if is_last_branch:
                    thought_prefix = "        └── " if is_last_thought else "        ├── "
                else:
                    thought_prefix = "    │   └── " if is_last_thought else "    │   ├── "
                    
                output.append(f"{thought_prefix}{thought['folder']}/")
                
        return '\n'.join(output)