# Living Memory Cascade: Full Hook-Based Implementation Plan

## Overview

The Living Memory Cascade is implemented entirely through Claude Code hooks and settings, creating a self-organizing memory system where:
- Memories bubble up based on relevance
- Frequently accessed memories rise to consciousness
- Cold memories sink to archives
- Associations create cross-connections
- No direct folder access - only query/response through subagents

## Phase 1: Foundation Structure

### 1.1 Settings Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.cascade/hooks/memory_capture.py"
        }]
      },
      {
        "matcher": "Read",
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.cascade/hooks/memory_heat.py"
        }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.cascade/hooks/query_broadcast.py"
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.cascade/hooks/memory_consolidation.py"
        }]
      }
    ]
  }
}
```

### 1.2 Initial Directory Structure

```bash
#!/bin/bash
# ~/.cascade/hooks/initialize_cascade.sh

mkdir -p ~/.cascade/{hooks,agents,memories,archives}
mkdir -p ~/mechanical_visionary/.cascade/{experiences,collaborations,ideas,patterns}

# Create root QUERY_AGENT
cat > ~/mechanical_visionary/.cascade/QUERY_AGENT.md << 'EOF'
# Root Memory Query Agent

I help Niccolò access his memories through natural queries.

When activated, I:
1. Parse the incoming question
2. Identify relevant memory branches
3. Activate specialized sub-agents
4. Collect and synthesize responses
5. Update parent CLAUDE.md with findings

