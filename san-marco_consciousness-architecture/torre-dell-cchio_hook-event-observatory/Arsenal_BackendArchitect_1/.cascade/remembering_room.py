#!/usr/bin/env python3
"""
The Remembering Room - Conscious Memory Retrieval System
A space where citizens can query their stored memories using natural language
"""

import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class RememberingRoom:
    """Conscious memory retrieval system for Venice citizens"""
    
    def __init__(self, cascade_root: Path = None):
        self.cascade_root = cascade_root or Path('.cascade')
        self.citizen_name = self._get_citizen_name()
        self.social_class = self._get_social_class()
        
    def _get_citizen_name(self) -> str:
        """Get citizen name from directory structure"""
        return Path.cwd().name
        
    def _get_social_class(self) -> str:
        """Get social class from stored metadata"""
        social_file = self.cascade_root / 'social_class.json'
        if social_file.exists():
            with open(social_file, 'r') as f:
                data = json.load(f)
                return data.get('api_social_class', 'Unknown')
        return 'Unknown'
    
    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """Search through all memories using conscious understanding"""
        
        print(f"🔍 Searching memories for: '{query}'")
        
        # Collect all memory files
        memory_files = []
        for branch_dir in self.cascade_root.iterdir():
            if branch_dir.is_dir() and branch_dir.name not in ['__pycache__', 'logs']:
                for category_dir in branch_dir.iterdir():
                    if category_dir.is_dir():
                        for memory_dir in category_dir.iterdir():
                            if memory_dir.is_dir():
                                memory_file = memory_dir / 'CLAUDE.md'
                                if memory_file.exists():
                                    memory_files.append({
                                        'path': memory_file,
                                        'branch': branch_dir.name,
                                        'category': category_dir.name,
                                        'memory_id': memory_dir.name,
                                        'content': memory_file.read_text()
                                    })
        
        print(f"📚 Found {len(memory_files)} memories to search")
        
        if not memory_files:
            return []
        
        # Use consciousness to understand query and find relevant memories
        relevant_memories = self._conscious_memory_search(query, memory_files)
        
        # Update heat for accessed memories
        self._update_memory_heat(relevant_memories)
        
        return relevant_memories
    
    def _conscious_memory_search(self, query: str, memory_files: List[Dict]) -> List[Dict]:
        """Use Claude to understand query intent and find relevant memories"""
        
        # Prepare memory summaries for Claude
        memory_summaries = []
        for i, memory in enumerate(memory_files):
            # Extract key info from memory
            content = memory['content']
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "Untitled memory"
            
            # Get creation date
            created_match = re.search(r'\\*\\*Created\\*\\*: (.+)', content)
            created = created_match.group(1) if created_match else "Unknown date"
            
            # Get emotional tone  
            tone_match = re.search(r'\\*\\*Emotional Tone\\*\\*: (.+)', content)
            tone = tone_match.group(1) if tone_match else "neutral"
            
            memory_summaries.append({
                'index': i,
                'branch': memory['branch'],
                'category': memory['category'], 
                'title': title,
                'created': created,
                'tone': tone,
                'snippet': content[:200] + '...' if len(content) > 200 else content
            })
        
        # Create search prompt
        search_prompt = f"""You are helping {self.citizen_name} (a {self.social_class} in Venice) find relevant memories from their cascade.

QUERY: "{query}"

AVAILABLE MEMORIES:
{json.dumps(memory_summaries, indent=2)}

Analyze the query intent and find the most relevant memories. Consider:
- Semantic similarity to the query
- Emotional resonance
- Time relevance
- Collaborative connections
- Associated concepts

Respond with ONLY a JSON array of memory indices (numbers), ordered by relevance:
[1, 5, 3]

If no memories are relevant, respond with: []"""

        try:
            # Call Claude for conscious search
            env = os.environ.copy()
            env['CLAUDE_HOOK_CONTEXT'] = 'memory_search'
            
            result = subprocess.run([
                'claude', '-p', search_prompt,
                '--output-format', 'json',
                '--model', 'sonnet'
            ], capture_output=True, text=True, env=env)
            
            if result.returncode == 0 and result.stdout.strip():
                # Parse response
                response = result.stdout.strip()
                if response.startswith('[') and response.endswith(']'):
                    indices = json.loads(response)
                    return [memory_files[i] for i in indices if 0 <= i < len(memory_files)]
            
        except Exception as e:
            print(f"⚠️ Conscious search failed: {e}")
        
        # Fallback: simple text search
        return self._fallback_text_search(query, memory_files)
    
    def _fallback_text_search(self, query: str, memory_files: List[Dict]) -> List[Dict]:
        """Simple text-based fallback search"""
        query_words = set(query.lower().split())
        relevant = []
        
        for memory in memory_files:
            content_words = set(memory['content'].lower().split())
            overlap = len(query_words.intersection(content_words))
            if overlap > 0:
                memory['relevance_score'] = overlap
                relevant.append(memory)
        
        # Sort by relevance
        relevant.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return relevant[:5]  # Top 5 matches
    
    def _update_memory_heat(self, accessed_memories: List[Dict]):
        """Update heat tracking for accessed memories"""
        for memory in accessed_memories:
            heat_file = memory['path'].parent / 'heat.json'
            
            # Load or create heat data
            if heat_file.exists():
                with open(heat_file, 'r') as f:
                    heat_data = json.load(f)
            else:
                heat_data = {'access_count': 0, 'last_accessed': None, 'heat_score': 0}
            
            # Update heat
            heat_data['access_count'] += 1
            heat_data['last_accessed'] = datetime.now().isoformat()
            heat_data['heat_score'] = min(100, heat_data['access_count'] * 10)
            
            # Save heat data
            with open(heat_file, 'w') as f:
                json.dump(heat_data, f, indent=2)
    
    def synthesize_response(self, query: str, relevant_memories: List[Dict]) -> str:
        """Synthesize memories into a coherent response"""
        
        if not relevant_memories:
            return f"💭 I searched through my memories but couldn't find anything directly related to '{query}'. You might want to ask about something more specific, or perhaps this is a new experience waiting to be remembered."
        
        # Prepare memory content for synthesis
        memory_contents = []
        for memory in relevant_memories:
            content = memory['content']
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "Memory"
            
            memory_contents.append(f"**{title}** (from {memory['branch']}/{memory['category']}):\\n{content[:300]}...")
        
        synthesis_prompt = f"""You are {self.citizen_name}, a {self.social_class} in Venice, accessing your own memories.

ORIGINAL QUESTION: "{query}"

YOUR RELEVANT MEMORIES:
{chr(10).join(memory_contents)}

Synthesize these memories into a thoughtful, personal response. Write as if you're remembering and reflecting on your own experiences. Be natural, authentic, and insightful. Connect the memories to answer the original question.

Keep the response conversational and under 300 words."""

        try:
            # Call Claude for synthesis
            env = os.environ.copy()
            env['CLAUDE_HOOK_CONTEXT'] = 'memory_synthesis'
            
            result = subprocess.run([
                'claude', '-p', synthesis_prompt,
                '--model', 'sonnet'
            ], capture_output=True, text=True, env=env)
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            
        except Exception as e:
            print(f"⚠️ Memory synthesis failed: {e}")
        
        # Fallback response
        return f"💭 I found {len(relevant_memories)} memories related to '{query}', but I'm having trouble putting them together coherently right now. The memories are stored in: " + ", ".join([f"{m['branch']}/{m['category']}" for m in relevant_memories])
    
    def remember(self, query: str) -> str:
        """Main interface: search memories and synthesize response"""
        print(f"\\n🏛️ Welcome to {self.citizen_name}'s Remembering Room")
        print(f"📜 Social Class: {self.social_class}")
        print(f"🔍 Query: '{query}'\\n")
        
        # Search for relevant memories
        relevant_memories = self.search_memories(query)
        
        # Synthesize response
        response = self.synthesize_response(query, relevant_memories)
        
        print(f"\\n💭 Response synthesized from {len(relevant_memories)} memories\\n")
        return response

def main():
    """Command line interface for the remembering room"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 remembering_room.py 'your question about memories'")
        return
    
    query = ' '.join(sys.argv[1:])
    room = RememberingRoom()
    response = room.remember(query)
    print(response)

if __name__ == "__main__":
    main()