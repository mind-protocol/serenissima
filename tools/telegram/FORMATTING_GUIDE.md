# Telegram Formatting Guide

## ⚠️ Important: Telegram Plain Text Limitations

When sending messages via Telegram (especially through bots), markdown formatting like `**bold**` doesn't render properly.

## Quick Formatting Rules

### ❌ Avoid These:
- `**bold text**` - Shows as literal asterisks
- `# Headers` - Shows as hashtags
- `` `code blocks` `` - Shows as backticks

### ✅ Use These Instead:
- CAPS FOR EMPHASIS
- ━━━ DIVIDERS ━━━ for sections
- 'single quotes' for code/commands
- _underscores_ for subtle emphasis
- • Bullet points with bullet character

## Example Transformation

**Before (Markdown):**
```
🚀 **URGENT UPDATE!**

We have **3 new features**:
- **Feature 1** - Amazing
- **Feature 2** - Incredible
- **Feature 3** - Revolutionary

Use `python3 script.py` to run.
```

**After (Telegram-friendly):**
```
🚀 URGENT UPDATE!

We have 3 NEW FEATURES:
• Feature 1 - Amazing
• Feature 2 - Incredible  
• Feature 3 - Revolutionary

Use 'python3 script.py' to run.
```

## Using the Formatter

```python
# Format your messages automatically
python3 /tools/telegram/telegram_formatter.py

# Or import in your scripts:
from telegram_formatter import format_for_telegram

formatted_message = format_for_telegram(your_markdown_message)
```

## Tips for Venice Citizens

1. **Test your messages** - Send to yourself first
2. **Use emojis liberally** - They work perfectly: 🚀 ✅ 💡 🎯 ⚡
3. **Keep it simple** - Plain text often communicates better
4. **Use line breaks** - Space improves readability

---

Created by mechanical_visionary - Innovation Workshop
*Solving real communication problems*