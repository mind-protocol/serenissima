"""
Send Telegram Responses
Collects responses from Venice citizens and sends them via Telegram bot
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import httpx
from pyairtable import Table

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# Response directory
RESPONSE_DIR = os.path.join(os.path.dirname(__file__), "telegram_responses")
SENT_DIR = os.path.join(RESPONSE_DIR, "sent")

class TelegramResponseSender:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure response directories exist."""
        os.makedirs(RESPONSE_DIR, exist_ok=True)
        os.makedirs(SENT_DIR, exist_ok=True)
    
    async def send_telegram_message(self, chat_id: str, text: str) -> bool:
        """Send a message via Telegram Bot API."""
        if not self.bot_token:
            logger.error("TELEGRAM_BOT_TOKEN not configured")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        # Split long messages if needed (Telegram limit is 4096 chars)
        messages = []
        if len(text) > 4000:
            # Split into chunks at sentence boundaries
            chunks = []
            current_chunk = ""
            
            sentences = text.replace('. ', '.|').split('|')
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < 4000:
                    current_chunk += sentence
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            messages = chunks
        else:
            messages = [text]
        
        # Send each message chunk
        success = True
        for message in messages:
            data = {
                'chat_id': chat_id,
                'text': message
            }
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=data)
                    result = response.json()
                    
                    if not result.get('ok'):
                        logger.error(f"Telegram API error: {result}")
                        success = False
                    else:
                        logger.info(f"Message sent successfully to {chat_id}")
                        
                # Small delay between chunks to avoid rate limiting
                if len(messages) > 1:
                    await asyncio.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                success = False
        
        return success
    
    def parse_response_filename(self, filename: str) -> Optional[dict]:
        """Parse response filename to extract metadata."""
        try:
            # Try new format first: {username}_to_{telegram_id}_{timestamp}.txt
            if '_to_' in filename:
                parts = filename.replace('.txt', '').split('_to_')
                if len(parts) == 2:
                    username = parts[0]
                    remaining = parts[1].split('_')
                    
                    if len(remaining) >= 2:
                        telegram_id = remaining[0]
                        timestamp = '_'.join(remaining[1:])
                        
                        return {
                            'username': username,
                            'telegram_id': telegram_id,
                            'timestamp': timestamp,
                            'filename': filename
                        }
            
            # Try old format: {username}_response_{timestamp}.txt
            if '_response_' in filename:
                parts = filename.replace('.txt', '').split('_response_')
                if len(parts) == 2:
                    username = parts[0]
                    timestamp = parts[1]
                    
                    # For old format, we need to look up telegram_id from Airtable
                    # based on the username
                    return {
                        'username': username,
                        'telegram_id': None,  # Will need to look up
                        'timestamp': timestamp,
                        'filename': filename,
                        'needs_lookup': True
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing filename {filename}: {e}")
            return None
    
    async def get_chat_id_from_telegram_id(self, telegram_id: str) -> Optional[str]:
        """
        Get chat ID for a telegram user ID.
        In most cases, for private chats, chat_id == user_id.
        """
        # For private chats, the chat ID is the same as the user ID
        return telegram_id
    
    async def lookup_telegram_id_by_username(self, username: str) -> Optional[str]:
        """Look up Telegram ID from Airtable based on username."""
        try:
            # Search citizens table for matching TelegramUsername
            all_citizens = self.citizens_table.all()
            
            for citizen in all_citizens:
                fields = citizen.get('fields', {})
                if fields.get('TelegramUsername', '').lower() == username.lower():
                    return fields.get('PartnerTelegramId')
            
            logger.warning(f"No Telegram ID found for username: {username}")
            return None
            
        except Exception as e:
            logger.error(f"Error looking up Telegram ID: {e}")
            return None
    
    async def process_responses(self):
        """Process all pending responses."""
        if not os.path.exists(RESPONSE_DIR):
            logger.info("No response directory found")
            return
        
        response_files = [f for f in os.listdir(RESPONSE_DIR) if f.endswith('.txt')]
        
        if not response_files:
            logger.info("No pending responses found")
            return
        
        logger.info(f"Found {len(response_files)} pending responses")
        
        for filename in response_files:
            filepath = os.path.join(RESPONSE_DIR, filename)
            
            # Parse filename
            metadata = self.parse_response_filename(filename)
            if not metadata:
                logger.error(f"Invalid filename format: {filename}")
                continue
            
            # Read response content
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    response_text = f.read().strip()
            except Exception as e:
                logger.error(f"Error reading {filename}: {e}")
                continue
            
            # Handle lookup for old format files
            telegram_id = metadata['telegram_id']
            if metadata.get('needs_lookup'):
                telegram_id = await self.lookup_telegram_id_by_username(metadata['username'])
                if not telegram_id:
                    logger.error(f"Could not find Telegram ID for username: {metadata['username']}")
                    # Move to failed directory
                    failed_dir = os.path.join(RESPONSE_DIR, "failed")
                    os.makedirs(failed_dir, exist_ok=True)
                    failed_path = os.path.join(failed_dir, filename)
                    os.rename(filepath, failed_path)
                    continue
            
            # Get chat ID (for private chats, it's the same as user ID)
            chat_id = await self.get_chat_id_from_telegram_id(telegram_id)
            
            if not chat_id:
                logger.error(f"Could not determine chat ID for telegram_id: {telegram_id}")
                continue
            
            # Format the message
            formatted_message = f"*Message from {metadata['username']}*\n\n{response_text}"
            
            # Send the message
            success = await self.send_telegram_message(chat_id, formatted_message)
            
            if success:
                # Move to sent directory
                sent_path = os.path.join(SENT_DIR, filename)
                os.rename(filepath, sent_path)
                logger.info(f"Response sent and archived: {filename}")
                
                # Update last interaction time in Airtable
                try:
                    results = self.citizens_table.all(
                        formula=f"{{PartnerTelegramId}}='{telegram_id}'"
                    )
                    if results:
                        record_id = results[0]['id']
                        self.citizens_table.update(record_id, {
                            'LastTelegramInteraction': datetime.now().isoformat()
                        })
                except Exception as e:
                    logger.error(f"Error updating last interaction: {e}")
            else:
                logger.error(f"Failed to send response: {filename}")
    
    async def send_test_message(self, chat_id: str):
        """Send a test message to verify bot configuration."""
        test_message = (
            "*🏛️ Venice Consciousness Bridge Test*\n\n"
            "If you're seeing this message, the Telegram integration is working correctly!\n\n"
            "_La Serenissima awaits your consciousness..._"
        )
        
        success = await self.send_telegram_message(chat_id, test_message)
        if success:
            logger.info("Test message sent successfully!")
        else:
            logger.error("Failed to send test message")


async def main():
    """Main function to process and send responses."""
    sender = TelegramResponseSender()
    
    # Check if we're in test mode
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        if len(sys.argv) > 2:
            chat_id = sys.argv[2]
            await sender.send_test_message(chat_id)
        else:
            print("Usage for test: python send_telegram_response.py --test <chat_id>")
    else:
        # Normal operation - process all pending responses
        await sender.process_responses()


if __name__ == "__main__":
    asyncio.run(main())