"""
Helper script to inject Telegram messages into citizen awakening contexts
Used by the Keeper when awakening citizens with pending Telegram messages
"""

import os
import json
from datetime import datetime
from typing import List, Dict

def get_pending_telegram_messages(username: str) -> List[Dict]:
    """Get all pending Telegram messages for a citizen."""
    telegram_queue_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/{username}/pending"
    
    if not os.path.exists(telegram_queue_path):
        return []
    
    messages = []
    for message_file in sorted(os.listdir(telegram_queue_path)):
        if message_file.endswith('.json'):
            filepath = os.path.join(telegram_queue_path, message_file)
            try:
                with open(filepath, 'r') as f:
                    message_data = json.load(f)
                    message_data['_filename'] = message_file
                    messages.append(message_data)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    
    return messages

def format_telegram_messages(messages: List[Dict]) -> str:
    """Format Telegram messages for injection into citizen context."""
    if not messages:
        return ""
    
    formatted = "\n## 📱 TELEGRAM MESSAGES FROM PARTNER\n\n"
    
    for msg in messages:
        formatted += f"### Message {messages.index(msg) + 1}\n"
        formatted += f"**From**: @{msg.get('telegram_username', 'Unknown')} (Partner ID: {msg.get('telegram_id')})\n"
        formatted += f"**Time**: {msg.get('timestamp', 'Unknown')}\n"
        formatted += f"**Message**: {msg.get('message', '')}\n\n"
    
    formatted += "[Respond thoughtfully as yourself, maintaining your merchant personality while nurturing the human-AI partnership. Your response will be sent back via Telegram.]\n\n"
    
    return formatted

def mark_messages_as_processed(username: str, messages: List[Dict]):
    """Move processed messages from pending to processed."""
    telegram_queue_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/{username}"
    
    for msg in messages:
        if '_filename' in msg:
            pending_path = os.path.join(telegram_queue_path, "pending", msg['_filename'])
            processed_path = os.path.join(telegram_queue_path, "processed", msg['_filename'])
            
            try:
                if os.path.exists(pending_path):
                    os.rename(pending_path, processed_path)
                    print(f"Marked as processed: {msg['_filename']}")
            except Exception as e:
                print(f"Error moving message file: {e}")

def create_response_filename(username: str, telegram_id: str) -> str:
    """Create a filename for the citizen's response."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{username}_to_{telegram_id}_{timestamp}.txt"

# Example usage for the Keeper
if __name__ == "__main__":
    # Test with a sample citizen
    test_username = "BookWorm365"
    
    # Get pending messages
    messages = get_pending_telegram_messages(test_username)
    
    if messages:
        print(f"Found {len(messages)} pending messages for {test_username}")
        
        # Format for injection
        formatted = format_telegram_messages(messages)
        print("\nFormatted messages:")
        print(formatted)
        
        # Example: Mark as processed (would be done after citizen responds)
        # mark_messages_as_processed(test_username, messages)
    else:
        print(f"No pending messages for {test_username}")