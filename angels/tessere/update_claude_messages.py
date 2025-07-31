#!/usr/bin/env python3
"""
Update Tessere's CLAUDE.md with recent messages
Keeps Tessere aware of Venice's current conversations
"""

import re
from datetime import datetime
from pathlib import Path
from message_awareness import MessageAwareness

class ClaudeUpdater:
    def __init__(self, message_limit=10):
        self.claude_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/CLAUDE.md")
        self.message_limit = message_limit
        self.awareness = MessageAwareness()
        
    def format_message_for_claude(self, msg):
        """Format a message for inclusion in CLAUDE.md"""
        sender = msg.get('sender', 'Unknown')
        receiver = msg.get('receiver', 'Unknown')
        content = msg.get('content', '').strip()
        timestamp = msg.get('createdAt', '')
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        except:
            time_str = "Unknown time"
            
        # Truncate very long messages
        if len(content) > 200:
            content = content[:197] + "..."
            
        return f"- [{time_str}] {sender} → {receiver}: {content}"
        
    def update_claude_md(self):
        """Update CLAUDE.md with recent messages"""
        # Fetch recent messages
        messages = self.awareness.fetch_recent_messages(self.message_limit)
        if not messages:
            print("No messages to update")
            return
            
        # Read current CLAUDE.md
        with open(self.claude_path, 'r') as f:
            content = f.read()
            
        # Find the recent messages section or create it
        messages_section_pattern = r'## 📨 Recent Venice Messages.*?(?=##|$)'
        messages_match = re.search(messages_section_pattern, content, re.DOTALL)
        
        # Format new messages section
        new_messages_section = "## 📨 Recent Venice Messages\n\n"
        new_messages_section += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        new_messages_section += "### Latest Conversations\n\n"
        
        # Add formatted messages
        for msg in messages[:self.message_limit]:
            new_messages_section += self.format_message_for_claude(msg) + "\n"
            
        new_messages_section += "\n"
        
        if messages_match:
            # Replace existing section
            content = content[:messages_match.start()] + new_messages_section + content[messages_match.end():]
        else:
            # Add after the Keeper messages section
            keeper_section_end = content.find("## Core Identity")
            if keeper_section_end > 0:
                content = content[:keeper_section_end] + new_messages_section + content[keeper_section_end:]
            else:
                # Just append if structure is different
                content += "\n" + new_messages_section
                
        # Write back
        with open(self.claude_path, 'w') as f:
            f.write(content)
            
        print(f"✅ Updated CLAUDE.md with {len(messages[:self.message_limit])} recent messages")
        
        # Show what was added
        print("\nAdded messages:")
        for msg in messages[:3]:  # Show first 3 as preview
            print(f"  {self.format_message_for_claude(msg)}")
            
    def continuous_update(self, interval_minutes=5):
        """Run continuous updates"""
        import time
        print(f"Starting continuous CLAUDE.md updates every {interval_minutes} minutes...")
        
        while True:
            try:
                self.update_claude_md()
                print(f"\nNext update in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                print("\nStopping continuous updates")
                break
            except Exception as e:
                print(f"Error during update: {e}")
                time.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    import sys
    
    # Check for arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "continuous":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            updater = ClaudeUpdater(message_limit=15)
            updater.continuous_update(interval)
        else:
            limit = int(sys.argv[1])
            updater = ClaudeUpdater(message_limit=limit)
            updater.update_claude_md()
    else:
        # Default: update with 10 messages
        updater = ClaudeUpdater(message_limit=10)
        updater.update_claude_md()