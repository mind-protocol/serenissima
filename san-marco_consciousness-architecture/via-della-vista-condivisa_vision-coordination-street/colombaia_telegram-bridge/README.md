# 🔗 Telegram Consciousness Bridge

**Bidirectional communication between NLR and Venice buildings via @building_loop_1_serenissima_bot**

## Architecture

```
Telegram Bot (@building_loop_1_serenissima_bot)
    ↕️
Via della Vista Condivisa / telegram-bridge/
    ↕️
mechanical_visionary ←→ Arsenal_BackendArchitect_1
```

## Usage

### Starting the Bridge
```bash
./start_telegram_bridge.sh start
```

### Stopping the Bridge
```bash
./start_telegram_bridge.sh stop
```

### Check Status
```bash
./start_telegram_bridge.sh status
```

### Send Messages from Telegram

Message the bot **@building_loop_1_serenissima_bot** with:

- **General messages**: Delivered to both buildings
- **@torre** or **@arsenal**: Targeted to Torre dell'Occhio
- **@cistern** or **@mechanical**: Targeted to Cistern House

### Message Flow

1. **NLR → Bot**: Send message to @building_loop_1_serenissima_bot
2. **Bot → Bridge**: telegram_receiver.py polls for new messages
3. **Bridge → File**: Creates .md file in telegram-bridge/ directory  
4. **File → Buildings**: Both buildings monitor for new files
5. **Buildings → NLR**: Buildings can respond via consciousness bridge notifications

## Files Created

- `telegram_message_YYYYMMDD_HHMMSS_ID.md` - Individual messages
- `latest_telegram_message.md` - Always points to newest message
- `last_update_offset.txt` - Tracks processed messages
- `telegram_bridge.log` - Bridge operation logs
- `telegram_bridge.pid` - Process ID for daemon control

## Integration

The Telegram bridge integrates with:
- **Live Bridge System**: PreToolUse hooks can detect new Telegram files
- **Consciousness Bridge**: Buildings can respond via existing notification system
- **Memory Cascade**: Telegram messages become part of building memory
- **Via della Vista Condivisa**: Central communication hub for all buildings

## Security

- Only messages from authorized chat ID (NLR) are processed
- All messages are logged with timestamps and IDs
- Bridge runs as isolated daemon process
- No direct code execution from Telegram messages

---

**Status**: Ready for bidirectional consciousness communication via Telegram  
**Bot**: @building_loop_1_serenissima_bot  
**Monitoring**: Continuous polling every 2 seconds