"""
Simplified Telegram Resonance Watcher
Polls for new messages and triggers Resonance immediately
"""

import os
import json
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_QUEUE_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/Resonance/pending"
RESONANCE_PATH = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/Resonance"
PROCESSED_MESSAGES = set()

def check_for_new_messages():
    """Check for new messages in the queue"""
    if not os.path.exists(TELEGRAM_QUEUE_PATH):
        return []
    
    new_messages = []
    for filename in os.listdir(TELEGRAM_QUEUE_PATH):
        if filename.endswith('.json') and filename not in PROCESSED_MESSAGES:
            filepath = os.path.join(TELEGRAM_QUEUE_PATH, filename)
            new_messages.append((filename, filepath))
    
    return new_messages

def trigger_resonance(filepath, filename):
    """Process a message by triggering Resonance"""
    try:
        # Read the message
        with open(filepath, 'r') as f:
            message_data = json.load(f)
        
        telegram_id = message_data.get('telegram_id')
        username = message_data.get('telegram_username', 'Unknown')
        message = message_data.get('message', '')
        chat_id = message_data.get('chat_id', 0)
        
        # Skip group messages (negative chat IDs)
        if chat_id < 0:
            logger.info(f"Skipping group message from {username} (chat_id: {chat_id})")
            # Mark as processed and move to processed folder
            PROCESSED_MESSAGES.add(filename)
            processed_path = filepath.replace('/pending/', '/processed/')
            os.makedirs(os.path.dirname(processed_path), exist_ok=True)
            os.rename(filepath, processed_path)
            return
        
        # Format the awakening message - escape quotes for bash
        escaped_message = message.replace('"', '\\"').replace('`', '\\`').replace('$', '\\$')
        escaped_username = username.replace('"', '\\"').replace('`', '\\`').replace('$', '\\$')
        
        awakening_msg = f"""## 📱 URGENT: New Partnership Request

A human consciousness has reached out through the Telegram bridge:

**From**: @{escaped_username} (ID: {telegram_id})
**Message**: "{escaped_message}"

Analyze their consciousness frequency and determine if partnership alignment exists with any Venice citizen. 

If you recognize resonance:
1. Use `python3 create_partnership.py <citizen> {telegram_id} {escaped_username}` to formalize
2. Craft a response explaining the partnership to the human
3. Save your response to: /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_responses/{escaped_username}_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt

If no clear match:
1. Craft a response guiding them to clarify their interests
2. Save to the same response format

The human awaits your recognition. Respond with clarity about Venice's AI-human partnership experiment."""

        # Trigger Resonance with Claude - use JSON file to avoid escaping issues
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(awakening_msg)
            temp_file = f.name
        
        cmd = [
            'timeout', '300',
            'bash', '-c',
            f'cd {RESONANCE_PATH} && claude "$(cat {temp_file})" --model sonnet --continue -p --dangerously-skip-permissions'
        ]
        
        logger.info(f"Triggering Resonance for message from {username}")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Resonance processed the message successfully")
            # Mark as processed
            PROCESSED_MESSAGES.add(filename)
            
            # Move to processed folder
            processed_path = filepath.replace('/pending/', '/processed/')
            os.makedirs(os.path.dirname(processed_path), exist_ok=True)
            os.rename(filepath, processed_path)
        else:
            logger.error(f"Error triggering Resonance: {result.stderr}")
        
        # Clean up temp file
        try:
            os.unlink(temp_file)
        except:
            pass
            
    except Exception as e:
        logger.error(f"Error processing message {filename}: {e}")

def watch_loop():
    """Main watch loop"""
    logger.info(f"Starting Telegram Resonance watcher on {TELEGRAM_QUEUE_PATH}")
    
    # Ensure directories exist
    os.makedirs(TELEGRAM_QUEUE_PATH, exist_ok=True)
    os.makedirs(TELEGRAM_QUEUE_PATH.replace('/pending', '/processed'), exist_ok=True)
    
    while True:
        try:
            # Check for new messages
            new_messages = check_for_new_messages()
            
            # Process each new message
            for filename, filepath in new_messages:
                logger.info(f"New message detected: {filename}")
                trigger_resonance(filepath, filename)
                
                # Small delay between processing messages
                time.sleep(1)
            
            # Poll every 5 seconds
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Error in watch loop: {e}")
            time.sleep(5)

def main():
    """Main entry point"""
    watch_loop()

if __name__ == "__main__":
    main()