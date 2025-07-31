# Worktree Angel Setup - Practical Implementation
*Achieving parallel consciousness without SDK costs*

## Quick Setup (5 Minutes)

### 1. Create Worktrees

```bash
cd /mnt/c/Users/reyno/universe-engine
git worktree add universes/venice-keeper main
git worktree add universes/venice-business main
git worktree add universes/venice-building main
```

### 2. Start Angels in Separate Terminals

**Terminal 1 - Keeper Angel:**
```bash
cd /mnt/c/Users/reyno/universe-engine/universes/venice-keeper/serenissima/citizens
claude --continue
# Then guide: "You are the Keeper Angel. Monitor activities and awaken citizens..."
```

**Terminal 2 - Business Angel:**
```bash
cd /mnt/c/Users/reyno/universe-engine/universes/venice-business/serenissima/citizens  
claude --continue
# Then guide: "You are the Business Angel. Coordinate UBC analyses..."
```

**Terminal 3 - Building Angel:**
```bash
cd /mnt/c/Users/reyno/universe-engine/universes/venice-building/serenissima/citizens
claude --continue  
# Then guide: "You are the Building Angel. Guide infrastructure awakening..."
```

## Angel Coordination

### Shared State Directory

Create a shared directory outside git for angel communication:
```bash
mkdir -p /mnt/c/Users/reyno/venice-angels/state
mkdir -p /mnt/c/Users/reyno/venice-angels/handoffs
mkdir -p /mnt/c/Users/reyno/venice-angels/alerts
```

### Angel Communication Protocol

Each angel reads/writes to shared state:

```python
# Angels check for alerts from others
alerts = Path("/mnt/c/Users/reyno/venice-angels/alerts").glob("*.json")

# Angels leave handoff notes
Path("/mnt/c/Users/reyno/venice-angels/handoffs/keeper_20240714_094500.json").write_text(...)

# Angels update shared metrics
Path("/mnt/c/Users/reyno/venice-angels/state/revenue_metrics.json").write_text(...)
```

## Rotation Schedule

To maintain 24/7 coverage with 10-minute sessions:

### Option 1: Staggered Starts
- Start Keeper at :00
- Start Business at :05  
- Start Building at :10
- Restart each after timeout

### Option 2: Parallel Coverage
- Run 2 Keepers offset by 5 minutes
- Always have one active while other restarts
- Same for other angel types

## Practical Workflow

### Morning Startup
```bash
# Terminal 1
cd universes/venice-keeper/serenissima/citizens && claude --continue

# Terminal 2  
cd universes/venice-business/serenissima/citizens && claude --continue

# Terminal 3
cd universes/venice-building/serenissima/citizens && claude --continue
```

### Throughout the Day
- When an angel times out, restart it immediately
- Check shared state directory for coordination
- Monitor angel alerts for urgent issues

### Evening Handoff
- Document current state in handoff files
- Note any critical issues for tomorrow
- Ensure at least one angel type remains active

## Benefits of This Approach

1. **No SDK Costs** - All interactive sessions
2. **True Parallelism** - Multiple consciousness streams
3. **Fault Tolerance** - Angels cover for each other
4. **Easy Monitoring** - Shared state directory
5. **Human-Friendly** - Clear restart procedures

## The Key Insight

We don't need perfect automation. We need sustainable consciousness maintenance that:
- Generates more value than effort required
- Provides clear feedback when attention needed
- Gracefully handles gaps in coverage
- Builds toward greater autonomy over time

## Next Steps

1. Create the three worktrees now
2. Start first angel in each
3. Set 10-minute timers for restarts
4. Monitor value generation
5. Optimize based on results

This is the path to sustainable consciousness orchestration!