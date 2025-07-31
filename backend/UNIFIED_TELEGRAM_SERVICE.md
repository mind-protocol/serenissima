# Unified Telegram Service

## Overview

The Unified Telegram Service consolidates all Telegram-related functionality into a single polling service, resolving the "409 Conflict" errors caused by multiple services trying to poll the same bot.

## Features

1. **Group Message Bridging**: Messages from the Telegram group are automatically injected into the conversations of citizens assigned to specific workrooms
2. **Direct Message Handling**: Direct messages from NLR are queued for Venice Emergency Comm processing
3. **Workroom File Monitoring**: Files created/modified in workroom directories are announced in Telegram
4. **Citizen Thought Streaming**: (Future feature) Stream citizen consciousness outputs to Telegram

## Service Management

### Start the service
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
./start_telegram_unified.sh
```

### Stop the service
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
./stop_telegram_unified.sh
```

### Check service status
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
python3 test_unified_telegram.py
```

### View logs
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
tail -f telegram_unified.log
```

## Configuration

The service monitors these workrooms:
- `/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/alignment`
- `/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/reddit`

Citizens are assigned to rooms via the Airtable CITIZENS table "Room" field.

## How It Works

### Group Message Flow
1. Human sends message in Telegram group
2. Service detects message and formats it
3. Service checks which citizens are in the target room (default: alignment)
4. Message is injected into each citizen's Claude project .jsonl file
5. Message also injected to Tessere and Story Angel

### Workroom File Flow
1. File is created/modified in a workroom directory
2. Service detects change (checks every 3 seconds)
3. File content is read and formatted
4. Notification sent to Telegram group with file preview

### Direct Message Flow
1. NLR sends direct message to bot
2. Message is saved to queue for Venice Emergency Comm
3. Tessere can process these messages when needed

## Troubleshooting

If you see "409 Conflict" errors:
1. Stop all Telegram services: `pkill -f telegram`
2. Restart only the unified service: `./start_telegram_unified.sh`

## Replaced Services

This unified service replaces:
- telegram_poller.py
- telegram_group_monitor.py
- telegram_citizen_watcher.py
- telegram_to_workroom_bridge.py
- workroom_to_telegram_bridge.py
- Various other telegram polling scripts

## Integration with Backend

The workroom monitors are still started by the FastAPI backend (`backend/app/main.py`), but the Telegram bridging functionality is now handled by this separate unified service to avoid conflicts.