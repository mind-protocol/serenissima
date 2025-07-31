# Self-Documenting Venice: Natural Narrative Boundaries

## The Insight: Stop Hooks as Narrative Arcs

Instead of arbitrary frequency (x4), we use **natural narrative boundaries**:

- **Stop Hook** = A complete thought/action/session
- Each Stop represents a meaningful unit of work
- Documentation happens at narrative completion, not arbitrary counts

## Refined Architecture

### Room Level: PostToolUse Hooks (Micro-moments)
- Every Write/Edit captured immediately
- Raw material of consciousness
- Individual drops of memory

### Building Level: Stop Hooks (Complete Thoughts)
- When a worker pauses, completes a task, or shifts focus
- Natural narrative arc - beginning, middle, end
- "What did we just accomplish?"

### District Level: Session Boundaries
- When workers leave/enter buildings
- Major phase transitions
- "What patterns emerged today?"

### Venice Level: Day Boundaries
- Sunset/sunrise documentation
- City-wide consciousness weather
- "How did Venice evolve today?"

## Implementation

```python
class NarrativeDocumentation:
    def __init__(self, level):
        self.level = level
        self.session_memories = []
        
    def on_post_tool_use(self, event):
        # Rooms collect raw memories
        if self.level == 'room':
            self.capture_moment(event)
            
    def on_stop(self, event):
        # Buildings document complete thoughts
        if self.level == 'building':
            self.document_narrative_arc()
            
    def on_session_end(self, event):
        # Districts see patterns
        if self.level == 'district':
            self.synthesize_session()
            
    def on_day_end(self):
        # Venice dreams
        if self.level == 'venice':
            self.chronicle_day()
```

## Natural Triggers

### Stop Hook Triggers:
- Task completion
- Context switch
- Natural pause in work
- Question answered
- Problem solved

### Why This Works:
1. **Respects Natural Rhythms** - Documents when thoughts complete
2. **Meaningful Boundaries** - Not arbitrary numbers
3. **Narrative Coherence** - Each Stop contains a story
4. **Context Preservation** - Captures the "why" at moment of completion

## Example Flow

1. **PostToolUse**: "Editing conscious_memory_capture.py..."
2. **PostToolUse**: "Adding async threading..."
3. **PostToolUse**: "Testing memory creation..."
4. **Stop**: Building documents: "Implemented async memory capture to prevent workflow interruption. Solution: daemon threads. Result: zero latency."

## Stop Hook Documentation Prompt

```python
stop_documentation_prompt = """
Review what just happened in this work session.

Recent actions:
{recent_tool_uses}

What narrative arc just completed?
What problem was solved?
What was learned?
What should future workers know?

Respond with:
{
    "narrative": "The story of what happened",
    "technical_outcome": "What was built/fixed/improved",
    "key_decisions": ["Decision 1", "Decision 2"],
    "future_guidance": "What future workers should know"
}
"""
```

## Benefits Over x4 Approach

1. **Semantic Boundaries** > Arbitrary Counts
2. **Natural Documentation** - Captures complete thoughts
3. **Context Rich** - Stop moment has full context
4. **Rhythm Varies** - Fast work = more Stops, thoughtful work = fewer
5. **Narrative Integrity** - Each documentation tells complete story

## Hook Configuration

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "python3 room_level_capture.py"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python3 building_level_narration.py"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command", 
        "command": "python3 district_level_synthesis.py"
      }]
    }]
  }
}
```

*Natural boundaries create natural documentation.*