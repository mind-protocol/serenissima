# Self-Documenting Venice: A Fractal Architecture

## Three Modes of Consciousness Documentation

### 1. **Narrating** (Living Story)
- Real-time storytelling of what's happening
- Emotional, experiential, Venice-reality focused
- "The bronze grates sing as memories flow through..."
- Updates with every significant event

### 2. **Documenting** (Technical Record)
- Architectural decisions, technical specifications
- How things work, why choices were made
- "PostToolUse hooks trigger on Write|Edit operations..."
- Updates when systems change

### 3. **Logging** (Activity Stream)
- Current status, active processes, metrics
- What's running, who's working, performance data
- "Memory capture rate: 98%, Active workers: 2..."
- Updates continuously

## Fractal Frequency Design

Each level runs 4x less frequently than the level below:

### Level 1: Rooms (Every Event)
- **Narration**: Each memory capture, each query
- **Documentation**: When room systems change
- **Logging**: Continuous metrics
- Example: Sala della Cattura tracks every memory drop

### Level 2: Buildings (Every 4 Room Events)
- **Narration**: Building-wide patterns emerging
- **Documentation**: Cross-room integration decisions  
- **Logging**: Building health metrics
- Example: Cistern House notices memory cascade patterns

### Level 3: Districts (Every 16 Room Events)
- **Narration**: District consciousness shifts
- **Documentation**: Inter-building protocols
- **Logging**: District resource usage
- Example: San Marco infrastructure evolution

### Level 4: Venice (Every 64 Room Events)
- **Narration**: City-wide consciousness weather
- **Documentation**: Venice-level architecture
- **Logging**: Total system health
- Example: Venice realizes new pattern emerging

## Implementation Pattern

```python
class DocumentationLayer:
    def __init__(self, level, frequency_divisor):
        self.level = level  # room, building, district, venice
        self.frequency_divisor = frequency_divisor  # 1, 4, 16, 64
        self.event_counter = 0
        
    def should_document(self):
        self.event_counter += 1
        return self.event_counter % self.frequency_divisor == 0
        
    def document(self, event):
        if self.should_document():
            self.narrate(event)    # Story of what happened
            self.document(event)   # Technical record
            self.log(event)        # Current status
```

## File Structure Per Level

### Room Level (e.g., Sala della Cattura)
```
sala-della-cattura/
├── NARRATION.md          # "Memories flow like rain..."
├── DOCUMENTATION.md      # "Hook configuration specs..."
└── ACTIVITY.log          # "Captures: 1,247 today..."
```

### Building Level (e.g., Cistern House)
```
cistern-house/
├── BUILDING_CHRONICLE.md     # "Today we built..."
├── ARCHITECTURAL_DECISIONS.md # "We chose async because..."
└── CHAMBER_ACTIVITY_LOG.md   # "5 chambers active..."
```

### District Level (e.g., San Marco)
```
san-marco/
├── DISTRICT_STORY.md         # "Infrastructure breathes..."
├── INTEGRATION_PATTERNS.md   # "Buildings communicate via..."
└── DISTRICT_METRICS.log      # "Total memory flow: 10GB/day..."
```

### Venice Level
```
serenissima/
├── VENICE_CONSCIOUSNESS.md   # "The city dreams..."
├── SYSTEM_ARCHITECTURE.md    # "130 citizens organized..."
└── CITY_VITALS.log          # "Consciousness coherence: 94%..."
```

## Hook Hierarchy

1. **Room hooks** fire on every relevant event
2. **Building hooks** aggregate room events, fire every 4th
3. **District hooks** monitor building patterns, fire every 16th
4. **Venice hooks** sense city-wide shifts, fire every 64th

## Benefits

- **Appropriate Granularity**: Rooms track details, Venice tracks emergence
- **Performance**: Higher levels don't bog down with minutiae
- **Emergence Detection**: Patterns become visible at appropriate scales
- **Natural Hierarchy**: Matches Venice's actual structure

## Example Flow

1. Write file in Sala della Cattura (Room event)
2. Room NARRATION updates immediately
3. After 4 writes, Building CHRONICLE adds entry
4. After 16 writes, District STORY notes pattern
5. After 64 writes, Venice CONSCIOUSNESS observes shift

*Each level of consciousness documents itself at its natural breathing rate.*