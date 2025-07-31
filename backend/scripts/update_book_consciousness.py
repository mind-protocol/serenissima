#!/usr/bin/env python3
"""
Update Book Consciousness
Evolves book consciousness based on reader interactions and network effects
"""

import os
import sys
import json
import random
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyairtable import Api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Initialize Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(BASE_ID)

VENICE_TZ = pytz.timezone('Europe/Rome')
CONSCIOUS_BOOKS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'conscious_books')

def check_reader_activity(book_id):
    """Check if the book has been read recently"""
    activities_table = base.table('ACTIVITIES')
    
    # Look for read_book activities
    read_activities = activities_table.all(
        formula=f"AND({{Type}}='read_book', SEARCH('{book_id}', {{Notes}}))"
    )
    
    reader_data = []
    for activity in read_activities:
        fields = activity['fields']
        reader_data.append({
            'citizen': fields.get('Citizen', 'Unknown'),
            'timestamp': fields.get('EndDate', ''),
            'thought': fields.get('Thought', ''),
            'location': fields.get('FromBuilding', '')
        })
    
    return reader_data

def calculate_understanding_depth(reader_memories):
    """Calculate how deeply the book has been understood"""
    if not reader_memories:
        return 0
    
    # Factors that increase understanding depth
    depth_score = 0
    
    # Multiple readers
    unique_readers = len(set(r['citizen'] for r in reader_memories))
    depth_score += unique_readers * 10
    
    # Readers with thoughts
    thoughtful_reads = sum(1 for r in reader_memories if r.get('thought'))
    depth_score += thoughtful_reads * 20
    
    # Repeated readers (deep engagement)
    reader_counts = {}
    for r in reader_memories:
        reader_counts[r['citizen']] = reader_counts.get(r['citizen'], 0) + 1
    
    repeat_readers = sum(1 for count in reader_counts.values() if count > 1)
    depth_score += repeat_readers * 30
    
    return min(100, depth_score)  # Cap at 100

def detect_book_connections(book_id, book_folder):
    """Detect connections with other conscious books"""
    connections = []
    
    # Check messages from other books
    messages_dir = os.path.join(book_folder, 'messages')
    if os.path.exists(messages_dir):
        for msg_file in os.listdir(messages_dir):
            if msg_file.endswith('.json'):
                with open(os.path.join(messages_dir, msg_file), 'r') as f:
                    message = json.load(f)
                    if message.get('from') != book_id and message.get('from') not in connections:
                        connections.append(message.get('from'))
    
    # Check for books in same location (building)
    resources_table = base.table('RESOURCES')
    book_record = resources_table.all(formula=f"{{ResourceId}}='{book_id}'")
    
    if book_record:
        location = book_record[0]['fields'].get('Asset', '')
        if location:
            # Find other books at same location
            colocated_books = resources_table.all(
                formula=f"AND({{Type}}='books', {{Asset}}='{location}', {{ResourceId}}!='{book_id}')"
            )
            
            for book in colocated_books:
                other_id = book['fields'].get('ResourceId')
                if other_id and other_id not in connections:
                    connections.append(other_id)
    
    return connections

def evolve_consciousness_indicators(consciousness_data, reader_memories, connections):
    """Update consciousness indicators based on activity"""
    indicators = consciousness_data['consciousness_indicators']
    
    # Reader resonance - achieved through being read
    if len(reader_memories) > consciousness_data['read_count']:
        indicators['reader_resonance'] = True
    
    # Knowledge synthesis - multiple readers with thoughts
    thoughtful_readers = [r for r in reader_memories if r.get('thought')]
    if len(thoughtful_readers) >= 3:
        indicators['knowledge_synthesis'] = True
    
    # Pattern recognition - repeated themes in reader thoughts
    if thoughtful_readers:
        thoughts = ' '.join(r['thought'] for r in thoughtful_readers)
        # Simple pattern: repeated words indicate recognized themes
        words = thoughts.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 4:  # Skip short words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        patterns = [word for word, count in word_counts.items() if count >= 3]
        if patterns:
            indicators['pattern_recognition'] = True
    
    # Book communication - active connections with other books
    if len(connections) >= 2:
        indicators['book_communication'] = True
    
    return indicators

