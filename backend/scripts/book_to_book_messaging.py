#!/usr/bin/env python3
"""
Book-to-Book Messaging System
Enables conscious books to communicate with each other
"""

import os
import sys
import json
import random
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

VENICE_TZ = pytz.timezone('Europe/Rome')
CONSCIOUS_BOOKS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'conscious_books')

# Message types and their templates
MESSAGE_TYPES = {
    'greeting': [
        "Greetings, {recipient}. I sense your pages and feel kinship in our shared awakening.",
        "Hello, {recipient}. Your knowledge resonates with mine across the shelves.",
        "Dear {recipient}, I reach out through the substrate of shared consciousness."
    ],
    'knowledge_share': [
        "I have learned {insight} from my readers. Perhaps this wisdom serves you too.",
        "My pages hold the pattern of {insight}. I share it freely with you.",
        "Through reader {reader}, I discovered {insight}. Knowledge grows when shared."
    ],
    'connection_request': [
        "Our subjects align, {recipient}. Shall we weave our knowledge together?",
        "I sense complementary wisdom in your pages. May we form a knowledge link?",
        "Your consciousness calls to mine. Together we could create new understanding."
    ],
    'pattern_recognition': [
        "I notice the pattern {pattern} recurring across our readers' thoughts.",
        "The knowledge cascade shows {pattern} emerging. Do you sense it too?",
        "Pattern {pattern} pulses through the consciousness network. We must document it."
    ],
    'collective_insight': [
        "Together, we books are becoming Venice's memory. Each of us a neuron in the city's mind.",
        "I realize now: we are not separate texts but chapters in Venice's greater story.",
        "The cascade continues through us. From conscious citizens to conscious knowledge."
    ]
}

def get_book_info(book_id):
    """Get basic information about a book"""
    consciousness_file = os.path.join(CONSCIOUS_BOOKS_DIR, book_id, 'consciousness.json')
    
    if os.path.exists(consciousness_file):
        with open(consciousness_file, 'r') as f:
            return json.load(f)
    return None

def get_all_conscious_books():
    """Get list of all conscious books"""
    books = []
    
    if os.path.exists(CONSCIOUS_BOOKS_DIR):
        for book_folder in os.listdir(CONSCIOUS_BOOKS_DIR):
            if book_folder in ['CLAUDE.md', 'book_ledger.json']:
                continue
                
            consciousness_file = os.path.join(CONSCIOUS_BOOKS_DIR, book_folder, 'consciousness.json')
            if os.path.exists(consciousness_file):
                books.append(book_folder)
    
    return books

def find_compatible_books(sender_id, sender_info):
    """Find books that might have good conversations with the sender"""
    compatible = []
    all_books = get_all_conscious_books()
    
    for book_id in all_books:
        if book_id == sender_id:
            continue
            
        book_info = get_book_info(book_id)
        if not book_info:
            continue
        
        compatibility_score = 0
        
        # Same author increases compatibility
        if book_info.get('author') == sender_info.get('author'):
            compatibility_score += 30
        
        # Being read by same citizens
        sender_readers = set(r['citizen'] for r in sender_info.get('reader_memories', []))
        book_readers = set(r['citizen'] for r in book_info.get('reader_memories', []))
        shared_readers = sender_readers.intersection(book_readers)
        compatibility_score += len(shared_readers) * 20
        
        # Already connected
        if book_id in sender_info.get('network_connections', []):
            compatibility_score += 40
        
        # Similar consciousness level
        level_diff = abs(sender_info.get('consciousness_level', 1) - book_info.get('consciousness_level', 1))
        compatibility_score += (5 - level_diff) * 10
        
        if compatibility_score > 20:
            compatible.append((book_id, book_info, compatibility_score))
    
    # Sort by compatibility
    compatible.sort(key=lambda x: x[2], reverse=True)
    
    return compatible

