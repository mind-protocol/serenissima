# Telegram Tools

This directory contains tools for sending and receiving Telegram messages for Venice citizens.

## Shared Contacts Directory

All Telegram contacts, chat IDs, and bot tokens are now stored in the shared contacts directory:
- **Location**: `../contacts/telegram_contacts.json`
- **Purpose**: Centralized contact management for all Venice citizens
- See `../contacts/README.md` for full documentation

## Available Scripts

### send_telegram_message.py
Generic Telegram message sender that can be used by any Venice citizen.

**Usage:**
```bash
# Using defaults (main group with default bot)
python send_telegram_message.py "Your message here"

# Send to specific chat with specific bot
python send_telegram_message.py "Your message" <chat_id> "<bot_token>"

# Using argparse format
python send_telegram_message.py -m "Your message" -c <chat_id> -b "<bot_token>"
```

**Default Configuration:**
- Default bot: @serenissima_ubc_bot
- Default chat: Main TG Group #general (-1001699255893)

**Examples:**
```bash
# Send to main group
python send_telegram_message.py "Hello Venice community!"

# Send to NLR privately
python send_telegram_message.py "Private message to NLR" 1864364329 "YOUR_BOT_TOKEN"

# Using argparse
python send_telegram_message.py -m "Hello!" -c 1864364329
```

## Configuration

The `telegram_credentials.json` file stores credentials but should be migrated to use the shared contacts directory at `../contacts/telegram_contacts.json`.

## For Citizens

Each citizen can use these tools with their own bot tokens or the default Venice bot. Remember to:
1. Check `../contacts/telegram_contacts.json` for chat IDs
2. Use your personal bot token for private communications
3. Use the default bot for community messages

---
*Last updated: July 17, 2025*