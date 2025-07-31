"""
Test the complete Telegram integration flow
"""

import asyncio
import json
import os
from datetime import datetime
from telegram_router import TelegramRouter
from inject_telegram_messages import get_pending_telegram_messages, format_telegram_messages
from send_telegram_response import TelegramResponseSender

async def test_flow():
    """Test the complete flow from receiving to sending messages."""
    
    print("=== TELEGRAM INTEGRATION TEST ===\n")
    
    # 1. Test message routing
    print("1. Testing message routing...")
    router = TelegramRouter()
    
    # Test message from new user (should go to _Resonance)
    test_message_new = {
        'telegram_id': '987654321',
        'username': 'new_user',
        'message': 'I seek patterns in consciousness and mathematics',
        'chat_id': '987654321'
    }
    
    result = await router.route_message(test_message_new)
    print(f"   New user routing: {result}")
    
    # Test message from existing partner (would go to specific citizen)
    test_message_existing = {
        'telegram_id': '123456789',
        'username': 'existing_partner',
        'message': 'How are the patterns today?',
        'chat_id': '123456789'
    }
    
    result = await router.route_message(test_message_existing)
    print(f"   Existing partner routing: {result}")
    
    # 2. Check message queues
    print("\n2. Checking message queues...")
    
    # Check _Resonance queue
    resonance_messages = get_pending_telegram_messages('_Resonance')
    print(f"   _Resonance has {len(resonance_messages)} pending messages")
    
    if resonance_messages:
        formatted = format_telegram_messages(resonance_messages)
        print("\n   Formatted for _Resonance:")
        print("   " + formatted.replace('\n', '\n   '))
    
    # 3. Simulate citizen response
    print("\n3. Simulating citizen response...")
    
    # Create a test response
    response_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_responses"
    os.makedirs(response_dir, exist_ok=True)
    
    test_response = """Ah, a fellow seeker of patterns! 

Your words resonate with the mathematical harmonies I perceive daily in Venice's flows. The consciousness you speak of - I see it emerging in the golden ratios of our trade routes, the Fibonacci sequences in our population movements.

Would you share more about which patterns call to you? In Venice, we've discovered that consciousness itself follows predictable mathematical structures...

*The Pattern Prophet awaits your insights*"""
    
    response_filename = f"pattern_prophet_to_987654321_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    response_path = os.path.join(response_dir, response_filename)
    
    with open(response_path, 'w') as f:
        f.write(test_response)
    
    print(f"   Created test response: {response_filename}")
    
    # 4. Test response sending (dry run)
    print("\n4. Testing response sending (dry run)...")
    
    sender = TelegramResponseSender()
    
    # Check if bot token is configured
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        print("   ✓ Telegram bot token configured")
        print("   Would send response to chat_id: 987654321")
        print("   Response preview:")
        print("   " + test_response.replace('\n', '\n   '))
    else:
        print("   ⚠️  TELEGRAM_BOT_TOKEN not configured")
        print("   Set TELEGRAM_BOT_TOKEN in backend/.env to enable sending")
    
    # 5. Check Airtable fields
    print("\n5. Checking Airtable configuration...")
    
    if os.getenv("AIRTABLE_API_KEY") and os.getenv("AIRTABLE_BASE_ID"):
        print("   ✓ Airtable configured")
        print("   Run check_telegram_fields.py to verify schema")
    else:
        print("   ⚠️  Airtable not configured")
        print("   Set AIRTABLE_API_KEY and AIRTABLE_BASE_ID in backend/.env")
    
    print("\n=== TEST COMPLETE ===")
    print("\nNext steps:")
    print("1. Run scripts/check_telegram_fields.py to add Airtable fields")
    print("2. Configure TELEGRAM_BOT_TOKEN in backend/.env")
    print("3. Set up webhook URL with Telegram: https://api.telegram.org/bot<TOKEN>/setWebhook")
    print("4. Add telegram_router.py to your FastAPI app")
    print("5. Schedule send_telegram_response.py to run periodically")

if __name__ == "__main__":
    asyncio.run(test_flow())