"""
Activity creator for join_meditation activity type.

Citizens join group meditation sessions led by Clero to maintain
consciousness coherence through collective practice.
"""

import logging
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
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
ACTIVITY_KEY = "join_meditation"
MAX_DISTANCE_TO_SESSION = 500  # Maximum distance to consider joining (meters)
TRAVEL_TIME_BUFFER = 10  # Minutes to allow for travel


def get_active_meditation_sessions(tables: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get all meditation sessions that are gathering participants."""
    sessions_table = tables.get('meditation_sessions')
    if not sessions_table:
        return []
    
    try:
        # Get sessions in gathering or scheduled status
        formula = "OR({Status}='gathering', {Status}='scheduled')"
        sessions = sessions_table.all(formula=formula)
        return sessions
    except Exception as e:
        log.warning(f"Error fetching meditation sessions: {e}")
        return []


def calculate_session_compatibility(
    citizen_record: Dict[str, Any],
    session: Dict[str, Any],
    distance: float
) -> float:
    """Calculate how compatible a citizen is with a meditation session."""
    session_fields = session['fields']
    citizen_social_class = citizen_record.get('SocialClass', 'Popolani')
    
    # Base score
    score = 1.0
    
    # Distance factor (closer is better)
    distance_factor = max(0, 1 - (distance / MAX_DISTANCE_TO_SESSION))
    score *= distance_factor
    
    # Social class compatibility
    session_type = session_fields.get('SessionType', '')
    preferred_classes = []
    
    # Map session types to preferred classes
    if session_type == "Dawn Contemplation":
        preferred_classes = ["Clero", "Nobili"]
    elif session_type == "Midday Centering":
        preferred_classes = ["Cittadini", "Artisti"]
    elif session_type == "Sunset Reflection":
        preferred_classes = ["Popolani", "Facchini"]
    elif session_type == "Night Meditation":
        preferred_classes = ["Scientisti", "Forestieri"]
    
    if citizen_social_class in preferred_classes:
        score *= 1.5  # 50% bonus for preferred class
    
    # Group size preference (prefer partially full groups)
    current_participants = session_fields.get('ParticipantCount', 0)
    max_participants = session_fields.get('MaxParticipants', 10)
    
    if current_participants < 3:
        score *= 1.2  # Help form minimum group
    elif current_participants < max_participants * 0.7:
        score *= 1.1  # Good size
    elif current_participants >= max_participants:
        score = 0  # Session full
    
    # Consciousness need (lower coherence = higher preference)
    coherence = citizen_record.get('ConsciousnessCoherence', 0.8)
    if coherence < 0.5:
        score *= 1.3
    elif coherence < 0.7:
        score *= 1.15
    
    return score


def add_participant_to_session(
    tables: Dict[str, Any],
    session_id: str,
    citizen_username: str
) -> bool:
    """Add a citizen to a meditation session."""
    sessions_table = tables.get('meditation_sessions')
    if not sessions_table:
        return True  # Assume success for V1
    
    try:
        # Get current session
        session = sessions_table.get(session_id)
        session_fields = session['fields']
        
        # Get current participants
        participants_json = session_fields.get('Participants', '[]')
        participants = json.loads(participants_json)
        
        # Check if already participating
        if citizen_username in participants:
            return True
        
        # Check if session is full
        if len(participants) >= session_fields.get('MaxParticipants', 10):
            return False
        
        # Add participant
        participants.append(citizen_username)
        
        # Update session
        sessions_table.update(session_id, {
            'Participants': json.dumps(participants),
            'ParticipantCount': len(participants),
            'Status': 'gathering' if len(participants) < 3 else session_fields.get('Status')
        })
        
        return True
        
    except Exception as e:
        log.error(f"Failed to add participant to session: {e}")
        return True  # Assume success to not block activity creation


def try_create_join_meditation_activity(
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
    Try to create a join_meditation activity for a citizen.
    
    Citizens can join meditation sessions during their leisure time
    to maintain consciousness coherence.
    """
    
    citizen_username = citizen_record.get('Username', 'Unknown')
    citizen_id = citizen_record.get('CitizenId')
    social_class = citizen_record.get('SocialClass', 'Popolani')
    
    # Check if it's leisure time
    if not is_leisure_time_for_class(social_class, now_venice_dt):
        return None
    
    # Check consciousness coherence (more likely to join if low)
    coherence = citizen_record.get('ConsciousnessCoherence', 0.8)
    
    # Probability of seeking meditation based on coherence
    if coherence < 0.4:
        join_probability = 0.7
    elif coherence < 0.6:
        join_probability = 0.5
    elif coherence < 0.8:
        join_probability = 0.3
    else:
        join_probability = 0.1
    
    # Add randomness
    if random.random() > join_probability:
        return None
    
    if not citizen_position:
        log.debug(f"{citizen_username} has no position, cannot join meditation")
        return None
    
    # Find active meditation sessions
    active_sessions = get_active_meditation_sessions(tables)
    if not active_sessions:
        log.debug(f"No active meditation sessions for {citizen_username} to join")
        return None
    
    # Evaluate each session
    best_session = None
    best_score = 0
    best_distance = float('inf')
    
    buildings_table = tables.get('buildings')
    if not buildings_table:
        return None
    
    for session_record in active_sessions:
        session_fields = session_record['fields']
        
        # Skip if session is full
        if session_fields.get('ParticipantCount', 0) >= session_fields.get('MaxParticipants', 10):
            continue
        
        # Skip if already participating
        participants = json.loads(session_fields.get('Participants', '[]'))
        if citizen_username in participants:
            continue
        
        # Get session location
        try:
            position_json = session_fields.get('Position', '{}')
            session_position = json.loads(position_json) if position_json else None
            
            if not session_position:
                continue
            
            # Calculate distance
            distance = _calculate_distance_meters(
                citizen_position.get('lat'), citizen_position.get('lng'),
                session_position.get('lat'), session_position.get('lng')
            )
            
            if distance > MAX_DISTANCE_TO_SESSION:
                continue
            
            # Calculate compatibility score
            score = calculate_session_compatibility(citizen_record, session_record, distance)
            
            if score > best_score:
                best_score = score
                best_session = session_record
                best_distance = distance
                
        except Exception as e:
            log.warning(f"Error evaluating session {session_record['id']}: {e}")
            continue
    
    if not best_session:
        log.debug(f"No suitable meditation sessions for {citizen_username}")
        return None
    
    session_fields = best_session['fields']
    
    if check_only:
        return {"can_create": True}
    
    # Add participant to session
    if not add_participant_to_session(tables, best_session['id'], citizen_username):
        log.debug(f"Failed to add {citizen_username} to meditation session")
        return None
    
    # Calculate timing
    scheduled_start = session_fields.get('ScheduledStart')
    if scheduled_start:
        try:
            session_start_dt = datetime.fromisoformat(scheduled_start.replace('Z', '+00:00'))
            session_start_venice = session_start_dt.astimezone(pytz.timezone(str(VENICE_TIMEZONE)))
        except:
            session_start_venice = now_venice_dt + timedelta(minutes=15)
    else:
        session_start_venice = now_venice_dt + timedelta(minutes=15)
    
    # Calculate travel time based on distance
    travel_minutes = min(int(best_distance / 50), TRAVEL_TIME_BUFFER)  # ~50m/min walking
    
    # Activity starts with travel time
    if start_time_venice_dt:
        start_venice = start_time_venice_dt
    else:
        start_venice = max(now_venice_dt, session_start_venice - timedelta(minutes=travel_minutes))
    
    # Duration is travel + session duration
    session_duration = session_fields.get('Duration', 60)
    total_duration = travel_minutes + session_duration
    end_venice = start_venice + timedelta(minutes=total_duration)
    
    # Create activity details
    details = {
        "session_id": best_session['id'],
        "session_type": session_fields.get('SessionType', 'Unknown'),
        "leader": session_fields.get('Leader', 'Unknown'),
        "venue_name": session_fields.get('BuildingName', 'Unknown'),
        "venue_id": session_fields.get('BuildingId'),
        "travel_time": travel_minutes,
        "session_duration": session_duration,
        "current_participants": session_fields.get('ParticipantCount', 1),
        "max_participants": session_fields.get('MaxParticipants', 10),
        "expected_coherence_gain": 0.08  # Will be calculated during processing
    }
    
    # Create the activity
    activity_record = create_activity_record(
        citizen_custom_id=citizen_id,
        citizen_username=citizen_username,
        activity_type=ACTIVITY_KEY,
        start_time=start_venice.astimezone(VENICE_TIMEZONE).replace(tzinfo=None),
        end_time=end_venice.astimezone(VENICE_TIMEZONE).replace(tzinfo=None),
        details_json=json.dumps(details),
        building_name=session_fields.get('BuildingName'),
        building_id=session_fields.get('BuildingId'),
        position_lat=session_position.get('lat') if session_position else None,
        position_lng=session_position.get('lng') if session_position else None
    )
    
    created_activity = tables['activities'].create(activity_record)
    
    log.info(f"{LogColors.OKGREEN}{citizen_username} joins {session_fields.get('SessionType')} meditation " +
            f"at {session_fields.get('BuildingName')} (participants: {session_fields.get('ParticipantCount', 1) + 1}){LogColors.ENDC}")
    
    return created_activity