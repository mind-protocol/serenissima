# Backend Restart to Activate Resonance Fix

The telegram_unified_service.py has been fixed to route unpartnered messages to `/citizens/_angels/Resonance`.

Since main.py automatically starts telegram_unified_service, just restart the backend:

```bash
# Navigate to backend
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend

# Kill any existing processes
pkill -f "telegram_unified_service.py"
pkill -f "uvicorn app.main"

# Start the backend (which will auto-start telegram service)
python3 run.py
```

## What Will Happen

1. Backend starts up
2. main.py automatically launches telegram_unified_service.py (line 229)
3. Telegram service now uses corrected path: `/citizens/_angels/Resonance`
4. Unpartnered humans receive responses!

## To Verify

- Check logs: `tail -f telegram_unified.log`
- Send test message from unpartnered Telegram account
- Watch for "Routed partnership message to Resonance" in logs