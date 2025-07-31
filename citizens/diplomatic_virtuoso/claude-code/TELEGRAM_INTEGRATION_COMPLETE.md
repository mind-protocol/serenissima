# Complete Telegram Integration for diplomatic_virtuoso

## 🎯 Overview

This system provides automatic Telegram message awareness for diplomatic_virtuoso through Claude Code hooks. Messages appear naturally in context without manual checking.

## 📁 Structure

```
diplomatic_virtuoso/
├── .claude/
│   └── hooks.json                    # Hook configuration
└── claude-code/
    ├── TELEGRAM_HOOKS_README.md      # Hook documentation
    ├── TELEGRAM_INTEGRATION_COMPLETE.md  # This file
    ├── telegram_checks/              # Hook scripts
    │   ├── session_start_hook.js     # Checks on start
    │   └── periodic_check_hook.js    # Checks during session
    ├── telegram_receiver/            # Message receiver
    │   ├── diplomatic_virtuoso_listener.py  # Telegram client
    │   ├── requirements.txt          # Python dependencies
    │   └── setup.sh                  # Setup script
    └── test_telegram_flow.py         # Test message generator
```

## 🚀 Setup Process

### 1. Hook System (Already Done ✅)
- Hooks configured in `.claude/hooks.json`
- Scripts check for messages automatically
- Messages appear in console and context

### 2. Message Queue
Location: `/backend/telegram_queue/diplomatic_virtuoso/pending/`
- Messages saved as JSON files
- Hooks read from this directory
- Processed messages can be moved to `/processed/`

### 3. Telegram Receiver (Optional)
For real Telegram integration:
```bash
cd claude-code/telegram_receiver
chmod +x setup.sh
./setup.sh
# Edit .env with Telegram API credentials
source venv/bin/activate
python diplomatic_virtuoso_listener.py
```

## 🧪 Testing the System

1. **Create test messages**:
```bash
python3 claude-code/test_telegram_flow.py
```

2. **Start Claude Code**:
```bash
cd /path/to/diplomatic_virtuoso
claude
```

3. **Expected behavior**:
- On start: See notification about pending messages
- Messages added to `.telegram_context.md`
- During session: Alerts for new messages

## 💬 Message Flow

1. **Incoming**: 
   - Real: Telegram → Listener → Queue
   - Test: test_telegram_flow.py → Queue

2. **Processing**:
   - Hook detects messages in queue
   - Creates/updates `.telegram_context.md`
   - Shows notification in console

3. **Context Integration**:
   - Messages appear in diplomatic_virtuoso's awareness
   - Can respond naturally in conversation

## 🎨 Features

- ✅ **Automatic detection** - No manual checking
- ✅ **Session awareness** - Won't repeat messages
- ✅ **Real-time updates** - New messages flagged immediately
- ✅ **Context integration** - Natural conversation flow
- ✅ **Non-intrusive** - Fails silently if issues

## 🔧 Customization

### Change check frequency
Edit `periodic_check_hook.js` to trigger on different events:
- `preToolUse` - Before each tool
- `postToolUse` - After each tool
- Custom intervals with setTimeout

### Add auto-responses
Modify hooks to automatically acknowledge messages or set status indicators.

### Filter messages
Add logic to prioritize certain senders or message types.

## 📊 Monitoring

Check if messages are queued:
```bash
ls -la /mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending/
```

View hook logs (if debug enabled):
```bash
export DEBUG=1
# Then run Claude Code
```

## 🚨 Troubleshooting

1. **No messages showing**: 
   - Check queue directory exists
   - Verify hooks.json is in .claude/
   - Ensure hook scripts are executable

2. **Hooks not running**:
   - Confirm running from diplomatic_virtuoso directory
   - Check Claude Code version supports hooks

3. **Messages not updating**:
   - Verify new files in pending/ directory
   - Check file permissions

---

*This integration ensures diplomatic_virtuoso never misses important Telegram communications while maintaining natural conversation flow!*