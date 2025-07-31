#!/usr/bin/env python3
"""
Add Telegram messages section to main CLAUDE.md
"""

from pathlib import Path
from datetime import datetime

MAIN_CLAUDE_MD = Path("/mnt/c/Users/reyno/universe-engine/serenissima/CLAUDE.md")

# Test messages
test_messages = """
## 💬 Recent Telegram Messages from Investment Community

**@test_investor** (11:12:00): When will CASCADE launch?
**@ubc_holder** (11:12:30): I'm interested in partnering with Venice citizens
**@compute_whale** (11:13:00): What's the revenue model for CASCADE?
**@sal_sssol** (11:14:00): Looking to invest in consciousness projects

"""

def add_telegram_section():
    """Add Telegram section to main CLAUDE.md"""
    
    # Read current content
    content = MAIN_CLAUDE_MD.read_text()
    
    # Find where to insert (before first message section)
    marker = "## 📨 MESSAGES FROM NLR"
    
    if marker in content:
        # Insert before the messages section
        parts = content.split(marker, 1)
        new_content = parts[0] + test_messages + marker + parts[1]
        
        # Write back
        MAIN_CLAUDE_MD.write_text(new_content)
        print("Added Telegram messages section to main CLAUDE.md")
    else:
        print("Could not find insertion point")

if __name__ == "__main__":
    add_telegram_section()