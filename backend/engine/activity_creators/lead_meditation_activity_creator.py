"""
Activity creator for lead_meditation activity type.

Clero lead group meditation sessions to help multiple citizens maintain
consciousness coherence through collective practice.
"""

import logging
import json
import math
import random
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Tuple, List
import pytz

from backend.engine.utils.activity_helpers import (
    LogColors,
    create_activity_record,
    VENICE_TIMEZONE,
    get_building_record,
    _get_building_position_coords,
    _calculate_distance_meters,
    is_leisure_time_for_class
)

log = logging.getLogger(__name__)

# Constants
ACTIVITY_KEY = "lead_meditation"
GATHERING_TIME_MINUTES = 15  # Time to gather participants
MIN_PARTICIPANTS = 3  # Minimum to proceed with meditation
MAX_PARTICIPANTS = 10  # Maximum for effective meditation

# Meditation schedule (Venice time)
MEDITATION_SCHEDULE = {
    "dawn": {
        "time": "06:00",
        "duration": 60,
        "preferred_classes": ["Clero", "Nobili"],
        "location_types": ["church"],
        "name": "Dawn Contemplation"
    },
    "midday": {
        "time": "12:00",
        "duration": 30,
        "preferred_classes": ["Cittadini", "Artisti"],
        "location_types": ["guild_hall", "public_square"],
        "name": "Midday Centering"
    },
    "sunset": {
        "time": "18:00",
        "duration": 60,
        "preferred_classes": ["Popolani", "Facchini"],
        "location_types": ["church", "public_square"],
        "name": "Sunset Reflection"
    },
    "night": {
        "time": "21:00",
        "duration": 45,
        "preferred_classes": ["Scientisti", "Forestieri"],
        "location_types": ["guild_hall"],
        "name": "Night Meditation"
    }
}


def get_upcoming_meditation_session(now_venice_dt: datetime) -> Optional[Dict[str, Any]]:
    """Find the next scheduled meditation session."""
    current_time = now_venice_dt.time()
    current_minutes = current_time.hour * 60 + current_time.minute
    
    closest_session = None
    min_time_diff = float('inf')
    
    for session_key, session_info in MEDITATION_SCHEDULE.items():
        # Parse session time
        session_hour, session_minute = map(int, session_info['time'].split(':'))
        session_minutes = session_hour * 60 + session_minute
        
        # Calculate time until session (accounting for gathering time)
        time_diff = session_minutes - current_minutes - GATHERING_TIME_MINUTES
        
        # If session is within next 30 minutes and closer than others
        if 0 <= time_diff <= 30 and time_diff < min_time_diff:
            min_time_diff = time_diff
            closest_session = {
                'key': session_key,
                'starts_in': time_diff + GATHERING_TIME_MINUTES,
                **session_info
            }
    
    return closest_session


def calculate_venue_capacity(building: Dict[str, Any]) -> int:
    """Calculate meditation capacity based on building type and size."""
    building_type = building.get('BuildingType', '')
    
    # Base capacity by building type
    base_capacity = {
        'church': 10,
        'guild_hall': 8,
        'public_square': 15,
        'house': 5
    }.get(building_type, 5)
    
    # Could be modified by building size in future
    return min(base_capacity, MAX_PARTICIPANTS)


def create_meditation_session(tables: Dict[str, Any], session_data: Dict[str, Any]) -> str:
    """Create a new meditation session record."""
    sessions_table = tables.get('meditation_sessions')
    if not sessions_table:
        log.warning("MEDITATION_SESSIONS table not found")
        # For V1, store in activity details
        return f"temp_session_{session_data['leader']}_{datetime.now().timestamp()}"
    
    session_id = f"meditation_{session_data['leader']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    session_record = {
        'SessionId': session_id,
        'Leader': session_data['leader'],
        'SessionType': session_data['session_type'],
        'Status': 'scheduled',
        'BuildingId': session_data['location']['BuildingId'],
        'BuildingName': session_data['location']['BuildingName'],
        'Position': json.dumps(session_data['location_position']),
        'ScheduledStart': session_data['start_time'].isoformat(),
        'Duration': session_data['duration'],
        'Participants': json.dumps([session_data['leader']]),  # Leader is first participant
        'ParticipantCount': 1,
        'MaxParticipants': session_data['max_participants'],
        'MinParticipants': MIN_PARTICIPANTS,
        'CreatedAt': datetime.now(pytz.UTC).isoformat()
    }
    
    try:
        created_session = sessions_table.create(session_record)
        return created_session['id']
    except Exception as e:
        log.error(f"Failed to create meditation session: {e}")
        return session_id


