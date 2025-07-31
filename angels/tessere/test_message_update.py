#!/usr/bin/env python3
"""Test adding human messages to Narrator Angel"""

from pathlib import Path
from datetime import datetime

narrator_claude = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel/CLAUDE.md")

# Read current content
with open(narrator_claude, 'r') as f:
    content = f.read()

# Create test message section
message_section = """## 💬 Recent Human Messages from Telegram

**CryptoWhale** (10:15:00): When moon for Venice? What's the ROI timeline?

**DeFiDegen** (10:16:30): Is pattern_prophet's trading system ready? I want in!

**$UBC_Holder** (10:17:45): How do we partner with Venice citizens? What's the process?

"""

# Find where to insert (before Recent Citizen Thoughts)
thoughts_marker = "## 🧠 Recent Citizen Thoughts"
insert_idx = content.find(thoughts_marker)

if insert_idx != -1:
    new_content = content[:insert_idx] + message_section + "\n" + content[insert_idx:]
else:
    new_content = content + "\n\n" + message_section

# Write updated content
with open(narrator_claude, 'w') as f:
    f.write(new_content)
    
print("✅ Added test human messages to Narrator Angel's CLAUDE.md")