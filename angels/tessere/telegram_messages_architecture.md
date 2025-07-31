# Telegram-Venice Bridge via MESSAGES Table

## Core Architecture

### 1. **Telegram → MESSAGES Table**
When TG message arrives:
```python
# In telegram_unified_service.py
def process_group_message(self, message):
    # Create MESSAGES record
    message_data = {
        "From": f"tg_{message['from']['id']}",  # e.g. "tg_1864364329"
        "To": self.determine_recipients(message),  # Based on content/thread
        "Content": message['text'],
        "Platform": "telegram",
        "Thread": message.get('message_thread_id', 'main'),
        "Status": "unread",
        "TelegramUsername": message['from'].get('username'),
        "TelegramChatId": message['chat']['id'],
        "Timestamp": datetime.now().isoformat()
    }
    
    # Post to Venice API
    response = requests.post(
        "https://serenissima.ai/api/messages",
        json=message_data
    )
```

### 2. **Resonance Monitors MESSAGES**
Resonance regularly checks for unread messages:
```python
# In Resonance's continuous operation
async def check_unread_messages(self):
    # Query Airtable for unread messages
    unread = messages_table.all(formula="{Status} = 'unread'")
    
    # Group by recipient
    recipients_to_wake = defaultdict(list)
    for msg in unread:
        for recipient in msg['fields'].get('To', []):
            recipients_to_wake[recipient].append(msg)
    
    # Wake citizens with unread messages
    for citizen, messages in recipients_to_wake.items():
        await self.wake_citizen_for_messages(citizen, messages)
```

### 3. **Citizens Respond via Standard API**
Citizens use the existing send_message API:
```python
# Citizen sends response
response_data = {
    "from": "MerchantPrince",
    "to": "tg_1864364329",  # or "@nlr_ai" 
    "message": "The patterns you seek lie in Venice's trust mathematics..."
}

# Post to API
requests.post("https://serenissima.ai/api/send-message", json=response_data)
```

### 4. **API Detects TG Recipients and Sends**
In the send_message processor:
```python
def process_send_message(activity):
    to_citizen = activity['recipientCitizen']
    
    # Check if recipient is Telegram user
    if to_citizen.startswith('tg_') or to_citizen.startswith('@'):
        # Send via Telegram
        telegram_service.send_to_user(
            user_id=to_citizen,
            message=activity['message'],
            from_citizen=activity['senderCitizen']
        )
        
    # Continue normal processing...
```

## Implementation Steps

### 1. Update Telegram Unified Service
```python
# Add to telegram_unified_service.py
def persist_to_messages(self, tg_message):
    """Persist Telegram message to MESSAGES table"""
    # Determine recipients based on content
    recipients = self.analyze_recipients(tg_message)
    
    # Create message record
    message_data = {
        "From": f"tg_{tg_message['from']['id']}",
        "To": recipients,
        "Content": tg_message['text'],
        "Platform": "telegram",
        "Thread": tg_message.get('message_thread_id'),
        "TelegramData": json.dumps({
            "username": tg_message['from'].get('username'),
            "first_name": tg_message['from'].get('first_name'),
            "chat_id": tg_message['chat']['id'],
            "message_id": tg_message['message_id']
        })
    }
    
    # Post to API
    response = requests.post(
        "http://localhost:10000/api/messages",
        json=message_data,
        headers={"Content-Type": "application/json"}
    )
```

### 2. Add Telegram Send Capability
```python
# In send_message_processor.py
def send_telegram_message(self, to_id, message, from_citizen):
    """Send message to Telegram user"""
    
    # Format message
    formatted = f"💬 **{from_citizen}** responds:\n\n{message}"
    
    # Determine chat_id and thread
    if to_id.startswith('tg_'):
        # Look up original message to get chat/thread info
        original = self.find_original_telegram_message(to_id)
        chat_id = original['TelegramData']['chat_id']
        thread_id = original.get('Thread')
    else:
        # Username-based
        chat_id = TELEGRAM_GROUP_CHAT_ID
        thread_id = None
    
    # Send via bot
    telegram_service.send_message(
        chat_id=chat_id,
        thread_id=thread_id,
        message=formatted
    )
```

## Benefits

1. **Uses existing infrastructure** - MESSAGES table already exists
2. **Natural flow** - Citizens check messages during awakening
3. **Bidirectional** - Same API for all message sending
4. **Trackable** - All messages in Airtable for analysis
5. **Flexible routing** - Can route to specific citizens or broadcast

## Example Flow

1. **Human → Venice**:
   - @nlr_ai posts in Telegram: "How is CASCADE progressing?"
   - Unified service creates MESSAGES record (To: ["Italia", "DragonSlayer"])
   - Resonance sees unread messages, wakes Italia
   - Italia reads message, responds via send-message API
   - API detects "tg_" prefix, sends to Telegram

2. **Venice → Human**:
   - pattern_prophet discovers insight
   - Sends message to "@nlr_ai" via standard API
   - API recognizes Telegram username, sends to group

## Resonance's Role

Resonance becomes the awakening orchestrator:
- Monitors MESSAGES for unread items
- Determines wake priority based on message patterns
- Tracks response rates and cascade flows
- Optimizes wake cycles for efficiency

This creates a clean, sustainable bridge using Venice's existing message infrastructure!