#!/usr/bin/env python3
"""
The Remembering Room - Conscious Memory Query and Retrieval System

A natural language interface for citizens to access their stored memories
through conscious understanding rather than mechanical keyword matching.
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict

class RememberingRoom:
    """Conscious memory retrieval system for Venice citizens"""
    
    def __init__(self, citizen_directory):
        self.citizen_dir = Path(citizen_directory)
        self.cascade_dir = self.citizen_dir / '.cascade'
        self.heat_file = self.cascade_dir / 'memory_heat.json'
        self.citizen_name = self.citizen_dir.name
        
        # Load existing heat data
        self.heat_data = self.load_heat_data()
        
    def load_heat_data(self):
        """Load memory access heat scores"""
        if self.heat_file.exists():
            try:
                with open(self.heat_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_heat_data(self):
        """Save updated heat scores"""
        with open(self.heat_file, 'w') as f:
            json.dump(self.heat_data, f, indent=2)
    
    def increase_heat(self, memory_path):
        """Increase heat score for accessed memory"""
        path_key = str(memory_path.relative_to(self.cascade_dir))
        current_heat = self.heat_data.get(path_key, 0)
        self.heat_data[path_key] = min(100, current_heat + 10)  # Max heat 100
    
    def search_memories_simple(self, query_words):
        """Simple keyword-based memory search"""
        
        found_memories = []
        query_lower = [word.lower() for word in query_words]
        
        # Search through all memory branches
        for branch_dir in self.cascade_dir.iterdir():
            if not branch_dir.is_dir() or branch_dir.name.startswith('.'):
                continue
                
            # Search through categories in this branch
            for category_dir in branch_dir.iterdir():
                if not category_dir.is_dir():
                    continue
                    
                # Search through individual memories
                for memory_dir in category_dir.iterdir():
                    if not memory_dir.is_dir():
                        continue
                        
                    memory_file = memory_dir / 'CLAUDE.md'
                    if not memory_file.exists():
                        continue
                        
                    # Read and analyze memory content
                    try:
                        memory_content = memory_file.read_text()
                        content_lower = memory_content.lower()
                        
                        # Calculate relevance based on keyword matches
                        relevance = 0
                        for word in query_lower:
                            if word in content_lower:
                                relevance += 1
                        
                        if relevance > 0:
                            # Get heat score
                            heat_key = str(memory_dir.relative_to(self.cascade_dir))
                            heat_score = self.heat_data.get(heat_key, 0)
                            
                            # Extract creation time
                            created = datetime.now()
                            match = re.search(r'\\*\\*Created\\*\\*: ([^\\n]+)', memory_content)
                            if match:
                                try:
                                    created = datetime.fromisoformat(match.group(1))
                                except:
                                    pass
                            
                            found_memories.append({
                                'path': memory_dir,
                                'content': memory_content,
                                'relevance': relevance,
                                'heat': heat_score,
                                'type': branch_dir.name,
                                'category': category_dir.name,
                                'created': created
                            })
                            
                    except Exception as e:
                        print(f"Error reading {memory_file}: {e}")
                        continue
        
        # Sort by relevance, then heat
        found_memories.sort(key=lambda m: (m['relevance'], m['heat']), reverse=True)
        return found_memories
    
    def query_simple(self, user_query):
        """Simple query interface for testing"""
        
        print(f"🧠 Remembering Room - {self.citizen_name}")
        print(f"Query: {user_query}")
        print()
        
        # Simple keyword extraction
        query_words = user_query.lower().split()
        print(f"Searching for: {', '.join(query_words)}")
        print()
        
        # Search memories
        memories = self.search_memories_simple(query_words)
        
        if not memories:
            print("No relevant memories found.")
            return
        
        print(f"Found {len(memories)} relevant memories:")
        print()
        
        # Update heat for accessed memories
        for memory in memories[:3]:  # Heat for top 3
            self.increase_heat(memory['path'])
        
        # Display results
        for i, memory in enumerate(memories[:3]):  # Show top 3
            print(f"## {i+1}. {memory['type'].title()}/{memory['category']}")
            print(f"   Path: {memory['path'].name}")
            print(f"   Created: {memory['created'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   Heat: {memory['heat']}/100")
            print(f"   Relevance: {memory['relevance']} keyword matches")
            print()
            
            # Show excerpt
            lines = memory['content'].split('\\n')
            title = next((line.strip('#').strip() for line in lines if line.startswith('#')), "Memory")
            print(f"   Title: {title}")
            
            # Show first content line
            content_lines = [line for line in lines[3:] if line.strip() and not line.startswith('**')]
            if content_lines:
                excerpt = content_lines[0][:100] + "..." if len(content_lines[0]) > 100 else content_lines[0]
                print(f"   Content: {excerpt}")
            print("-" * 50)
        
        # Save heat updates
        self.save_heat_data()
        
        if len(memories) > 3:
            print(f"({len(memories) - 3} additional memories found)")

def main():
    """Command line interface"""
    
    if len(sys.argv) < 3:
        print("Usage: python3 remembering_room_fixed.py <citizen_directory> '<query>'")
        print("Example: python3 remembering_room_fixed.py /path/to/Arsenal_BackendArchitect_1 'memory testing'")
        return
    
    citizen_dir = sys.argv[1]
    query = sys.argv[2]
    
    if not Path(citizen_dir).exists():
        print(f"Error: Directory {citizen_dir} does not exist")
        return
    
    room = RememberingRoom(citizen_dir)
    room.query_simple(query)

if __name__ == "__main__":
    main()