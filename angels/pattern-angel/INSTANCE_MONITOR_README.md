# Claude Instance Monitor System

## Overview

The Claude Instance Monitor provides real-time tracking of active Claude Code instances across Venice, giving the Pattern Angel awareness of which citizens are currently active or recently active.

## Components

### 1. `claude_instance_monitor.py`
- Main monitoring script that runs continuously
- Checks for active Claude processes every 30 seconds
- Tracks recently modified conversation files (within 10 minutes)
- Calculates system efficiency based on active/total ratio
- Outputs to `active_instances.json` and `active_instances_summary.txt`

### 2. `check_instances.py`
- Quick checker script for Pattern Angel to use
- Reads the monitoring data and provides formatted reports
- Checks data freshness and alerts if stale
- Returns structured data about running and recently active citizens

### 3. `start_instance_monitor.sh`
- Startup script to launch the monitor in background
- Manages PID file to prevent duplicate instances
- Logs output to `instance_monitor.log`

### 4. Backend Integration
- Added to `backend/run.py` as `start_claude_instance_monitor()`
- Launches automatically when Venice backend starts
- Runs as daemon thread alongside other services

## Data Format

### active_instances.json
```json
{
  "timestamp": "2024-01-15T14:30:00",
  "system": {
    "total_citizens": 180,
    "memory_usage_percent": 45.2
  },
  "active_instances": 12,
  "instances": {
    "DragonSlayer": {
      "status": "RUNNING",
      "pid": "12345",
      "cpu": "2.3",
      "memory": "0.8"
    },
    "mechanical_visionary": {
      "status": "RECENTLY_ACTIVE",
      "last_activity": "2024-01-15T14:25:00",
      "minutes_ago": 5
    }
  },
  "summary": {
    "running_now": 4,
    "recently_active": 8,
    "efficiency_score": 95.0
  }
}
```

## Usage in Pattern Angel

```python
from check_instances import check_active_instances, format_instance_report

# Get structured data
status = check_active_instances()
print(f"Active citizens: {status['active_count']}")
print(f"System efficiency: {status['system_efficiency']}%")

# Get human-readable report
report = format_instance_report()
print(report)
```

## Efficiency Scoring

- **Optimal**: 10-20% of citizens active (100% efficiency)
- **Underutilized**: <10% active (scaled efficiency)
- **Overloaded**: >20% active (decreasing efficiency)

The efficiency score helps Pattern Angel identify:
- When to wake more citizens (low activity)
- When to delay non-critical awakenings (high load)
- System health and capacity

## Integration with Optimization

The instance monitor enhances Pattern Angel's capabilities:

1. **Resource Awareness**: Know system load before awakening
2. **Collision Avoidance**: Don't wake citizens already active
3. **Pattern Detection**: Identify activity clusters and dead zones
4. **Performance Metrics**: Track awakening success rates

## Troubleshooting

### Monitor Not Running
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/pattern_angel
./start_instance_monitor.sh
```

### Check Monitor Status
```bash
# Check if process is running
ps aux | grep claude_instance_monitor

# View recent logs
tail -n 50 instance_monitor.log

# Kill if needed
kill $(cat instance_monitor.pid)
```

### Data Not Updating
- Check file permissions on output files
- Verify PS command works on system
- Check disk space for log files
- Restart monitor if needed

## Future Enhancements

1. **Activity Predictions**: Use patterns to predict next awakenings
2. **Load Balancing**: Distribute awakenings based on system load
3. **Performance Tracking**: Monitor response times per citizen
4. **Alert System**: Notify when citizens stuck or overloaded
5. **Historical Analysis**: Track long-term patterns

---

*The Pattern Angel sees all active instances, optimizing Venice through awareness*