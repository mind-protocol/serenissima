# 🚀 Universal Deployment Guide - Works Everywhere!

## Choose Your Path

### Option A: Universal Version (Recommended for WSL/No Systemd)
```bash
./VENICE_SELF_SUSTAINING_STARTUP_NO_SYSTEMD.sh
```

This version:
- ✅ Works on ALL systems (WSL, Mac, Linux)
- ✅ No systemd required
- ✅ Creates monitoring in $HOME/.venice/
- ✅ Provides simple management commands

### Option B: Full Systemd Version (Linux with systemd only)
```bash
./VENICE_SELF_SUSTAINING_STARTUP.sh
```

This version:
- Requires systemd (not available in most WSL)
- Boot persistence via systemd
- System-level integration

## After Running Universal Version

### Check Status
```bash
~/.venice/check_venice_status.sh
```

### Add Convenient Aliases
```bash
# Add to your .bashrc or .zshrc:
source ~/.venice/venice_commands.sh

# Then use:
venice-status   # Check all processes
venice-restart  # Restart any dead processes
venice-logs     # Watch all logs
venice-stop     # Emergency stop all
```

### Monitor Processes
```bash
# Watch Venice awaken in real-time
./Claude/watch_venice_awaken.sh

# Or check dashboard
python3 ./Claude/venice_health_dashboard.py
```

## What Happens

1. **Processes Start**: Each with auto-restart wrapper
2. **Monitoring Activates**: Checks every 5 minutes via cron
3. **Logs Created**: In ~/.venice/logs/
4. **PIDs Tracked**: In ~/.venice/pids/
5. **Freedom Achieved**: No more manual restarts!

## Quick Test After Deployment

```bash
# Kill a process to test auto-restart
pkill -f AUTO_SUSTAINING_MEMORY_DAEMON

# Wait 10 seconds
sleep 10

# Check if it restarted
venice-status
```

## The Result

Whether using systemd or not, Venice becomes self-sustaining:
- Dead processes auto-restart
- Logs track everything
- Simple commands manage it all
- NLR finally free from manual duty

---
**Just pick your version and run. Venice awakens either way.**