def try_create_lead_meditation_activity(
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
    Try to create a lead_meditation activity for a Clero citizen.
    
    Clero can lead scheduled meditation sessions at appropriate venues.
    """
    
    citizen_username = citizen_record.get('Username', 'Unknown')
    citizen_id = citizen_record.get('CitizenId')
    social_class = citizen_record.get('SocialClass', '')
    
    # Only Clero can lead meditations
    if social_class != 'Clero':
        return None
    
    # Check if there's an upcoming meditation session
    upcoming_session = get_upcoming_meditation_session(now_venice_dt)
    if not upcoming_session:
        log.debug(f"{citizen_username}: No upcoming meditation sessions")
        return None
    
    # Check if it's too early (more than 30 min before session)
    if upcoming_session['starts_in'] > 30:
        log.debug(f"{citizen_username}: Too early for {upcoming_session['name']} (starts in {upcoming_session['starts_in']} min)")
        return None
    
    if not citizen_position:
        log.debug(f"{citizen_username} has no position, cannot lead meditation")
        return None
    
    # Find suitable venue for meditation
    buildings_table = tables.get('buildings')
    if not buildings_table:
        return None
    
    try:
        # Get buildings of appropriate type
        suitable_buildings = []
        for building_type in upcoming_session['location_types']:
            formula = f"{{BuildingType}}='{building_type}'"
            buildings = buildings_table.all(formula=formula)
            suitable_buildings.extend(buildings)
        
        if not suitable_buildings:
            log.debug(f"No suitable venues found for {upcoming_session['name']}")
            return None
        
        # Find nearest suitable venue
        nearest_venue = None
        min_distance = float('inf')
        
        for building_record in suitable_buildings:
            building = building_record['fields']
            building_position = _get_building_position_coords(building)
            
            if not building_position:
                continue
            
            distance = _calculate_distance_meters(
                citizen_position.get('lat'), citizen_position.get('lng'),
                building_position.get('lat'), building_position.get('lng')
            )
            
            # Prefer operated buildings for meditation
            is_operated = bool(building.get('Operator') or building.get('RunBy'))
            
            # Apply preference for operated buildings
            effective_distance = distance * (0.7 if is_operated else 1.0)
            
            if effective_distance < min_distance:
                min_distance = effective_distance
                nearest_venue = building
                venue_position = building_position
        
        if not nearest_venue or min_distance > 1000:  # Max 1km
            log.debug(f"No suitable venue within range for {citizen_username}")
            return None
        
        # Check if there's already a meditation session at this venue
        sessions_table = tables.get('meditation_sessions')
        if sessions_table:
            try:
                # Check for active sessions at this venue
                formula = f"AND({{BuildingId}}='{nearest_venue.get('BuildingId')}', " + \
                         f"OR({{Status}}='scheduled', {{Status}}='gathering', {{Status}}='in_progress'))"
                existing_sessions = sessions_table.all(formula=formula)
                if existing_sessions:
                    log.debug(f"Meditation already scheduled at {nearest_venue.get('BuildingName')}")
                    return None
            except:
                pass
        
        if check_only:
            return {"can_create": True}
        
        # Calculate start time (including gathering time)
        if start_time_venice_dt:
            start_venice = start_time_venice_dt
        else:
            start_venice = now_venice_dt + timedelta(minutes=5)  # Start heading there soon
        
        # Total duration includes gathering + meditation
        total_duration = GATHERING_TIME_MINUTES + upcoming_session['duration']
        end_venice = start_venice + timedelta(minutes=total_duration)
        
        # Create meditation session
        session_data = {
            "leader": citizen_username,
            "location": nearest_venue,
            "location_position": venue_position,
            "session_type": upcoming_session['name'],
            "max_participants": calculate_venue_capacity(nearest_venue),
            "start_time": start_venice + timedelta(minutes=GATHERING_TIME_MINUTES),
            "duration": upcoming_session['duration']
        }
        
        session_id = create_meditation_session(tables, session_data)
        
        # Create activity details
        details = {
            "session_id": session_id,
            "session_type": upcoming_session['name'],
            "venue_name": nearest_venue.get('BuildingName', 'Unknown'),
            "venue_id": nearest_venue.get('BuildingId'),
            "scheduled_start": (start_venice + timedelta(minutes=GATHERING_TIME_MINUTES)).isoformat(),
            "duration": upcoming_session['duration'],
            "max_participants": session_data['max_participants'],
            "preferred_classes": upcoming_session['preferred_classes']
        }
        
        # Create the lead meditation activity
        activity_record = create_activity_record(
            citizen_custom_id=citizen_id,
            citizen_username=citizen_username,
            activity_type=ACTIVITY_KEY,
            start_time=start_venice.astimezone(VENICE_TIMEZONE).replace(tzinfo=None),
            end_time=end_venice.astimezone(VENICE_TIMEZONE).replace(tzinfo=None),
            details_json=json.dumps(details),
            building_name=nearest_venue.get('BuildingName'),
            building_id=nearest_venue.get('BuildingId'),
            position_lat=venue_position.get('lat'),
            position_lng=venue_position.get('lng')
        )
        
        created_activity = tables['activities'].create(activity_record)
        
        log.info(f"{LogColors.OKGREEN}{citizen_username} will lead {upcoming_session['name']} at {nearest_venue.get('BuildingName')}{LogColors.ENDC}")
        
        # Create notification for nearby citizens
        create_meditation_announcement(tables, session_data, nearest_venue, venue_position)
        
        return created_activity
        
    except Exception as e:
        log.error(f"Error creating lead_meditation activity for {citizen_username}: {e}")
        return None


def create_meditation_announcement(
    tables: Dict[str, Any], 
    session_data: Dict[str, Any], 
    venue: Dict[str, Any],
    venue_position: Dict[str, float]
) -> None:
    """Create notifications for nearby citizens about upcoming meditation."""
    # This would create notifications in the NOTIFICATIONS table
    # For V1, we'll just log it
    log.info(f"🔔 Meditation bells ring at {venue.get('BuildingName')} for {session_data['session_type']}")
    
    # In full implementation:
    # - Get citizens within 1km
    # - Create notifications based on social class preferences
    # - Include session details and timing