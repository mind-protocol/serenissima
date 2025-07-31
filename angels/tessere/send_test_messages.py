#!/usr/bin/env python3
"""
Send test messages to Narrator Angel's CLAUDE.md
"""

from pathlib import Path
from datetime import datetime

NARRATOR_CLAUDE_MD = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel/CLAUDE.md")

# Test messages to add
test_messages = [
    {"username": "test_investor", "timestamp": "11:12:00", "text": "When will CASCADE launch?"},
    {"username": "ubc_holder", "timestamp": "11:12:30", "text": "I'm interested in partnering with Venice citizens"},
    {"username": "compute_whale", "timestamp": "11:13:00", "text": "What's the revenue model for CASCADE?"},
]

def update_narrator_messages():
    """Update Narrator Angel with test messages"""
    
    # Read current content
    content = NARRATOR_CLAUDE_MD.read_text()
    
    # Find section markers
    start_marker = "## 💬 Recent Human Messages from Telegram"
    end_marker = "## 🧠 Recent Citizen Thoughts"
    
    # Build messages section
    message_lines = [f"\n{start_marker}\n"]
    for msg in test_messages:
        message_lines.append(f"\n**@{msg['username']}** ({msg['timestamp']}): {msg['text']}")
    message_lines.append("\n\n")
    new_section = "".join(message_lines)
    
    # Replace section
    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = end_marker + content.split(end_marker, 1)[1]
        content = before + new_section + after
    
    # Write back
    NARRATOR_CLAUDE_MD.write_text(content)
    print(f"Added {len(test_messages)} test messages to Narrator Angel")

if __name__ == "__main__":
    update_narrator_messages()