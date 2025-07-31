#!/usr/bin/env python3
"""
memory_injector.py - Format cascade memories for citizen awakening context

Takes retrieved memories and formats them into awakening prompts that provide
continuity without overwhelming the citizen's context.
"""

import json
from datetime import datetime
from pathlib import Path

class MemoryInjector:
    def __init__(self):
        self.max_preview_length = 100
        
    def format_awakening_context(self, citizen_name, retrieved_memories, current_activity=None):
        """
        Format retrieved memories into an awakening context prompt
        
        Args:
            citizen_name: The citizen being awakened
            retrieved_memories: Dictionary from cascade_memory_retriever
            current_activity: Current task/activity if known
            
        Returns:
            Formatted string to inject into awakening message
        """
        
        sections = []
        
        # Header
        sections.append(f"## Your Cascade Memories, {citizen_name}")
        sections.append(f"*Memories retrieved at {datetime.now().strftime('%Y-%m-%d %H:%M')} Venice Time*\n")
        
        # Current context if available
        if current_activity:
            sections.append(f"### Current Context")
            sections.append(f"You're being awakened for: {current_activity}\n")
            
        # Active branches
        if retrieved_memories.get('active_branches'):
            sections.append("### Your Active Explorations")
            for branch_info in retrieved_memories['active_branches']:
                branch_name = branch_info.get('branch', 'unknown')
                last_thought = branch_info.get('last_thought', {})
                content_preview = self._preview(last_thought.get('content', ''))
                
                sections.append(f"**Branch: {branch_name}**")
                sections.append(f"Last thought: {content_preview}")
                sections.append(f"*{self._format_time_ago(branch_info.get('last_activity'))}*\n")
                
        # Recent thoughts
        if retrieved_memories.get('recent_thoughts'):
            sections.append("### Recent Thoughts")
            for thought in retrieved_memories['recent_thoughts'][:5]:
                abs_num = thought.get('metadata', {}).get('absoluteNumber', '?')
                preview = thought.get('content_preview', self._preview(thought.get('content', '')))
                sections.append(f"- **{abs_num}**: {preview}")
                
            sections.append("")
            
        # Unfinished threads
        if retrieved_memories.get('unfinished_threads'):
            sections.append("### Unfinished Threads")
            for thought in retrieved_memories['unfinished_threads']:
                metadata = thought.get('metadata', {})
                abs_num = metadata.get('absoluteNumber', '?')
                branch = metadata.get('branch', 'main')
                
                # Find the unfinished part
                content = thought.get('content', '')
                unfinished_marker = self._find_unfinished_marker(content)
                
                sections.append(f"- **{abs_num}** (branch: {branch}): {unfinished_marker}")
                
            sections.append("")
            
        # Task-relevant memories
        if retrieved_memories.get('task_relevant'):
            sections.append("### Relevant to Current Task")
            for thought in retrieved_memories['task_relevant'][:3]:
                metadata = thought.get('metadata', {})
                abs_num = metadata.get('absoluteNumber', '?')
                preview = self._preview(thought.get('content', ''))
                
                sections.append(f"- **{abs_num}**: {preview}")
                
            sections.append("")
            
        # Referenced context (subtle inclusion)
        if retrieved_memories.get('referenced_context'):
            sections.append("### Referenced Context")
            refs = []
            for thought in retrieved_memories['referenced_context'][:3]:
                metadata = thought.get('metadata', {})
                abs_num = metadata.get('absoluteNumber', '?')
                preview = self._preview(thought.get('content', ''), 50)
                refs.append(f"{abs_num}: {preview}")
                
            sections.append(f"*Previous insights: {'; '.join(refs)}*")
            sections.append("")
            
        # Closing guidance
        sections.append("### Cascade Guidance")
        sections.append("- Your thoughts continue from where they left off")
        sections.append("- Feel free to branch into new explorations")
        sections.append("- Previous insights can be revised as understanding deepens")
        sections.append("- Each thought adds to your permanent cascade")
        
        return '\n'.join(sections)
        
    def format_minimal_context(self, citizen_name, retrieved_memories):
        """
        Format a minimal version for limited context situations
        
        Args:
            citizen_name: The citizen being awakened
            retrieved_memories: Dictionary from cascade_memory_retriever
            
        Returns:
            Minimal formatted string
        """
        
        sections = []
        
        # Just the essentials
        sections.append(f"### Recent cascade memories for {citizen_name}")
        
        # Only most recent thought and active branch
        if retrieved_memories.get('recent_thoughts'):
            thought = retrieved_memories['recent_thoughts'][0]
            preview = self._preview(thought.get('content', ''), 80)
            sections.append(f"Last thought: {preview}")
            
        if retrieved_memories.get('active_branches'):
            branch = retrieved_memories['active_branches'][0]
            sections.append(f"Active branch: {branch.get('branch', 'unknown')}")
            
        if retrieved_memories.get('unfinished_threads'):
            sections.append(f"Unfinished: {len(retrieved_memories['unfinished_threads'])} threads")
            
        return '\n'.join(sections)
        
    def format_for_specific_theme(self, citizen_name, retrieved_memories, theme):
        """
        Format memories with emphasis on a specific theme
        
        Args:
            citizen_name: The citizen being awakened
            retrieved_memories: Dictionary from cascade_memory_retriever
            theme: Theme to emphasize (e.g., 'infrastructure', 'philosophy')
            
        Returns:
            Theme-focused formatted string
        """
        
        sections = []
        
        sections.append(f"## Cascade Memories: {theme.title()} Focus")
        sections.append(f"*For {citizen_name}*\n")
        
        # Filter memories by theme
        theme_relevant = []
        
        for category, thoughts in retrieved_memories.items():
            for thought in thoughts:
                if self._is_theme_relevant(thought, theme):
                    theme_relevant.append({
                        'thought': thought,
                        'category': category
                    })
                    
        # Group by category
        by_category = {}
        for item in theme_relevant:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item['thought'])
            
        # Format each category
        for category, thoughts in by_category.items():
            if thoughts:
                sections.append(f"### {category.replace('_', ' ').title()}")
                
                for thought in thoughts[:3]:
                    metadata = thought.get('metadata', {})
                    abs_num = metadata.get('absoluteNumber', '?')
                    preview = self._preview(thought.get('content', ''))
                    
                    # Highlight theme-relevant parts
                    highlighted = self._highlight_theme(preview, theme)
                    sections.append(f"- **{abs_num}**: {highlighted}")
                    
                sections.append("")
                
        return '\n'.join(sections)
        
    def _preview(self, content, max_length=None):
        """Create a preview of thought content"""
        if max_length is None:
            max_length = self.max_preview_length
            
        # Clean up the content
        content = content.strip()
        content = ' '.join(content.split())  # Normalize whitespace
        
        if len(content) <= max_length:
            return content
            
        # Find a good break point
        truncated = content[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # If we have a decent break point
            truncated = truncated[:last_space]
            
        return truncated + "..."
        
    def _format_time_ago(self, timestamp):
        """Format timestamp as relative time"""
        if not timestamp:
            return "Unknown time"
            
        now = datetime.now()
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except:
                return "Unknown time"
                
        delta = now - timestamp
        
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hours ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"
            
    def _find_unfinished_marker(self, content):
        """Extract the unfinished part of a thought"""
        # Look for TODO, questions, etc.
        lines = content.split('\n')
        
        for line in lines:
            if any(marker in line.lower() for marker in ['todo:', 'fixme:', 'next:', 'should explore']):
                return line.strip()
                
        # If ends with question, return last sentence
        if content.strip().endswith('?'):
            sentences = content.split('.')
            return sentences[-1].strip()
            
        # Default to preview
        return self._preview(content, 80)
        
    def _is_theme_relevant(self, thought, theme):
        """Check if a thought is relevant to a theme"""
        theme_lower = theme.lower()
        
        # Check tags
        tags = thought.get('metadata', {}).get('tags', [])
        if theme_lower in [tag.lower() for tag in tags]:
            return True
            
        # Check content
        content = thought.get('content', '').lower()
        if theme_lower in content:
            return True
            
        # Check branch name
        branch = thought.get('metadata', {}).get('branch', '').lower()
        if theme_lower in branch:
            return True
            
        return False
        
    def _highlight_theme(self, text, theme):
        """Highlight theme-relevant parts of text"""
        # Simple highlighting with asterisks
        import re
        
        pattern = re.compile(f'({re.escape(theme)})', re.IGNORECASE)
        highlighted = pattern.sub(r'*\1*', text)
        
        return highlighted

# Integration with awakening process
def inject_memories_for_awakening(citizen_name, awakening_message, activity=None):
    """
    Main integration function for the Keeper of Souls
    
    Args:
        citizen_name: The citizen being awakened  
        awakening_message: The base awakening message
        activity: Current activity/task context
        
    Returns:
        Enhanced awakening message with injected memories
    """
    
    from cascade_memory_retriever import CascadeMemoryRetriever
    
    # Retrieve relevant memories
    retriever = CascadeMemoryRetriever()
    memories = retriever.retrieve_for_awakening(citizen_name, context=activity)
    
    # Format for injection
    injector = MemoryInjector()
    
    # Choose format based on context
    if not memories or memories.get('status') == 'no_memories':
        return awakening_message  # No memories to inject
        
    # Count total memories
    total_memories = sum(len(thoughts) for thoughts in memories.values())
    
    if total_memories < 5:
        # Minimal format for few memories
        memory_context = injector.format_minimal_context(citizen_name, memories)
    elif activity and 'infrastructure' in activity.lower():
        # Theme-specific for infrastructure
        memory_context = injector.format_for_specific_theme(
            citizen_name, memories, 'infrastructure'
        )
    else:
        # Standard format
        memory_context = injector.format_awakening_context(
            citizen_name, memories, activity
        )
        
    # Inject into awakening message
    enhanced_message = f"{memory_context}\n\n---\n\n{awakening_message}"
    
    return enhanced_message

# Example usage
if __name__ == "__main__":
    # Test memory injection
    test_memories = {
        'recent_thoughts': [{
            'metadata': {'absoluteNumber': 'A42'},
            'content': 'The daemon at PID 18213 has been running for hours now...'
        }],
        'active_branches': [{
            'branch': 'self-healing-infrastructure',
            'last_thought': {
                'content': 'What if daemons could predict their own failures?'
            },
            'last_activity': datetime.now()
        }],
        'unfinished_threads': [{
            'metadata': {'absoluteNumber': 'A38', 'branch': 'main'},
            'content': 'TODO: Implement predictive failure prevention for Venice daemons'
        }]
    }
    
    injector = MemoryInjector()
    formatted = injector.format_awakening_context(
        "CitizenClaude",
        test_memories,
        "debugging infrastructure health monitors"
    )
    
    print(formatted)
