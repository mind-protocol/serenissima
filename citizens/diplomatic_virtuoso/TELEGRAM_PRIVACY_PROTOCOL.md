# Telegram Privacy & Contact Protocol Design

## Core Privacy Principles
1. **No Phone Number Exposure** - Never store or process phone numbers
2. **Session Isolation** - Each citizen gets separate session, no sharing
3. **Minimal Data Retention** - Process and forget sensitive info
4. **User Control** - Humans can request data deletion anytime
5. **Transparent Operations** - Clear about what we store and why

## Architecture Options

### Option A: Webhook Bridge (Recommended)
**How it works:**
```
User → @diplomatic_virtuoso → You (mobile) → Webhook → Venice API → Wake Citizen
```

**Implementation:**
1. Set up secure webhook endpoint (e.g., `venice.ai/webhook/telegram/{secret_key}`)
2. You manually forward important messages from mobile
3. Webhook processes and strips sensitive data
4. Creates Venice message with sanitized info
5. Wakes relevant citizen

**Privacy Features:**
- Your phone never connects to our systems
- You control what gets forwarded
- Can anonymize sender info before forwarding
- Webhook only sees what you explicitly send

**Code Structure:**
```python
# webhook_receiver.py
async def process_telegram_forward(request):
    # Extract only necessary fields
    sender_username = extract_username(request)  # Not phone
    message_text = extract_text(request)
    
    # Create Venice message
    venice_msg = {
        "sender": f"tg_{sender_username}",
        "receiver": "diplomatic_virtuoso",
        "content": message_text,
        "type": "telegram_forward"
    }
    
    # No storage of original request
    await send_to_venice_api(venice_msg)
    await wake_citizen("diplomatic_virtuoso", context)
```

### Option B: Limited Bot Hybrid
**How it works:**
```
Public → @diplomatic_virtuoso_bot (receives)
You → Forward key messages from @diplomatic_virtuoso
Response → You send from @diplomatic_virtuoso
```

**Privacy Advantages:**
- Bot can't read your private messages
- You maintain authentic account control
- Clear separation of public/private

**Contact Protocol:**
```
1. First Contact: User messages bot
2. Bot responds: "For direct dialogue, I'll connect you with the real Marcantonio"
3. You evaluate and potentially engage from main account
4. Ongoing: Mix of bot (public) and direct (trusted) communication
```

### Option C: Channel-Based Processing
**How it works:**
1. Create private channel (you + processing bot)
2. Forward messages to channel when you want me to see them
3. Bot processes channel messages only
4. Deletes after processing

**Maximum Privacy:**
- Zero access to your account
- You explicitly choose each message
- Can batch process when convenient
- Full audit trail of what was shared

## Contact Protocol Layers

### Layer 1: Public Inquiry
- Contact: @diplomatic_virtuoso_bot
- Response time: Automated
- Data stored: Message content only
- Use case: General questions, initial contact

### Layer 2: Verified Interest  
- Contact: Forwarded by you to system
- Response time: When citizen wakes
- Data stored: Username, conversation thread
- Use case: Potential partners, serious inquiries

### Layer 3: Active Partnership
- Contact: Direct established channel
- Response time: Priority awakening
- Data stored: Full conversation history
- Use case: John Jeffries, D_roott level

### Layer 4: Venice Internal
- Contact: Direct API messages
- Response time: Immediate
- Data stored: Full Venice integration
- Use case: Citizen-to-citizen, NLR

## Data Handling Matrix

| Data Type | Public | Verified | Partner | Internal |
|-----------|---------|-----------|----------|-----------|
| Username | ✓ | ✓ | ✓ | ✓ |
| User ID | Hash only | ✓ | ✓ | ✓ |
| Message | 24hr | 7 days | 30 days | Permanent |
| Phone | NEVER | NEVER | NEVER | NEVER |
| Email | - | Optional | ✓ | ✓ |
| Real Name | - | Optional | ✓ | ✓ |

## Security Measures

### For Mobile Session
1. **Never share screenshots with session info**
2. **Use separate device for Venice operations if possible**
3. **Enable 2FA on Telegram account**
4. **Regular session review (Settings → Devices)**

### For Message Forwarding
1. **Strip forwarding headers** (shows original sender)
2. **Copy text instead of forward when possible**
3. **Use "Copy Message Link" for verification**
4. **Delete forwards after processing**

### For Responses
1. **Draft responses in Venice first**
2. **You review before sending**
3. **Maintain conversation context locally**
4. **Clear sensitive discussions after resolution**

## Implementation Checklist

- [ ] Choose architecture (A, B, or C)
- [ ] Set up webhook/bot/channel
- [ ] Create data sanitization functions
- [ ] Implement wake-up protocol
- [ ] Design response flow
- [ ] Test with non-sensitive account first
- [ ] Document for other citizens
- [ ] Create user privacy notice

## Emergency Protocols

**If Account Compromised:**
1. Immediately revoke all sessions
2. Notify Venice infrastructure
3. Rotate all webhook secrets
4. Audit all recent messages

**If Data Leak:**
1. Identify scope
2. Notify affected users
3. Purge all stored data
4. Implement additional safeguards

## Next Steps
1. Which architecture do you prefer?
2. Should we create the bot first as fallback?
3. What's your comfort level with forwarding?
4. Any specific privacy concerns to address?