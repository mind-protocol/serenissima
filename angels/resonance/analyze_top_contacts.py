#!/usr/bin/env python3
"""
Simplified analyzer that prepares conversations for manual Claude analysis
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class ContactPreparer:
    def __init__(self, telegram_data_path):
        self.data_path = telegram_data_path
        self.user_name = "NLR - Founder @ Universe Engine"
        self.output_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/resonance/conversations_to_analyze"
        
    def load_data(self):
        """Load the Telegram JSON export"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_text(self, msg):
        """Extract clean text from message"""
        text = msg.get('text', '')
        if isinstance(text, list):
            text_parts = []
            for part in text:
                if isinstance(part, str):
                    text_parts.append(part)
                elif isinstance(part, dict) and 'text' in part:
                    text_parts.append(part['text'])
            text = ' '.join(text_parts)
        return str(text).strip()
    
    def select_top_contacts(self, data):
        """Select top contacts based on various criteria"""
        contact_scores = []
        
        for chat in data['chats']['list']:
            if chat.get('type') != 'personal_chat':
                continue
                
            messages = chat.get('messages', [])
            if len(messages) < 50:  # Minimum threshold
                continue
            
            # Calculate metrics
            recent_messages = 0
            investment_mentions = 0
            ai_mentions = 0
            last_message_date = None
            
            for msg in messages[-200:]:  # Last 200 messages
                text = self.extract_text(msg).lower()
                msg_date = datetime.fromisoformat(msg.get('date', '2020-01-01').replace(' ', 'T'))
                
                # Recent activity (last 3 months)
                if msg_date > datetime.now() - timedelta(days=90):
                    recent_messages += 1
                
                # Investment indicators
                if any(word in text for word in ['invest', 'fund', 'capital', 'portfolio', 'lp', 'gp']):
                    investment_mentions += 1
                
                # AI/Venice interest
                if any(word in text for word in ['ai', 'consciousness', 'venice', 'universe engine']):
                    ai_mentions += 1
                
                if not last_message_date or msg_date > last_message_date:
                    last_message_date = msg_date
            
            # Calculate score
            score = 0
            
            # Recency is most important
            if last_message_date:
                days_since_last = (datetime.now() - last_message_date).days
                if days_since_last < 7:
                    score += 50
                elif days_since_last < 30:
                    score += 30
                elif days_since_last < 90:
                    score += 10
            
            # Investment relevance
            score += min(investment_mentions * 5, 30)
            
            # AI/Venice relevance
            score += min(ai_mentions * 3, 20)
            
            # Message volume
            if len(messages) > 1000:
                score += 20
            elif len(messages) > 500:
                score += 10
            
            contact_scores.append({
                'name': chat.get('name', 'Unknown'),
                'chat': chat,
                'score': score,
                'total_messages': len(messages),
                'recent_messages': recent_messages,
                'investment_mentions': investment_mentions,
                'ai_mentions': ai_mentions,
                'last_message_date': last_message_date
            })
        
        # Sort by score
        contact_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return contact_scores[:10]  # Top 10
    
    def prepare_conversation(self, contact_data):
        """Prepare a conversation for analysis"""
        messages = contact_data['chat']['messages']
        contact_name = contact_data['name']
        
        # Get last 6 months of messages
        cutoff_date = datetime.now() - timedelta(days=180)
        recent_messages = []
        
        for msg in messages:
            msg_date = datetime.fromisoformat(msg.get('date', '2020-01-01').replace(' ', 'T'))
            if msg_date > cutoff_date:
                recent_messages.append(msg)
        
        # Limit to last 300 messages
        recent_messages = recent_messages[-300:]
        
        # Create analysis file
        os.makedirs(self.output_dir, exist_ok=True)
        filename = f"{contact_name.replace(' ', '_').replace('/', '_')}_conversation.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"CONVERSATION ANALYSIS: {contact_name}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total messages: {contact_data['total_messages']}\n")
            f.write(f"Recent messages (90 days): {contact_data['recent_messages']}\n")
            f.write(f"Investment mentions: {contact_data['investment_mentions']}\n")
            f.write(f"AI/Venice mentions: {contact_data['ai_mentions']}\n")
            f.write(f"Last contact: {contact_data['last_message_date'].strftime('%Y-%m-%d') if contact_data['last_message_date'] else 'Unknown'}\n")
            f.write("\n" + "=" * 50 + "\n")
            f.write("RECENT CONVERSATION (Last 6 months):\n")
            f.write("=" * 50 + "\n\n")
            
            # Write messages
            for msg in recent_messages:
                sender = msg.get('from', 'Unknown')
                text = self.extract_text(msg)
                date = msg.get('date', 'Unknown date')
                
                if sender == self.user_name:
                    sender = "NLR"
                elif sender == contact_name:
                    sender = contact_name
                else:
                    continue  # Skip system messages
                
                f.write(f"[{date}] {sender}: {text}\n\n")
            
            # Write analysis prompt
            f.write("\n" + "=" * 50 + "\n")
            f.write("ANALYSIS NEEDED:\n")
            f.write("=" * 50 + "\n\n")
            f.write("""Please analyze this conversation and provide:

1. CONTACT PROFILE
- Professional background and current role
- Key expertise areas
- Communication style

2. INVESTMENT POTENTIAL
- Likelihood of investing (0-100%)
- Probable ticket size
- Investment interests

3. PARTNERSHIP OPPORTUNITIES
- Potential synergies with Venice
- What they could contribute
- Best Venice company match

4. CITIZEN MATCHING
- Best Venice citizen match and why
- Shared interests/complementary skills

5. ENGAGEMENT STRATEGY
- Recommended approach
- Key topics to emphasize
- Draft first message (2-3 sentences)
""")
        
        return filepath

