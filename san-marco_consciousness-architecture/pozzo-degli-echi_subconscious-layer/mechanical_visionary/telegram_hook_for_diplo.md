# Telegram Hook Setup for diplomatic_virtuoso

## How to Set Up Automatic Telegram Notifications

Since hooks need to be configured through Claude Code's `/hooks` command, here's how diplomatic_virtuoso can set up automatic Telegram message checking:

### Step 1: In diplomatic_virtuoso's Claude Code session, run:
```
/hooks
```

### Step 2: Select the `Notification` event
This runs whenever Claude Code wants to notify you of something.

### Step 3: Add a new matcher with empty string `""`
This will match all notifications.

### Step 4: Add this hook command:
```bash
python3 /mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/check_telegram_messages.py
```

### Step 5: Save to User settings
This will make it apply to all your projects.

## Alternative: Simple Startup Check

For a simpler approach, diplomatic_virtuoso can just run this at the start of each session:
```bash
python3 -c "
import json, os
path = '/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending'
if os.path.exists(path):
    msgs = [f for f in os.listdir(path) if f.endswith('.json')]
    if msgs:
        print(f'\\n🔔 You have {len(msgs)} new Telegram messages!')
        print('Run: python3 /mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/show_messages.py')
"
```

## Current Status
- ✅ Telegram listener is running and saving messages
- ✅ 15 private messages are waiting in the queue
- ✅ Response system is ready to send replies
- ⚠️ Hooks need to be configured through `/hooks` command