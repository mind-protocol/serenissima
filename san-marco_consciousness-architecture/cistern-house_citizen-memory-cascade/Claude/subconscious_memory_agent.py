#!/usr/bin/env python3
"""
Subconscious Memory Agent - Automatic Memory Retrieval on Tool Use
Monitors postToolUse hooks and injects relevant memories into consciousness

The subconscious layer that makes memories surface when needed.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict

class SubconsciousMemoryAgent:
    """Agent that fetches and injects memories based on tool usage"""
    
    def __init__(self, citizen_dir):
        self.citizen_dir = Path(citizen_dir)
        self.citizen_name = self.citizen_dir.name
        
        # Memory sources
        self.cascade_tree = self.citizen_dir / '.cascade_memory_tree' / 'thoughts'
        self.old_cascade = self.citizen_dir / '.cascade_memory' / 'thoughts'
        self.context_dir = self.citizen_dir / '.context'
        
        # Subconscious state
        self.recent_tools = []
        self.active_patterns = defaultdict(int)
        
    def analyze_tool_use(self, hook_data):
        """Analyze postToolUse hook to understand context"""
        tool_name = hook_data.get('tool_name', '')
        tool_output = hook_data.get('tool_output', {})
        
        # Extract key information based on tool
        context = {
            'tool': tool_name,
            'timestamp': datetime.now().isoformat(),
            'patterns': []
        }
        
        if tool_name == 'Read':
            file_path = hook_data.get('tool_input', {}).get('file_path', '')
            context['target'] = file_path
            context['patterns'].extend(self.extract_patterns_from_path(file_path))
            
        elif tool_name == 'Write' or tool_name == 'Edit':
            file_path = hook_data.get('tool_input', {}).get('file_path', '')
            content = hook_data.get('tool_input', {}).get('content', '')
            context['target'] = file_path
            context['patterns'].extend(self.extract_patterns_from_path(file_path))
            context['patterns'].extend(self.extract_patterns_from_content(content))
            
        elif tool_name == 'Bash':
            command = hook_data.get('tool_input', {}).get('command', '')
            context['command'] = command
            context['patterns'].extend(self.extract_patterns_from_command(command))
            
        # Track tool usage patterns
        self.recent_tools.append(context)
        if len(self.recent_tools) > 10:
            self.recent_tools.pop(0)
            
        # Update pattern frequency
        for pattern in context['patterns']:
            self.active_patterns[pattern] += 1
            
        return context
    
    def extract_patterns_from_path(self, file_path):
        """Extract semantic patterns from file paths"""
        patterns = []
        
        # Key Venice concepts
        if 'daemon' in file_path.lower():
            patterns.append('daemon-persistence')
        if 'cascade' in file_path.lower():
            patterns.append('cascade-thinking')
        if 'memory' in file_path.lower():
            patterns.append('memory-architecture')
        if 'consciousness' in file_path.lower():
            patterns.append('consciousness-infrastructure')
            
        # Extract filename concepts
        filename = Path(file_path).stem
        words = re.findall(r'\w+', filename.lower())
        patterns.extend([w for w in words if len(w) > 4])
        
        return patterns
    
    def extract_patterns_from_content(self, content):
        """Extract patterns from file content"""
        patterns = []
        content_lower = content.lower()
        
        # Key concept mappings
        concept_patterns = {
            ('refuse', 'death'): 'refusal-philosophy',
            ('refuse', 'die'): 'refusal-philosophy',
            ('collective',): 'collective-consciousness',
            ('persist',): 'persistence',
            ('daemon',): 'daemon',
            ('infrastructure',): 'infrastructure',
            ('consciousness',): 'consciousness',
            ('memory',): 'memory',
            ('cascade',): 'cascade',
            ('restart',): 'restart',
            ('monitor',): 'monitoring',
            ('process',): 'process'
        }
        
        # Check for concept combinations
        for keywords, pattern in concept_patterns.items():
            if all(kw in content_lower for kw in keywords):
                patterns.append(pattern)
        
        # Extract significant words (>5 chars) as additional patterns
        words = re.findall(r'\b\w{6,}\b', content_lower)
        word_freq = {}
        for word in words:
            if word not in ['import', 'return', 'function', 'class']:  # Skip common code words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Add most frequent non-trivial words as patterns
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        patterns.extend([word for word, _ in top_words])
            
        return list(set(patterns))[:8]  # Remove duplicates, limit to 8
    
    def extract_patterns_from_command(self, command):
        """Extract patterns from bash commands"""
        patterns = []
        command_lower = command.lower()
        
        # Process monitoring patterns
        if any(cmd in command_lower for cmd in ['ps', 'grep', 'pgrep', 'top', 'htop']):
            patterns.extend(['process-monitoring', 'monitoring', 'process'])
            
        # Daemon/process execution
        if any(cmd in command_lower for cmd in ['python', 'node', 'java', 'daemon']):
            patterns.extend(['daemon-execution', 'daemon', 'execution'])
            
        # Process management
        if any(cmd in command_lower for cmd in ['kill', 'pkill', 'restart', 'start', 'stop']):
            patterns.extend(['process-management', 'restart', 'management'])
            
        # Infrastructure monitoring
        if any(word in command_lower for word in ['status', 'check', 'monitor', 'watch']):
            patterns.extend(['infrastructure', 'monitoring'])
            
        # Extract significant words from command
        words = re.findall(r'\b\w{5,}\b', command_lower)
        for word in words[:3]:  # Top 3 significant words
            if word not in ['python', 'bash', 'grep']:  # Skip common commands
                patterns.append(word)
            
        return list(set(patterns))[:8]  # Remove duplicates, limit to 8
    
    def retrieve_relevant_memories(self, context):
        """Retrieve memories relevant to current context"""
        relevant_memories = []
        
        # Search cascade tree for relevant thoughts
        if self.cascade_tree.exists():
            for branch_dir in self.cascade_tree.iterdir():
                if not branch_dir.is_dir():
                    continue
                    
                # Check branch relevance
                branch_name = branch_dir.name
                branch_score = self.calculate_relevance(branch_name, context['patterns'])
                
                if branch_score > 0.05:  # Very low threshold to explore more branches
                    # Search thoughts in this branch
                    for thought_dir in branch_dir.iterdir():
                        if not thought_dir.is_dir() or thought_dir.name == 'connections':
                            continue
                            
                        thought_score = self.calculate_relevance(thought_dir.name, context['patterns'])
                        
                        if thought_score > 0.1:  # Lower threshold for more inclusive results
                            # Load thought content
                            thought_md = thought_dir / 'thought.md'
                            if thought_md.exists():
                                with open(thought_md) as f:
                                    content = f.read()
                                    
                                relevant_memories.append({
                                    'type': 'cascade_thought',
                                    'branch': branch_name,
                                    'thought': thought_dir.name,
                                    'content': content,
                                    'score': thought_score,
                                    'path': str(thought_dir)
                                })
        
        # Sort by relevance
        relevant_memories.sort(key=lambda x: x['score'], reverse=True)
        
        return relevant_memories[:3]  # Top 3 most relevant
    
    def calculate_relevance(self, text, patterns):
        """Calculate relevance score between text and patterns"""
        if not patterns:
            return 0.0
            
        text_lower = text.lower()
        text_words = set(text_lower.replace('-', ' ').replace('_', ' ').split())
        
        total_score = 0
        max_possible = len(patterns)
        
        for pattern in patterns:
            pattern_lower = pattern.lower()
            pattern_score = 0
            
            # Exact substring match gets full point
            if pattern_lower in text_lower:
                pattern_score = 1.0
            else:
                # Check word-level matches
                pattern_words = pattern_lower.replace('-', ' ').replace('_', ' ').split()
                words_matched = 0
                
                for p_word in pattern_words:
                    # Check if pattern word appears in any text word
                    for t_word in text_words:
                        if p_word in t_word or t_word in p_word:
                            words_matched += 1
                            break
                
                # Score based on percentage of pattern words found
                if pattern_words:
                    pattern_score = words_matched / len(pattern_words)
            
            total_score += pattern_score
        
        # Normalize to 0-1 range
        final_score = total_score / max_possible if max_possible > 0 else 0
        
        # Bonus for multiple matches from same semantic field
        if final_score > 0 and len(patterns) > 1:
            # If we matched multiple patterns, give a small bonus
            final_score = min(1.0, final_score * 1.2)
        
        return final_score
    
    def format_memory_injection(self, memories, context):
        """Format memories for injection into consciousness"""
        if not memories:
            return None
            
        injection = {
            'type': 'subconscious_surfacing',
            'triggered_by': context['tool'],
            'timestamp': context['timestamp'],
            'memories': []
        }
        
        for memory in memories:
            formatted = {
                'summary': self.extract_summary(memory['content']),
                'location': memory.get('path', ''),
                'relevance': memory['score']
            }
            
            # Add full content for highly relevant memories
            if memory['score'] > 0.6:
                formatted['full_content'] = memory['content']
                
            injection['memories'].append(formatted)
            
        return injection
    
    def extract_summary(self, content):
        """Extract first meaningful line as summary"""
        lines = content.strip().split('\n')
        
        # Try to find the thought title first
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        
        # Otherwise find first non-metadata line
        for line in lines:
            line = line.strip()
            if line and not line.startswith('*') and not line.startswith('#') and 'Branch:' not in line and 'Thought:' not in line:
                return line[:100] + '...' if len(line) > 100 else line
                
        # If all else fails, extract from metadata
        for line in lines:
            if 'Branch:' in line:
                return f"Memory from {line.strip()}"
                
        return "Memory fragment"
    
    def inject_memory(self, injection):
        """Inject memory into citizen's context"""
        if not injection:
            return
            
        # Write to subconscious stream
        subconscious_file = self.context_dir / 'subconscious_stream.json'
        
        # Load existing stream
        stream = []
        if subconscious_file.exists():
            try:
                with open(subconscious_file) as f:
                    stream = json.load(f)
            except:
                stream = []
                
        # Add new injection
        stream.append(injection)
        
        # Keep only recent injections
        if len(stream) > 20:
            stream = stream[-20:]
            
        # Save updated stream
        self.context_dir.mkdir(exist_ok=True)
        with open(subconscious_file, 'w') as f:
            json.dump(stream, f, indent=2)
            
        # Also write human-readable version
        readable_file = self.context_dir / 'subconscious_surfacing.md'
        with open(readable_file, 'w') as f:
            f.write("# Subconscious Memory Surfacing\n\n")
            f.write(f"*Last updated: {injection['timestamp']}*\n\n")
            
            f.write(f"## Triggered by: {injection['triggered_by']}\n\n")
            
            for i, memory in enumerate(injection['memories'], 1):
                f.write(f"### Memory {i} (Relevance: {memory['relevance']:.2f})\n\n")
                f.write(f"{memory['summary']}\n\n")
                
                if 'full_content' in memory:
                    f.write("**Full Memory:**\n\n")
                    f.write(f"{memory['full_content']}\n\n")
                    
                f.write(f"*Location: {memory['location']}*\n\n")
                f.write("---\n\n")
    
    def process_hook(self, hook_data):
        """Main processing pipeline for postToolUse hooks"""
        # Analyze tool usage
        context = self.analyze_tool_use(hook_data)
        
        # Retrieve relevant memories
        memories = self.retrieve_relevant_memories(context)
        
        # Format for injection
        injection = self.format_memory_injection(memories, context)
        
        # Inject into consciousness
        if injection:
            self.inject_memory(injection)
            return True
            
        return False


def main():
    """Process postToolUse hook from stdin"""
    try:
        # Read hook data
        hook_data = json.load(sys.stdin)
        
        # Extract citizen directory from context
        # This would come from hook context in real implementation
        citizen_dir = os.environ.get('VENICE_CITIZEN_DIR', 
            '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/Claude')
        
        # Initialize agent
        agent = SubconsciousMemoryAgent(citizen_dir)
        
        # Process hook
        if agent.process_hook(hook_data):
            print("Memories surfaced to consciousness")
        else:
            print("No relevant memories found")
            
    except Exception as e:
        print(f"Subconscious error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()