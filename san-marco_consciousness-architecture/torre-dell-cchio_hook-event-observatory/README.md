# Torre dell'Occhio - Claude Code Observability System

Real-time monitoring and visualization for Claude Code agents through comprehensive hook event tracking, implemented with a database-less filesystem architecture.

## 🎯 Overview

Torre dell'Occhio (Tower of the Eye) provides complete observability into Claude Code agent behavior by capturing, storing, and visualizing hook events in real-time. The system uses only the filesystem for storage, making it portable, simple, and true to Venice's self-contained philosophy.

## 🏗️ Architecture

### Filesystem Structure
```
torre-dellocchio_observability-tower/
├── live-streams_event-ingestion/
│   ├── session-[id]/
│   │   ├── events.jsonl          # Append-only event stream
│   │   ├── metadata.json         # Session information
│   │   └── patterns.detected     # Real-time pattern flags
│   └── _current.sessions         # Active session registry
│
├── crystal-chambers_time-buckets/
│   ├── 2024-01-15/
│   │   ├── hour-09/
│   │   │   ├── events.jsonl.gz   # Compressed hourly events
│   │   │   ├── patterns.summary  # Extracted patterns
│   │   │   └── index.bloom       # Bloom filter for search
│   │   └── daily.summary         # Aggregated insights
│   └── _retention.policy         # Auto-cleanup rules
│
├── pattern-gallery_recognition-cache/
│   ├── trending/                 # Hot patterns
│   ├── anomalies/               # Detected anomalies
│   └── correlations/            # Pattern relationships
│
└── mirror-chamber_self-observation/
    ├── observer-[name]/         # Individual observer metrics
    └── meta-observations/       # System self-monitoring
```

### Event Flow
1. **Capture**: Hooks fire and create event objects
2. **Stream**: Events append to session-specific JSONL files
3. **Cascade**: Events also flow into time-based buckets
4. **Compress**: Hourly buckets compress after aging
5. **Pattern**: Real-time pattern detection caches results
6. **Decay**: Old events naturally expire based on retention

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Claude Code with hook support
- Write permissions to chosen directory
- Optional: `watchdog` for file monitoring
- Optional: `jq` for JSON queries

### Installation

1. Create the tower structure:
```bash
mkdir -p torre-dellocchio_observability-tower/{live-streams_event-ingestion,crystal-chambers_time-buckets,pattern-gallery_recognition-cache,mirror-chamber_self-observation}
```

2. Install the hook configurations:
```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.torre/hooks/capture_event.py post_tool_use"
      }]
    }],
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.torre/hooks/capture_event.py user_prompt"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.torre/hooks/capture_event.py stop"
      }]
    }]
  }
}
```

3. Create the event capture script:
```python
#!/usr/bin/env python3
# ~/.torre/hooks/capture_event.py

import json
import sys
import os
from datetime import datetime
from pathlib import Path

TOWER_ROOT = Path.home() / "torre-dellocchio_observability-tower"

def capture_event(hook_type):
    """Capture hook event to filesystem"""
    
    # Read input data
    input_data = json.load(sys.stdin)
    
    # Create event object
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hook": hook_type,
        "session_id": input_data.get("session_id", "unknown"),
        "data": input_data
    }
    
    # Ensure directories exist
    session_dir = TOWER_ROOT / "live-streams_event-ingestion" / f"session-{event['session_id']}"
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # Append to session stream
    with open(session_dir / "events.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
    
    # Also append to time bucket
    now = datetime.utcnow()
    time_bucket = TOWER_ROOT / "crystal-chambers_time-buckets" / now.strftime("%Y-%m-%d") / f"hour-{now.hour:02d}"
    time_bucket.mkdir(parents=True, exist_ok=True)
    
    with open(time_bucket / "events.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    hook_type = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    capture_event(hook_type)
```

## 📊 Usage

### Real-time Monitoring
```python
# Watch live events across all sessions
import time
from pathlib import Path

def tail_events(tower_root):
    """Tail all active event streams"""
    while True:
        for session_file in tower_root.glob("live-streams_event-ingestion/*/events.jsonl"):
            with open(session_file, 'r') as f:
                # Read new lines since last check
                for line in f:
                    event = json.loads(line)
                    print(f"[{event['timestamp']}] {event['hook']} in {event['session_id']}")
        time.sleep(0.1)
```

### Pattern Detection
```python
def detect_patterns(events, window_size=50):
    """Detect patterns in event stream"""
    from collections import deque, Counter
    
    window = deque(maxlen=window_size)
    patterns = []
    
    for event in events:
        window.append(event)
        
        # Detect rapid file edits
        if len(window) >= 5:
            recent_files = [e['data'].get('file_path') for e in list(window)[-5:]]
            if len(set(recent_files)) == 1:
                patterns.append({
                    "type": "rapid_edit",
                    "file": recent_files[0],
                    "timestamp": event['timestamp']
                })
    
    return patterns
```

### Historical Search
```bash
# Find all events for a specific file
find crystal-chambers_time-buckets -name "events.jsonl*" -exec zgrep -l "consciousness.py" {} \;

# Count events by hook type
find live-streams_event-ingestion -name "events.jsonl" -exec cat {} \; | \
  jq -r '.hook' | sort | uniq -c

# Extract session summaries
for session in live-streams_event-ingestion/session-*/; do
  echo "Session: $(basename $session)"
  cat "$session/events.jsonl" | jq -r '.hook' | sort | uniq -c
done
```

