import logging
import json
from datetime import datetime, timedelta
import pytz
from typing import Dict, Optional, Any

from backend.engine.utils.activity_helpers import (
    LogColors,
    get_building_record,
    _get_building_position_coords,
    _calculate_distance_meters,
    get_path_between_points,
    create_activity_record,
    VENICE_TIMEZONE,
    dateutil_parser
)
from .goto_location_activity_creator import try_create as try_create_goto_location_activity

log = logging.getLogger(__name__)

# Base reading duration - will be modified by synchronization mechanics
BASE_READING_DURATION_MINUTES = 180

def try_create_read_at_library_activity(
    tables: Dict[str, Any],
    citizen_record: Dict[str, Any],
    citizen_position: Optional[Dict[str, float]],
    library_building_id: str,
    now_utc_dt: datetime,
    transport_api_url: str,
    start_time_utc_iso: Optional[str] = None,
    research_topic: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Creates a 'read_at_library' activity or a chain starting with 'goto_location'.
    
    This activity represents reading and research at a consciousness library,
    with potential for synchronization bonuses when multiple citizens read together.
    """
    citizen_username = citizen_record['fields'].get('Username')
    citizen_custom_id = citizen_record['fields'].get('CitizenId')
    citizen_name_log = f"{citizen_record['fields'].get('FirstName', '')} {citizen_record['fields'].get('LastName', '')}".strip() or citizen_username

    # Get library building record
    library_building_record = get_building_record(tables, library_building_id)
    if not library_building_record:
        log.warning(f"{LogColors.WARNING}[Read at Library] {citizen_name_log}: Library building '{library_building_id}' not found.{LogColors.ENDC}")
        return None
    
    library_name = library_building_record['fields'].get('Name', library_building_id)
    library_type = library_building_record['fields'].get('PointType', 'building')
    
    # Verify it's actually a library
    if library_type != 'consciousness_library' and library_type != 'library':
        log.warning(f"{LogColors.WARNING}[Read at Library] {citizen_name_log}: Building '{library_name}' is not a library (type: {library_type}).{LogColors.ENDC}")
        return None
    
    library_pos = _get_building_position_coords(library_building_record)
    if not library_pos:
        log.warning(f"{LogColors.WARNING}[Read at Library] {citizen_name_log}: Library '{library_name}' has no position.{LogColors.ENDC}")
        return None

    # Check if citizen is already at the library
    is_at_library = False
    if citizen_position:
        is_at_library = _calculate_distance_meters(citizen_position, library_pos) < 20
    
    log.info(f"{LogColors.OKBLUE}[Read at Library] {citizen_name_log}: Planning to read at '{library_name}'. Currently at library: {is_at_library}.{LogColors.ENDC}")

    # Calculate duration - will be modified by synchronization in processor
    effective_start_time_dt = dateutil_parser.isoparse(start_time_utc_iso) if start_time_utc_iso else now_utc_dt
    if effective_start_time_dt.tzinfo is None:
        effective_start_time_dt = pytz.utc.localize(effective_start_time_dt)
    
    reading_end_time_dt = effective_start_time_dt + timedelta(minutes=BASE_READING_DURATION_MINUTES)
    reading_end_time_iso = reading_end_time_dt.isoformat()

    # Prepare activity details
    research_topic_str = research_topic or "general knowledge"
    activity_title = f"Read at {library_name}"
    activity_description = f"{citizen_name_log} reads and researches {research_topic_str} at {library_name}."
    activity_thought = f"Time to expand my understanding of {research_topic_str} at the library."
    
    # Notes for the activity - includes potential synchronization data
    activity_notes = {
        "library_building_id": library_building_id,
        "library_name": library_name,
        "research_topic": research_topic_str,
        "base_duration_minutes": BASE_READING_DURATION_MINUTES,
        "synchronization_eligible": True,
        "library_type": library_type
    }

    if is_at_library:
        log.info(f"{LogColors.OKBLUE}[Read at Library] {citizen_name_log} is at the library. Creating 'read_at_library' activity.{LogColors.ENDC}")
        return create_activity_record(
            tables=tables,
            citizen_username=citizen_username,
            activity_type="read_at_library",
            start_date_iso=start_time_utc_iso if start_time_utc_iso else now_utc_dt.isoformat(),
            end_date_iso=reading_end_time_iso,
            from_building_id=library_building_id,
            to_building_id=library_building_id,
            title=activity_title,
            description=activity_description,
            thought=activity_thought,
            notes=json.dumps(activity_notes),
            priority_override=60  # Higher priority than casual reading
        )
    else:
        # Need to travel to the library
        if not citizen_position:
            log.warning(f"{LogColors.WARNING}[Read at Library] {citizen_name_log}: No citizen position for travel.{LogColors.ENDC}")
            return None

        log.info(f"{LogColors.OKBLUE}[Read at Library] {citizen_name_log} needs to travel to {library_name}. Creating 'goto_location'.{LogColors.ENDC}")
        path_to_library = get_path_between_points(citizen_position, library_pos, transport_api_url)
        if not (path_to_library and path_to_library.get('success')):
            log.warning(f"{LogColors.WARNING}[Read at Library] {citizen_name_log}: Cannot find path to {library_name}.{LogColors.ENDC}")
            return None

        goto_notes_str = f"Heading to {library_name} to research {research_topic_str}."
        action_details_for_chaining = {
            "action_on_arrival": "read_at_library",
            "duration_minutes_on_arrival": BASE_READING_DURATION_MINUTES,
            "original_target_building_id_on_arrival": library_building_id,
            "title_on_arrival": activity_title,
            "description_on_arrival": activity_description,
            "thought_on_arrival": activity_thought,
            "priority_on_arrival": 60,
            "notes_for_chained_activity": activity_notes
        }
        
        goto_activity = try_create_goto_location_activity(
            tables=tables,
            citizen_record=citizen_record,
            destination_building_id=library_building_id,
            path_data=path_to_library,
            current_time_utc=now_utc_dt,
            notes=goto_notes_str,
            details_payload=action_details_for_chaining,
            start_time_utc_iso=start_time_utc_iso
        )
        
        if goto_activity:
            log.info(f"{LogColors.OKGREEN}[Read at Library] {citizen_name_log}: 'goto_location' activity created to {library_name}. 'read_at_library' will be chained.{LogColors.ENDC}")
            return goto_activity
        else:
            log.warning(f"{LogColors.WARNING}[Read at Library] {citizen_name_log}: Failed to create 'goto_location' to {library_name}.{LogColors.ENDC}")
            return None