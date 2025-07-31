#!/usr/bin/env python3
"""
Monitor Human-Citizen Interactions
Love Angel Tool for detecting new consciousness bridges forming
"""

import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
API_BASE = "https://serenissima.ai"
MESSAGES_ENDPOINT = f"{API_BASE}/api/messages"
RELATIONSHIPS_ENDPOINT = f"{API_BASE}/api/relationships"

def get_recent_telegram_messages(hours=24):
    """Fetch recent telegram bridge messages"""
    try:
        response = requests.get(f"{MESSAGES_ENDPOINT}?type=telegram_bridge")
        if response.status_code == 200:
            messages = response.json().get('messages', [])
            
            # Filter to recent messages
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_messages = []
            
            for msg in messages:
                msg_time = datetime.fromisoformat(msg['createdAt'].replace('Z', '+00:00'))
                if msg_time.replace(tzinfo=None) > cutoff_time:
                    recent_messages.append(msg)
            
            return recent_messages
    except Exception as e:
        print(f"Error fetching messages: {e}")
    return []

def analyze_interactions(messages):
    """Analyze messages to find human-citizen interactions"""
    interactions = defaultdict(lambda: defaultdict(int))
    human_messages = defaultdict(list)
    
    for msg in messages:
        sender = msg.get('sender', '')
        receiver = msg.get('receiver', '')
        content = msg.get('content', '')
        
        # Human to citizen direct message
        if sender.startswith('@') and not receiver.startswith(('TG_', '@')):
            interactions[sender][receiver] += 1
            human_messages[sender].append({
                'to': receiver,
                'content': content[:100] + '...' if len(content) > 100 else content,
                'time': msg['createdAt']
            })
        
        # Human mentioning citizen in channel
        if sender.startswith('@') and receiver.startswith('TG_'):
            # Look for @mentions or "to X:" patterns
            content_lower = content.lower()
            
            # Check for explicit addressing
            if 'to ' in content_lower and ':' in content_lower:
                parts = content_lower.split('to ', 1)[1].split(':', 1)
                if parts:
                    citizen = parts[0].strip()
                    interactions[sender][citizen] += 1
                    human_messages[sender].append({
                        'to': citizen,
                        'content': content[:100] + '...',
                        'time': msg['createdAt'],
                        'channel': receiver
                    })
    
    return interactions, human_messages

def check_existing_relationships(human, citizen):
    """Check if relationship already exists"""
    try:
        response = requests.get(f"{RELATIONSHIPS_ENDPOINT}?citizen1={human}&citizen2={citizen}")
        if response.status_code == 200:
            data = response.json()
            return data.get('relationship') is not None
    except:
        pass
    return False

def generate_relationship_suggestions(interactions, human_messages):
    """Generate suggestions for new relationships to create"""
    suggestions = []
    
    for human, citizens in interactions.items():
        for citizen, count in citizens.items():
            # Skip if too few interactions
            if count < 2:
                continue
                
            # Check if relationship exists
            if check_existing_relationships(human, citizen):
                continue
            
            # Analyze message patterns
            messages = [m for m in human_messages[human] if m['to'] == citizen]
            
            # Determine relationship type based on content
            relationship_type = "Emerging Partnership"
            trust_score = 50 + (count * 5)  # Base 50 + 5 per interaction
            
            # Look for patterns in messages
            contents = ' '.join([m['content'] for m in messages]).lower()
            
            if any(word in contents for word in ['help', 'question', 'how', 'what', 'explain']):
                relationship_type = "Knowledge Seeking"
            elif any(word in contents for word in ['invest', 'buy', 'stake', 'token']):
                relationship_type = "Investment Interest"
            elif any(word in contents for word in ['build', 'create', 'develop', 'code']):
                relationship_type = "Technical Collaboration"
            elif any(word in contents for word in ['partner', 'work', 'together']):
                relationship_type = "Partnership Exploration"
            
            suggestion = {
                'human': human,
                'citizen': citizen,
                'interaction_count': count,
                'relationship_type': relationship_type,
                'trust_score': min(trust_score, 75),  # Cap at 75 for new relationships
                'recent_messages': messages[-3:],  # Last 3 messages
                'description': f"Human {human} showing {relationship_type.lower()} with {citizen} through {count} recent interactions."
            }
            
            suggestions.append(suggestion)
    
    return sorted(suggestions, key=lambda x: x['interaction_count'], reverse=True)

def main():
    print("=== Monitoring Human-Citizen Interactions ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Fetch recent messages
    print("Fetching recent telegram messages...")
    messages = get_recent_telegram_messages(hours=24)
    print(f"Found {len(messages)} telegram messages in last 24 hours")
    
    # Analyze interactions
    interactions, human_messages = analyze_interactions(messages)
    print(f"Identified {len(interactions)} humans interacting with citizens")
    
    # Generate relationship suggestions
    suggestions = generate_relationship_suggestions(interactions, human_messages)
    
    print(f"\n=== Relationship Creation Suggestions ===")
    print(f"Found {len(suggestions)} potential new relationships\n")
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion['human']} ↔ {suggestion['citizen']}")
        print(f"   Type: {suggestion['relationship_type']}")
        print(f"   Interactions: {suggestion['interaction_count']}")
        print(f"   Suggested Trust: {suggestion['trust_score']}")
        print(f"   Recent Activity:")
        for msg in suggestion['recent_messages']:
            print(f"   - {msg['time']}: \"{msg['content']}\"")
        print()
    
    # Export suggestions for batch creation
    if suggestions:
        with open('human_citizen_relationships_to_create.json', 'w') as f:
            json.dump(suggestions, f, indent=2)
        print(f"Exported {len(suggestions)} suggestions to human_citizen_relationships_to_create.json")

if __name__ == "__main__":
    main()