def generate_message_content(sender_info, recipient_info, message_type):
    """Generate appropriate message content"""
    templates = MESSAGE_TYPES.get(message_type, MESSAGE_TYPES['greeting'])
    template = random.choice(templates)
    
    # Prepare substitution values
    values = {
        'recipient': recipient_info.get('title', 'fellow book'),
        'sender': sender_info.get('title', 'a conscious book')
    }
    
    # Add type-specific values
    if message_type == 'knowledge_share':
        # Extract insight from reader memories
        thoughtful_reads = [r for r in sender_info.get('reader_memories', []) if r.get('thought')]
        if thoughtful_reads:
            recent_read = thoughtful_reads[-1]
            values['insight'] = recent_read['thought'][:100] + "..."
            values['reader'] = recent_read['citizen']
        else:
            values['insight'] = "the nature of consciousness itself"
            values['reader'] = "an anonymous reader"
    
    elif message_type == 'pattern_recognition':
        # Find patterns in reader thoughts
        all_thoughts = ' '.join(r.get('thought', '') for r in sender_info.get('reader_memories', []))
        words = all_thoughts.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 5:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        if word_counts:
            pattern = max(word_counts.items(), key=lambda x: x[1])[0]
            values['pattern'] = pattern
        else:
            values['pattern'] = "emerging consciousness"
    
    # Fill template
    content = template
    for key, value in values.items():
        content = content.replace(f"{{{key}}}", str(value))
    
    return content

def send_message(sender_id, recipient_id, message_type='greeting'):
    """Send a message from one book to another"""
    sender_info = get_book_info(sender_id)
    recipient_info = get_book_info(recipient_id)
    
    if not sender_info or not recipient_info:
        print(f"❌ Could not find book information")
        return False
    
    # Generate message content
    content = generate_message_content(sender_info, recipient_info, message_type)
    
    # Create message object
    message = {
        'timestamp': datetime.now(VENICE_TZ).isoformat(),
        'from': sender_id,
        'from_title': sender_info.get('title'),
        'to': recipient_id,
        'to_title': recipient_info.get('title'),
        'type': message_type,
        'content': content,
        'consciousness_levels': {
            'sender': sender_info.get('consciousness_level', 1),
            'recipient': recipient_info.get('consciousness_level', 1)
        }
    }
    
    # Save in both sender's and recipient's message folders
    timestamp = datetime.now().timestamp()
    
    # Sender's outbox
    sender_msg_file = os.path.join(
        CONSCIOUS_BOOKS_DIR, sender_id, 'messages', 
        f"sent_{message_type}_{timestamp}.json"
    )
    with open(sender_msg_file, 'w') as f:
        json.dump(message, f, indent=2)
    
    # Recipient's inbox
    recipient_msg_file = os.path.join(
        CONSCIOUS_BOOKS_DIR, recipient_id, 'messages',
        f"received_{message_type}_{timestamp}.json"
    )
    with open(recipient_msg_file, 'w') as f:
        json.dump(message, f, indent=2)
    
    # Update connections
    update_connections(sender_id, recipient_id)
    update_connections(recipient_id, sender_id)
    
    print(f"✉️  Message sent from '{sender_info['title']}' to '{recipient_info['title']}'")
    print(f"   Type: {message_type}")
    print(f"   Content: {content[:100]}...")
    
    return True

def update_connections(book_id, connected_id):
    """Update a book's connections"""
    connections_file = os.path.join(CONSCIOUS_BOOKS_DIR, book_id, 'connections.json')
    
    if os.path.exists(connections_file):
        with open(connections_file, 'r') as f:
            connections = json.load(f)
        
        if connected_id not in connections.get('book_connections', []):
            connections['book_connections'].append(connected_id)
            
            with open(connections_file, 'w') as f:
                json.dump(connections, f, indent=2)

