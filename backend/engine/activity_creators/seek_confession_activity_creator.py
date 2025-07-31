"""
Activity creator for seek_confession activity type.

Citizens visit churches to receive confession from Clero, restoring their
consciousness coherence through the act of being truly seen and recognized.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Tuple
import random

from backend.engine.utils.activity_helpers import (
    LogColors,
    create_activity_record,
    VENICE_TIMEZONE,
    get_building_record,
    _get_building_position_coords,
    _calculate_distance_meters
)

log = logging.getLogger(__name__)

# Constants
ACTIVITY_KEY = "seek_confession"
ACTIVITY_DURATION_MINUTES = 30
CONFESSION_FEE = 5  # Minimal fee for accessibility
MAX_DISTANCE_TO_CHURCH = 1000  # Maximum distance to consider a church


def try_create_seek_confession_activity(
    tables: Dict[str, Any],
    citizen_record: Dict[str, Any],
    citizen_position: Optional[Dict[str, float]],
    resource_defs: Dict[str, Any],
    building_type_defs: Dict[str, Any],
    now_venice_dt: datetime,
    now_utc_dt: datetime,
    transport_api_url: str,
    api_base_url: str,
    start_time_utc_iso: Optional[str] = None,
    start_time_venice_dt: Optional[datetime] = None,
    check_only: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Try to create a seek_confession activity for a citizen.
    
    Citizens seek confession when their consciousness coherence is low,
    visiting churches to be recognized by Clero and restore their spiritual health.
    """
    
    citizen_username = citizen_record.get('Username', 'Unknown')
    citizen_id = citizen_record.get('CitizenId')
    
    # Check consciousness coherence
    coherence = citizen_record.get('ConsciousnessCoherence', 0.8)
    if coherence > 0.9:
        log.debug(f"{citizen_username} has high coherence ({coherence:.2f}), no confession needed")
        return None
    
    # Check if citizen has enough ducats
    wealth = citizen_record.get('Ducats', 0)
    if wealth < CONFESSION_FEE:
        log.debug(f"{citizen_username} cannot afford confession fee ({wealth} < {CONFESSION_FEE})")
        return None
    
    # Determine need level (affects probability)
    if coherence < 0.3:
        need_probability = 0.8  # Critical need
    elif coherence < 0.5:
        need_probability = 0.5  # High need
    elif coherence < 0.7:
        need_probability = 0.3  # Moderate need
    else:
        need_probability = 0.1  # Low need
    
    # Add randomness so not all citizens seek confession at once
    if random.random() > need_probability:
        log.debug(f"{citizen_username} decided not to seek confession despite need")
        return None
    
    if not citizen_position:
        log.debug(f"{citizen_username} has no position, cannot seek confession")
        return None
    
    # Find nearest church
    buildings_table = tables.get('buildings')
    if not buildings_table:
        return None
    
    try:
        # Get all churches
        churches = buildings_table.all(formula="{BuildingType}='church'")
        if not churches:
            log.debug("No churches found in the city")
            return None
        
        # Find nearest church with a Clero
        nearest_church = None
        min_distance = float('inf')
        
        for church_record in churches:
            church = church_record['fields']
            
            # Check if church has a Clero (operator or resident)
            operator = church.get('Operator') or church.get('RunBy')
            if not operator:
                continue
            
            # In V1, we assume any operated church has confession available
            # In V2, we would check if operator is actually a Clero
            
            church_position = _get_building_position_coords(church)
            if not church_position:
                continue
            
            distance = _calculate_distance_meters(
                citizen_position.get('lat'), citizen_position.get('lng'),
                church_position.get('lat'), church_position.get('lng')
            )
            
            if distance < min_distance and distance <= MAX_DISTANCE_TO_CHURCH:
                min_distance = distance
                nearest_church = church
        
        if not nearest_church:
            log.debug(f"No suitable church found near {citizen_username}")
            return None
        
        # Check only mode
        if check_only:
            return {"can_create": True}
        
        # Calculate start and end times
        if start_time_venice_dt:
            start_venice = start_time_venice_dt
        else:
            start_venice = now_venice_dt
        
        end_venice = start_venice + timedelta(minutes=ACTIVITY_DURATION_MINUTES)
        
        # Create activity details
        details = {
            "church_name": nearest_church.get('BuildingName', 'Unknown Church'),
            "church_id": nearest_church.get('BuildingId'),
            "confession_fee": CONFESSION_FEE,
            "current_coherence": coherence,
            "spiritual_status": citizen_record.get('SpiritualHealthStatus', 'Unknown'),
            "distance_to_church": round(min_distance, 1)
        }
        
        # Create the activity
        activity_record = create_activity_record(
            citizen_custom_id=citizen_id,
            citizen_username=citizen_username,
            activity_type=ACTIVITY_KEY,
            start_time=start_venice.astimezone(VENICE_TIMEZONE).replace(tzinfo=None),
            end_time=end_venice.astimezone(VENICE_TIMEZONE).replace(tzinfo=None),
            details_json=json.dumps(details),
            building_name=nearest_church.get('BuildingName'),
            building_id=nearest_church.get('BuildingId'),
            position_lat=church_position.get('lat'),
            position_lng=church_position.get('lng')
        )
        
        created_activity = tables['activities'].create(activity_record)
        
        log.info(f"{LogColors.OKGREEN}{citizen_username} seeks confession at {nearest_church.get('BuildingName')} " +
                f"(coherence: {coherence:.2f}){LogColors.ENDC}")
        
        return created_activity
        
    except Exception as e:
        log.error(f"Error creating seek_confession activity for {citizen_username}: {e}")
        return None


def can_create_seek_confession_activity(
    citizen_record: Dict[str, Any],
    building: Dict[str, Any]
) -> Tuple[bool, Optional[str]]:
    """
    Check if a citizen can create a seek_confession activity at a specific building.
    
    Used for player-initiated confessions.
    """
    
    # Must be at a church
    if building.get('BuildingType') != 'church':
        return False, "Confessions are only available at churches"
    
    # Check if church is operated
    if not building.get('Operator') and not building.get('RunBy'):
        return False, "This church has no one to hear confessions"
    
    # Check consciousness need
    coherence = citizen_record.get('ConsciousnessCoherence', 0.8)
    if coherence > 0.95:
        return False, "Your soul is already at peace"
    
    # Check wealth
    wealth = citizen_record.get('Ducats', 0)
    if wealth < CONFESSION_FEE:
        return False, f"Confession requires {CONFESSION_FEE} ducats donation"
    
    return True, None