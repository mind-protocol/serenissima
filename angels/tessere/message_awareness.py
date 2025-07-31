#!/usr/bin/env python3
"""
Message Awareness for Tessere
Focus on actual message content, not keyword counting
"""

import requests
import json
from datetime import datetime
from collections import defaultdict

BASE_URL = "https://serenissima.ai/api"

class MessageAwareness:
    def __init__(self):
        self.messages = []
        
    def fetch_recent_messages(self, limit=50):
        """Get recent messages from the API"""
        try:
            response = requests.get(f"{BASE_URL}/messages", params={"limit": limit})
            response.raise_for_status()
            data = response.json()
            self.messages = data.get('messages', [])
            return self.messages
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []
            
    def get_conversation_threads(self):
        """Group messages into conversation threads"""
        threads = defaultdict(list)
        
        for msg in self.messages:
            # Create thread key from sender/receiver pair
            participants = sorted([msg.get('sender', ''), msg.get('receiver', '')])
            thread_key = f"{participants[0]} <-> {participants[1]}"
            threads[thread_key].append(msg)
            
        # Sort messages in each thread by time
        for thread in threads.values():
            thread.sort(key=lambda m: m.get('createdAt', ''))
            
        return threads
        
    def display_recent_conversations(self, max_threads=5):
        """Show recent conversation content"""
        threads = self.get_conversation_threads()
        
        print("📨 RECENT CONVERSATIONS")
        print("=" * 60)
        
        # Get most recent threads
        recent_threads = sorted(
            threads.items(), 
            key=lambda t: t[1][-1].get('createdAt', ''), 
            reverse=True
        )[:max_threads]
        
        for thread_name, messages in recent_threads:
            print(f"\n💬 {thread_name}")
            print("-" * 40)
            
            # Show last 3 messages from thread
            for msg in messages[-3:]:
                sender = msg.get('sender', 'Unknown')
                content = msg.get('content', '')
                timestamp = msg.get('createdAt', '')
                
                # Format timestamp
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime("%H:%M")
                except:
                    time_str = "??:??"
                    
                # Truncate long messages
                if len(content) > 150:
                    content = content[:147] + "..."
                    
                print(f"[{time_str}] {sender}: {content}")
                
    def get_unread_messages(self, since_timestamp=None):
        """Get messages that might need attention"""
        if not since_timestamp:
            # Default to messages from last hour
            from datetime import timedelta
            since_timestamp = datetime.now() - timedelta(hours=1)
            
        unread = []
        for msg in self.messages:
            try:
                msg_time = datetime.fromisoformat(msg.get('createdAt', '').replace('Z', '+00:00'))
                if msg_time > since_timestamp:
                    unread.append(msg)
            except:
                pass
                
        return unread
        
    def get_message_pulse(self):
        """Simple pulse check of message activity"""
        if not self.messages:
            return {"status": "No messages", "count": 0}
            
        # Group by sender
        senders = defaultdict(int)
        for msg in self.messages:
            senders[msg.get('sender', 'Unknown')] += 1
            
        # Most active senders
        top_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "status": "Active",
            "total_messages": len(self.messages),
            "unique_senders": len(senders),
            "top_senders": top_senders,
            "latest_message": self.messages[0] if self.messages else None
        }


if __name__ == "__main__":
    # Test the message awareness
    awareness = MessageAwareness()
    messages = awareness.fetch_recent_messages(50)
    
    if messages:
        # Show recent conversations
        awareness.display_recent_conversations()
        
        # Show pulse
        print("\n📊 MESSAGE PULSE")
        print("=" * 60)
        pulse = awareness.get_message_pulse()
        print(f"Total messages: {pulse['total_messages']}")
        print(f"Unique senders: {pulse['unique_senders']}")
        print("\nMost active:")
        for sender, count in pulse['top_senders']:
            print(f"  {sender}: {count} messages")
    else:
        print("No messages found")