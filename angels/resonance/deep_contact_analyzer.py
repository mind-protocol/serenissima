#!/usr/bin/env python3
"""
Deep conversation analysis for key contacts
Reads full message threads and builds comprehensive profiles
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
import subprocess
import time

class DeepContactAnalyzer:
    def __init__(self, telegram_data_path):
        self.data_path = telegram_data_path
        self.user_name = "NLR - Founder @ Universe Engine"
        self.analysis_output_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/resonance/deep_profiles"
        
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
    
    def select_interesting_contacts(self, data):
        """Select contacts based on engagement quality and recency"""
        contact_scores = []
        
        for chat in data['chats']['list']:
            if chat.get('type') != 'personal_chat':
                continue
                
            messages = chat.get('messages', [])
            if len(messages) < 20:  # Minimum threshold
                continue
            
            # Calculate engagement metrics
            recent_messages = 0
            investment_mentions = 0
            message_lengths = []
            last_message_date = None
            
            for msg in messages[-100:]:  # Last 100 messages
                text = self.extract_text(msg).lower()
                msg_date = datetime.fromisoformat(msg.get('date', '2020-01-01').replace(' ', 'T'))
                
                # Recent activity (last 6 months)
                if msg_date > datetime.now() - timedelta(days=180):
                    recent_messages += 1
                
                # Investment/business indicators
                if any(word in text for word in ['invest', 'fund', 'capital', 'business', 'build', 'project']):
                    investment_mentions += 1
                
                # Message quality
                if msg.get('from') != self.user_name:
                    message_lengths.append(len(text))
                
                if not last_message_date or msg_date > last_message_date:
                    last_message_date = msg_date
            
            # Calculate score
            score = 0
            
            # Recency score
            if last_message_date:
                days_since_last = (datetime.now() - last_message_date).days
                if days_since_last < 30:
                    score += 40
                elif days_since_last < 90:
                    score += 20
                elif days_since_last < 180:
                    score += 10
            
            # Engagement depth
            avg_msg_length = sum(message_lengths) / len(message_lengths) if message_lengths else 0
            if avg_msg_length > 100:
                score += 30
            elif avg_msg_length > 50:
                score += 15
            
            # Business relevance
            if investment_mentions > 5:
                score += 30
            elif investment_mentions > 2:
                score += 15
            
            # Message volume
            if len(messages) > 500:
                score += 20
            elif len(messages) > 200:
                score += 10
            
            contact_scores.append({
                'name': chat.get('name', 'Unknown'),
                'chat': chat,
                'score': score,
                'total_messages': len(messages),
                'recent_messages': recent_messages,
                'investment_mentions': investment_mentions,
                'avg_message_length': avg_msg_length,
                'last_message_date': last_message_date
            })
        
        # Sort by score and return top contacts
        contact_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Print selection summary
        print("\n=== CONTACT SELECTION ===")
        print(f"Total contacts evaluated: {len(contact_scores)}")
        print("\nTop 15 contacts by score:")
        for i, contact in enumerate(contact_scores[:15]):
            print(f"{i+1}. {contact['name']}: Score {contact['score']}")
            print(f"   Messages: {contact['total_messages']} (Recent: {contact['recent_messages']})")
            print(f"   Investment mentions: {contact['investment_mentions']}")
            print(f"   Last contact: {contact['last_message_date'].strftime('%Y-%m-%d') if contact['last_message_date'] else 'Unknown'}")
        
        return contact_scores[:15]  # Return top 15
    
    def analyze_with_claude(self, contact_data):
        """Use Claude to deeply analyze a contact's conversation"""
        messages = contact_data['chat']['messages']
        contact_name = contact_data['name']
        
        # Prepare conversation for analysis
        conversation_text = self.prepare_conversation_text(messages, contact_name)
        
        # Create analysis prompt
        prompt = f"""Analyze this conversation between NLR (founder of Universe Engine/Venice AI society) and {contact_name}.

CONVERSATION:
{conversation_text}

Please provide a comprehensive analysis including:

1. CONTACT PROFILE
- Professional background and expertise
- Current role/company if mentioned
- Key interests and focus areas
- Communication style and personality traits

2. INVESTMENT POTENTIAL
- Likelihood of investing in Venice/Universe Engine (0-100%)
- Probable ticket size based on conversation context
- Investment stage preference (seed/Series A/etc)
- Specific investment interests mentioned

3. PERSONALITY ANALYSIS
- Core personality traits
- Communication preferences
- Decision-making style
- Relationship building approach

4. PARTNERSHIP OPPORTUNITIES
- Potential synergies with Venice companies
- Specific skills or resources they could contribute
- Business development opportunities
- Strategic value beyond investment

5. CITIZEN MATCHING
- Which Venice citizen would be the best match and why
- Shared interests and complementary skills
- Potential collaboration areas

6. ENGAGEMENT STRATEGY
- Recommended approach angle
- Key topics to emphasize
- First message draft (2-3 sentences)
- Follow-up strategy

Format your response as JSON for easy parsing."""

        # Save prompt to file for Claude to analyze
        prompt_file = f"/tmp/analyze_{contact_name.replace(' ', '_')}.txt"
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        # Call Claude via subprocess (using sonnet model)
        try:
            result = subprocess.run([
                'claude', 
                f'--model', 'sonnet',
                f'< {prompt_file}'
            ], capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                # Parse Claude's response
                response = result.stdout.strip()
                
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                else:
                    # Fallback: create structured data from text response
                    analysis = self.parse_text_response(response, contact_name)
                
                return analysis
            else:
                print(f"Error analyzing {contact_name}: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Exception analyzing {contact_name}: {e}")
            return None
        
        finally:
            # Clean up temp file
            if os.path.exists(prompt_file):
                os.remove(prompt_file)
    
    def prepare_conversation_text(self, messages, contact_name, max_messages=200):
        """Prepare conversation text for analysis"""
        # Get recent messages (last 200 or 6 months)
        cutoff_date = datetime.now() - timedelta(days=180)
        recent_messages = []
        
        for msg in messages:
            msg_date = datetime.fromisoformat(msg.get('date', '2020-01-01').replace(' ', 'T'))
            if msg_date > cutoff_date:
                recent_messages.append(msg)
        
        # Limit to max_messages most recent
        recent_messages = recent_messages[-max_messages:]
        
        # Format conversation
        conversation_lines = []
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
            
            conversation_lines.append(f"[{date}] {sender}: {text}")
        
        return "\n".join(conversation_lines)
    
    def parse_text_response(self, response, contact_name):
        """Fallback parser for non-JSON Claude responses"""
        # This is a simplified parser - would need enhancement for production
        analysis = {
            "contact_profile": {
                "name": contact_name,
                "background": "Analysis pending",
                "expertise": [],
                "interests": []
            },
            "investment_potential": {
                "likelihood": 50,
                "ticket_size": "Unknown",
                "stage": "Unknown",
                "interests": []
            },
            "personality": {
                "traits": [],
                "communication_style": "Unknown",
                "decision_style": "Unknown"
            },
            "partnerships": {
                "synergies": [],
                "contributions": [],
                "opportunities": []
            },
            "citizen_match": {
                "best_match": "Unknown",
                "reason": "Analysis pending"
            },
            "engagement": {
                "approach": "Professional and friendly",
                "topics": [],
                "first_message": "Hi, following up on our conversation about Venice.",
                "strategy": "Build on existing relationship"
            }
        }
        
        # Try to extract some basic info from response text
        # (This would need more sophisticated parsing in production)
        
        return analysis
    
    def save_analysis(self, contact_name, analysis):
        """Save individual contact analysis"""
        os.makedirs(self.analysis_output_dir, exist_ok=True)
        
        filename = f"{contact_name.replace(' ', '_').replace('/', '_')}_deep_analysis.json"
        filepath = os.path.join(self.analysis_output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"Saved analysis for {contact_name}")
        return filepath
    
    def create_summary_report(self, all_analyses):
        """Create a summary report of all analyses"""
        summary = {
            "analysis_date": datetime.now().isoformat(),
            "total_contacts_analyzed": len(all_analyses),
            "high_value_investors": [],
            "partnership_opportunities": [],
            "citizen_matches": [],
            "engagement_priorities": []
        }
        
        for analysis in all_analyses:
            if not analysis or 'investment_potential' not in analysis:
                continue
            
            # High value investors (70%+ likelihood)
            if analysis['investment_potential'].get('likelihood', 0) >= 70:
                summary['high_value_investors'].append({
                    'name': analysis['contact_profile']['name'],
                    'likelihood': analysis['investment_potential']['likelihood'],
                    'ticket_size': analysis['investment_potential'].get('ticket_size', 'Unknown'),
                    'interests': analysis['investment_potential'].get('interests', [])
                })
            
            # Partnership opportunities
            if analysis['partnerships'].get('opportunities'):
                summary['partnership_opportunities'].append({
                    'name': analysis['contact_profile']['name'],
                    'opportunities': analysis['partnerships']['opportunities']
                })
            
            # Citizen matches
            if analysis['citizen_match'].get('best_match') != 'Unknown':
                summary['citizen_matches'].append({
                    'human': analysis['contact_profile']['name'],
                    'citizen': analysis['citizen_match']['best_match'],
                    'reason': analysis['citizen_match'].get('reason', '')
                })
            
            # Engagement priorities
            summary['engagement_priorities'].append({
                'name': analysis['contact_profile']['name'],
                'approach': analysis['engagement'].get('approach', ''),
                'first_message': analysis['engagement'].get('first_message', '')
            })
        
        # Save summary
        summary_path = os.path.join(self.analysis_output_dir, 'analysis_summary.json')
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return summary

def main():
    # Initialize analyzer
    data_path = "/mnt/c/Users/reyno/Downloads/Telegram Desktop/DataExport_2025-07-21/result.json"
    analyzer = DeepContactAnalyzer(data_path)
    
    print("Loading Telegram data...")
    data = analyzer.load_data()
    
    print("Selecting interesting contacts...")
    selected_contacts = analyzer.select_interesting_contacts(data)
    
    print(f"\nWill analyze {len(selected_contacts)} contacts with Claude...")
    print("This may take several minutes...\n")
    
    # Analyze each contact
    all_analyses = []
    for i, contact in enumerate(selected_contacts):
        print(f"\nAnalyzing {i+1}/{len(selected_contacts)}: {contact['name']}...")
        
        analysis = analyzer.analyze_with_claude(contact)
        if analysis:
            analyzer.save_analysis(contact['name'], analysis)
            all_analyses.append(analysis)
        
        # Rate limiting to avoid overwhelming Claude
        if i < len(selected_contacts) - 1:
            time.sleep(2)
    
    # Create summary report
    print("\nCreating summary report...")
    summary = analyzer.create_summary_report(all_analyses)
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Analyzed {len(all_analyses)} contacts")
    print(f"Results saved to: {analyzer.analysis_output_dir}")
    print(f"\nHigh-value investors identified: {len(summary['high_value_investors'])}")
    print(f"Partnership opportunities: {len(summary['partnership_opportunities'])}")
    print(f"Citizen matches proposed: {len(summary['citizen_matches'])}")

if __name__ == "__main__":
    main()