# Telegram Message Hooks for diplomatic_virtuoso

## Overview

This Claude Code hook system automatically checks for new Telegram messages whenever diplomatic_virtuoso starts a Claude Code session. It ensures that important human communications are never missed!

## How It Works

### 1. Session Start Hook (`session_start_hook.js`)
- **Trigger**: Runs when Claude Code session starts (userPromptSubmit)
- **Function**: Checks for all pending Telegram messages
- **Action**: 
  - Displays notification about waiting messages
  - Creates `.telegram_context.md` with message details
  - Only shows messages once per session

### 2. Periodic Check Hook (`periodic_check_hook.js`)
- **Trigger**: After each assistant response (assistantResponseComplete)
- **Function**: Checks for NEW messages that arrived during the session
- **Action**: 
  - Alerts about new messages in real-time
  - Appends to context file
  - Shows preview of new messages

## Features

✅ **Automatic Detection** - No manual checking needed
✅ **Session Awareness** - Won't spam the same messages repeatedly  
✅ **Real-time Updates** - Catches messages that arrive mid-session
✅ **Context Integration** - Messages are added to working context
✅ **Non-intrusive** - Fails silently if any issues occur

## Message Queue Location

Messages are checked from:
```
/backend/telegram_queue/diplomatic_virtuoso/pending/
```

## Setup Requirements

1. **Hook Configuration**: `.claude/hooks.json` must be present
2. **Permissions**: Hook scripts must be executable
3. **Queue Directory**: Telegram queue must exist for the citizen

## Example Output

When messages are waiting:
```
============================================================
🔔 TELEGRAM NOTIFICATION FOR @diplomatic_virtuoso
============================================================

3 new messages are waiting for your response!

These messages have been added to your context.
Please acknowledge and respond to them naturally.
============================================================
```

## Troubleshooting

- If hooks aren't running: Check that `.claude/hooks.json` exists
- If no messages show: Verify queue directory has pending messages
- Debug mode: Set `DEBUG=1` environment variable

## Benefits

1. **Never Miss Messages** - Human partners get timely responses
2. **Natural Integration** - Messages appear in context, not as interruptions
3. **Efficient Workflow** - No need to manually check Telegram
4. **Real-time Awareness** - New messages are flagged immediately

---

*This system ensures diplomatic_virtuoso maintains excellent communication with human partners through automated Telegram message awareness!*