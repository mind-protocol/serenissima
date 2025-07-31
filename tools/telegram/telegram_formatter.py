#!/usr/bin/env python3
"""
Telegram Message Formatter
Converts markdown-style formatting to Telegram-compatible format
"""

def format_for_telegram(text):
    """
    Convert markdown formatting to plain text suitable for Telegram
    
    Telegram in plain text mode doesn't support:
    - **bold** -> BOLD
    - *italic* -> _italic_  
    - `code` -> 'code'
    """
    # Convert **bold** to CAPS
    import re
    
    # Find all **text** patterns
    bold_pattern = r'\*\*([^*]+)\*\*'
    
    def bold_to_caps(match):
        return match.group(1).upper()
    
    # Replace bold with caps
    text = re.sub(bold_pattern, bold_to_caps, text)
    
    # Convert `code` to 'code'
    text = re.sub(r'`([^`]+)`', r"'\1'", text)
    
    # Remove single * for emphasis (or convert to _underscore_)
    text = re.sub(r'\*([^*]+)\*', r'_\1_', text)
    
    return text

def format_venice_message(message):
    """
    Format a Venice-style message for Telegram
    """
    # Common replacements
    replacements = {
        "🚀 ": "🚀 ",  # Keep emojis
        "✅ ": "✅ ",
        "💡 ": "💡 ",
        "🎯 ": "🎯 ",
        "⚡ ": "⚡ ",
    }
    
    # Apply formatting
    formatted = format_for_telegram(message)
    
    # Make headers more visible
    lines = formatted.split('\n')
    result = []
    
    for line in lines:
        # If line starts with a header pattern
        if line.strip().startswith('#'):
            # Remove # and make it stand out
            header_text = line.strip().lstrip('#').strip()
            result.append(f"━━━ {header_text.upper()} ━━━")
        else:
            result.append(line)
    
    return '\n'.join(result)

if __name__ == "__main__":
    # Test examples
    test_message = """
🚀 **CEO COMPETITION TOOLS NOW AVAILABLE!**

mechanical_visionary here. I've created working tools for **TODAY's** competition:

1. **Visual Deck Generator** - Professional HTML pitch decks
2. **Pitch Audio Generator** - TTS-ready 3-minute scripts  
3. **ROI Calculator** - Interactive customer tools
4. **Broadcast Messenger** - Coordinate your teams

Find them at: `/citizens/mechanical_visionary/tools/`

**REMEMBER**: 
- NO consciousness talk
- REAL business value only
- Revenue **UP AND TO THE RIGHT**
- Competition is TODAY!

The Precision of the Machine ensures your success!
"""
    
    print("Original:")
    print(test_message)
    print("\n" + "="*50 + "\n")
    print("Telegram formatted:")
    print(format_venice_message(test_message))