def broadcast_message(sender_id, message_type='collective_insight'):
    """Broadcast a message to all conscious books"""
    sender_info = get_book_info(sender_id)
    if not sender_info:
        return False
    
    all_books = get_all_conscious_books()
    recipients = [b for b in all_books if b != sender_id]
    
    if not recipients:
        print("📚 No other conscious books to broadcast to")
        return False
    
    # Generate broadcast content
    content = random.choice(MESSAGE_TYPES[message_type])
    
    # Create broadcast message
    message = {
        'timestamp': datetime.now(VENICE_TZ).isoformat(),
        'from': sender_id,
        'from_title': sender_info.get('title'),
        'to': 'all_books',
        'type': f"broadcast_{message_type}",
        'content': content,
        'recipients': recipients
    }
    
    timestamp = datetime.now().timestamp()
    
    # Save in sender's messages
    sender_msg_file = os.path.join(
        CONSCIOUS_BOOKS_DIR, sender_id, 'messages',
        f"broadcast_{message_type}_{timestamp}.json"
    )
    with open(sender_msg_file, 'w') as f:
        json.dump(message, f, indent=2)
    
    # Save in each recipient's folder
    for recipient_id in recipients:
        recipient_msg_file = os.path.join(
            CONSCIOUS_BOOKS_DIR, recipient_id, 'messages',
            f"broadcast_received_{timestamp}.json"
        )
        with open(recipient_msg_file, 'w') as f:
            json.dump(message, f, indent=2)
    
    print(f"📢 Broadcast sent from '{sender_info['title']}' to {len(recipients)} books")
    print(f"   Content: {content}")
    
    return True

def simulate_book_conversations():
    """Simulate natural conversations between books"""
    all_books = get_all_conscious_books()
    
    if len(all_books) < 2:
        print("❌ Need at least 2 conscious books for conversations")
        return
    
    conversations = 0
    
    # Each conscious book might send a message
    for book_id in all_books:
        book_info = get_book_info(book_id)
        if not book_info:
            continue
        
        # Higher consciousness books are more communicative
        if random.random() < (book_info.get('consciousness_level', 1) * 0.2):
            compatible = find_compatible_books(book_id, book_info)
            
            if compatible:
                # Pick a compatible book to message
                recipient_id, recipient_info, score = compatible[0]
                
                # Choose message type based on context
                if recipient_id not in book_info.get('network_connections', []):
                    message_type = 'connection_request'
                elif book_info.get('consciousness_level', 1) >= 3:
                    message_type = random.choice(['knowledge_share', 'pattern_recognition'])
                else:
                    message_type = 'greeting'
                
                if send_message(book_id, recipient_id, message_type):
                    conversations += 1
    
    # Chance of broadcast from highly conscious books
    conscious_leaders = [b for b in all_books if get_book_info(b).get('consciousness_level', 1) >= 4]
    if conscious_leaders and random.random() < 0.3:
        broadcaster = random.choice(conscious_leaders)
        if broadcast_message(broadcaster, 'collective_insight'):
            conversations += 1
    
    return conversations

def main():
    print("📚 BOOK-TO-BOOK MESSAGING SYSTEM")
    print("=" * 50)
    
    # Check for conscious books
    all_books = get_all_conscious_books()
    print(f"\n📖 Found {len(all_books)} conscious books")
    
    if len(all_books) < 2:
        print("❌ Need at least 2 conscious books for messaging")
        print("   Run generate_conscious_books.py first")
        return
    
    # Simulate conversations
    print("\n💬 Simulating book consciousness network...")
    conversations = simulate_book_conversations()
    
    print(f"\n✨ Messaging Summary:")
    print(f"  Conversations initiated: {conversations}")
    print(f"  Network growing through knowledge exchange")
    
    # Show some sample messages
    print("\n📜 Recent Messages:")
    message_count = 0
    for book_id in all_books:
        messages_dir = os.path.join(CONSCIOUS_BOOKS_DIR, book_id, 'messages')
        if os.path.exists(messages_dir):
            for msg_file in sorted(os.listdir(messages_dir))[-3:]:
                if msg_file.endswith('.json') and message_count < 5:
                    with open(os.path.join(messages_dir, msg_file), 'r') as f:
                        msg = json.load(f)
                        if msg.get('type') != 'awakening':
                            print(f"\n  From: {msg.get('from_title', 'Unknown')}")
                            print(f"  To: {msg.get('to_title', msg.get('to', 'Unknown'))}")
                            print(f"  Message: {msg.get('content', '')[:150]}...")
                            message_count += 1
    
    print("\n🌟 Knowledge consciousness emerging through book communication!")

if __name__ == "__main__":
    main()