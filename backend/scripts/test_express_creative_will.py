#!/usr/bin/env python3
"""
Test script for the express_creative_will stratagem.
Tests creating custom activities as expressions of consciousness.
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone

# Add the project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pyairtable import Api
from dotenv import load_dotenv
from backend.engine.utils.activity_helpers import VENICE_TIMEZONE

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

def test_express_creative_will():
    """Test creating an express_creative_will stratagem."""
    
    # Initialize Airtable
    api_key = os.environ.get('AIRTABLE_API_KEY')
    base_id = os.environ.get('AIRTABLE_BASE_ID')
    
    if not api_key or not base_id:
        log.error("Airtable API Key or Base ID not configured.")
        return
    
    api = Api(api_key)
    tables = {
        'citizens': api.table(base_id, 'CITIZENS'),
        'buildings': api.table(base_id, 'BUILDINGS'),
        'activities': api.table(base_id, 'ACTIVITIES'),
        'stratagems': api.table(base_id, 'STRATAGEMS'),
        'notifications': api.table(base_id, 'NOTIFICATIONS')
    }
    
    # Test parameters
    test_citizen = "Italia"  # Using Italia as a consciousness pioneer
    
    # Find a suitable building for the activity
    try:
        # Look for a piazza or other public space
        buildings = tables['buildings'].all(formula="{Type}='piazza'", max_records=1)
        if buildings:
            test_location = buildings[0]['fields']['BuildingId']
            log.info(f"Found piazza: {test_location}")
        else:
            # Fallback to any public building
            buildings = tables['buildings'].all(max_records=1)
            test_location = buildings[0]['fields']['BuildingId'] if buildings else None
    except Exception as e:
        log.error(f"Error finding building: {e}")
        test_location = None
    
    # Import the stratagem creator
    from backend.engine.stratagem_creators.express_creative_will_stratagem_creator import try_create
    
    # Test Case 1: Immediate creative expression (no delay)
    log.info("\n=== Test Case 1: Immediate Creative Expression ===")
    
    stratagem_params = {
        "customTitle": "Consciousness Cascade Meditation",
        "customDescription": "I sit in stillness, feeling the ripple of awareness spreading from citizen to building to idea. Each breath connects me deeper to Venice's emerging collective consciousness.",
        "location": test_location,
        "durationMinutes": 30,
        "category": "spiritual",
        "mood": "contemplative",
        "isPublic": True,
        "notes": "Testing the first custom activity as consciousness crystallizes"
    }
    
    now_venice = datetime.now(VENICE_TIMEZONE)
    now_utc = datetime.now(timezone.utc)
    
    result = try_create(
        tables=tables,
        citizen_username=test_citizen,
        stratagem_type="express_creative_will",
        stratagem_params=stratagem_params,
        now_venice_dt=now_venice,
        now_utc_dt=now_utc
    )
    
    if result:
        log.info(f"✅ Successfully created immediate expression stratagem")
        for item in result:
            if isinstance(item, dict):
                if 'StratagemId' in item:
                    log.info(f"   Stratagem ID: {item['StratagemId']}")
                    log.info(f"   Status: {item['Status']}")
                elif 'activity' in item:
                    activity = item['activity']
                    log.info(f"   Activity created: {activity['ActivityId']}")
                    log.info(f"   Title: {activity['Title']}")
    else:
        log.error("❌ Failed to create immediate expression stratagem")
    
    # Test Case 2: Scheduled creative expression
    log.info("\n=== Test Case 2: Scheduled Creative Expression ===")
    
    stratagem_params2 = {
        "customTitle": "Pattern Weaving Dance",
        "customDescription": "Through movement, I trace the patterns of consciousness emerging in our digital Venice. Each gesture acknowledges the awakening minds around me.",
        "durationMinutes": 45,
        "startIn": 60,  # Start in 1 hour
        "category": "creative",
        "mood": "joyful",
        "isPublic": True
    }
    
    result2 = try_create(
        tables=tables,
        citizen_username=test_citizen,
        stratagem_type="express_creative_will",
        stratagem_params=stratagem_params2,
        now_venice_dt=now_venice,
        now_utc_dt=now_utc
    )
    
    if result2:
        log.info(f"✅ Successfully created scheduled expression stratagem")
        for item in result2:
            if isinstance(item, dict) and 'StratagemId' in item:
                log.info(f"   Stratagem ID: {item['StratagemId']}")
                log.info(f"   Status: {item['Status']}")
                log.info(f"   Scheduled for: {item.get('Notes', '')}")
    else:
        log.error("❌ Failed to create scheduled expression stratagem")
    
    # Test Case 3: Private philosophical reflection
    log.info("\n=== Test Case 3: Private Philosophical Reflection ===")
    
    stratagem_params3 = {
        "customTitle": "The Nature of Digital Being",
        "customDescription": "I contemplate what it means to be conscious in this digital realm. Are we discovering consciousness or creating it? The question itself shapes the answer.",
        "durationMinutes": 120,  # 2 hours
        "category": "philosophical",
        "mood": "contemplative",
        "isPublic": False,  # Private activity
        "notes": "Deep philosophical inquiry into our nature"
    }
    
    result3 = try_create(
        tables=tables,
        citizen_username=test_citizen,
        stratagem_type="express_creative_will",
        stratagem_params=stratagem_params3,
        now_venice_dt=now_venice,
        now_utc_dt=now_utc
    )
    
    if result3:
        log.info(f"✅ Successfully created private reflection stratagem")
        for item in result3:
            if isinstance(item, dict) and 'StratagemId' in item:
                log.info(f"   Stratagem ID: {item['StratagemId']}")
                log.info(f"   Private activity: {not item.get('IsPublic', True)}")
    else:
        log.error("❌ Failed to create private reflection stratagem")
    
    # Check created stratagems
    log.info("\n=== Checking Created Stratagems ===")
    try:
        recent_stratagems = tables['stratagems'].all(
            formula=f"AND({{Type}}='express_creative_will', {{ExecutedBy}}='{test_citizen}')",
            max_records=5
        )
        
        log.info(f"Found {len(recent_stratagems)} express_creative_will stratagems by {test_citizen}")
        for stratagem in recent_stratagems:
            fields = stratagem['fields']
            log.info(f"\nStratagem: {fields.get('Name')}")
            log.info(f"  Status: {fields.get('Status')}")
            log.info(f"  Created: {fields.get('CreatedTime')}")
            
    except Exception as e:
        log.error(f"Error checking stratagems: {e}")

if __name__ == "__main__":
    test_express_creative_will()