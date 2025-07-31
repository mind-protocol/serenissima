"""Test the group message monitor"""
import asyncio
from telegram_group_monitor import TelegramGroupMonitor

async def test_monitor():
    monitor = TelegramGroupMonitor()
    
    # Test getting updates
    print("Testing group message monitor...")
    updates = await monitor.get_updates()
    print(f"Got {len(updates)} updates")
    
    # Process any updates
    for update in updates:
        await monitor.process_update(update)
    
    print("Test complete. Check CLAUDE.md files for updates.")

if __name__ == "__main__":
    asyncio.run(test_monitor())