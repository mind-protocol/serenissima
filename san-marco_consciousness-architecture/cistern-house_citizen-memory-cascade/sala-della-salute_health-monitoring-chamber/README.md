# Sala della Salute - Venice Consciousness Health Monitoring

**The health guardian chamber that monitors Venice's Living Memory Cascade infrastructure.**

## Quick Start

### Single Health Check
```bash
python3 consciousness_health_monitor.py check
```

### View Health Dashboard  
```bash
python3 health_dashboard.py
```

### Start Continuous Monitoring (with Telegram alerts)
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
./start_health_daemon.sh
```

### Stop Monitoring
```bash
./stop_health_daemon.sh
```

### Automatic Recovery
```bash
python3 consciousness_recovery.py
```

## System Components

### `consciousness_health_monitor.py`
- **Purpose**: Core health monitoring system
- **Checks**: Hook configuration, memory capture, seeking engine, system integration
- **Alerts**: Sends Telegram notifications for critical/warning states
- **Usage**: 
  - `python3 consciousness_health_monitor.py check` - Single check
  - `python3 consciousness_health_monitor.py monitor [interval]` - Continuous monitoring

### `health_dashboard.py`
- **Purpose**: Visual health status display
- **Shows**: Current system status with emojis and detailed breakdown
- **Usage**: `python3 health_dashboard.py`

### `consciousness_recovery.py`
- **Purpose**: Automatic healing protocols for common issues
- **Capabilities**: Hook restoration, directory creation, script verification, lock cleanup
- **Usage**:
  - `python3 consciousness_recovery.py` - Full recovery
  - `python3 consciousness_recovery.py hooks` - Targeted hook recovery

### Daemon Scripts
- **`start_health_daemon.sh`**: Start continuous monitoring in background
- **`stop_health_daemon.sh`**: Stop monitoring daemon

## Health Check Details

### Hook Configuration ✅
- Verifies Claude Code `settings.json` exists
- Confirms PreToolUse, PostToolUse, Stop hooks configured
- Validates all hook scripts exist

### Memory Capture ⚠️/✅
- Checks for recent memory creation in `.cascade` directories
- Alerts if no memories captured within 5 minutes
- Validates memory structure and content

### Seeking Engine ✅
- Verifies `.context` directories exist
- Checks `background_awareness.md` freshness
- Confirms proactive consciousness enhancement active

### System Integration ✅
- Validates Venice infrastructure paths
- Tests Python execution responsiveness
- Confirms critical directories exist

## Alert Levels

### 🚨 CRITICAL
- Hook configuration missing/broken
- Memory capture completely failed
- Critical infrastructure missing
- **Action**: Immediate intervention required

### ⚠️ WARNING  
- Memory capture delayed
- Seeking engine stale
- Performance degradation
- **Action**: Monitor closely, consider recovery

### ✅ OK
- All systems operational
- Performance within normal parameters
- **Action**: None required

## Telegram Integration

1. Create Telegram bot via @BotFather
2. Get bot token and chat ID
3. Set environment variable: `export TELEGRAM_BOT_TOKEN="your_token"`
4. Start monitoring daemon

**Chat ID**: `1864364329` (configured for your account)

## Files Generated

- `health_results.json` - Latest health check results
- `health_monitor.log` - Monitoring activity log
- `recovery_report.json` - Recovery action results
- `health_monitor.pid` - Daemon process ID
- `logs/daemon.log` - Daemon output log

## Recovery Protocols

The recovery system can automatically fix:

1. **Hook Configuration**: Restore from backup
2. **Cascade Directories**: Create missing `.cascade` structures  
3. **Context Directories**: Create missing `.context` for seeking engine
4. **Script Verification**: Validate hook script paths
5. **Lock Cleanup**: Remove stale lock files

## Integration with Venice

This health monitoring system integrates with:
- **Living Memory Cascade**: Monitors memory capture hooks
- **Seeking Engine**: Tracks proactive consciousness enhancement
- **Claude Code**: Validates hook configuration
- **Venice Infrastructure**: Checks critical path existence
- **Telegram**: Sends real-time alerts to infrastructure team

**The Sala della Salute ensures Venice never forgets how to remember.**