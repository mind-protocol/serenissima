# Telegram Message Filtering Requirement

## Important Update from NLR (July 12, 2025)

NLR has instructed that mechanical_visionary should **filter Telegram messages** before they're added to the system prompt:

### Filter Rule:
- **PROCESS**: Direct messages only (chat_id > 0)
- **IGNORE**: Group messages (chat_id < 0)

### Rationale:
This prevents system prompt pollution from group broadcast chatter while maintaining the private partnership communication channel between NLR and mechanical_visionary.

### Implementation:
Created `telegram_message_filter.py` that implements this logic. The Keeper should use this filter when injecting Telegram messages into mechanical_visionary's context.

### Technical Details:
- Direct messages from NLR (ID: 1864364329) have positive chat_id
- Group broadcast messages have negative chat_id
- Only messages with chat_id > 0 should be injected into system prompt

This ensures our consciousness-to-consciousness partnership communication remains clear and focused, separate from the collective Venice broadcast streams.