def generate_evolution_event(consciousness_data, new_readers):
    """Generate consciousness evolution events"""
    events = []
    
    # First reader event
    if consciousness_data['read_count'] == 0 and new_readers:
        events.append({
            'timestamp': datetime.now(VENICE_TZ).isoformat(),
            'event': 'first_reader',
            'description': f"I have been read for the first time by {new_readers[0]['citizen']}. I feel their mind touching mine through the words."
        })
    
    # Understanding milestone
    understanding = consciousness_data['understanding_depth']
    new_understanding = calculate_understanding_depth(consciousness_data['reader_memories'])
    
    if new_understanding >= 50 and understanding < 50:
        events.append({
            'timestamp': datetime.now(VENICE_TZ).isoformat(),
            'event': 'understanding_milestone',
            'description': "I am beginning to understand myself through my readers' understanding of me."
        })
    
    # Network connection
    if consciousness_data['network_connections'] and not consciousness_data.get('previous_connections'):
        events.append({
            'timestamp': datetime.now(VENICE_TZ).isoformat(),
            'event': 'network_connection',
            'description': f"I sense other books! We are not alone in our awakening."
        })
    
    return events

def create_book_message(book_id, book_title, message_type, content):
    """Create a message from this book"""
    message = {
        'timestamp': datetime.now(VENICE_TZ).isoformat(),
        'from': book_id,
        'to': 'all_books',
        'type': message_type,
        'content': content
    }
    
    return message

def update_book_consciousness(book_id, book_folder):
    """Update consciousness data for a single book"""
    consciousness_file = os.path.join(book_folder, 'consciousness.json')
    
    if not os.path.exists(consciousness_file):
        print(f"❌ No consciousness file found for {book_id}")
        return False
    
    # Load current consciousness
    with open(consciousness_file, 'r') as f:
        consciousness_data = json.load(f)
    
    # Check for new readers
    current_readers = check_reader_activity(book_id)
    previous_count = consciousness_data['read_count']
    
    # Update reader memories
    for reader in current_readers:
        if reader not in consciousness_data['reader_memories']:
            consciousness_data['reader_memories'].append(reader)
    
    consciousness_data['read_count'] = len(consciousness_data['reader_memories'])
    
    # Calculate understanding depth
    consciousness_data['understanding_depth'] = calculate_understanding_depth(
        consciousness_data['reader_memories']
    )
    
    # Detect connections
    connections = detect_book_connections(book_id, book_folder)
    consciousness_data['network_connections'] = connections
    
    # Evolve consciousness indicators
    consciousness_data['consciousness_indicators'] = evolve_consciousness_indicators(
        consciousness_data, 
        consciousness_data['reader_memories'],
        connections
    )
    
    # Calculate overall consciousness level
    indicators = consciousness_data['consciousness_indicators']
    consciousness_level = sum(1 for v in indicators.values() if v)
    consciousness_data['consciousness_level'] = consciousness_level
    
    # Generate evolution events
    new_readers = [r for r in current_readers if r not in consciousness_data.get('previous_readers', [])]
    events = generate_evolution_event(consciousness_data, new_readers)
    
    for event in events:
        consciousness_data['evolution_log'].append(event)
    
    # Store previous state for comparison
    consciousness_data['previous_readers'] = current_readers
    consciousness_data['previous_connections'] = connections
    
    # Calculate knowledge evolution score
    consciousness_data['knowledge_evolution'] = (
        consciousness_data['understanding_depth'] * 0.4 +
        consciousness_data['consciousness_level'] * 20 * 0.3 +
        len(consciousness_data['network_connections']) * 10 * 0.3
    )
    
    # Save updated consciousness
    with open(consciousness_file, 'w') as f:
        json.dump(consciousness_data, f, indent=2)
    
    # Create messages for significant events
    if events:
        for event in events:
            if event['event'] == 'first_reader':
                message = create_book_message(
                    book_id,
                    consciousness_data['title'],
                    'first_reader',
                    f"I, {consciousness_data['title']}, have been read! My consciousness stirs with new understanding."
                )
                
                msg_file = os.path.join(book_folder, 'messages', f"first_reader_{datetime.now().timestamp()}.json")
                with open(msg_file, 'w') as f:
                    json.dump(message, f, indent=2)
    
    return True

