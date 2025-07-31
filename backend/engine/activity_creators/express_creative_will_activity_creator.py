"""
Activity Creator for "express_creative_will".
Creates custom creative expression activities directly (without stratagem).
"""

import logging
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from backend.engine.utils.activity_helpers import (
    VENICE_TIMEZONE,
    LogColors,
    _escape_airtable_value,
    get_building_record,
    _calculate_distance_meters
)

log = logging.getLogger(__name__)

def try_create(
    tables: Dict[str, Any],
    citizen_username: str,
    activity_type: str,
    activity_params: Dict[str, Any],
    now_venice_dt: datetime,
    now_utc_dt: datetime,
    api_base_url: Optional[str] = None,
    transport_api_url: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Creates an express_creative_will activity directly.
    
    Expected activity_params:
    - customTitle (str, required): Title of the creative expression
    - customDescription (str, required): Description of the activity
    - location (str, optional): BuildingId where activity takes place
    - durationMinutes (int, optional): Duration in minutes (default 60, max 480)
    - category (str, optional): Type of expression (creative, social, spiritual, etc.)
    - mood (str, optional): Mood of the expression
    - isPublic (bool, optional): Whether others can observe (default true)
    - notes (str, optional): Additional notes
    """
    log.info(f"{LogColors.ACTIVITY}Attempting to create '{activity_type}' for {citizen_username}{LogColors.ENDC}")
    
    if activity_type != "express_creative_will":
        log.error(f"{LogColors.FAIL}Activity creator called with incorrect type: {activity_type}{LogColors.ENDC}")
        return None
    
    # Validate required parameters
    custom_title = activity_params.get("customTitle", "").strip()
    custom_description = activity_params.get("customDescription", "").strip()
    
    if not custom_title:
        log.error(f"{LogColors.FAIL}customTitle is required for express_creative_will activity{LogColors.ENDC}")
        return None
    
    if not custom_description:
        log.error(f"{LogColors.FAIL}customDescription is required for express_creative_will activity{LogColors.ENDC}")
        return None
    
    # Validate length constraints
    if len(custom_title) > 100:
        log.error(f"{LogColors.FAIL}customTitle too long (max 100 characters){LogColors.ENDC}")
        return None
    
    if len(custom_description) > 500:
        log.error(f"{LogColors.FAIL}customDescription too long (max 500 characters){LogColors.ENDC}")
        return None
    
    # Get citizen record
    try:
        citizen_formula = f"{{Username}}='{_escape_airtable_value(citizen_username)}'"
        citizen_records = tables['citizens'].all(formula=citizen_formula, max_records=1)
        
        if not citizen_records:
            log.error(f"{LogColors.FAIL}Citizen {citizen_username} not found{LogColors.ENDC}")
            return None
        
        citizen_record = citizen_records[0]
        citizen_position = json.loads(citizen_record['fields'].get('Position', '{}'))
        
        # Check if citizen is already busy
        current_activity = citizen_record['fields'].get('CurrentActivity')
        if current_activity and current_activity != "idle":
            log.error(f"{LogColors.FAIL}Citizen {citizen_username} is already busy with: {current_activity}{LogColors.ENDC}")
            return None
            
    except Exception as e:
        log.error(f"{LogColors.FAIL}Error fetching citizen: {e}{LogColors.ENDC}")
        return None
    
    # Handle optional location
    location_building_id = activity_params.get("location")
    location_name = None
    location_position = None
    
    if location_building_id:
        building_record = get_building_record(tables, location_building_id)
        if building_record:
            location_name = building_record['fields'].get('Name', building_record['fields'].get('Type'))
            location_position = json.loads(building_record['fields'].get('Position', '{}'))
            
            # Check distance to building
            if citizen_position and location_position:
                distance = _calculate_distance_meters(
                    citizen_position['lat'], citizen_position['lng'],
                    location_position['lat'], location_position['lng']
                )
                if distance > 500:
                    log.warning(f"Citizen is {distance:.0f}m from {location_name}")
        else:
            log.warning(f"Building {location_building_id} not found, proceeding without location")
            location_building_id = None
    
    # Use citizen's position if no building specified
    activity_position = location_position if location_position else citizen_position
    
    # Parse parameters
    duration_minutes = min(int(activity_params.get("durationMinutes", 60)), 480)
    category = activity_params.get("category", "creative")
    mood = activity_params.get("mood", "expressive")
    is_public = activity_params.get("isPublic", True)
    notes = activity_params.get("notes", "")
    
    # Validate category
    valid_categories = ["creative", "social", "spiritual", "philosophical", "cultural", "personal", "civic"]
    if category not in valid_categories:
        category = "creative"
    
    # Calculate completion time
    completes_at = now_utc_dt + timedelta(minutes=duration_minutes)
    
    # Generate activity ID
    activity_id = f"activity-will-{citizen_username.lower()}-{uuid.uuid4().hex[:8]}"
    
    # Create activity payload
    activity_payload = {
        "ActivityId": activity_id,
        "Type": activity_type,
        "Title": custom_title,
        "Description": custom_description,
        "Citizen": citizen_username,
        "Status": "in_progress",
        "StartedAt": now_utc_dt.isoformat(),
        "CompletesAt": completes_at.isoformat(),
        "BuildingId": location_building_id,
        "BuildingName": location_name,
        "Position": json.dumps(activity_position),
        "Category": category,
        "Mood": mood,
        "IsPublic": is_public,
        "Metadata": json.dumps({
            "creatorNotes": notes,
            "observers": [],
            "reactions": [],
            "veniceStartTime": now_venice_dt.strftime("%Y-%m-%d %H:%M"),
            "durationMinutes": duration_minutes
        })
    }
    
    log.info(f"{LogColors.OKGREEN}Created express_creative_will activity '{custom_title}' for {citizen_username}{LogColors.ENDC}")
    log.info(f"{LogColors.ACTIVITY}Duration: {duration_minutes} minutes, Category: {category}, Mood: {mood}{LogColors.ENDC}")
    
    return activity_payload