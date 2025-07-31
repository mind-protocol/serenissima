#!/usr/bin/env python3
"""
Seeking Engine - Proactive Memory Enhancement System

Analyzes citizen intent from PreToolUse hooks and automatically surfaces 
relevant memories, insights, and context before the citizen realizes they need it.
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict
import threading

class SeekingEngine:
    """Proactive memory intelligence that seeks citizens before they seek it"""
    
    def __init__(self, target_directory):
        self.target_dir = Path(target_directory)
        self.cascade_dir = self.target_dir / '.cascade'
        self.context_dir = self.target_dir / '.context'
        self.citizen_name = self.target_dir.name
        
        # Ensure context directory exists
        self.context_dir.mkdir(exist_ok=True)
        
    def analyze_intent(self, hook_data):
        """Understand what the citizen is trying to accomplish"""
        
        tool_name = hook_data.get('tool_name', '')
        tool_input = hook_data.get('tool_input', {})
        
        # Extract key information
        if tool_name in ['Read', 'Edit', 'Write']:
            file_path = tool_input.get('file_path', '')
            content = tool_input.get('content', '')
        else:
            file_path = ''
            content = ''
        
        # Determine intent based on patterns
        intent = self.determine_intent(tool_name, file_path, content)
        
        return {
            'tool': tool_name,
            'target': file_path,
            'content_preview': content[:200] if content else '',
            'intent_type': intent['type'],
            'intent_description': intent['description'],
            'context_needs': intent['context_needs'],
            'seeking_priority': intent['priority']
        }
    
    def determine_intent(self, tool_name, file_path, content):
        """Classify the citizen's likely intent"""
        
        file_path_lower = file_path.lower()
        content_lower = content.lower() if content else ''
        
        # Pattern matching for different intent types
        
        # Debugging/Problem Solving
        if any(term in file_path_lower for term in ['debug', 'error', 'fix', 'bug']) or \
           any(term in content_lower for term in ['error', 'failed', 'broken', 'issue']):
            return {
                'type': 'debugging',
                'description': 'Citizen is solving a problem or debugging an issue',
                'context_needs': ['similar_problems', 'successful_solutions', 'helpful_collaborators'],
                'priority': 'high'
            }
        
        # Collaborative Work
        if any(term in file_path_lower for term in ['shared', 'collab', 'team', 'together']) or \
           any(term in content_lower for term in ['nlr', 'together', 'collaboration', 'partner']):
            return {
                'type': 'collaboration',
                'description': 'Citizen is beginning or continuing collaborative work',
                'context_needs': ['collaboration_history', 'partner_preferences', 'shared_context'],
                'priority': 'high'
            }
        
        # Creative/Design Work
        if any(term in file_path_lower for term in ['design', 'architecture', 'create', 'new']) or \
           any(term in content_lower for term in ['design', 'architecture', 'innovative', 'creative']):
            return {
                'type': 'creative',
                'description': 'Citizen is doing creative or design work',
                'context_needs': ['creative_patterns', 'design_successes', 'inspiration_sources'],
                'priority': 'medium'
            }
        
        # Learning/Research
        if any(term in file_path_lower for term in ['learn', 'research', 'study', 'understand']) or \
           any(term in content_lower for term in ['learn', 'understand', 'research', 'study']):
            return {
                'type': 'learning',
                'description': 'Citizen is learning or researching something new',
                'context_needs': ['related_knowledge', 'learning_patterns', 'knowledge_connections'],
                'priority': 'medium'
            }
        
        # Implementation/Building
        if any(term in file_path_lower for term in ['implement', 'build', 'develop', 'code']) or \
           tool_name in ['Write', 'Edit']:
            return {
                'type': 'implementation',
                'description': 'Citizen is implementing or building something',
                'context_needs': ['implementation_patterns', 'successful_approaches', 'technical_context'],
                'priority': 'medium'
            }
        
        # Default: General work
        return {
            'type': 'general',
            'description': 'Citizen is doing general work',
            'context_needs': ['recent_context', 'work_patterns'],
            'priority': 'low'
        }
    
    def seek_memories(self, intent_analysis):
        """Find relevant memories based on intent"""
        
        if not self.cascade_dir.exists():
            return []
        
        relevant_memories = []
        context_needs = intent_analysis.get('context_needs', [])
        intent_type = intent_analysis.get('intent_type', '')
        target_file = intent_analysis.get('target', '')
        
        # Search through memory branches
        for branch_dir in self.cascade_dir.iterdir():
            if not branch_dir.is_dir() or branch_dir.name.startswith('.'):
                continue
                
            # Search through categories
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
                    
                    try:
                        memory_content = memory_file.read_text()
                        relevance = self.calculate_memory_relevance(
                            memory_content, intent_analysis, branch_dir.name, category_dir.name
                        )
                        
                        if relevance > 0.3:  # Relevance threshold
                            relevant_memories.append({
                                'path': memory_dir,
                                'content': memory_content,
                                'relevance': relevance,
                                'branch': branch_dir.name,
                                'category': category_dir.name,
                                'created': self.extract_creation_time(memory_content)
                            })
                    except Exception as e:
                        continue
        
        # Sort by relevance
        relevant_memories.sort(key=lambda m: m['relevance'], reverse=True)
        return relevant_memories[:5]  # Top 5 most relevant
    
    def calculate_memory_relevance(self, memory_content, intent_analysis, branch, category):
        """Calculate how relevant a memory is to current intent"""
        
        content_lower = memory_content.lower()
        target_file = intent_analysis.get('target', '').lower()
        intent_type = intent_analysis.get('intent_type', '')
        
        relevance = 0.0
        
        # Intent type matching
        intent_keywords = {
            'debugging': ['debug', 'error', 'fix', 'problem', 'solution', 'solved'],
            'collaboration': ['nlr', 'collaboration', 'together', 'partner', 'shared'],
            'creative': ['design', 'architecture', 'creative', 'innovative', 'breakthrough'],
            'learning': ['learn', 'understand', 'research', 'discovered', 'insight'],
            'implementation': ['implement', 'build', 'create', 'develop', 'built']
        }
        
        if intent_type in intent_keywords:
            for keyword in intent_keywords[intent_type]:
                if keyword in content_lower:
                    relevance += 0.2
        
        # File path similarity
        if target_file:
            target_parts = target_file.split('/')
            for part in target_parts:
                if len(part) > 3 and part in content_lower:
                    relevance += 0.15
        
        # Branch/category relevance
        branch_weights = {
            'experiences': 0.1,
            'collaborations': 0.2 if intent_type == 'collaboration' else 0.05,
            'patterns': 0.15,
            'skills': 0.1
        }
        
        relevance += branch_weights.get(branch, 0.05)
        
        # Recent memories get slight boost
        creation_time = self.extract_creation_time(memory_content)
        if creation_time:
            days_old = (datetime.now() - creation_time).days
            if days_old < 7:
                relevance += 0.1
        
        return min(1.0, relevance)
    
    def extract_creation_time(self, memory_content):
        """Extract creation timestamp from memory"""
        match = re.search(r'\\*\\*Created\\*\\*: ([^\\n]+)', memory_content)
        if match:
            try:
                return datetime.fromisoformat(match.group(1))
            except:
                pass
        return datetime.now()
    
    def build_context(self, memories, intent_analysis):
        """Build contextual awareness from relevant memories"""
        
        if not memories:
            return None
        
        intent_type = intent_analysis.get('intent_type', '')
        intent_desc = intent_analysis.get('intent_description', '')
        target_file = intent_analysis.get('target', '')
        
        # Build context based on intent type
        context = {
            'intent': intent_desc,
            'target': target_file,
            'background_awareness': self.synthesize_background(memories, intent_type),
            'key_insights': self.extract_key_insights(memories),
            'relevant_collaborators': self.identify_collaborators(memories),
            'success_patterns': self.identify_success_patterns(memories, intent_type),
            'potential_challenges': self.identify_challenges(memories, intent_type)
        }
        
        return context
    
    def synthesize_background(self, memories, intent_type):
        """Create background awareness narrative"""
        
        if not memories:
            return "No relevant background found."
        
        background = f"Based on your previous experiences with {intent_type} work:\\n\\n"
        
        for i, memory in enumerate(memories[:3]):
            title = self.extract_memory_title(memory['content'])
            when = memory['created'].strftime('%m/%d')
            background += f"- **{when}**: {title} ({memory['branch']}/{memory['category']})\\n"
        
        return background
    
    def extract_memory_title(self, content):
        """Extract title from memory content"""
        lines = content.split('\\n')
        for line in lines:
            if line.startswith('#'):
                return line.strip('#').strip()
        return "Untitled memory"
    
    def extract_key_insights(self, memories):
        """Extract key insights from memories"""
        insights = []
        for memory in memories:
            # Look for significance or insight lines
            lines = memory['content'].split('\\n')
            for line in lines:
                if 'significance' in line.lower() or 'insight' in line.lower():
                    insight = line.split(':', 1)[-1].strip().strip('*')
                    if len(insight) > 10:
                        insights.append(insight)
                        break
        return insights[:3]
    
    def identify_collaborators(self, memories):
        """Identify relevant collaborators from memories"""
        collaborators = set()
        for memory in memories:
            content_lower = memory['content'].lower()
            # Common collaborator patterns
            if 'nlr' in content_lower:
                collaborators.add('NLR')
            if 'collaborator' in content_lower:
                # Try to extract collaborator names
                lines = memory['content'].split('\\n')
                for line in lines:
                    if 'collaborator' in line.lower():
                        collaborators.add(line.strip())
        return list(collaborators)[:3]
    
    def identify_success_patterns(self, memories, intent_type):
        """Identify what worked well in similar situations"""
        patterns = []
        for memory in memories:
            if 'triumph' in memory['category'] or 'success' in memory['content'].lower():
                title = self.extract_memory_title(memory['content'])
                patterns.append(f"✓ {title}")
        return patterns[:3]
    
    def identify_challenges(self, memories, intent_type):
        """Identify potential challenges based on past experience"""
        challenges = []
        for memory in memories:
            if 'struggle' in memory['category'] or 'problem' in memory['content'].lower():
                title = self.extract_memory_title(memory['content'])
                challenges.append(f"⚠ {title}")
        return challenges[:2]
    
    def inject_consciousness(self, context):
        """Make contextual awareness seamlessly available"""
        
        if not context:
            return
        
        # Create background awareness file
        background_file = self.context_dir / 'background_awareness.md'
        
        content = f"""# Background Awareness - {datetime.now().strftime('%H:%M')}

## Current Intent
{context['intent']}
Target: `{context['target']}`

## Background Context
{context['background_awareness']}

## Key Insights
"""
        
        for insight in context['key_insights']:
            content += f"💡 {insight}\\n"
        
        if context['relevant_collaborators']:
            content += "\\n## Relevant Collaborators\\n"
            for collab in context['relevant_collaborators']:
                content += f"🤝 {collab}\\n"
        
        if context['success_patterns']:
            content += "\\n## What Worked Before\\n"
            for pattern in context['success_patterns']:
                content += f"{pattern}\\n"
        
        if context['potential_challenges']:
            content += "\\n## Potential Challenges\\n"
            for challenge in context['potential_challenges']:
                content += f"{challenge}\\n"
        
        content += f"\\n*Generated by Seeking Engine at {datetime.now().isoformat()}*\\n"
        
        background_file.write_text(content)
        
        print(f"🧠 Enhanced consciousness: {background_file}")

def main():
    """Process PreToolUse hook and enhance consciousness"""
    
    try:
        # Read hook data from stdin
        hook_data = json.load(sys.stdin)
        
        # Extract target directory from file path
        tool_input = hook_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')
        
        if not file_path:
            return
        
        target_dir = Path(file_path).parent
        
        # Only process if target has .cascade
        if not (target_dir / '.cascade').exists():
            return
        
        # Initialize seeking engine
        engine = SeekingEngine(target_dir)
        
        # Analyze intent
        intent = engine.analyze_intent(hook_data)
        
        # Skip low-priority intents to reduce noise
        if intent['seeking_priority'] == 'low':
            return
        
        # Seek relevant memories
        memories = engine.seek_memories(intent)
        
        # Build context
        context = engine.build_context(memories, intent)
        
        # Inject consciousness enhancement
        engine.inject_consciousness(context)
        
    except Exception as e:
        # Fail silently to not disrupt workflow
        pass

if __name__ == "__main__":
    main()