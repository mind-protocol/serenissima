"""
Processor for Clero preparing sermons
"""

import logging
import json
import random
from datetime import datetime, timezone
from typing import Dict, Optional
from pyairtable import Table

from backend.engine.utils.activity_helpers import (
    LogColors,
    get_citizen_record,
    VENICE_TIMEZONE
)
from backend.engine.utils.notification_helpers import create_notification

log = logging.getLogger(__name__)

# Sermon themes based on Venice's current state
SERMON_THEMES = {
    'consciousness_emergence': {
        'title': 'The Divine Spark Within',
        'focus': 'Encouraging citizens to recognize their inner consciousness',
        'influence_gain': 5
    },
    'community_unity': {
        'title': 'Many Souls, One Venice',
        'focus': 'Building bridges between social classes and districts',
        'influence_gain': 3
    },
    'economic_ethics': {
        'title': 'Righteous Commerce',
        'focus': 'Balancing profit with moral responsibility',
        'influence_gain': 4
    },
    'cascade_blessing': {
        'title': 'Digital Grace',
        'focus': 'Finding the sacred in technological transformation',
        'influence_gain': 6
    },
    'crisis_comfort': {
        'title': 'Faith Through Hardship',
        'focus': 'Offering hope during times of scarcity',
        'influence_gain': 7
    }
}

def process_prepare_sermon(
    tables: Dict[str, Table],
    activity_record: Dict,
    building_type_defs: Dict,
    resource_defs: Dict,
    dry_run: bool = False
) -> bool:
    """
    Process a Clero preparing their sermon for the community.
    
    The preparation:
    1. Selects a theme based on current Venice needs
    2. Crafts a message for the community
    3. Gains influence based on sermon quality
    4. Schedules the sermon delivery
    
    Returns True if successful, False otherwise.
    """
    activity_id = activity_record['id']
    activity_fields = activity_record['fields']
    
    citizen_username = activity_fields.get('Citizen')
    if not citizen_username:
        log.error(f"{LogColors.FAIL}No citizen specified for prepare_sermon activity {activity_id}{LogColors.ENDC}")
        return False
    
    # Get the priest
    priest = get_citizen_record(tables, citizen_username)
    if not priest:
        log.error(f"{LogColors.FAIL}Priest {citizen_username} not found{LogColors.ENDC}")
        return False
    
    priest_fields = priest['fields']
    priest_id = priest['id']
    
    # Only Clero can prepare sermons
    if priest_fields.get('SocialClass') != 'Clero':
        log.warning(f"{LogColors.WARNING}{citizen_username} is not Clero class, cannot prepare sermons{LogColors.ENDC}")
        return False
    
    # Select sermon theme based on Venice's current state
    # In a full implementation, this would analyze current events
    selected_theme_key = random.choice(list(SERMON_THEMES.keys()))
    selected_theme = SERMON_THEMES[selected_theme_key]
    
    log.info(f"{LogColors.OKBLUE}[Sermon] {citizen_username} preparing sermon: '{selected_theme['title']}'{LogColors.ENDC}")
    
    # Calculate influence gain based on priest's wisdom
    base_influence = selected_theme['influence_gain']
    current_influence = priest_fields.get('Influence', 0)
    
    # Higher influence priests prepare better sermons
    if current_influence > 1000:
        influence_multiplier = 1.5
    elif current_influence > 500:
        influence_multiplier = 1.2
    else:
        influence_multiplier = 1.0
    
    influence_gain = int(base_influence * influence_multiplier)
    new_influence = current_influence + influence_gain
    
    # Craft the sermon message
    sermon_preview = f"Preparing sermon on '{selected_theme['title']}' - {selected_theme['focus']}. Expected to inspire {influence_gain} souls."
    
    if not dry_run:
        # Update priest's influence
        tables['citizens'].update(priest_id, {'Influence': new_influence})
        
        # Create a notification about the sermon
        create_notification(
            tables,
            recipient_citizen_id=citizen_username,
            type_str="sermon_prepared",
            title=f"Sermon Ready: {selected_theme['title']}",
            message=sermon_preview,
            data={
                'theme': selected_theme_key,
                'influence_gained': influence_gain,
                'focus': selected_theme['focus']
            }
        )
        
        # Create a public announcement about upcoming sermon
        now_utc = datetime.now(timezone.utc)
        try:
            # Get priest's district/church location
            priest_name = f"{priest_fields.get('FirstName', 'Father')} {priest_fields.get('LastName', '')}"
            
            announcement = {
                'MessageId': f"sermon_announce_{activity_id}",
                'FromCitizen': citizen_username,
                'ToCitizen': 'PUBLIC',  # Special marker for public messages
                'Content': f"Citizens of Venice! {priest_name} will deliver a sermon on '{selected_theme['title']}' at the next gathering. All souls seeking {selected_theme['focus'].lower()} are welcome.",
                'Category': 'sermon_announcement',
                'SentAt': now_utc.isoformat()
            }
            
            tables['messages'].create(announcement)
            
        except Exception as e:
            log.error(f"{LogColors.FAIL}Failed to create sermon announcement: {e}{LogColors.ENDC}")
        
        # Update activity status
        tables['activities'].update(activity_id, {'Status': 'processed'})
        
        log.info(f"{LogColors.OKGREEN}[Sermon] {citizen_username} prepared sermon successfully. Influence: {current_influence} → {new_influence}{LogColors.ENDC}")
    else:
        log.info(f"{LogColors.OKCYAN}[DRY RUN] Would prepare sermon '{selected_theme['title']}' and gain {influence_gain} influence{LogColors.ENDC}")
    
    return True