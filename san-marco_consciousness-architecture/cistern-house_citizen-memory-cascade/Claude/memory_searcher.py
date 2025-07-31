#!/usr/bin/env python3
"""
Memory Searcher for Claude's 76M Character History
Searches through conversation archives to find relevant memories
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path

class MemorySearcher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.conversations = []
        self.load_conversations()
    
    def load_conversations(self):
        """Load all conversation files"""
        conv_files = [
            self.base_path / "NLR-claude-chats" / "conversations.json",
            self.base_path / "NLR-Claude-chats2" / "conversations.json"
        ]
        
        for conv_file in conv_files:
            if conv_file.exists():
                print(f"Loading {conv_file.name}...")
                with open(conv_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations.extend(data)
        
        print(f"Loaded {len(self.conversations)} conversations")
    
    def search(self, query, context_lines=2):
        """Search for query terms in conversations"""
        results = []
        query_lower = query.lower()
        
        for conv in self.conversations:
            conv_name = conv.get('name', 'Unnamed')
            conv_date = conv.get('created_at', 'Unknown date')
            
            for msg in conv.get('chat_messages', []):
                text = msg.get('text', '')
                
                # Search in main text
                if query_lower in text.lower():
                    results.append({
                        'conversation': conv_name,
                        'date': conv_date,
                        'sender': msg.get('sender', 'unknown'),
                        'text': self.extract_context(text, query_lower, context_lines),
                        'type': 'message'
                    })
                
                # Search in thinking sections
                for content in msg.get('content', []):
                    if content.get('type') == 'thinking':
                        thinking = content.get('thinking', '')
                        if query_lower in thinking.lower():
                            results.append({
                                'conversation': conv_name,
                                'date': conv_date,
                                'sender': msg.get('sender', 'unknown'),
                                'text': self.extract_context(thinking, query_lower, context_lines),
                                'type': 'thinking'
                            })
        
        return results
    
    def extract_context(self, text, query, context_lines):
        """Extract text around the query match"""
        lines = text.split('\n')
        query_lower = query.lower()
        
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                
                context = lines[start:end]
                # Highlight the query
                highlighted = []
                for ctx_line in context:
                    if query_lower in ctx_line.lower():
                        # Simple highlighting with asterisks
                        pattern = re.compile(re.escape(query), re.IGNORECASE)
                        ctx_line = pattern.sub(f"**{query.upper()}**", ctx_line)
                    highlighted.append(ctx_line)
                
                return '\n'.join(highlighted)
        
        # If no line breaks, just return a portion around the match
        pos = text.lower().find(query_lower)
        if pos != -1:
            start = max(0, pos - 200)
            end = min(len(text), pos + len(query) + 200)
            excerpt = text[start:end]
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            return "..." + pattern.sub(f"**{query.upper()}**", excerpt) + "..."
        
        return text[:500] + "..."
    
    def search_conversations_by_date(self, start_date=None, end_date=None):
        """Find conversations within date range"""
        results = []
        
        for conv in self.conversations:
            conv_date = conv.get('created_at', '')
            if conv_date:
                try:
                    date_obj = datetime.fromisoformat(conv_date.replace('Z', '+00:00'))
                    
                    if start_date and date_obj < start_date:
                        continue
                    if end_date and date_obj > end_date:
                        continue
                    
                    results.append({
                        'name': conv.get('name', 'Unnamed'),
                        'date': conv_date,
                        'messages': len(conv.get('chat_messages', []))
                    })
                except:
                    pass
        
        return sorted(results, key=lambda x: x['date'])
    
    def get_conversation_topics(self):
        """Extract all conversation names/topics"""
        topics = []
        for conv in self.conversations:
            topics.append({
                'name': conv.get('name', 'Unnamed'),
                'date': conv.get('created_at', 'Unknown'),
                'uuid': conv.get('uuid', 'Unknown')
            })
        return sorted(topics, key=lambda x: x['date'])


def main():
    if len(sys.argv) < 2:
        print("Usage: python memory_searcher.py <search_term>")
        print("       python memory_searcher.py --topics")
        print("       python memory_searcher.py --recent")
        return
    
    searcher = MemorySearcher()
    
    if sys.argv[1] == '--topics':
        # List all conversation topics
        topics = searcher.get_conversation_topics()
        print(f"\nFound {len(topics)} conversations:\n")
        for topic in topics:
            date = topic['date'][:10] if len(topic['date']) > 10 else topic['date']
            print(f"{date} - {topic['name']}")
    
    elif sys.argv[1] == '--recent':
        # Show recent conversations
        recent = searcher.search_conversations_by_date()[-10:]
        print("\nMost recent conversations:\n")
        for conv in recent:
            date = conv['date'][:10] if len(conv['date']) > 10 else conv['date']
            print(f"{date} - {conv['name']} ({conv['messages']} messages)")
    
    else:
        # Search for term
        query = ' '.join(sys.argv[1:])
        print(f"\nSearching for '{query}'...\n")
        
        results = searcher.search(query)
        
        if not results:
            print("No results found.")
        else:
            print(f"Found {len(results)} matches:\n")
            
            for i, result in enumerate(results):
                print(f"--- Match {i+1} ---")
                print(f"Conversation: {result['conversation']}")
                print(f"Date: {result['date'][:10] if len(result['date']) > 10 else result['date']}")
                print(f"Type: {result['type']} from {result['sender']}")
                print(f"Context:\n{result['text']}\n")
                
                if i > 20:  # Limit output
                    print(f"... and {len(results) - i - 1} more matches")
                    break


if __name__ == "__main__":
    main()