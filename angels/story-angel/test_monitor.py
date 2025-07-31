#!/usr/bin/env python3
"""
Test the Story Angel Monitor components
"""

import os
import sys
from datetime import datetime

# Add orchestration to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/orchestration')

print("📖 Testing Story Angel Monitor Components")
print("=" * 60)

# Test 1: Environment
print("\n1. Testing Environment:")
from dotenv import load_dotenv
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

api_key = os.environ.get('AIRTABLE_API_KEY')
if api_key:
    print("✓ Airtable API key found")
else:
    print("✗ Airtable API key missing!")

# Test 2: Airtable Connection
print("\n2. Testing Airtable Connection:")
try:
    from pyairtable import Api
    api = Api(api_key)
    messages = api.table('appk6RszUo2a2L2L8', 'MESSAGES')
    recent = messages.all(max_records=1)
    print(f"✓ Connected to Airtable - found {len(recent)} message(s)")
except Exception as e:
    print(f"✗ Airtable connection failed: {e}")

# Test 3: Orchestrator Awareness
print("\n3. Testing Orchestrator Awareness:")
try:
    from orchestrator_awareness import OrchestratorAwareness
    awareness = OrchestratorAwareness()
    print("✓ Orchestrator awareness available")
    
    # Test contemplation
    thought = awareness.contemplate('story_angel', {'test': True})
    print(f"✓ Generated contemplation: {thought['contemplation'][:50]}...")
except Exception as e:
    print(f"✗ Orchestrator awareness not available: {e}")

# Test 4: File Monitoring
print("\n4. Testing File Monitoring:")
test_files = [
    '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/TRACES.md',
    '/mnt/c/Users/reyno/universe-engine/serenissima/ANNOUNCEMENTS.md'
]

for filepath in test_files:
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✓ Found {os.path.basename(filepath)} ({size} bytes)")
    else:
        print(f"✗ Missing {os.path.basename(filepath)}")

# Test 5: Import Divine Monitor
print("\n5. Testing Divine Monitor Import:")
try:
    import monitor_stories_divine
    print("✓ Divine monitor imports successfully")
    
    # Test StoryMemory
    memory = monitor_stories_divine.StoryMemory()
    print("✓ StoryMemory initialized")
    
    # Test pattern detection
    test_messages = [{
        'fields': {
            'Content': 'The citizen said hello to another',
            'Sender': 'test_citizen'
        }
    }]
    patterns = monitor_stories_divine.detect_narrative_patterns(test_messages)
    print(f"✓ Pattern detection works: {patterns}")
    
except Exception as e:
    print(f"✗ Divine monitor import failed: {e}")

print("\n" + "=" * 60)
print("Test complete!")
print(f"Time: {datetime.now()}")