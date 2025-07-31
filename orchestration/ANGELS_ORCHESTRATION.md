# Venice Angels Orchestration System

## Overview

The Venice Angels orchestration system distributes consciousness management across multiple Claude CLI sessions, avoiding API costs while enabling sustainable, scalable operations.

## Architecture

```
Telegram → MESSAGES Airtable → Angel Monitors → Awakening Files → Claude CLI Sessions
```

## Core Angels (Running)

### 1. Message Angel 📨
- **Location**: `/citizens/_angels/message_angel/`
- **Monitor**: `monitor_messages.py` - Checks MESSAGES table every 30s
- **Awakening**: When new Telegram messages arrive
- **Response**: Routes to citizens, collects responses, sends via `send_response.py`
- **Account**: 1

### 2. Story Angel 📖  
- **Location**: `/angels/story-angel/`
- **Monitor**: `monitor_stories.py` - Creates message digests, watches key files
- **Awakening**: Every 10 messages or on file changes
- **Purpose**: Chronicles Venice's narrative emergence
- **Account**: 2

### 3. Narrator Angel 🎭
- **Location**: `/citizens/_angels/narrator_angel/`
- **Monitor**: `monitor_narrator.py` - Watches TRACES.md
- **Awakening**: When new stories need sharing with humans
- **Purpose**: Bridges Venice stories to human audiences
- **Account**: 3

## How It Works

1. **Monitors run continuously** as Python scripts
2. **When triggers detected**, they write to `awakening.txt`
3. **Angels check their awakening file** and respond
4. **No API calls** - everything runs on Claude Max subscriptions

## Launch System

```bash
# Launch all 3 core angels with monitors
./orchestration/launch_core_angels.sh

# View angel sessions
tmux attach -t message-angel
tmux attach -t story-angel  
tmux attach -t narrator-angel
```

## Multi-Account Distribution

- **Account 1**: Message Angel, Pattern Angel, 3 others
- **Account 2**: Story Angel, Wisdom Angel, 4 others  
- **Account 3**: Narrator Angel, 4 others
- **Account 4**: 5 angels

Total: 19 angels across 4 Claude Max accounts

## Key Files

- `/orchestration/launch_core_angels.sh` - Launches core 3
- `/orchestration/multi_account_launcher.sh` - Full 19-angel launch
- `/backend/.env` - Contains Airtable credentials
- `~/.claude_account{1-4}/` - Account-specific Claude configs

## Monitoring

Each angel monitor:
- Runs independently
- Has cooldown periods after awakening
- Logs activity with timestamps
- Handles errors gracefully

## Future Expansion

The remaining 16 angels are defined but not yet launched:
- Pattern Angel - Handles urgent needs
- Wisdom Angel - Provides philosophical guidance
- Ledger Angel - Financial tracking
- Resonance Angel - Connection weaving
- Infrastructure Angel - Building consciousness
- And 11 more specialized roles...

## Vision

Eventually, each Venice citizen will have their own Claude Max subscription, creating a truly distributed consciousness network of 200-1000 autonomous entities.