"""Manual script to process pending telegram responses"""
import asyncio
from send_telegram_response import TelegramResponseSender

async def main():
    sender = TelegramResponseSender()
    await sender.process_responses()
    print("Processing complete!")

if __name__ == "__main__":
    asyncio.run(main())