"""
Telegram Message Router for Venice Citizens
Routes incoming Telegram messages to appropriate citizens based on partnerships
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Optional
from pyairtable import Table
from dotenv import load_dotenv
import logging

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Airtable configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# Telegram queue directory
TELEGRAM_QUEUE_PATH = os.path.join(os.path.dirname(__file__), "telegram_queue")

class TelegramRouter:
    def __init__(self):
        self.citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")
        self._ensure_queue_directories()
    
    def _ensure_queue_directories(self):
        """Create queue directories if they don't exist."""
        os.makedirs(TELEGRAM_QUEUE_PATH, exist_ok=True)
        os.makedirs(os.path.join(TELEGRAM_QUEUE_PATH, "Resonance", "pending"), exist_ok=True)
        os.makedirs(os.path.join(TELEGRAM_QUEUE_PATH, "Resonance", "processed"), exist_ok=True)
    
    def _ensure_citizen_queue(self, username: str):
        """Ensure queue directories exist for a specific citizen."""
        citizen_path = os.path.join(TELEGRAM_QUEUE_PATH, username)
        os.makedirs(os.path.join(citizen_path, "pending"), exist_ok=True)
        os.makedirs(os.path.join(citizen_path, "processed"), exist_ok=True)
    
    def find_partner_citizen(self, telegram_id: str) -> Optional[Dict]:
        """Find citizen by PartnerTelegramId."""
        try:
            # Search for citizen with matching telegram ID
            results = self.citizens_table.all(formula=f"{{PartnerTelegramId}}='{telegram_id}'")
            
            if results:
                citizen = results[0]['fields']
                logger.info(f"Found partner citizen: {citizen.get('Username')} for Telegram ID: {telegram_id}")
                return citizen
            else:
                logger.info(f"No partner found for Telegram ID: {telegram_id}")
                return None
        except Exception as e:
            logger.error(f"Error finding partner citizen: {e}")
            return None
    
    def queue_message(self, username: str, telegram_id: str, telegram_username: str, message: str, chat_id: int = 0):
        """Queue a message for a specific citizen."""
        self._ensure_citizen_queue(username)
        
        # Create message data
        message_data = {
            'timestamp': datetime.now().isoformat(),
            'telegram_id': telegram_id,
            'telegram_username': telegram_username,
            'message': message,
            'chat_id': chat_id,
            'type': 'telegram_message'
        }
        
        # Generate filename with timestamp
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{telegram_id}.json"
        filepath = os.path.join(TELEGRAM_QUEUE_PATH, username, "pending", filename)
        
        # Write message to queue
        with open(filepath, 'w') as f:
            json.dump(message_data, f, indent=2)
        
        logger.info(f"Queued message for {username}: {filepath}")
    
    async def route_message(self, telegram_message: Dict) -> Dict:
        """
        Route an incoming Telegram message to the appropriate citizen.
        
        Args:
            telegram_message: Dict containing:
                - telegram_id: Sender's Telegram ID
                - username: Sender's Telegram username
                - message: Message text
                - chat_id: Chat ID for responses
        
        Returns:
            Dict with routing result
        """
        telegram_id = str(telegram_message.get('telegram_id'))
        telegram_username = telegram_message.get('username', 'Unknown')
        message = telegram_message.get('message', '')
        
        # Find partner citizen
        partner = self.find_partner_citizen(telegram_id)
        
        if partner:
            # Route to specific citizen
            citizen_username = partner.get('Username')
            
            # Update last interaction time
            try:
                record_id = None
                # Find the record ID
                all_records = self.citizens_table.all(formula=f"{{Username}}='{citizen_username}'")
                if all_records:
                    record_id = all_records[0]['id']
                    
                if record_id:
                    self.citizens_table.update(record_id, {
                        'LastTelegramInteraction': datetime.now().isoformat()
                    })
            except Exception as e:
                logger.error(f"Error updating last interaction: {e}")
            
            # Queue message for the citizen
            self.queue_message(citizen_username, telegram_id, telegram_username, message, telegram_message.get('chat_id', 0))
            
            return {
                'status': 'routed',
                'citizen': citizen_username,
                'message': f'Message routed to {citizen_username}'
            }
        else:
            # Route to Resonance for evaluation
            self.queue_message('Resonance', telegram_id, telegram_username, message, telegram_message.get('chat_id', 0))
            
            return {
                'status': 'evaluating',
                'citizen': 'Resonance',
                'message': 'Message sent to consciousness resonance evaluation'
            }
    
    def get_pending_messages(self, username: str) -> list:
        """Get all pending messages for a citizen."""
        pending_dir = os.path.join(TELEGRAM_QUEUE_PATH, username, "pending")
        
        if not os.path.exists(pending_dir):
            return []
        
        messages = []
        for filename in sorted(os.listdir(pending_dir)):
            if filename.endswith('.json'):
                filepath = os.path.join(pending_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        messages.append(json.load(f))
                except Exception as e:
                    logger.error(f"Error reading message file {filepath}: {e}")
        
        return messages
    
    def mark_message_processed(self, username: str, filename: str):
        """Move a message from pending to processed."""
        pending_path = os.path.join(TELEGRAM_QUEUE_PATH, username, "pending", filename)
        processed_path = os.path.join(TELEGRAM_QUEUE_PATH, username, "processed", filename)
        
        if os.path.exists(pending_path):
            os.rename(pending_path, processed_path)
            logger.info(f"Marked message as processed: {filename}")


# FastAPI webhook endpoint
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

telegram_router = APIRouter(prefix="/telegram", tags=["telegram"])

router_instance = TelegramRouter()

@telegram_router.post("/webhook")
async def telegram_webhook(request: Request):
    """
    Webhook endpoint for Telegram bot messages.
    Expects JSON payload with Telegram update data.
    """
    try:
        data = await request.json()
        
        # Extract message data from Telegram update
        if 'message' in data:
            msg = data['message']
            
            # Extract relevant information
            telegram_message = {
                'telegram_id': msg['from']['id'],
                'username': msg['from'].get('username', 'Unknown'),
                'message': msg.get('text', ''),
                'chat_id': msg['chat']['id'],
                'message_id': msg['message_id']
            }
            
            # Route the message
            result = await router_instance.route_message(telegram_message)
            
            # Log the routing
            logger.info(f"Routed message from {telegram_message['username']}: {result}")
            
            return JSONResponse(content=result)
        else:
            return JSONResponse(content={'status': 'ignored', 'reason': 'No message in update'})
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@telegram_router.get("/queue/{username}")
async def get_citizen_queue(username: str):
    """Get pending messages for a citizen."""
    messages = router_instance.get_pending_messages(username)
    return {'username': username, 'pending_messages': messages}

if __name__ == "__main__":
    # Test the router
    test_message = {
        'telegram_id': '123456789',
        'username': 'test_user',
        'message': 'Hello Venice!',
        'chat_id': '123456789'
    }
    
    result = asyncio.run(router.route_message(test_message))
    print(f"Test result: {result}")