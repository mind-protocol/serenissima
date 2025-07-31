#!/usr/bin/env python3
"""
cascade_memory_retriever.py - Intelligent retrieval from cascade memory filesystem

Provides semantic search, branch-aware retrieval, and reference graph traversal
for finding relevant memories during citizen awakening.
"""

import json
import os
from pathlib import Path
import yaml
from datetime import datetime, timedelta
import re
from collections import defaultdict
import math

class CascadeMemoryRetriever:
    def __init__(self, base_path="/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"):
        self.base_path = Path(base_path)
        
    def retrieve_for_awakening(self, citizen_name, context=None, max_tokens=2000):
        """
        Retrieve relevant memories for citizen awakening
        
        Args:
            citizen_name: The citizen being awakened
            context: Current activity/task context
            max_tokens: Maximum tokens to include in injection
            
        Returns:
            Dictionary with categorized relevant memories
        """
        
        cascade_path = self.base_path / "citizens" / citizen_name / "cascade"
        if not cascade_path.exists():
            return {"status": "no_memories", "thoughts": []}
            
        # Load citizen's index
        index_path = cascade_path / "index.json"
        if index_path.exists():
            with open(index_path, 'r') as f:
                index = json.load(f)
        else:
            index = {"thoughts": []}
            
        # Categorize retrieval targets
        relevant_memories = {
            "recent_thoughts": [],
            "active_branches": [],
            "unfinished_threads": [],
            "referenced_context": [],
            "task_relevant": []
        }
        
        # 1. Get recent thoughts (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        for thought in index.get('thoughts', [])[-10:]:  # Last 10 thoughts
            if self._parse_timestamp(thought.get('timestamp', '')) > recent_cutoff:
                relevant_memories['recent_thoughts'].append(thought)
                
        # 2. Find active branches (branches with recent activity)
        branches = self._find_active_branches(cascade_path)
        relevant_memories['active_branches'] = branches[:3]  # Top 3 active branches
        
        # 3. Identify unfinished threads
        unfinished = self._find_unfinished_threads(cascade_path)
        relevant_memories['unfinished_threads'] = unfinished[:2]
        
        # 4. If context provided, find task-relevant thoughts
        if context:
            task_relevant = self._search_by_context(cascade_path, context)
            relevant_memories['task_relevant'] = task_relevant[:5]
            
        # 5. Load referenced thoughts
        all_refs = []
        for category in relevant_memories.values():
            for thought in category:
                refs = thought.get('references', [])
                all_refs.extend(refs)
                
        referenced = self._load_referenced_thoughts(cascade_path, list(set(all_refs)))
        relevant_memories['referenced_context'] = referenced
        
        # Limit total size
        relevant_memories = self._limit_token_size(relevant_memories, max_tokens)
        
        return relevant_memories
        
    def search_semantic(self, citizen_name, query, limit=10):
        """
        Semantic search through a citizen's cascade memories
        
        Args:
            citizen_name: The citizen whose memories to search
            query: Search query
            limit: Maximum results
            
        Returns:
            List of relevant thoughts with relevance scores
        """
        
        cascade_path = self.base_path / "citizens" / citizen_name / "cascade"
        results = []
        
        # Simple TF-IDF style scoring for now
        query_terms = query.lower().split()
        
        for thought_file in cascade_path.rglob("*.md"):
            if thought_file.is_file():
                thought = self._load_thought(thought_file)
                score = self._calculate_relevance(thought, query_terms)
                
                if score > 0:
                    results.append({
                        'thought': thought,
                        'score': score,
                        'filepath': thought_file
                    })
                    
        # Sort by relevance score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:limit]
        
    def trace_thought_lineage(self, citizen_name, thought_id):
        """
        Trace the cascade lineage of a specific thought
        
        Args:
            citizen_name: The citizen
            thought_id: A{n} or S{n} identifier
            
        Returns:
            Dictionary with ancestors, descendants, and siblings
        """
        
        cascade_path = self.base_path / "citizens" / citizen_name / "cascade"
        lineage = {
            'ancestors': [],    # Thoughts this was branched from
            'descendants': [],  # Thoughts branched from this
            'siblings': [],     # Other thoughts in same branch/sequence
            'revisions': []     # Thoughts that revised this one
        }
        
        # Find the thought file
        target_thought = None
        for thought_file in cascade_path.rglob("*.md"):
            if thought_id in thought_file.name:
                target_thought = self._load_thought(thought_file)
                break
                
        if not target_thought:
            return lineage
            
        # Trace relationships through the cascade structure
        target_branch = target_thought.get('metadata', {}).get('branch', 'main')
        target_sequence = target_thought.get('metadata', {}).get('sequence', '')
        
        for thought_file in cascade_path.rglob("*.md"):
            thought = self._load_thought(thought_file)
            metadata = thought.get('metadata', {})
            
            # Find siblings (same branch/sequence)
            if metadata.get('branch') == target_branch and metadata.get('sequence') == target_sequence:
                if metadata.get('absoluteNumber') != thought_id:
                    lineage['siblings'].append(thought)
                    
            # Find revisions
            if metadata.get('revises') == thought_id:
                lineage['revisions'].append(thought)
                
        return lineage
        
    def _find_active_branches(self, cascade_path):
        """Find branches with recent activity"""
        branches_path = cascade_path / "branches"
        active_branches = []
        
        if branches_path.exists():
            for branch_dir in branches_path.iterdir():
                if branch_dir.is_dir():
                    # Get most recent thought in branch
                    recent = None
                    recent_time = datetime.min
                    
                    for thought_file in branch_dir.glob("*.md"):
                        thought = self._load_thought(thought_file)
                        thought_time = self._parse_timestamp(
                            thought.get('metadata', {}).get('timestamp', '')
                        )
                        if thought_time > recent_time:
                            recent = thought
                            recent_time = thought_time
                            
                    if recent:
                        active_branches.append({
                            'branch': branch_dir.name,
                            'last_thought': recent,
                            'last_activity': recent_time
                        })
                        
        # Sort by recency
        active_branches.sort(key=lambda x: x['last_activity'], reverse=True)
        return active_branches
        
    def _find_unfinished_threads(self, cascade_path):
        """Identify thoughts that seem to need continuation"""
        unfinished = []
        
        # Look for thoughts with questions or TODOs
        for thought_file in cascade_path.rglob("*.md"):
            thought = self._load_thought(thought_file)
            content = thought.get('content', '')
            
            # Heuristics for unfinished thoughts
            if any(marker in content.lower() for marker in ['todo', 'fixme', 'next:', 'should explore', 'need to']):
                unfinished.append(thought)
            elif content.strip().endswith('?'):
                unfinished.append(thought)
                
        return unfinished
        
    def _search_by_context(self, cascade_path, context):
        """Find thoughts relevant to current context/task"""
        context_terms = context.lower().split()
        relevant = []
        
        for thought_file in cascade_path.rglob("*.md"):
            thought = self._load_thought(thought_file)
            score = self._calculate_relevance(thought, context_terms)
            
            if score > 0.3:  # Threshold for relevance
                relevant.append({
                    'thought': thought,
                    'relevance': score
                })
                
        relevant.sort(key=lambda x: x['relevance'], reverse=True)
        return [r['thought'] for r in relevant]
        
    def _load_referenced_thoughts(self, cascade_path, references):
        """Load specific thoughts by their IDs"""
        referenced = []
        
        for ref in references:
            for thought_file in cascade_path.rglob("*.md"):
                if ref in thought_file.name:
                    referenced.append(self._load_thought(thought_file))
                    break
                    
        return referenced
        
    def _calculate_relevance(self, thought, query_terms):
        """Calculate relevance score between thought and query terms"""
        content = thought.get('content', '').lower()
        metadata = str(thought.get('metadata', {})).lower()
        
        # Simple scoring based on term frequency
        score = 0
        content_words = content.split()
        
        for term in query_terms:
            # Content matches (weighted higher)
            content_matches = content_words.count(term)
            score += content_matches * 2
            
            # Metadata matches
            if term in metadata:
                score += 1
                
            # Tag matches (weighted highest)
            tags = thought.get('metadata', {}).get('tags', [])
            if term in [tag.lower() for tag in tags]:
                score += 3
                
        # Normalize by content length
        if len(content_words) > 0:
            score = score / math.log(len(content_words) + 1)
            
        return score
        
    def _limit_token_size(self, memories, max_tokens):
        """Limit total size of memories to fit in context"""
        # Rough token estimation (1 token ≈ 4 chars)
        total_chars = 0
        limited = {}
        
        for category, thoughts in memories.items():
            limited[category] = []
            
            for thought in thoughts:
                thought_chars = len(str(thought))
                if total_chars + thought_chars < max_tokens * 4:
                    limited[category].append(thought)
                    total_chars += thought_chars
                else:
                    break
                    
        return limited
        
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
        
    def _parse_timestamp(self, timestamp_str):
        """Parse timestamp string to datetime"""
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            return datetime.min

# Example usage
if __name__ == "__main__":
    retriever = CascadeMemoryRetriever()
    
    # Retrieve memories for CitizenClaude awakening
    memories = retriever.retrieve_for_awakening(
        "citizenclaude",
        context="infrastructure debugging daemon health"
    )
    
    print("=== Memory Retrieval for CitizenClaude ===\n")
    
    for category, thoughts in memories.items():
        if thoughts:
            print(f"\n{category.upper()}:")
            for thought in thoughts[:2]:  # Show first 2 in each category
                metadata = thought.get('metadata', {})
                print(f"  - {metadata.get('absoluteNumber', '?')}: {thought.get('content', '')[:60]}...")
