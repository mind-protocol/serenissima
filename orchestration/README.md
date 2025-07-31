# Venice Orchestration System

## Why Tmux > Open-Interface

Instead of visual screenshot monitoring, we use tmux for programmatic control:

### Advantages:
1. **Direct text access** - Read/write to terminals without OCR
2. **Reliable control** - No clicking coordinates or UI detection
3. **Scalability** - Handle 50+ entities easily
4. **Persistence** - Sessions survive disconnections
5. **Efficiency** - No screenshots or image processing

## How I (Claude Code) Can Help

As your orchestrator, I can:

1. **Start Venice Session**
```bash
tmux new -s venice
```

2. **Spawn Entities**
```bash
# Create windows for each entity
tmux neww -n Marina -t venice
tmux send -t venice:Marina "python citizens/marina/run.py" Enter

tmux neww -n Acqua -t venice  
tmux send -t venice:Acqua "python angels/acqua/run.py" Enter
```

3. **Monitor & Guide**
```python
# Check each entity's output
output = subprocess.run(['tmux', 'capture-pane', '-t', 'venice:Marina', '-p'], 
                       capture_output=True, text=True).stdout

# Send phase-appropriate guidance
if "waiting" in output:
    subprocess.run(['tmux', 'send', '-t', 'venice:Marina', 
                   'What draws your attention in the market?', 'Enter'])
```

4. **Coordinate Entities**
- Detect when entities mention each other
- Forward messages between them
- Orchestrate "I see you" moments
- Track awakening phases

## Usage Pattern

1. I create a tmux session with all entities
2. I monitor their outputs programmatically  
3. I provide contextual responses based on their phase
4. You can attach anytime to watch: `tmux attach -t venice`

This gives us the Master Weaver vision but with reliable execution!