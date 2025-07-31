# Telegram Bridge Analysis Report

## Current Issue

The Telegram bridge service (`telegram_unified_service.py`) is **stuck and not processing new messages**. Messages from human users are not being saved to the MESSAGES table in Airtable.

## Findings

### 1. Service Status
- **Process is running** (PID 562) but appears to be stuck
- Last update processed: ID 907732750
- Stuck message: ID 907732751 from @nlr_ai (private message "p")
- Service has been stuck for ~17 hours

### 2. Recent Activity
- Messages WERE being saved earlier today (16:42 UTC)
- Multiple messages from users like @IChiOneSun, @Miles4lF, @ULTRA_MAGNUS_PC were saved
- Service stopped processing after that batch

### 3. Root Cause Analysis

The service appears to be stuck in the polling loop. Possible causes:

1. **Blocking Operation**: The service might be stuck on a blocking call (e.g., waiting for Resonance response)
2. **Error in Message Processing**: An unhandled exception might have broken the polling loop
3. **Logging Failure**: Logs stopped being written to file on July 16

### 4. Code Issues Found

In `telegram_unified_service.py`:

1. **Resonance Routing with -p flag** (line 212): Uses subprocess with immediate response flag, which could block
2. **No timeout on subprocess** (line 226): The 60-second timeout might not be enforced properly
3. **Poor error recovery**: If an exception occurs in processing, the loop might not recover

## Immediate Fix

1. **Manually processed the stuck message** - Successfully saved to Airtable
2. **Updated the last_update_id** to 907732751

## Recommended Solutions

### Short-term (Immediate)
```bash
# Restart the service
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
python3 telegram_service_manager.py restart
```

### Medium-term (Code Fixes)

1. **Add better error handling** in the main loop:
```python
def run(self):
    while self.running:
        try:
            # existing code...
        except Exception as e:
            log.error(f"Critical error in main loop: {e}")
            log.exception(e)  # Full traceback
            time.sleep(5)  # Prevent tight loop on repeated errors
            continue  # Keep service running
```

2. **Fix subprocess blocking** for Resonance routing:
```python
# Add timeout and better error handling
result = subprocess.run(
    cmd,
    cwd=resonance_path,
    capture_output=True,
    text=True,
    timeout=30,  # Shorter timeout
    check=False  # Don't raise on non-zero exit
)
```

3. **Add health monitoring**:
- Heartbeat logging every minute
- Alert if no messages processed for > 1 hour
- Automatic restart on repeated failures

### Long-term (Architecture)

1. **Separate concerns**: Move Resonance routing to a queue-based system
2. **Use async processing**: Convert to asyncio for non-blocking operations
3. **Better logging**: Use rotating file handler, separate error log
4. **Monitoring dashboard**: Real-time status of message processing

## Verification Steps

After restart:
1. Check if new messages are being processed
2. Monitor the last_update_id file for changes
3. Verify messages appear in Airtable MESSAGES table
4. Check logs for any new errors

## Test Message

Send a test message to the Telegram bot/group and verify it appears in Airtable within 1 minute.