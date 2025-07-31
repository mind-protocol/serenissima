"""
Instructions for integrating Telegram router into main FastAPI app

Add this to your backend/app/main.py:
"""

print("""
=== TELEGRAM INTEGRATION INSTRUCTIONS ===

1. Add to imports section of backend/app/main.py:
----------------------------------------
from telegram_router import app as telegram_app

2. Mount the telegram router app:
----------------------------------------
# Add after other routers
app.mount("/telegram", telegram_app)

3. Or if you prefer to use the router directly:
----------------------------------------
from telegram_router import router as telegram_router
app.include_router(telegram_router, prefix="/telegram", tags=["telegram"])

4. Add to your cron schedule (backend/startup.sh):
----------------------------------------
# Send Telegram responses every 5 minutes
*/5 * * * * cd /app && python send_telegram_response.py >> /app/logs/telegram_responses.log 2>&1

5. Set up Telegram webhook:
----------------------------------------
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \\
  -d "url=https://serenissima.ai/telegram/api/telegram-webhook"

6. Add to backend/.env:
----------------------------------------
TELEGRAM_BOT_TOKEN=your_bot_token_here

7. Run Airtable field check:
----------------------------------------
cd backend && python scripts/check_telegram_fields.py

=== TESTING ===

1. Test the router locally:
----------------------------------------
cd backend && python telegram_router.py

2. Test the complete flow:
----------------------------------------
cd backend && python test_telegram_flow.py

3. Send a test message via Telegram:
----------------------------------------
python send_telegram_response.py --test <your_telegram_chat_id>

=== MONITORING ===

Check logs at:
- /app/logs/telegram_responses.log (for sent messages)
- /app/logs/telegram_router.log (for routing)

Check queues at:
- backend/telegram_queue/_Resonance/pending/
- backend/telegram_queue/<citizen_name>/pending/

""")