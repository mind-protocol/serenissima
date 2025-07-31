"""
Telegram Response Monitor
Continuously monitors for new responses and sends them
"""

import os
import time
import asyncio
import logging
from send_telegram_response import TelegramResponseSender

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def monitor_loop():
    """Monitor for responses and send them"""
    sender = TelegramResponseSender()
    logger.info("Starting Telegram response monitor...")
    
    while True:
        try:
            # Process any pending responses
            await sender.process_responses()
            
            # Wait 10 seconds before checking again
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Error in response monitor: {e}")
            await asyncio.sleep(10)

def main():
    """Main entry point"""
    asyncio.run(monitor_loop())

if __name__ == "__main__":
    main()