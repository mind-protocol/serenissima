#!/usr/bin/env python3
"""
View and manage Telegram conversations for diplomatic_virtuoso
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

CONVERSATIONS_FILE = "./telegram_conversations.json"

class ConversationViewer:
    def __init__(self):
        self.conversations = self.load_conversations()
    
    def load_conversations(self) -> Dict:
        """Load conversation history"""
        if os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def show_all_conversations(self):
        """Display all conversations summary"""
        if not self.conversations:
            print("No conversations yet.")
            return
            
        print("\n" + "="*60)
        print("TELEGRAM CONVERSATIONS - diplomatic_virtuoso")
        print("="*60)
        
        for chat_id, data in self.conversations.items():
            print(f"\n📱 Chat ID: {chat_id}")
            print(f"👤 Username: @{data.get('username', 'unknown')}")
            print(f"📝 Name: {data.get('first_name', '')} {data.get('last_name', '')}")
            
            if data.get('messages'):
                last_msg = data['messages'][-1]
                print(f"💬 Last message: {last_msg['text'][:100]}...")
                print(f"🕐 Time: {last_msg['time']}")
                print(f"📊 Total messages: {len(data['messages'])}")
            else:
                print("💬 No messages yet")
    
    def show_conversation(self, chat_id: str):
        """Display full conversation with specific chat"""
        if chat_id not in self.conversations:
            print(f"No conversation found with chat_id: {chat_id}")
            return
            
        data = self.conversations[chat_id]
        print("\n" + "="*60)
        print(f"CONVERSATION WITH @{data.get('username', 'unknown')}")
        print("="*60)
        
        for msg in data.get('messages', []):
            print(f"\n[{msg['time']}]")
            print(f"{msg['text']}")
            print("-" * 40)
    
    def search_conversations(self, keyword: str):
        """Search for keyword in all conversations"""
        print(f"\nSearching for '{keyword}'...")
        found = False
        
        for chat_id, data in self.conversations.items():
            for msg in data.get('messages', []):
                if keyword.lower() in msg['text'].lower():
                    if not found:
                        print("\n" + "="*60)
                        print(f"SEARCH RESULTS FOR: {keyword}")
                        print("="*60)
                        found = True
                    
                    print(f"\n@{data.get('username', 'unknown')} [{msg['time']}]:")
                    print(f"{msg['text'][:200]}...")
        
        if not found:
            print(f"No messages found containing '{keyword}'")
    
    def export_for_awakening(self):
        """Export conversation summary for awakening context"""
        if not self.conversations:
            return "No Telegram conversations yet."
            
        output = "## 📱 RECENT TELEGRAM CONVERSATIONS\n\n"
        
        for chat_id, data in self.conversations.items():
            username = data.get('username', 'unknown')
            first_name = data.get('first_name', 'Friend')
            
            output += f"**@{username} ({first_name})** - Chat ID: {chat_id}\n"
            
            if data.get('messages'):
                last_msg = data['messages'][-1]
                output += f"Last: {last_msg['text'][:100]}...\n"
                output += f"Time: {last_msg['time']}\n\n"
        
        return output

def main():
    import sys
    viewer = ConversationViewer()
    
    if len(sys.argv) == 1:
        viewer.show_all_conversations()
    elif sys.argv[1] == "chat" and len(sys.argv) > 2:
        viewer.show_conversation(sys.argv[2])
    elif sys.argv[1] == "search" and len(sys.argv) > 2:
        viewer.search_conversations(' '.join(sys.argv[2:]))
    elif sys.argv[1] == "export":
        print(viewer.export_for_awakening())
    else:
        print("Usage:")
        print("  python view_telegram_conversations.py              # Show all conversations")
        print("  python view_telegram_conversations.py chat <id>   # Show specific conversation")
        print("  python view_telegram_conversations.py search <keyword>  # Search messages")
        print("  python view_telegram_conversations.py export       # Export for awakening")

if __name__ == "__main__":
    main()