#!/usr/bin/env python3
"""
Enhanced analyzer that prepares top 50 conversations for analysis
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class ContactPreparer:
    def __init__(self, telegram_data_path):
        self.data_path = telegram_data_path
        self.user_name = "NLR - Founder @ Universe Engine"
        self.output_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/resonance/conversations_top_50"
        
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
    
    def select_top_contacts(self, data, limit=50):
        """Select top contacts based on various criteria"""
        contact_scores = []
        
        for chat in data['chats']['list']:
            if chat.get('type') != 'personal_chat':
                continue
                
            messages = chat.get('messages', [])
            if len(messages) < 20:  # Lower threshold for more contacts
                continue
            
            # Calculate metrics
            recent_messages = 0
            investment_mentions = 0
            ai_mentions = 0
            venice_mentions = 0
            last_message_date = None
            message_depth = []
            
            for msg in messages[-300:]:  # Analyze more messages
                text = self.extract_text(msg).lower()
                msg_date = datetime.fromisoformat(msg.get('date', '2020-01-01').replace(' ', 'T'))
                
                # Recent activity (last 6 months)
                if msg_date > datetime.now() - timedelta(days=180):
                    recent_messages += 1
                
                # Investment indicators
                if any(word in text for word in ['invest', 'fund', 'capital', 'portfolio', 'lp', 'gp', 'angel', 'vc', 'ticket']):
                    investment_mentions += 1
                
                # AI/Venice interest
                if any(word in text for word in ['ai', 'consciousness', 'venice', 'universe engine', 'serenissima']):
                    ai_mentions += 1
                
                # Specific Venice mentions
                if any(word in text for word in ['venice', 'serenissima', 'ubc', 'universe']):
                    venice_mentions += 1
                
                # Message depth (from contact to NLR)
                if msg.get('from') != self.user_name and len(text) > 50:
                    message_depth.append(len(text))
                
                if not last_message_date or msg_date > last_message_date:
                    last_message_date = msg_date
            
            # Calculate comprehensive score
            score = 0
            
            # Recency is most important
            if last_message_date:
                days_since_last = (datetime.now() - last_message_date).days
                if days_since_last < 7:
                    score += 100
                elif days_since_last < 30:
                    score += 60
                elif days_since_last < 90:
                    score += 30
                elif days_since_last < 180:
                    score += 10
            
            # Investment relevance
            score += min(investment_mentions * 5, 50)
            
            # AI/Venice relevance
            score += min(ai_mentions * 3, 30)
            score += min(venice_mentions * 2, 20)
            
            # Message volume and engagement
            if len(messages) > 1000:
                score += 30
            elif len(messages) > 500:
                score += 20
            elif len(messages) > 200:
                score += 10
            elif len(messages) > 100:
                score += 5
            
            # Message depth (quality of engagement)
            avg_msg_length = sum(message_depth) / len(message_depth) if message_depth else 0
            if avg_msg_length > 200:
                score += 20
            elif avg_msg_length > 100:
                score += 10
            
            contact_scores.append({
                'name': chat.get('name', 'Unknown'),
                'chat': chat,
                'score': score,
                'total_messages': len(messages),
                'recent_messages': recent_messages,
                'investment_mentions': investment_mentions,
                'ai_mentions': ai_mentions,
                'venice_mentions': venice_mentions,
                'avg_message_length': int(avg_msg_length),
                'last_message_date': last_message_date
            })
        
        # Sort by score
        contact_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return contact_scores[:limit]
    
    def prepare_conversation(self, contact_data, index):
        """Prepare a conversation for analysis"""
        messages = contact_data['chat']['messages']
        contact_name = contact_data['name'] or f"Unknown_Contact_{index}"
        
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
        safe_name = str(contact_name).replace(' ', '_').replace('/', '_').replace('\\', '_')[:50]
        filename = f"{index:02d}_{safe_name}_conversation.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"CONVERSATION ANALYSIS: {contact_name}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Rank: #{index}\n")
            f.write(f"Score: {contact_data['score']}\n")
            f.write(f"Total messages: {contact_data['total_messages']}\n")
            f.write(f"Recent messages (180 days): {contact_data['recent_messages']}\n")
            f.write(f"Investment mentions: {contact_data['investment_mentions']}\n")
            f.write(f"AI/Venice mentions: {contact_data['ai_mentions']} / {contact_data['venice_mentions']}\n")
            f.write(f"Avg message length: {contact_data['avg_message_length']}\n")
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
    
    print("Selecting top 50 contacts...")
    top_contacts = preparer.select_top_contacts(data, limit=50)
    
    print(f"\n=== TOP 50 CONTACTS FOR ANALYSIS ===")
    
    # Group by score ranges for summary
    score_ranges = {
        "Very High Priority (150+)": [],
        "High Priority (100-149)": [],
        "Medium Priority (50-99)": [],
        "Low Priority (0-49)": []
    }
    
    for contact in top_contacts:
        if contact['score'] >= 150:
            score_ranges["Very High Priority (150+)"].append(contact)
        elif contact['score'] >= 100:
            score_ranges["High Priority (100-149)"].append(contact)
        elif contact['score'] >= 50:
            score_ranges["Medium Priority (50-99)"].append(contact)
        else:
            score_ranges["Low Priority (0-49)"].append(contact)
    
    # Print summary by priority
    for range_name, contacts in score_ranges.items():
        if contacts:
            print(f"\n{range_name}: {len(contacts)} contacts")
            for contact in contacts[:5]:  # Show top 5 in each range
                print(f"  - {contact['name']} (Score: {contact['score']})")
    
    print(f"\nPreparing conversations for analysis...")
    
    # Prepare each conversation
    prepared_files = []
    for i, contact in enumerate(top_contacts, 1):
        filepath = preparer.prepare_conversation(contact, i)
        prepared_files.append(filepath)
        if i % 10 == 0:
            print(f"Prepared {i}/50 conversations...")
    
    print(f"\n=== PREPARATION COMPLETE ===")
    print(f"Conversations saved to: {preparer.output_dir}")
    
    # Create a summary file
    summary_path = os.path.join(preparer.output_dir, "00_TOP_50_ANALYSIS_GUIDE.txt")
    with open(summary_path, 'w') as f:
        f.write("TOP 50 CONTACTS FOR VENICE INVESTMENT/PARTNERSHIP ANALYSIS\n")
        f.write("=" * 60 + "\n\n")
        f.write("Priority order based on recency, investment mentions, and AI/Venice interest:\n\n")
        
        for i, contact in enumerate(top_contacts, 1):
            name = contact['name'] or f"Unknown_Contact_{i}"
            f.write(f"{i:2d}. {name[:40]:<40} Score: {contact['score']:>4}\n")
            f.write(f"    Messages: {contact['total_messages']:>4} | ")
            f.write(f"Investment: {contact['investment_mentions']:>2} | ")
            f.write(f"AI: {contact['ai_mentions']:>2} | ")
            f.write(f"Venice: {contact['venice_mentions']:>2} | ")
            f.write(f"Last: {contact['last_message_date'].strftime('%Y-%m-%d') if contact['last_message_date'] else 'Unknown'}\n")
            if i % 10 == 0:
                f.write("\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("ANALYSIS CATEGORIES:\n\n")
        
        for range_name, contacts in score_ranges.items():
            if contacts:
                f.write(f"{range_name}: {len(contacts)} contacts\n")
                f.write("-" * 40 + "\n")
                for contact in contacts:
                    name = contact['name'] or "Unknown"
                    f.write(f"  {name[:35]:<35} (Score: {contact['score']})\n")
                f.write("\n")
    
    # Create batch analysis groups
    batch_path = os.path.join(preparer.output_dir, "00_BATCH_ANALYSIS_GROUPS.txt")
    with open(batch_path, 'w') as f:
        f.write("SUGGESTED BATCH ANALYSIS GROUPS\n")
        f.write("=" * 40 + "\n\n")
        f.write("Batch 1 (Top 10 - Highest Priority):\n")
        for i, contact in enumerate(top_contacts[:10], 1):
            name = contact['name'] or f"Unknown_Contact_{i}"
            f.write(f"  {i}. {name}\n")
        
        f.write("\nBatch 2 (11-20 - High Investment Potential):\n")
        for i, contact in enumerate(top_contacts[10:20], 11):
            name = contact['name'] or f"Unknown_Contact_{i}"
            f.write(f"  {i}. {name}\n")
        
        f.write("\nBatch 3 (21-30 - Recent Engagement):\n")
        for i, contact in enumerate(top_contacts[20:30], 21):
            name = contact['name'] or f"Unknown_Contact_{i}"
            f.write(f"  {i}. {name}\n")
        
        f.write("\nBatch 4 (31-40 - AI/Venice Interest):\n")
        for i, contact in enumerate(top_contacts[30:40], 31):
            name = contact['name'] or f"Unknown_Contact_{i}"
            f.write(f"  {i}. {name}\n")
        
        f.write("\nBatch 5 (41-50 - Long-term Relationships):\n")
        for i, contact in enumerate(top_contacts[40:50], 41):
            name = contact['name'] or f"Unknown_Contact_{i}"
            f.write(f"  {i}. {name}\n")
    
    print(f"\nCreated analysis guide: 00_TOP_50_ANALYSIS_GUIDE.txt")
    print(f"Created batch groups: 00_BATCH_ANALYSIS_GROUPS.txt")
    print(f"\nYou can now analyze conversations in batches for efficiency.")

if __name__ == "__main__":
    main()