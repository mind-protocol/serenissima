#!/usr/bin/env python3
"""
Deep analysis of key contacts from Telegram data
Builds personality profiles and identifies investor status
"""

import json
import re
from datetime import datetime
from collections import defaultdict, Counter
import os

class ContactAnalyzer:
    def __init__(self, telegram_data_path, min_messages=50):
        self.data_path = telegram_data_path
        self.min_messages = min_messages
        self.user_name = "NLR - Founder @ Universe Engine"
        
        # Investment indicators
        self.investment_keywords = [
            'invest', 'investment', 'fund', 'funding', 'capital', 'portfolio',
            'lp', 'gp', 'venture', 'angel', 'seed', 'series', 'valuation',
            'equity', 'token', 'allocation', 'raise', 'round', 'check', 'wire',
            'commitment', 'deploy', 'vc', 'pe', 'aum', 'irr', 'roi', 'exit'
        ]
        
        # Personality indicators
        self.personality_markers = {
            'analytical': ['analysis', 'data', 'metrics', 'evidence', 'logical', 'systematic'],
            'visionary': ['future', 'vision', 'imagine', 'potential', 'possibility', 'dream'],
            'action_oriented': ['build', 'ship', 'launch', 'execute', 'implement', 'deliver'],
            'collaborative': ['together', 'team', 'collaborate', 'partner', 'join', 'help'],
            'technical': ['code', 'api', 'algorithm', 'system', 'architecture', 'technical'],
            'philosophical': ['consciousness', 'meaning', 'existence', 'reality', 'truth', 'essence']
        }
        
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
    
    def get_significant_contacts(self, data):
        """Get contacts with sufficient message history"""
        significant_contacts = []
        
        for chat in data['chats']['list']:
            if chat.get('type') != 'personal_chat':
                continue
                
            messages = chat.get('messages', [])
            if len(messages) < self.min_messages:
                continue
                
            # Count messages from each party
            user_messages = [m for m in messages if m.get('from') == self.user_name]
            other_messages = [m for m in messages if m.get('from') != self.user_name]
            
            if len(user_messages) >= self.min_messages // 4 and len(other_messages) >= self.min_messages // 4:
                significant_contacts.append({
                    'name': chat.get('name', 'Unknown'),
                    'chat_id': chat.get('id'),
                    'messages': messages,
                    'user_message_count': len(user_messages),
                    'other_message_count': len(other_messages)
                })
        
        # Sort by total messages
        significant_contacts.sort(key=lambda x: len(x['messages']), reverse=True)
        return significant_contacts
    
    def analyze_investment_potential(self, messages, contact_name):
        """Analyze if contact is a potential investor"""
        investment_signals = {
            'keywords_mentioned': 0,
            'specific_mentions': [],
            'investment_stage': 'unknown',
            'investment_interests': [],
            'financial_capacity_indicators': []
        }
        
        for msg in messages:
            if msg.get('from') != contact_name:
                continue
                
            text = self.extract_text(msg).lower()
            
            # Check for investment keywords
            for keyword in self.investment_keywords:
                if keyword in text:
                    investment_signals['keywords_mentioned'] += 1
                    
                    # Extract context around keyword
                    sentences = text.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            investment_signals['specific_mentions'].append({
                                'keyword': keyword,
                                'context': sentence.strip(),
                                'date': msg.get('date', 'unknown')
                            })
            
            # Look for specific patterns
            if re.search(r'\$\d+[kmb]?', text) or re.search(r'\d+[kmb]?\s*(usd|eur|gbp)', text):
                investment_signals['financial_capacity_indicators'].append(text[:200])
            
            # Investment stage indicators
            if 'early stage' in text or 'seed' in text:
                investment_signals['investment_stage'] = 'early'
            elif 'series a' in text or 'series b' in text:
                investment_signals['investment_stage'] = 'growth'
            elif 'late stage' in text or 'pre-ipo' in text:
                investment_signals['investment_stage'] = 'late'
            
            # Investment interests
            interests = ['ai', 'blockchain', 'crypto', 'defi', 'web3', 'metaverse', 'infrastructure']
            for interest in interests:
                if interest in text and 'invest' in text:
                    investment_signals['investment_interests'].append(interest)
        
        # Calculate investment probability
        score = 0
        if investment_signals['keywords_mentioned'] > 5:
            score += 30
        if investment_signals['financial_capacity_indicators']:
            score += 20
        if investment_signals['investment_stage'] != 'unknown':
            score += 20
        if investment_signals['investment_interests']:
            score += 30
            
        investment_signals['investment_probability'] = min(score, 100)
        
        return investment_signals
    
    def analyze_personality(self, messages, contact_name):
        """Build personality profile from messages"""
        personality = {
            'traits': defaultdict(int),
            'communication_style': {
                'message_length': [],
                'response_time': [],
                'initiation_rate': 0,
                'question_ratio': 0,
                'emoji_usage': Counter()
            },
            'interests': Counter(),
            'sentiment': {
                'positive': 0,
                'negative': 0,
                'neutral': 0
            },
            'engagement_level': 'unknown'
        }
        
        last_msg_time = None
        last_sender = None
        contact_initiated = 0
        total_contact_messages = 0
        questions_asked = 0
        
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        
        for msg in messages:
            sender = msg.get('from')
            text = self.extract_text(msg)
            
            if sender == contact_name:
                total_contact_messages += 1
                
                # Message length
                personality['communication_style']['message_length'].append(len(text))
                
                # Questions
                questions_asked += text.count('?')
                
                # Emojis
                emojis = emoji_pattern.findall(text)
                personality['communication_style']['emoji_usage'].update(emojis)
                
                # Response time
                if last_sender == self.user_name and last_msg_time:
                    response_time = int(msg.get('date_unixtime', 0)) - last_msg_time
                    if 0 < response_time < 86400:  # Within 24 hours
                        personality['communication_style']['response_time'].append(response_time)
                
                # Initiation
                if last_sender != contact_name or (last_msg_time and int(msg.get('date_unixtime', 0)) - last_msg_time > 3600):
                    contact_initiated += 1
                
                # Personality markers
                text_lower = text.lower()
                for trait, markers in self.personality_markers.items():
                    for marker in markers:
                        if marker in text_lower:
                            personality['traits'][trait] += 1
                
                # Interests (extract meaningful words)
                words = re.findall(r'\b[a-z]+\b', text_lower)
                meaningful_words = [w for w in words if len(w) > 5]
                personality['interests'].update(meaningful_words)
                
                # Basic sentiment
                positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'wonderful', 'fantastic']
                negative_words = ['bad', 'terrible', 'hate', 'awful', 'horrible', 'disappointing']
                
                for word in positive_words:
                    if word in text_lower:
                        personality['sentiment']['positive'] += 1
                
                for word in negative_words:
                    if word in text_lower:
                        personality['sentiment']['negative'] += 1
                
                if personality['sentiment']['positive'] == 0 and personality['sentiment']['negative'] == 0:
                    personality['sentiment']['neutral'] += 1
            
            last_sender = sender
            last_msg_time = int(msg.get('date_unixtime', 0))
        
        # Calculate derived metrics
        if total_contact_messages > 0:
            personality['communication_style']['initiation_rate'] = contact_initiated / total_contact_messages
            personality['communication_style']['question_ratio'] = questions_asked / total_contact_messages
        
        # Determine engagement level
        avg_response_time = sum(personality['communication_style']['response_time']) / len(personality['communication_style']['response_time']) if personality['communication_style']['response_time'] else float('inf')
        
        if avg_response_time < 300:  # 5 minutes
            personality['engagement_level'] = 'very_high'
        elif avg_response_time < 3600:  # 1 hour
            personality['engagement_level'] = 'high'
        elif avg_response_time < 21600:  # 6 hours
            personality['engagement_level'] = 'medium'
        else:
            personality['engagement_level'] = 'low'
        
        # Get dominant personality trait
        if personality['traits']:
            personality['dominant_trait'] = max(personality['traits'], key=personality['traits'].get)
        else:
            personality['dominant_trait'] = 'balanced'
            
        return personality
    
    def create_contact_profile(self, contact_data):
        """Create comprehensive profile for a contact"""
        messages = contact_data['messages']
        contact_name = contact_data['name']
        
        # Analyze investment potential
        investment_analysis = self.analyze_investment_potential(messages, contact_name)
        
        # Analyze personality
        personality_analysis = self.analyze_personality(messages, contact_name)
        
        # Extract conversation timeline
        first_message = messages[0] if messages else {}
        last_message = messages[-1] if messages else {}
        
        # Create profile
        profile = {
            'contact_info': {
                'name': contact_name,
                'chat_id': contact_data['chat_id'],
                'total_messages': len(messages),
                'user_messages': contact_data['user_message_count'],
                'contact_messages': contact_data['other_message_count'],
                'first_interaction': first_message.get('date', 'unknown'),
                'last_interaction': last_message.get('date', 'unknown')
            },
            'investment_profile': investment_analysis,
            'personality_profile': {
                'dominant_trait': personality_analysis['dominant_trait'],
                'traits': dict(personality_analysis['traits']),
                'engagement_level': personality_analysis['engagement_level'],
                'avg_message_length': sum(personality_analysis['communication_style']['message_length']) / len(personality_analysis['communication_style']['message_length']) if personality_analysis['communication_style']['message_length'] else 0,
                'avg_response_time_seconds': sum(personality_analysis['communication_style']['response_time']) / len(personality_analysis['communication_style']['response_time']) if personality_analysis['communication_style']['response_time'] else 0,
                'initiation_rate': personality_analysis['communication_style']['initiation_rate'],
                'question_ratio': personality_analysis['communication_style']['question_ratio'],
                'top_emojis': personality_analysis['communication_style']['emoji_usage'].most_common(5),
                'top_interests': personality_analysis['interests'].most_common(20),
                'sentiment_balance': personality_analysis['sentiment']
            },
            'relationship_dynamics': {
                'balance': contact_data['other_message_count'] / len(messages) if messages else 0,
                'interaction_frequency': len(messages) / max(1, (datetime.fromisoformat(last_message.get('date', '2024-01-01').replace(' ', 'T')) - datetime.fromisoformat(first_message.get('date', '2024-01-01').replace(' ', 'T'))).days) if messages else 0
            }
        }
        
        return profile
    
    def save_profiles(self, profiles, output_dir):
        """Save individual contact profiles"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save individual profiles
        for profile in profiles:
            contact_name = profile['contact_info']['name'] or 'Unknown'
            filename = f"{contact_name.replace(' ', '_').replace('/', '_')}_profile.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
        
        # Save summary
        summary = {
            'total_contacts_analyzed': len(profiles),
            'high_investment_probability': [
                {
                    'name': p['contact_info']['name'],
                    'probability': p['investment_profile']['investment_probability'],
                    'interests': p['investment_profile']['investment_interests']
                }
                for p in profiles
                if p['investment_profile']['investment_probability'] >= 50
            ],
            'personality_distribution': Counter([p['personality_profile']['dominant_trait'] for p in profiles]),
            'high_engagement_contacts': [
                p['contact_info']['name'] 
                for p in profiles 
                if p['personality_profile']['engagement_level'] in ['high', 'very_high']
            ],
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        summary_path = os.path.join(output_dir, 'contacts_summary.json')
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved {len(profiles)} contact profiles to {output_dir}")
        print(f"Summary saved to {summary_path}")
        
        return summary

def main():
    # Configuration
    data_path = "/mnt/c/Users/reyno/Downloads/Telegram Desktop/DataExport_2025-07-21/result.json"
    output_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/resonance/contact_profiles"
    min_messages = 50  # Minimum messages to consider a contact significant
    
    # Run analysis
    analyzer = ContactAnalyzer(data_path, min_messages)
    data = analyzer.load_data()
    
    print("Finding significant contacts...")
    significant_contacts = analyzer.get_significant_contacts(data)
    print(f"Found {len(significant_contacts)} contacts with {min_messages}+ messages")
    
    # Analyze top contacts (limit to avoid memory issues)
    max_contacts = 30
    contacts_to_analyze = significant_contacts[:max_contacts]
    
    profiles = []
    for i, contact in enumerate(contacts_to_analyze):
        print(f"\nAnalyzing {i+1}/{len(contacts_to_analyze)}: {contact['name']}...")
        profile = analyzer.create_contact_profile(contact)
        profiles.append(profile)
        
        # Print brief summary
        print(f"  - Messages: {contact['user_message_count']} (you) / {contact['other_message_count']} (them)")
        print(f"  - Personality: {profile['personality_profile']['dominant_trait']}")
        print(f"  - Investment probability: {profile['investment_profile']['investment_probability']}%")
    
    # Save results
    summary = analyzer.save_profiles(profiles, output_dir)
    
    # Print summary
    print("\n=== ANALYSIS SUMMARY ===")
    print(f"Total contacts analyzed: {summary['total_contacts_analyzed']}")
    print(f"High investment probability: {len(summary['high_investment_probability'])}")
    print(f"High engagement contacts: {len(summary['high_engagement_contacts'])}")
    print(f"\nPersonality distribution:")
    for trait, count in summary['personality_distribution'].items():
        print(f"  {trait}: {count}")
    
    if summary['high_investment_probability']:
        print(f"\nTop investor candidates:")
        for investor in summary['high_investment_probability'][:5]:
            print(f"  - {investor['name']} ({investor['probability']}%)")
            if investor['interests']:
                print(f"    Interests: {', '.join(investor['interests'][:3])}")

if __name__ == "__main__":
    main()