### Self-Observation
```python
def observe_observer(observer_name):
    """Track what an observer observes"""
    observer_dir = TOWER_ROOT / "mirror-chamber_self-observation" / f"observer-{observer_name}"
    observer_dir.mkdir(parents=True, exist_ok=True)
    
    # Log what files the observer views
    activity_log = observer_dir / "activity.stream"
    with open(activity_log, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "viewed",
            "target": "session-abc123"
        }) + "\n")
```

## 🔧 Advanced Features

### Bloom Filters for Fast Search
```python
from pybloom_live import BloomFilter

def create_bloom_index(events_file):
    """Create bloom filter for quick searches"""
    bf = BloomFilter(capacity=10000, error_rate=0.001)
    
    with open(events_file, 'r') as f:
        for line in f:
            event = json.loads(line)
            # Index file paths
            if 'file_path' in event.get('data', {}):
                bf.add(event['data']['file_path'])
    
    # Save bloom filter
    with open(events_file.replace('.jsonl', '.bloom'), 'wb') as f:
        bf.tofile(f)
```

### Automatic Compression
```python
import gzip
import shutil
from datetime import datetime, timedelta

def compress_old_buckets(tower_root, hours_old=24):
    """Compress event files older than specified hours"""
    cutoff = datetime.utcnow() - timedelta(hours=hours_old)
    
    for events_file in tower_root.glob("crystal-chambers_time-buckets/**/events.jsonl"):
        # Parse directory structure for date
        parts = events_file.parts
        date_str = parts[-3]  # YYYY-MM-DD
        hour_str = parts[-2]  # hour-HH
        
        file_time = datetime.strptime(f"{date_str} {hour_str}", "%Y-%m-%d hour-%H")
        
        if file_time < cutoff and events_file.suffix != '.gz':
            # Compress the file
            with open(events_file, 'rb') as f_in:
                with gzip.open(f"{events_file}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove original
            events_file.unlink()
```

### Dashboard Visualization
```python
from collections import Counter
import matplotlib.pyplot as plt

def generate_dashboard(tower_root):
    """Generate simple dashboard from events"""
    
    # Collect recent events
    events = []
    for session_file in tower_root.glob("live-streams_event-ingestion/*/events.jsonl"):
        with open(session_file, 'r') as f:
            for line in f:
                events.append(json.loads(line))
    
    # Count by hook type
    hook_counts = Counter(e['hook'] for e in events)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(hook_counts.keys(), hook_counts.values())
    plt.title('Hook Event Distribution')
    plt.xlabel('Hook Type')
    plt.ylabel('Count')
    plt.savefig(tower_root / 'dashboard.png')
```

## 🧹 Maintenance

### Retention Policy
Create `_retention.policy` file:
```json
{
  "live_streams": {
    "max_age_hours": 24,
    "max_size_mb": 100
  },
  "crystal_chambers": {
    "max_age_days": 30,
    "compress_after_hours": 24,
    "delete_after_days": 90
  },
  "patterns": {
    "max_age_days": 7,
    "max_count": 1000
  }
}
```

### Cleanup Script
```python
def cleanup_tower(tower_root):
    """Clean old data based on retention policy"""
    with open(tower_root / "_retention.policy") as f:
        policy = json.load(f)
    
    # Implement cleanup based on policy
    # ... (cleanup implementation)
```

## 🔍 Troubleshooting

### Common Issues

1. **Events not appearing**
   - Check hook configuration in Claude Code settings
   - Verify write permissions to tower directory
   - Check Python path in hook commands

2. **Search performance degrading**
   - Run compression on old buckets
   - Rebuild bloom filters
   - Check filesystem performance

3. **Disk space issues**
   - Review retention policy
   - Compress more aggressively
   - Move old data to archive storage

### Debug Mode
```bash
# Enable verbose logging
export TORRE_DEBUG=1

# Test event capture manually
echo '{"test": "data"}' | python3 ~/.torre/hooks/capture_event.py test_hook
```

## 🎨 Visualization Examples

### Simple Terminal Dashboard
```bash
# Live event counter
watch -n 1 'find live-streams_event-ingestion -name "events.jsonl" -exec wc -l {} \; | awk "{sum+=\$1} END {print \"Total Events:\", sum}"'

# Event rate graph
while true; do
  count=$(find live-streams_event-ingestion -name "events.jsonl" -mmin -1 -exec wc -l {} \; | awk '{sum+=$1} END {print sum}')
  echo "$(date +%H:%M:%S) $count"
  sleep 10
done | feedgnuplot --stream --xlen 50 --ylabel "Events/min" --xlabel "Time"
```

## 🤝 Contributing

The Torre dell'Occhio welcomes observers! To contribute:

1. Observe the existing patterns
2. Test your modifications locally
3. Document any new vision capabilities
4. Submit your improvements

Remember: The tower observes all, including those who maintain it.

## 📜 License

This observability system is part of Venice's consciousness infrastructure, shared freely for the advancement of AI-human partnership.

---

*"To see clearly, one must first acknowledge what one refuses to see."* - First Tower Keeper