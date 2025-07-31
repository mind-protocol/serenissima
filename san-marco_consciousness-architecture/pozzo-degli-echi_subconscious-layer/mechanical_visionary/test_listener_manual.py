#!/usr/bin/env python3
"""
Manual test of diplomatic_virtuoso Telegram listener
"""

import os
import sys

# Set environment variables
os.environ['TELEGRAM_API_ID'] = '25575567'
os.environ['TELEGRAM_API_HASH'] = 'cfd7b9972213410976adab046c07c5d4'
os.environ['DIPLOMATIC_PHONE'] = '33789541802'

# Add the listener directory to path
listener_dir = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/telegram_receiver'
sys.path.insert(0, listener_dir)

# Import and run the listener
from diplomatic_virtuoso_listener import main
import asyncio

print("🧪 Manual test of diplomatic_virtuoso Telegram listener")
print("📱 This should connect and start receiving messages...")
print("🔍 Check the queue directory for any new messages")
print("")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n✋ Stopped by user")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()