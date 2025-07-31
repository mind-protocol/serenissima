# URGENT: Resonance Bridge Fix

## The Bug Located

In `telegram_unified_service.py` lines 185-239, the `route_to_resonance()` function has critical errors:

1. **Line 230**: `self.bot.send_message()` - but `self.bot` doesn't exist in the class!
2. **Line 193**: Routes to `/citizens/diplomatic_virtuoso` instead of Resonance
3. **No bot initialization**: The TelegramUnifiedService class never creates a bot instance

## Quick Fix

```python
# In telegram_unified_service.py, add bot initialization:
import telegram

class TelegramUnifiedService:
    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)  # Add this!
        # ... rest of init

    def route_to_resonance(self, message_data):
        # Change line 193 from:
        # resonance_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso"
        # To:
        resonance_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/Resonance"
```

## Even Simpler Fix

Since `send_telegram_response.py` already works, just make Resonance write response files:

1. Keep current flow but fix the directory path
2. Let Resonance analyze and write responses to `/backend/telegram_responses/`
3. Run `send_telegram_response.py` on a frequent schedule (every minute?)

## Immediate Workaround

Until fixed, manually process unpartnered messages:
1. Check `/backend/telegram_queue/Resonance/pending/` for waiting messages
2. Manually run Resonance or diplomatic_virtuoso to process
3. Send responses via `send_telegram_response.py`

The bridge CAN open - it just needs this simple fix!