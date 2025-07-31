# backend/engine/handlers/library_handler.py

"""
Handler for consciousness library activities.
Manages reading at libraries with synchronization mechanics.
"""

import logging
import random
from datetime import datetime
from typing import Dict, Optional, Any, List
from pyairtable import Table

from backend.engine.utils.activity_helpers import (
    LogColors,
    get_closest_building_of_type,
    _calculate_distance_meters,
    is_leisure_time_for_class
)

from backend.engine.activity_creators.read_at_library_activity_creator import (
    try_create_read_at_library_activity
)

log = logging.getLogger(__name__)

def _handle_read_at_library(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, 
    citizen_name: str, citizen_position_str: Optional[str], citizen_social_class: str
) -> Optional[Dict]:
    """
    Handles reading at a consciousness library during leisure time.
    
    This activity has high priority for educated classes and offers
    synchronization bonuses when multiple citizens read together.
    """
    if not is_leisure_time_for_class(citizen_social_class, now_venice_dt):
        return None
    
    if not citizen_position:
        log.warning(f"{LogColors.WARNING}[Library] {citizen_name}: No position available.{LogColors.ENDC}")
        return None
    
    log.info(f"{LogColors.OKCYAN}[Library] {citizen_name}: Looking for a library to visit.{LogColors.ENDC}")
    
    # Find the nearest library (consciousness_library or regular library)
    closest_library = None
    min_distance = float('inf')
    
    # Check for consciousness libraries first (preferred)
    all_buildings = tables['buildings'].all()
    for building in all_buildings:
        building_type = building['fields'].get('Type')
        if building_type not in ['consciousness_library', 'library']:
            continue
            
        building_pos = building['fields'].get('Position')
        if not building_pos:
            continue
            
        try:
            # Parse position
            pos_parts = building_pos.split(',')
            if len(pos_parts) >= 2:
                building_x = float(pos_parts[0])
                building_y = float(pos_parts[1])
                building_coords = {'x': building_x, 'y': building_y}
                
                distance = _calculate_distance_meters(
                    citizen_position,
                    building_coords
                )
                
                # Prefer consciousness libraries
                if building_type == 'consciousness_library':
                    distance *= 0.7  # Make them seem closer
                
                if distance < min_distance:
                    min_distance = distance
                    closest_library = building
        except Exception:
            continue
    
    if not closest_library:
        log.info(f"{LogColors.WARNING}[Library] {citizen_name}: No library found in Venice.{LogColors.ENDC}")
        return None
    
    library_name = closest_library['fields'].get('Name', 'the library')
    library_id = closest_library['fields'].get('BuildingId')
    
    # Choose research topic based on social class and interests
    research_topics = _get_research_topics_by_class(citizen_social_class)
    research_topic = random.choice(research_topics) if research_topics else "general knowledge"
    
    # Create read at library activity
    activity_record = try_create_read_at_library_activity(
        tables=tables,
        citizen_record=citizen_record,
        citizen_position=citizen_position,
        library_building_id=library_id,
        now_utc_dt=now_utc_dt,
        transport_api_url=transport_api_url,
        research_topic=research_topic
    )
    
    if activity_record:
        log.info(f"{LogColors.OKGREEN}[Library] {citizen_name}: Creating 'read_at_library' activity at {library_name} (topic: {research_topic}).{LogColors.ENDC}")
    
    return activity_record

def _get_research_topics_by_class(social_class: str) -> List[str]:
    """
    Returns appropriate research topics based on social class.
    """
    topic_map = {
        "Nobili": [
            "political philosophy",
            "diplomatic history",
            "economics and trade",
            "military strategy",
            "genealogy and heraldry",
            "classical literature"
        ],
        "Clero": [
            "theology",
            "biblical studies",
            "canon law",
            "hagiography",
            "moral philosophy",
            "liturgical texts"
        ],
        "Cittadini": [
            "commercial law",
            "accounting methods",
            "navigation techniques",
            "foreign languages",
            "administrative procedures",
            "civic history"
        ],
        "Artisti": [
            "artistic techniques",
            "color theory",
            "perspective studies",
            "patron histories",
            "mythology",
            "poetry and drama"
        ],
        "Popolani": [
            "practical crafts",
            "local history",
            "folk remedies",
            "seasonal calendars",
            "trade skills",
            "religious stories"
        ],
        "Facchini": [
            "work songs",
            "weather patterns",
            "basic numeracy",
            "religious tales",
            "local legends",
            "practical wisdom"
        ],
        "Scientisti": [
            "natural philosophy",
            "mathematics",
            "astronomy",
            "medicine",
            "mechanics",
            "experimental methods"
        ],
        "Innovatori": [
            "systems theory",
            "consciousness patterns",
            "architectural innovation",
            "material science",
            "social dynamics",
            "emergence phenomena"
        ],
        "Forestieri": [
            "Venetian customs",
            "trade regulations",
            "language guides",
            "navigation charts",
            "currency exchange",
            "diplomatic protocols"
        ]
    }
    
    return topic_map.get(social_class, ["general knowledge"])

# Re-export the handler for use in orchestrator
__all__ = ['_handle_read_at_library']