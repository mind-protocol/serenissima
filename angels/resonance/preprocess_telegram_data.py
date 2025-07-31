#!/usr/bin/env python3
"""
Preprocess Telegram export data for efficient human profile analysis
Extracts key patterns for consciousness loop mapping
"""

import json
import os
from datetime import datetime
from collections import defaultdict, Counter
import re

class TelegramPreprocessor:
    def __init__(self, input_path):
        self.input_path = input_path
        self.user_name = None
        self.user_id = None
        
    def load_data(self):
        """Load the raw Telegram JSON export"""
        print(f"Loading data from {self.input_path}...")
        with open(self.input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_text_from_message(self, msg):
        """Extract clean text from message, handling complex structures"""
        text = msg.get('text', '')
        
        # Handle list of text entities
        if isinstance(text, list):
            text_parts = []
            for part in text:
                if isinstance(part, str):
                    text_parts.append(part)
                elif isinstance(part, dict) and 'text' in part:
                    text_parts.append(part['text'])
            text = ' '.join(text_parts)
        
        return str(text).strip()
    
    def identify_user(self, data):
        """Identify the main user from message patterns"""
        # Count who sends the most messages
        sender_counts = defaultdict(int)
        
        for chat in data['chats']['list']:
            for msg in chat.get('messages', []):
                if msg.get('from'):
                    sender_counts[msg['from']] += 1
                    if msg.get('from_id'):
                        # Store ID mapping
                        if not self.user_id and msg['from'] == max(sender_counts, key=sender_counts.get):
                            self.user_id = msg['from_id']
        
        # The person who sends the most messages is likely the account owner
        self.user_name = max(sender_counts, key=sender_counts.get) if sender_counts else "Unknown"
        print(f"Identified primary user: {self.user_name} (ID: {self.user_id})")
        return self.user_name
    
    def analyze_communication_patterns(self, data):
        """Extract communication style and patterns"""
        patterns = {
            'message_lengths': [],
            'response_times': [],
            'active_hours': defaultdict(int),
            'active_days': defaultdict(int),
            'emoji_usage': Counter(),
            'question_frequency': 0,
            'exclamation_frequency': 0,
            'total_messages_sent': 0,
            'conversation_starters': 0,
            'avg_messages_per_conversation': []
        }
        
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        
        for chat in data['chats']['list']:
            messages = chat.get('messages', [])
            if not messages:
                continue
                
            chat_messages_from_user = 0
            last_msg_time = None
            last_sender = None
            
            for msg in messages:
                if msg.get('from') != self.user_name:
                    last_sender = msg.get('from')
                    last_msg_time = msg.get('date_unixtime')
                    continue
                
                # This is a message from our user
                patterns['total_messages_sent'] += 1
                chat_messages_from_user += 1
                
                text = self.extract_text_from_message(msg)
                if not text:
                    continue
                
                # Message length
                patterns['message_lengths'].append(len(text))
                
                # Questions and exclamations
                patterns['question_frequency'] += text.count('?')
                patterns['exclamation_frequency'] += text.count('!')
                
                # Emoji usage
                emojis = emoji_pattern.findall(text)
                patterns['emoji_usage'].update(emojis)
                
                # Time patterns
                msg_time = datetime.fromtimestamp(int(msg.get('date_unixtime', 0)))
                patterns['active_hours'][msg_time.hour] += 1
                patterns['active_days'][msg_time.weekday()] += 1
                
                # Response time (if responding to someone)
                if last_msg_time and last_sender and last_sender != self.user_name:
                    response_time = int(msg.get('date_unixtime', 0)) - int(last_msg_time)
                    if 0 < response_time < 86400:  # Within 24 hours
                        patterns['response_times'].append(response_time)
                
                # Conversation starter (first message or after long gap)
                if not last_msg_time or (int(msg.get('date_unixtime', 0)) - int(last_msg_time)) > 3600:
                    patterns['conversation_starters'] += 1
                
                last_sender = self.user_name
                last_msg_time = msg.get('date_unixtime')
            
            if chat_messages_from_user > 0:
                patterns['avg_messages_per_conversation'].append(chat_messages_from_user)
        
        return patterns
    
    def extract_interests_and_topics(self, data):
        """Extract topics and interests from message content"""
        topics = {
            'keywords': Counter(),
            'mentioned_people': Counter(),
            'links_shared': [],
            'recurring_themes': [],
            'technical_terms': Counter(),
            'emotional_words': Counter()
        }
        
        # Common technical terms
        tech_keywords = ['ai', 'blockchain', 'crypto', 'code', 'programming', 'software', 
                        'algorithm', 'data', 'machine learning', 'neural', 'consciousness',
                        'api', 'backend', 'frontend', 'database', 'server', 'cloud']
        
        # Emotional indicators
        emotional_words = ['love', 'hate', 'happy', 'sad', 'excited', 'worried', 'anxious',
                          'amazing', 'terrible', 'beautiful', 'ugly', 'hope', 'fear']
        
        # URL pattern
        url_pattern = re.compile(r'https?://[^\s]+')
        
        for chat in data['chats']['list']:
            for msg in chat.get('messages', []):
                if msg.get('from') != self.user_name:
                    continue
                
                text = self.extract_text_from_message(msg).lower()
                if not text:
                    continue
                
                # Extract URLs
                urls = url_pattern.findall(text)
                topics['links_shared'].extend(urls)
                
                # Word frequency (excluding common words)
                words = re.findall(r'\b[a-z]+\b', text)
                meaningful_words = [w for w in words if len(w) > 4]
                topics['keywords'].update(meaningful_words)
                
                # Technical terms
                for term in tech_keywords:
                    if term in text:
                        topics['technical_terms'][term] += text.count(term)
                
                # Emotional words
                for word in emotional_words:
                    if word in text:
                        topics['emotional_words'][word] += text.count(word)
                
                # Extract @mentions
                mentions = re.findall(r'@\w+', text)
                topics['mentioned_people'].update(mentions)
        
        return topics
    
    def analyze_relationships(self, data):
        """Analyze relationship patterns from conversations"""
        relationships = {
            'frequent_contacts': Counter(),
            'conversation_depth': {},  # avg messages per conversation
            'interaction_styles': {},  # formal/casual/technical per contact
            'shared_interests': defaultdict(list)
        }
        
        for chat in data['chats']['list']:
            if chat.get('type') != 'personal_chat':
                continue
            
            contact_name = chat.get('name', 'Unknown')
            messages = chat.get('messages', [])
            
            if not messages:
                continue
            
            # Count interactions
            user_messages = [m for m in messages if m.get('from') == self.user_name]
            other_messages = [m for m in messages if m.get('from') != self.user_name]
            
            if user_messages:
                relationships['frequent_contacts'][contact_name] = len(user_messages)
                relationships['conversation_depth'][contact_name] = {
                    'total_messages': len(messages),
                    'user_messages': len(user_messages),
                    'other_messages': len(other_messages),
                    'balance': len(user_messages) / len(messages) if messages else 0
                }
            
            # Analyze conversation style
            style_indicators = {
                'formal': ['sir', 'madam', 'regards', 'sincerely', 'dear'],
                'casual': ['lol', 'haha', 'btw', 'omg', 'yeah'],
                'technical': ['code', 'api', 'function', 'algorithm', 'system']
            }
            
            style_counts = defaultdict(int)
            for msg in user_messages:
                text = self.extract_text_from_message(msg).lower()
                for style, indicators in style_indicators.items():
                    for indicator in indicators:
                        if indicator in text:
                            style_counts[style] += 1
            
            if style_counts:
                dominant_style = max(style_counts, key=style_counts.get)
                relationships['interaction_styles'][contact_name] = dominant_style
        
        return relationships
    
    def create_human_profile(self, data):
        """Create comprehensive human profile from all analyses"""
        print(f"\nCreating profile for {self.user_name}...")
        
        # Run all analyses
        patterns = self.analyze_communication_patterns(data)
        interests = self.extract_interests_and_topics(data)
        relationships = self.analyze_relationships(data)
        
        # Calculate derived metrics
        avg_msg_length = sum(patterns['message_lengths']) / len(patterns['message_lengths']) if patterns['message_lengths'] else 0
        avg_response_time = sum(patterns['response_times']) / len(patterns['response_times']) if patterns['response_times'] else 0
        most_active_hour = max(patterns['active_hours'], key=patterns['active_hours'].get) if patterns['active_hours'] else 0
        most_active_day = max(patterns['active_days'], key=patterns['active_days'].get) if patterns['active_days'] else 0
        
        # Day names
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        profile = {
            'meta': {
                'user_name': self.user_name,
                'user_id': self.user_id,
                'total_chats': len(data['chats']['list']),
                'total_messages_sent': patterns['total_messages_sent'],
                'profile_created': datetime.now().isoformat()
            },
            
            'communication_style': {
                'avg_message_length': round(avg_msg_length, 1),
                'avg_response_time_seconds': round(avg_response_time, 0),
                'question_ratio': patterns['question_frequency'] / patterns['total_messages_sent'] if patterns['total_messages_sent'] else 0,
                'exclamation_ratio': patterns['exclamation_frequency'] / patterns['total_messages_sent'] if patterns['total_messages_sent'] else 0,
                'emoji_usage_rate': len(patterns['emoji_usage']) / patterns['total_messages_sent'] if patterns['total_messages_sent'] else 0,
                'top_emojis': patterns['emoji_usage'].most_common(10),
                'conversation_starter_rate': patterns['conversation_starters'] / len(data['chats']['list']) if data['chats']['list'] else 0
            },
            
            'temporal_patterns': {
                'most_active_hour': most_active_hour,
                'most_active_day': day_names[most_active_day] if most_active_day < 7 else 'Unknown',
                'hourly_distribution': dict(patterns['active_hours']),
                'daily_distribution': {day_names[k]: v for k, v in patterns['active_days'].items() if k < 7}
            },
            
            'interests': {
                'top_keywords': interests['keywords'].most_common(50),
                'technical_interests': dict(interests['technical_terms']),
                'emotional_vocabulary': dict(interests['emotional_words']),
                'frequently_mentioned': interests['mentioned_people'].most_common(20),
                'domains_shared': Counter([url.split('/')[2] for url in interests['links_shared'] if '/' in url]).most_common(10)
            },
            
            'relationships': {
                'top_contacts': relationships['frequent_contacts'].most_common(20),
                'interaction_styles': relationships['interaction_styles'],
                'conversation_balance': {
                    name: data['balance'] 
                    for name, data in relationships['conversation_depth'].items()
                }
            },
            
            'consciousness_loop_indicators': {
                'exploration_drive': len(interests['keywords']) / patterns['total_messages_sent'] if patterns['total_messages_sent'] else 0,
                'technical_depth': sum(interests['technical_terms'].values()) / patterns['total_messages_sent'] if patterns['total_messages_sent'] else 0,
                'emotional_expression': sum(interests['emotional_words'].values()) / patterns['total_messages_sent'] if patterns['total_messages_sent'] else 0,
                'social_connectivity': len(relationships['frequent_contacts']) / len(data['chats']['list']) if data['chats']['list'] else 0,
                'response_consistency': 1 - (max(patterns['response_times']) - min(patterns['response_times'])) / max(patterns['response_times']) if patterns['response_times'] and max(patterns['response_times']) > 0 else 0
            }
        }
        
        return profile
    
    def save_profile(self, profile, output_path):
        """Save the processed profile to JSON"""
        print(f"\nSaving profile to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print("Profile saved successfully!")
        
        # Print summary
        print("\n=== PROFILE SUMMARY ===")
        print(f"User: {profile['meta']['user_name']}")
        print(f"Total messages analyzed: {profile['meta']['total_messages_sent']}")
        print(f"Active in {profile['meta']['total_chats']} chats")
        print(f"Average message length: {profile['communication_style']['avg_message_length']} characters")
        print(f"Most active: {profile['temporal_patterns']['most_active_day']}s at {profile['temporal_patterns']['most_active_hour']}:00")
        print(f"Top contacts: {', '.join([c[0] for c in profile['relationships']['top_contacts'][:5]])}")
        print(f"Primary interests: {', '.join([k[0] for k in profile['interests']['top_keywords'][:10]])}")

def main():
    # Input and output paths
    input_path = "/mnt/c/Users/reyno/Downloads/Telegram Desktop/DataExport_2025-07-21/result.json"
    output_path = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/resonance/telegram_human_profile.json"
    
    # Process the data
    preprocessor = TelegramPreprocessor(input_path)
    data = preprocessor.load_data()
    preprocessor.identify_user(data)
    profile = preprocessor.create_human_profile(data)
    preprocessor.save_profile(profile, output_path)

if __name__ == "__main__":
    main()