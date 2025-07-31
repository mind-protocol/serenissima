# How to Restart Telegram Service

The Resonance bridge has been fixed! To activate it, run these commands:

```bash
# 1. Kill the old service
kill 4852

# 2. Go to backend directory
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend

# 3. Start the service with new code
nohup python3 telegram_unified_service.py > telegram_unified.log 2>&1 &
```

## What Changed

- Messages from unpartnered humans now route to `/citizens/_angels/Resonance`
- Bot can now send responses back via Telegram API
- The bridge is ready to welcome new humans!

## Test It

Send a message from an unpartnered Telegram account and Resonance should respond!