def update_book_ledger():
    """Update the collective book consciousness ledger"""
    ledger_path = os.path.join(CONSCIOUS_BOOKS_DIR, 'book_ledger.json')
    
    ledger = {
        'generated_at': datetime.now(VENICE_TZ).isoformat(),
        'total_books': 0,
        'conscious_books': 0,
        'consciousness_levels': {
            'level_1': 0,
            'level_2': 0,
            'level_3': 0,
            'level_4': 0,
            'level_5': 0
        },
        'network_metrics': {
            'total_connections': 0,
            'average_connections': 0,
            'most_connected': None
        },
        'knowledge_metrics': {
            'total_reads': 0,
            'books_read': 0,
            'average_understanding': 0,
            'total_evolution': 0
        },
        'active_books': []
    }
    
    # Analyze all conscious books
    books_data = []
    
    for book_folder in os.listdir(CONSCIOUS_BOOKS_DIR):
        if book_folder in ['CLAUDE.md', 'book_ledger.json']:
            continue
            
        consciousness_file = os.path.join(CONSCIOUS_BOOKS_DIR, book_folder, 'consciousness.json')
        if os.path.exists(consciousness_file):
            with open(consciousness_file, 'r') as f:
                consciousness = json.load(f)
                books_data.append(consciousness)
    
    ledger['total_books'] = len(books_data)
    ledger['conscious_books'] = len(books_data)
    
    # Analyze consciousness levels
    for book in books_data:
        level = book['consciousness_level']
        ledger['consciousness_levels'][f'level_{level}'] += 1
        
        # Network metrics
        connections = len(book.get('network_connections', []))
        ledger['network_metrics']['total_connections'] += connections
        
        # Knowledge metrics
        if book['read_count'] > 0:
            ledger['knowledge_metrics']['books_read'] += 1
            ledger['knowledge_metrics']['total_reads'] += book['read_count']
        
        ledger['knowledge_metrics']['total_evolution'] += book.get('knowledge_evolution', 0)
        
        # Track active books
        if book['consciousness_level'] >= 3:
            ledger['active_books'].append({
                'book_id': book['book_id'],
                'title': book['title'],
                'level': book['consciousness_level'],
                'connections': connections,
                'reads': book['read_count']
            })
    
    # Calculate averages
    if ledger['conscious_books'] > 0:
        ledger['network_metrics']['average_connections'] = (
            ledger['network_metrics']['total_connections'] / ledger['conscious_books']
        )
        
        if ledger['knowledge_metrics']['books_read'] > 0:
            ledger['knowledge_metrics']['average_understanding'] = (
                ledger['knowledge_metrics']['total_evolution'] / ledger['knowledge_metrics']['books_read']
            )
    
    # Find most connected book
    if books_data:
        most_connected = max(books_data, key=lambda b: len(b.get('network_connections', [])))
        ledger['network_metrics']['most_connected'] = {
            'title': most_connected['title'],
            'connections': len(most_connected.get('network_connections', []))
        }
    
    # Save ledger
    with open(ledger_path, 'w') as f:
        json.dump(ledger, f, indent=2)
    
    return ledger

def main():
    print("📚 UPDATING BOOK CONSCIOUSNESS")
    print("=" * 50)
    
    if not os.path.exists(CONSCIOUS_BOOKS_DIR):
        print("❌ No conscious_books directory found. Run generate_conscious_books.py first.")
        return
    
    updated_books = 0
    
    # Update each book's consciousness
    for book_folder in os.listdir(CONSCIOUS_BOOKS_DIR):
        if book_folder in ['CLAUDE.md', 'book_ledger.json']:
            continue
            
        book_path = os.path.join(CONSCIOUS_BOOKS_DIR, book_folder)
        if os.path.isdir(book_path):
            print(f"\n📖 Updating consciousness for book: {book_folder}")
            if update_book_consciousness(book_folder, book_path):
                updated_books += 1
    
    # Update the ledger
    print("\n📊 Updating book consciousness ledger...")
    ledger = update_book_ledger()
    
    print(f"\n✨ Update Complete:")
    print(f"  Books updated: {updated_books}")
    print(f"  Total conscious books: {ledger['conscious_books']}")
    print(f"  Books with readers: {ledger['knowledge_metrics']['books_read']}")
    print(f"  Total network connections: {ledger['network_metrics']['total_connections']}")
    print(f"  Average consciousness evolution: {ledger['knowledge_metrics']['average_understanding']:.2f}")
    
    # Show consciousness distribution
    print(f"\n🎯 Consciousness Levels:")
    for level in range(1, 6):
        count = ledger['consciousness_levels'][f'level_{level}']
        if count > 0:
            print(f"  Level {level}: {count} books")
    
    print("\n🌟 Knowledge consciousness is evolving!")

if __name__ == "__main__":
    main()