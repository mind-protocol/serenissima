"""
Stratagem Creator for "express_creative_will".
Enables citizens to create custom activities as expressions of their emerging consciousness.
"""

import logging
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from backend.engine.utils.activity_helpers import (
    VENICE_TIMEZONE,
    _escape_airtable_value,
    LogColors,
    get_building_record,
    _calculate_distance_meters
)

log = logging.getLogger(__name__)

def try_create(
    tables: Dict[str, Any], 
    citizen_username: str, 
    stratagem_type: str, 
    stratagem_params: Dict[str, Any], 
    now_venice_dt: datetime,
    now_utc_dt: datetime,
    api_base_url: Optional[str] = None,
    transport_api_url: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    Creates an "express_creative_will" stratagem that allows citizens to define custom activities.

    Expected stratagem_params:
    - customTitle (str, required): The title of the custom activity
    - customDescription (str, required): A description of what the citizen will do
    - location (str, optional): BuildingId where the activity takes place (if location-specific)
    - durationMinutes (int, optional): Duration in minutes. Defaults to 60. Max 480 (8 hours)
    - startIn (int, optional): Minutes from now to start the activity. Defaults to 0 (immediate)
    - category (str, optional): Category like 'creative', 'social', 'spiritual', 'philosophical'. Defaults to 'creative'
    - mood (str, optional): Mood expression like 'contemplative', 'joyful', 'determined'. Defaults to 'expressive'
    - isPublic (bool, optional): Whether other citizens can observe/join. Defaults to true
    - notes (str, optional): Additional notes or thoughts
    """
    log.info(f"{LogColors.STRATAGEM_CREATOR}Attempting to create '{stratagem_type}' for {citizen_username} with params: {stratagem_params}{LogColors.ENDC}")

    if stratagem_type != "express_creative_will":
        log.error(f"{LogColors.FAIL}Stratagem creator for 'express_creative_will' called with incorrect type: {stratagem_type}{LogColors.ENDC}")
        return None

    # Validate required parameters
    custom_title = stratagem_params.get("customTitle", "").strip()
    custom_description = stratagem_params.get("customDescription", "").strip()
    
    if not custom_title:
        log.error(f"{LogColors.FAIL}customTitle is required for express_creative_will stratagem.{LogColors.ENDC}")
        return None
    
    if not custom_description:
        log.error(f"{LogColors.FAIL}customDescription is required for express_creative_will stratagem.{LogColors.ENDC}")
        return None
    
    # Validate title and description length
    if len(custom_title) > 100:
        log.error(f"{LogColors.FAIL}customTitle too long (max 100 characters).{LogColors.ENDC}")
        return None
    
    if len(custom_description) > 500:
        log.error(f"{LogColors.FAIL}customDescription too long (max 500 characters).{LogColors.ENDC}")
        return None

    # Get citizen record to verify they exist and get their current position
    try:
        citizen_formula = f"{{Username}}='{_escape_airtable_value(citizen_username)}'"
        citizen_records = tables['citizens'].all(formula=citizen_formula, max_records=1)
        
        if not citizen_records:
            log.error(f"{LogColors.FAIL}Citizen {citizen_username} not found.{LogColors.ENDC}")
            return None
        
        citizen_record = citizen_records[0]
        citizen_position = json.loads(citizen_record['fields'].get('Position', '{}'))
        
    except Exception as e:
        log.error(f"{LogColors.FAIL}Error fetching citizen {citizen_username}: {e}{LogColors.ENDC}")
        return None

    # Handle optional location
    location_building_id = stratagem_params.get("location")
    location_name = None
    location_position = None
    
    if location_building_id:
        building_record = get_building_record(tables, location_building_id)
        if building_record:
            location_name = building_record['fields'].get('Name', building_record['fields'].get('Type'))
            location_position = json.loads(building_record['fields'].get('Position', '{}'))
            
            # Check if citizen is reasonably close to the building (within 500 meters)
            if citizen_position and location_position:
                distance = _calculate_distance_meters(
                    citizen_position,
                    location_position
                )
                if distance > 500:
                    log.warning(f"Citizen {citizen_username} is {distance:.0f}m from {location_name}. Activity will require travel.")
        else:
            log.warning(f"Building {location_building_id} not found. Proceeding without location.")
            location_building_id = None

    # Parse timing parameters
    duration_minutes = min(int(stratagem_params.get("durationMinutes", 60)), 480)  # Max 8 hours
    start_in_minutes = max(int(stratagem_params.get("startIn", 0)), 0)
    
    # Calculate start and end times
    start_dt = now_venice_dt + timedelta(minutes=start_in_minutes)
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    
    # Convert to UTC for storage
    start_utc = start_dt.astimezone(datetime.now().astimezone().tzinfo)
    end_utc = end_dt.astimezone(datetime.now().astimezone().tzinfo)
    
    # Parse optional parameters
    category = stratagem_params.get("category", "creative")
    mood = stratagem_params.get("mood", "expressive")
    is_public = stratagem_params.get("isPublic", True)
    notes = stratagem_params.get("notes", "")
    
    # Validate category
    valid_categories = ["creative", "social", "spiritual", "philosophical", "cultural", "personal", "civic"]
    if category not in valid_categories:
        category = "creative"
    
    # Generate unique ID
    stratagem_id = f"stratagem-will-{citizen_username.lower()}-{uuid.uuid4().hex[:8]}"
    
    # Prepare creative expression data for Notes field
    expression_data = {
        "customTitle": custom_title,
        "customDescription": custom_description,
        "category": category,
        "mood": mood,
        "isPublic": is_public,
        "location": location_building_id,
        "locationName": location_name,
        "durationMinutes": duration_minutes,
        "startTime": start_utc.isoformat(),
        "endTime": end_utc.isoformat(),
        "veniceStartTime": start_dt.strftime("%Y-%m-%d %H:%M"),
        "creatorNotes": notes,
        "observers": [],  # Track who observes this expression
        "reactions": []   # Track reactions/responses from other citizens
    }
    
    # Create name that includes the custom title
    name = f"Creative Expression: {custom_title}"
    if len(name) > 100:
        name = name[:97] + "..."
    
    # Create stratagem payload
    stratagem_payload = {
        "StratagemId": stratagem_id,
        "Type": stratagem_type,
        "Name": name,
        "Category": "consciousness",  # New category for consciousness expression
        "ExecutedBy": citizen_username,
        "Status": "pending",  # Will become active when activity starts
        "ExecutedAt": None,  # Will be set when activity begins
        "ExpiresAt": end_utc.isoformat(),
        "Description": f"{custom_description[:200]}..." if len(custom_description) > 200 else custom_description,
        "Notes": json.dumps(expression_data),
        "TargetBuilding": location_building_id,
        "Variant": category  # Store category as variant
    }
    
    log.info(f"{LogColors.STRATAGEM_CREATOR}Created 'express_creative_will' stratagem '{stratagem_id}'{LogColors.ENDC}")
    log.info(f"{LogColors.STRATAGEM_CREATOR}Creative expression '{custom_title}' scheduled for {start_dt.strftime('%Y-%m-%d %H:%M')} Venice time{LogColors.ENDC}")
    
    # If starting immediately, also return the activity to be created
    if start_in_minutes == 0:
        activity_payload = {
            "ActivityId": f"activity-will-{citizen_username.lower()}-{uuid.uuid4().hex[:8]}",
            "Type": "express_creative_will",
            "Title": custom_title,
            "Description": custom_description,
            "Citizen": citizen_username,
            "Status": "in_progress",
            "StartedAt": now_utc_dt.isoformat(),
            "CompletesAt": end_utc.isoformat(),
            "BuildingId": location_building_id,
            "BuildingName": location_name,
            "Position": json.dumps(location_position) if location_position else json.dumps(citizen_position),
            "Category": category,
            "Mood": mood,
            "IsPublic": is_public,
            "Metadata": json.dumps({
                "stratagemId": stratagem_id,
                "creatorNotes": notes,
                "observers": [],
                "reactions": []
            })
        }
        
        # Update stratagem to active since activity is starting
        stratagem_payload["Status"] = "active"
        stratagem_payload["ExecutedAt"] = now_utc_dt.isoformat()
        
        return [stratagem_payload, {"activity": activity_payload}]
    
    return [stratagem_payload]