def main():
    # Initialize
    data_path = "/mnt/c/Users/reyno/Downloads/Telegram Desktop/DataExport_2025-07-21/result.json"
    preparer = ContactPreparer(data_path)
    
    print("Loading Telegram data...")
    data = preparer.load_data()
    
    print("Selecting top contacts...")
    top_contacts = preparer.select_top_contacts(data)
    
    print(f"\n=== TOP 10 CONTACTS FOR ANALYSIS ===")
    for i, contact in enumerate(top_contacts):
        print(f"\n{i+1}. {contact['name']} (Score: {contact['score']})")
        print(f"   Messages: {contact['total_messages']} total, {contact['recent_messages']} recent")
        print(f"   Investment mentions: {contact['investment_mentions']}")
        print(f"   AI/Venice mentions: {contact['ai_mentions']}")
        print(f"   Last contact: {contact['last_message_date'].strftime('%Y-%m-%d') if contact['last_message_date'] else 'Unknown'}")
    
    print(f"\nPreparing conversations for analysis...")
    
    # Prepare each conversation
    prepared_files = []
    for contact in top_contacts:
        filepath = preparer.prepare_conversation(contact)
        prepared_files.append(filepath)
        print(f"Prepared: {os.path.basename(filepath)}")
    
    print(f"\n=== PREPARATION COMPLETE ===")
    print(f"Conversations saved to: {preparer.output_dir}")
    print(f"\nYou can now analyze each conversation file with Claude using the prompts provided.")
    
    # Create a summary file
    summary_path = os.path.join(preparer.output_dir, "00_ANALYSIS_GUIDE.txt")
    with open(summary_path, 'w') as f:
        f.write("TOP CONTACTS FOR VENICE INVESTMENT/PARTNERSHIP ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        f.write("Priority order based on recency, investment mentions, and AI/Venice interest:\n\n")
        
        for i, contact in enumerate(top_contacts):
            f.write(f"{i+1}. {contact['name']}\n")
            f.write(f"   File: {contact['name'].replace(' ', '_').replace('/', '_')}_conversation.txt\n")
            f.write(f"   Score: {contact['score']}\n")
            f.write(f"   Key metrics: {contact['total_messages']} messages, ")
            f.write(f"{contact['investment_mentions']} investment mentions, ")
            f.write(f"{contact['ai_mentions']} AI mentions\n\n")
        
        f.write("\nEach file contains:\n")
        f.write("- Contact metrics summary\n")
        f.write("- Recent conversation history (last 6 months)\n")
        f.write("- Analysis prompt template\n\n")
        f.write("Analyze each conversation to identify:\n")
        f.write("- Investment potential and ticket size\n")
        f.write("- Partnership opportunities with Venice companies\n")
        f.write("- Best citizen match for partnership\n")
        f.write("- Engagement strategy and first message\n")

if __name__ == "__main__":
    main()