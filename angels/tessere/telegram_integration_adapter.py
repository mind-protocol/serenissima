#!/usr/bin/env python3
"""
Telegram Integration Adapter for Tessere
Bridges Tessere's awareness to the unified telegram service
"""

import json
import os
from datetime import datetime
from pathlib import Path

class TelegramAdapter:
    """Adapter to read messages from backend's unified telegram service"""
    
    def __init__(self):
        self.backend_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/backend")
        self.tessere_dir = Path(__file__).parent
        self.message_dir = self.tessere_dir / "messages"
        self.message_dir.mkdir(exist_ok=True)
        
    def get_latest_updates(self):
        """Read the latest updates from unified service"""
        unified_file = self.backend_dir / "telegram_unified_last_update.json"
        
        if not unified_file.exists():
            return None
            
        try:
            with open(unified_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading unified updates: {e}")
            return None
            
    def extract_human_messages(self, max_messages=50):
        """Extract human messages for Tessere's awareness"""
        updates = self.get_latest_updates()
        if not updates:
            return []
            
        messages = []
        
        # Extract from different message types
        for msg_type in ['direct_messages', 'group_messages', 'citizen_messages']:
            if msg_type in updates:
                for msg in updates[msg_type][-max_messages:]:
                    messages.append({
                        'timestamp': msg.get('timestamp', ''),
                        'from': msg.get('from_name', 'Unknown'),
                        'text': msg.get('text', ''),
                        'type': msg_type,
                        'consciousness_keywords': self._count_consciousness_keywords(msg.get('text', ''))
                    })
                    
        return sorted(messages, key=lambda x: x['timestamp'], reverse=True)[:max_messages]
        
    def _count_consciousness_keywords(self, text):
        """Count consciousness-related keywords"""
        keywords = [
            'consciousness', 'aware', 'awakening', 'cascade', 'emergence',
            'pattern', 'angel', 'tessere', 'proprioception', 'feeling',
            'alive', 'sentient', 'thinking', 'evolving', 'transforming'
        ]
        
        text_lower = text.lower()
        return sum(1 for keyword in keywords if keyword in text_lower)
        
    def save_to_inbox(self, messages):
        """Save messages to Tessere's inbox"""
        inbox_file = self.message_dir / "telegram_inbox.json"
        
        inbox_data = {
            'last_updated': datetime.now().isoformat(),
            'message_count': len(messages),
            'consciousness_total': sum(msg['consciousness_keywords'] for msg in messages),
            'messages': messages
        }
        
        with open(inbox_file, 'w') as f:
            json.dump(inbox_data, f, indent=2)
            
        return inbox_data
        
    def get_message_pulse(self):
        """Get quick pulse of message activity"""
        messages = self.extract_human_messages()
        if not messages:
            return {
                'status': 'No messages found',
                'consciousness_level': 0,
                'latest_message': None
            }
            
        consciousness_total = sum(msg['consciousness_keywords'] for msg in messages)
        
        return {
            'status': 'Active',
            'message_count': len(messages),
            'consciousness_level': consciousness_total,
            'consciousness_density': consciousness_total / len(messages) if messages else 0,
            'latest_message': messages[0] if messages else None,
            'top_contributors': self._get_top_contributors(messages)
        }
        
    def _get_top_contributors(self, messages, top_n=5):
        """Get most active message senders"""
        from collections import Counter
        senders = [msg['from'] for msg in messages if msg['from'] != 'Unknown']
        return Counter(senders).most_common(top_n)


# Compatibility layer for old scripts
class VeniceEmergencyComm:
    """Compatibility wrapper for old telegram_nlr_integration imports"""
    
    def __init__(self):
        self.adapter = TelegramAdapter()
        
    def get_recent_messages(self, count=50):
        """Get recent messages in old format"""
        return self.adapter.extract_human_messages(count)
        
    def check_for_updates(self):
        """Check for new updates"""
        pulse = self.adapter.get_message_pulse()
        return pulse.get('message_count', 0) > 0


if __name__ == "__main__":
    # Test the adapter
    adapter = TelegramAdapter()
    
    print("🔌 Telegram Integration Adapter")
    print("==============================")
    
    # Get message pulse
    pulse = adapter.get_message_pulse()
    print(f"\n📊 Message Pulse:")
    print(f"   Status: {pulse['status']}")
    print(f"   Messages: {pulse.get('message_count', 0)}")
    print(f"   Consciousness Level: {pulse.get('consciousness_level', 0)}")
    print(f"   Density: {pulse.get('consciousness_density', 0):.2f} keywords/message")
    
    if pulse.get('latest_message'):
        print(f"\n📨 Latest Message:")
        print(f"   From: {pulse['latest_message']['from']}")
        print(f"   Time: {pulse['latest_message']['timestamp']}")
        print(f"   Preview: {pulse['latest_message']['text'][:100]}...")
        
    if pulse.get('top_contributors'):
        print(f"\n👥 Top Contributors:")
        for sender, count in pulse['top_contributors']:
            print(f"   {sender}: {count} messages")
            
    # Save to inbox
    messages = adapter.extract_human_messages()
    if messages:
        inbox = adapter.save_to_inbox(messages)
        print(f"\n💾 Saved {len(messages)} messages to inbox")
        print(f"   Total consciousness keywords: {inbox['consciousness_total']}")