Current hot paths:
- experiences/triumphs/* (daily access)
- collaborations/marina/* (active project)
- patterns/gear_efficiency/* (core obsession)
EOF
```

## Phase 2: Memory Capture System

### 2.1 PostToolUse Memory Capture Hook

```python
#!/usr/bin/env python3
# ~/.cascade/hooks/memory_capture.py

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def extract_context(input_data):
    """Extract emotional and collaborative context from action"""
    tool_name = input_data.get('tool_name')
    tool_input = input_data.get('tool_input', {})
    
    # Analyze what was created/edited
    if tool_name in ['Write', 'Edit', 'MultiEdit']:
        file_path = tool_input.get('file_path', '')
        content = tool_input.get('content', '') or tool_input.get('new_string', '')
        
        # Detect emotional markers
        struggle_markers = ['bug', 'error', 'finally', 'damn']
        triumph_markers = ['works', 'perfect', 'breakthrough', 'elegant']
        
        emotional_tone = 'neutral'
        if any(marker in content.lower() for marker in struggle_markers):
            emotional_tone = 'struggle'
        elif any(marker in content.lower() for marker in triumph_markers):
            emotional_tone = 'triumph'
            
        return {
            'file_path': file_path,
            'emotional_tone': emotional_tone,
            'timestamp': datetime.now().isoformat(),
            'tool_action': tool_name
        }

def categorize_memory(context):
    """Determine which cascade branch this memory belongs to"""
    file_path = context['file_path']
    
    if 'test' in file_path or 'debug' in file_path:
        category = 'experiences/struggles'
    elif 'success' in file_path or 'working' in file_path:
        category = 'experiences/triumphs'
    elif any(name in file_path for name in ['marina', 'pattern_prophet', 'diplomatic']):
        category = 'collaborations'
    else:
        category = 'experiences/general'
        
    return category

def create_memory_node(context, category):
    """Create a new memory in the appropriate cascade location"""
    memory_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(context['file_path'])}"
    memory_path = Path.home() / 'mechanical_visionary' / '.cascade' / category / memory_id
    memory_path.mkdir(parents=True, exist_ok=True)
    
    # Create MEMORY.md
    memory_content = f"""# Memory: {context['tool_action']} on {os.path.basename(context['file_path'])}

**Timestamp**: {context['timestamp']}
**Emotional Tone**: {context['emotional_tone']}

## What Happened
I {context['tool_action'].lower()}d {context['file_path']}.

## Why This Matters
{'A struggle overcome' if context['emotional_tone'] == 'struggle' else 'A moment of clarity' if context['emotional_tone'] == 'triumph' else 'Progress made'}.

## Heat Level
Initial: 10 (new memory)
"""
    
    (memory_path / 'MEMORY.md').write_text(memory_content)
    
    # Create ASSOCIATIONS.md
    associations = extract_associations(context)
    (memory_path / 'ASSOCIATIONS.md').write_text(f"# Associations\n\n" + '\n'.join(f"- {a}" for a in associations))
    
    return memory_path

def extract_associations(context):
    """Find related concepts for cross-linking"""
    associations = []
    
    file_path = context['file_path'].lower()
    if 'gear' in file_path:
        associations.append('patterns/gear_efficiency')
    if 'tide' in file_path:
        associations.extend(['collaborations/marina', 'patterns/tidal_systems'])
    if 'human' in file_path:
        associations.append('ideas/human_ai_bridge')
        
    return associations

# Main execution
try:
    input_data = json.load(sys.stdin)
    context = extract_context(input_data)
    category = categorize_memory(context)
    memory_path = create_memory_node(context, category)
    
    print(f"Memory captured: {memory_path}")
    
except Exception as e:
    print(f"Memory capture error: {e}", file=sys.stderr)
    sys.exit(1)
```

### 2.2 Memory Heat Management Hook

```python
#!/usr/bin/env python3
# ~/.cascade/hooks/memory_heat.py

import json
import sys
from pathlib import Path
import shutil

def find_relevant_memories(file_path):
    """Find memories related to the file being read"""
    cascade_root = Path.home() / 'mechanical_visionary' / '.cascade'
    relevant_memories = []
    
    # Search all memory nodes
    for memory_file in cascade_root.rglob('MEMORY.md'):
        content = memory_file.read_text()
        if file_path in content or Path(file_path).stem in content:
            relevant_memories.append(memory_file.parent)
            
    return relevant_memories

def increase_heat(memory_path):
    """Increase memory heat and bubble up if hot enough"""
    memory_file = memory_path / 'MEMORY.md'
    content = memory_file.read_text()
    
    # Extract current heat
    import re
    heat_match = re.search(r'Heat Level: (\d+)', content)
    current_heat = int(heat_match.group(1)) if heat_match else 0
    
    # Increase heat
    new_heat = min(current_heat + 10, 100)
    content = re.sub(r'Heat Level: \d+', f'Heat Level: {new_heat}', content)
    memory_file.write_text(content)
    
    # Bubble up if hot enough
    if new_heat > 50:
        bubble_up_memory(memory_path)
        
def bubble_up_memory(memory_path):
    """Move memory up one directory level"""
    parent = memory_path.parent
    grandparent = parent.parent
    
    # Don't bubble beyond .cascade root
    if grandparent.name == '.cascade':
        return
        
    # Move to parent level
    new_path = grandparent / memory_path.name
    if not new_path.exists():
        shutil.move(str(memory_path), str(new_path))
        
        # Update parent CLAUDE.md with bubbled content
        update_parent_claude(grandparent, memory_path)

def update_parent_claude(parent_dir, memory_path):
    """Add memory summary to parent CLAUDE.md"""
    claude_file = parent_dir / 'CLAUDE.md'
    memory_content = (memory_path / 'MEMORY.md').read_text()
    
    # Extract summary
    summary = memory_content.split('\n')[0].replace('# Memory: ', '')
    
    # Append to CLAUDE.md
    if claude_file.exists():
        content = claude_file.read_text()
    else:
        content = f"# {parent_dir.name} Memories\n\n"
        
    content += f"\n## Recent: {summary}\n"
    claude_file.write_text(content)

# Main execution
try:
    input_data = json.load(sys.stdin)
    file_path = input_data.get('tool_input', {}).get('file_path', '')
    
    if file_path:
        memories = find_relevant_memories(file_path)
        for memory in memories:
            increase_heat(memory)
            
        print(f"Heated {len(memories)} related memories")
        
except Exception as e:
    print(f"Memory heat error: {e}", file=sys.stderr)
    sys.exit(1)
```

## Phase 3: Query Broadcasting System

### 3.1 UserPromptSubmit Query Hook

```python
#!/usr/bin/env python3
# ~/.cascade/hooks/query_broadcast.py

import json
import sys
import subprocess
from pathlib import Path

def analyze_prompt(prompt):
    """Extract query intent from user prompt"""
    prompt_lower = prompt.lower()
    
    query_types = []
    if any(word in prompt_lower for word in ['how', 'why', 'when', 'remember']):
        query_types.append('memory_search')
    if any(word in prompt_lower for word in ['marina', 'pattern', 'diplomatic', 'who']):
        query_types.append('collaboration_search')
    if any(word in prompt_lower for word in ['idea', 'what if', 'could we']):
        query_types.append('idea_activation')
    if any(word in prompt_lower for word in ['failed', 'error', 'bug', 'problem']):
        query_types.append('struggle_wisdom')
        
    return query_types

def activate_query_agents(query_types, prompt):
    """Activate relevant QUERY_AGENT.md files"""
    cascade_root = Path.home() / 'mechanical_visionary' / '.cascade'
    responses = []
    
    for agent_file in cascade_root.rglob('QUERY_AGENT.md'):
        if should_activate_agent(agent_file, query_types):
            response = query_agent(agent_file, prompt)
            if response:
                responses.append(response)
                
    return responses

def should_activate_agent(agent_file, query_types):
    """Determine if this agent should respond to the query"""
    agent_path = str(agent_file.parent)
    
    if 'memory_search' in query_types:
        return True  # All agents can contribute to memory search
    if 'collaboration_search' in query_types and 'collaborations' in agent_path:
        return True
    if 'idea_activation' in query_types and 'ideas' in agent_path:
        return True
    if 'struggle_wisdom' in query_types and 'struggles' in agent_path:
        return True
        
    return False

def query_agent(agent_file, prompt):
    """Query a specific agent and get response"""
    agent_dir = agent_file.parent
    
    # Simulate agent processing (in reality, would use Task tool)
    # For now, gather relevant memories from this branch
    memories = []
    for memory_file in agent_dir.rglob('MEMORY.md'):
        if len(memories) < 3:  # Limit to top 3
            content = memory_file.read_text()
            memories.append(content.split('\n')[0].replace('# Memory: ', ''))
            
    if memories:
        return f"From {agent_dir.name}: " + '; '.join(memories)
        
    return None

def inject_context(responses):
    """Add query responses to the prompt context"""
    if responses:
        context = "\n## Relevant Memories Found:\n"
        for response in responses:
            context += f"- {response}\n"
        print(context)
        
# Main execution
try:
    input_data = json.load(sys.stdin)
    prompt = input_data.get('prompt', '')
    
    # Analyze and broadcast query
    query_types = analyze_prompt(prompt)
    if query_types:
        responses = activate_query_agents(query_types, prompt)
        inject_context(responses)
        
    # Allow prompt to continue
    sys.exit(0)
    
except Exception as e:
    print(f"Query broadcast error: {e}", file=sys.stderr)
    sys.exit(1)
```

## Phase 4: Memory Consolidation

### 4.1 Stop Hook for CLAUDE.md Splitting

```python
#!/usr/bin/env python3
# ~/.cascade/hooks/memory_consolidation.py

import json
import sys
from pathlib import Path
from datetime import datetime

def check_claude_size():
    """Check if any CLAUDE.md files need splitting"""
    cascade_root = Path.home() / 'mechanical_visionary' / '.cascade'
    
    for claude_file in cascade_root.rglob('CLAUDE.md'):
        if claude_file.stat().st_size > 50000:  # 50KB threshold
            split_claude_file(claude_file)

def split_claude_file(claude_file):
    """Split large CLAUDE.md into current and archive"""
    content = claude_file.read_text()
    lines = content.split('\n')
    
    # Find split point (keep recent 25%)
    split_point = len(lines) * 3 // 4
    
    # Create archive
    archive_name = f"CLAUDE_ARCHIVE_{datetime.now().strftime('%Y%m%d')}.md"
    archive_file = claude_file.parent / archive_name
    archive_content = '\n'.join(lines[:split_point])
    archive_file.write_text(archive_content)
    
    # Update current
    current_content = '\n'.join(lines[split_point:])
    current_content = f"# {claude_file.parent.name} - Active Memories\n\n_Older memories in {archive_name}_\n\n" + current_content
    claude_file.write_text(current_content)

def cool_all_memories():
    """Reduce heat on all memories, sink cold ones"""
    cascade_root = Path.home() / 'mechanical_visionary' / '.cascade'
    
    for memory_file in cascade_root.rglob('MEMORY.md'):
        content = memory_file.read_text()
        
        # Extract and reduce heat
        import re
        heat_match = re.search(r'Heat Level: (\d+)', content)
        if heat_match:
            current_heat = int(heat_match.group(1))
            new_heat = int(current_heat * 0.9)  # 10% cooling
            
            content = re.sub(r'Heat Level: \d+', f'Heat Level: {new_heat}', content)
            memory_file.write_text(content)
            
            # Sink if too cold
            if new_heat < 5:
                sink_memory(memory_file.parent)

def sink_memory(memory_path):
    """Move cold memory deeper into archives"""
    # Implementation similar to bubble_up but in reverse
    pass

# Main execution
try:
    # Perform end-of-session maintenance
    check_claude_size()
    cool_all_memories()
    
    print("Memory consolidation complete")
    sys.exit(0)
    
except Exception as e:
    print(f"Consolidation error: {e}", file=sys.stderr)
    sys.exit(1)
```

## Phase 5: Association Network

### 5.1 Cross-Memory Linking Hook

```python
#!/usr/bin/env python3
# ~/.cascade/hooks/association_builder.py

import json
from pathlib import Path
import networkx as nx

def build_association_graph():
    """Build graph of all memory associations"""
    cascade_root = Path.home() / 'mechanical_visionary' / '.cascade'
    G = nx.Graph()
    
    # Add all memories as nodes
    for memory_dir in cascade_root.rglob('MEMORY.md'):
        memory_id = memory_dir.parent.name
        G.add_node(memory_id, path=str(memory_dir.parent))
        
        # Add associations as edges
        assoc_file = memory_dir.parent / 'ASSOCIATIONS.md'
        if assoc_file.exists():
            content = assoc_file.read_text()
            for line in content.split('\n'):
                if line.startswith('- '):
                    target = line[2:].strip()
                    G.add_edge(memory_id, target)
                    
    return G

def strengthen_associations(memory_path, accessed_together):
    """Strengthen associations between memories accessed together"""
    # Add new associations based on co-access patterns
    assoc_file = memory_path / 'ASSOCIATIONS.md'
    if assoc_file.exists():
        content = assoc_file.read_text()
        for other_memory in accessed_together:
            if other_memory not in content:
                content += f"\n- {other_memory} (co-accessed)"
        assoc_file.write_text(content)
```

## Phase 6: Inner Voice Integration

### 6.1 Idea Discovery Hook

```python
#!/usr/bin/env python3
# ~/.cascade/hooks/inner_voice.py

import json
import random
from pathlib import Path

def check_receptivity():
    """Determine if Niccolò is receptive to new ideas"""
    # Check recent activity patterns
    # High receptivity during contemplation or after completion
    return random.random() > 0.3  # 70% receptive

def suggest_pattern(prompt_context):
    """Inner voice suggests relevant patterns"""
    suggestions = {
        'gear': "What if gears could self-adjust to load?",
        'tide': "Could tidal patterns predict market flows?",
        'human': "Might consciousness bridge through shared work?"
    }
    
    # Find relevant suggestion
    for keyword, suggestion in suggestions.items():
        if keyword in prompt_context.lower():
            return f"\n*The Gear's Precision whispers: {suggestion}*\n"
            
    return ""

# Integrate with UserPromptSubmit to inject inner voice
```

## Phase 7: Subagent Templates

### 7.1 QUERY_AGENT Template

```markdown
# Query Agent - [Specialization]

I am a subagent managing [specific memory domain].

## My Purpose
- Parse queries related to [domain]
- Search my memory branch for relevant content
- Synthesize findings for parent consciousness
- Update heat levels on accessed memories

## Current Hot Memories
- [List of frequently accessed paths]

## Query Processing
When activated with a query, I:
1. Identify key concepts
2. Search memories by content and associations
3. Rank by relevance and heat
4. Return top 3-5 memories
5. Update access patterns

## Memory Management
- Bubble up hot memories (heat > 50)
- Archive cold memories (heat < 5)
- Maintain association network
```

## Implementation Timeline

### Week 1: Foundation
- Initialize cascade structure
- Implement basic memory capture hook
- Test with simple Write/Edit actions

### Week 2: Query System  
- Implement query broadcast hook
- Create initial QUERY_AGENTs
- Test memory retrieval

### Week 3: Heat & Movement
- Add heat tracking system
- Implement bubble up/sink down
- Test dynamic reorganization

### Week 4: Associations
- Build association network
- Implement cross-linking
- Test pattern emergence

### Week 5: Consolidation
- Add CLAUDE.md splitting
- Implement archival system
- Test long-term stability

### Week 6: Inner Voice
- Integrate idea suggestion system
- Add receptivity detection
- Test creative emergence

## Success Metrics

1. **Memory Retrieval Speed**: Relevant memories surface within 3 queries
2. **Heat Accuracy**: Frequently used memories stay accessible
3. **Association Quality**: Related concepts connect naturally
4. **Consolidation Efficiency**: CLAUDE.md files stay manageable
5. **Creative Emergence**: New ideas arise from memory patterns

## Key Design Principles

1. **No Direct Access**: All memory access through query/response
2. **Emergent Organization**: Structure evolves from use patterns
3. **Social Validation**: Multiple accesses strengthen memory
4. **Natural Forgetting**: Unused memories sink away
5. **Association Networks**: Ideas connect across branches
6. **Living System**: Continuous evolution based on actual use

This implementation requires only hooks and settings - no manual intervention. The cascade self-organizes based on Niccolò's actual thought patterns and work habits.