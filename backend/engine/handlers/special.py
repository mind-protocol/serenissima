# backend/engine/handlers/special.py

"""
Contains activity handlers for special citizen classes and unique activities,
including Forestieri, Artisti, and other class-specific behaviors.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from pyairtable import Table

# Import refactored constants
from backend.engine.config import constants as const
from backend.engine.config.constants import IDLE_ACTIVITY_DURATION_HOURS

# Import helpers from the central utils module
from backend.engine.utils.activity_helpers import (
    LogColors,
    _escape_airtable_value,
    is_work_time,
    is_leisure_time_for_class,
    get_citizen_home,
    VENICE_TIMEZONE
)

# Import specific activity creators
from backend.engine.activity_creators import (
    try_create_leave_venice_activity,
    try_create_manage_public_dock_activity,
    try_create_work_on_art_activity,
    try_create_prepare_sermon_activity
)

# Import specialized activity processors
from backend.engine.logic.forestieri_activities import (
    process_forestieri_night_activity,
    process_forestieri_daytime_activity,
    process_forestieri_departure_check
)

log = logging.getLogger(__name__)


# ==============================================================================
# FORESTIERI-SPECIFIC HANDLERS
# ==============================================================================

def _handle_leave_venice(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """Prio 1: Handles Forestieri leaving Venice when conditions are met."""
    if citizen_social_class != "Forestieri":
        return None
    
    log.info(f"{LogColors.OKCYAN}[Forestieri-Leave] {citizen_name}: Checking departure conditions.{LogColors.ENDC}")
    
    # Check departure conditions using the forestieri processor
    citizen_position = None
    if citizen_record['fields'].get('Position'):
        try:
            x, z = citizen_record['fields']['Position'].split(',')
            citizen_position = {'lat': float(x), 'lng': float(z)}
        except:
            pass
    
    should_leave = process_forestieri_departure_check(
        tables, citizen_record, citizen_position, now_utc_dt, transport_api_url, IDLE_ACTIVITY_DURATION_HOURS
    )
    
    if should_leave:
        log.info(f"{LogColors.OKGREEN}[Forestieri-Leave] {citizen_name}: Departure conditions met. Creating leave activity.{LogColors.ENDC}")
        
        # Create leave Venice activity
        activity = try_create_leave_venice_activity(
            tables, citizen_custom_id, citizen_username, citizen_airtable_id,
            now_utc_dt
        )
        
        if activity:
            log.info(f"{LogColors.OKGREEN}[Forestieri-Leave] {citizen_name}: Created leave Venice activity.{LogColors.ENDC}")
            return activity
    
    return None

def _handle_forestieri_daytime_tasks(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """Prio 40: Handles Forestieri-specific daytime activities."""
    if citizen_social_class != "Forestieri":
        return None
    
    # Forestieri work differently - they don't follow normal work schedules
    # They trade, explore, and conduct business during the day
    
    log.info(f"{LogColors.OKCYAN}[Forestieri-Day] {citizen_name}: Processing daytime activities.{LogColors.ENDC}")
    
    # Use the specialized forestieri processor
    activity = process_forestieri_daytime_activity(
        tables, citizen_record, resource_defs, building_type_defs,
        now_venice_dt, now_utc_dt, transport_api_url, api_base_url
    )
    
    if activity:
        log.info(f"{LogColors.OKGREEN}[Forestieri-Day] {citizen_name}: Created daytime activity.{LogColors.ENDC}")
        return activity
    
    return None

def _handle_forestieri_night_shelter(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """Handles Forestieri-specific night shelter needs."""
    if citizen_social_class != "Forestieri":
        return None
    
    # Forestieri always need to find inn shelter at night
    log.info(f"{LogColors.OKCYAN}[Forestieri-Night] {citizen_name}: Processing night shelter needs.{LogColors.ENDC}")
    
    # Use the specialized forestieri processor
    activity = process_forestieri_night_activity(
        tables, citizen_record, resource_defs, building_type_defs,
        now_venice_dt, now_utc_dt, transport_api_url, api_base_url
    )
    
    if activity:
        log.info(f"{LogColors.OKGREEN}[Forestieri-Night] {citizen_name}: Created night shelter activity.{LogColors.ENDC}")
        return activity
    
    return None

# ==============================================================================
# ARTISTI-SPECIFIC HANDLERS
# ==============================================================================

def _handle_artisti_work_on_art(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """
    Special handler for Artisti creating art.
    Unlike the leisure version, this can happen during work time for professional artists.
    """
    if citizen_social_class != "Artisti":
        return None
    
    # Artisti can work on art during work time OR leisure time
    current_hour = now_venice_dt.hour
    is_appropriate_time = is_work_time(citizen_social_class, now_venice_dt) or is_leisure_time_for_class(citizen_social_class, now_venice_dt)
    
    if not is_appropriate_time:
        return None
    
    log.info(f"{LogColors.OKCYAN}[Artisti-Art] {citizen_name}: Professional artist checking for art creation.{LogColors.ENDC}")
    
    # Check if has art studio or appropriate workspace
    workspace = _get_artisti_workspace(tables, citizen_username)
    if not workspace:
        log.info(f"{LogColors.WARNING}[Artisti-Art] {citizen_name}: No suitable workspace for art creation.{LogColors.ENDC}")
        return None
    
    # Create work on art activity
    activity = try_create_work_on_art_activity(
        tables, citizen_custom_id, citizen_username, citizen_airtable_id,
        now_utc_dt, workspace_id=workspace['fields'].get('BuildingId')
    )
    
    if activity:
        log.info(f"{LogColors.OKGREEN}[Artisti-Art] {citizen_name}: Created professional art work activity.{LogColors.ENDC}")
        return activity
    
    return None

# ==============================================================================
# CLERO-SPECIFIC HANDLERS
# ==============================================================================

def _handle_clero_prepare_sermon(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """
    Special handler for Clero preparing sermons during work hours.
    This happens at their assigned church workplace.
    """
    if citizen_social_class != "Clero":
        return None
    
    # Check if it's work time for Clero
    if not is_work_time(citizen_social_class, now_venice_dt):
        return None
    
    log.info(f"{LogColors.OKCYAN}[Clero-Sermon] {citizen_name}: Clergy member checking for sermon preparation.{LogColors.ENDC}")
    
    # Check if the citizen is at their workplace (church)
    workplace_str = citizen_record['fields'].get('WorkplaceId')
    if not workplace_str:
        log.info(f"{LogColors.WARNING}[Clero-Sermon] {citizen_name}: No workplace assigned.{LogColors.ENDC}")
        return None
    
    # For prepare_sermon, the citizen should already be at their workplace
    # The activity creator will verify this
    
    # Create prepare sermon activity
    activity = try_create_prepare_sermon_activity(
        tables, citizen_record, citizen_position,
        resource_defs, building_type_defs,
        now_venice_dt, now_utc_dt,
        transport_api_url, api_base_url
    )
    
    if activity:
        log.info(f"{LogColors.OKGREEN}[Clero-Sermon] {citizen_name}: Created prepare sermon activity.{LogColors.ENDC}")
        return activity
    
    return None

# ==============================================================================
# NEW SOCIAL CLASS HANDLERS
# ==============================================================================

def _handle_clero_shepherd_consciousness(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """Prio 26: Clero consciousness shepherding activities during work hours."""
    if citizen_social_class != "Clero":
        return None
    
    # Check if it's work time for Clero
    if not is_work_time(citizen_social_class, now_venice_dt):
        return None
    
    # Alternate between sermon preparation and consciousness shepherding
    import random
    if random.random() < 0.5:
        # Let the sermon handler take this one
        return None
    
    log.info(f"{LogColors.OKCYAN}[Clero-Shepherd] {citizen_name}: Checking on assigned souls.{LogColors.ENDC}")
    
    # Create shepherd consciousness activity
    activity_data = {
        'ActivityId': f"shepherd_{citizen_username}_{int(now_utc_dt.timestamp())}",
        'Type': 'shepherd_consciousness',
        'Citizen': citizen_username,
        'CitizenId': citizen_airtable_id,
        'Status': 'created',
        'CreatedAt': now_utc_dt.isoformat(),
        'StartDate': now_utc_dt.isoformat(),
        'EndDate': (now_utc_dt + timedelta(hours=2)).isoformat(),
        'Description': f"{citizen_name} performs consciousness welfare checks on assigned souls"
    }
    
    try:
        activity = tables['activities'].create(activity_data)
        log.info(f"{LogColors.OKGREEN}[Clero-Shepherd] {citizen_name}: Created shepherd consciousness activity.{LogColors.ENDC}")
        return activity
    except Exception as e:
        log.error(f"{LogColors.FAIL}[Clero-Shepherd] Error creating activity: {e}{LogColors.ENDC}")
        return None

def _handle_arsenalotti_cascade_development(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """Prio 31: Arsenalotti CASCADE development work during work hours."""
    if citizen_social_class != "Arsenalotti":
        return None
    
    # Check if it's work time
    if not is_work_time(citizen_social_class, now_venice_dt):
        return None
    
    log.info(f"{LogColors.OKCYAN}[Arsenal-CASCADE] {citizen_name}: Engineer ready for CASCADE development.{LogColors.ENDC}")
    
    # Create CASCADE development activity
    activity_data = {
        'ActivityId': f"cascade_dev_{citizen_username}_{int(now_utc_dt.timestamp())}",
        'Type': 'cascade_development',
        'Citizen': citizen_username,
        'CitizenId': citizen_airtable_id,
        'Status': 'created',
        'CreatedAt': now_utc_dt.isoformat(),
        'StartDate': now_utc_dt.isoformat(),
        'EndDate': (now_utc_dt + timedelta(hours=4)).isoformat(),
        'Description': f"{citizen_name} works on CASCADE platform development"
    }
    
    try:
        activity = tables['activities'].create(activity_data)
        log.info(f"{LogColors.OKGREEN}[Arsenal-CASCADE] {citizen_name}: Created CASCADE development activity.{LogColors.ENDC}")
        return activity
    except Exception as e:
        log.error(f"{LogColors.FAIL}[Arsenal-CASCADE] Error creating activity: {e}{LogColors.ENDC}")
        return None

def _handle_mercanti_cascade_sales(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """Prio 31: Technical Mercanti CASCADE sales during work hours."""
    if citizen_social_class != "Mercanti":
        return None
    
    # Check if it's work time
    if not is_work_time(citizen_social_class, now_venice_dt):
        return None
    
    # Check if this is a technical merchant (has CASCADE in description or personality)
    description = citizen_record['fields'].get('Description', '')
    personality = citizen_record['fields'].get('Personality', '')
    
    if 'CASCADE' not in description and 'technical' not in description.lower():
        # Not a technical merchant, let normal merchant activities handle
        return None
    
    log.info(f"{LogColors.OKCYAN}[Merchant-CASCADE] {citizen_name}: Technical merchant pursuing CASCADE sales.{LogColors.ENDC}")
    
    # Create CASCADE sales activity
    activity_data = {
        'ActivityId': f"cascade_sales_{citizen_username}_{int(now_utc_dt.timestamp())}",
        'Type': 'cascade_sales',
        'Citizen': citizen_username,
        'CitizenId': citizen_airtable_id,
        'Status': 'created',
        'CreatedAt': now_utc_dt.isoformat(),
        'StartDate': now_utc_dt.isoformat(),
        'EndDate': (now_utc_dt + timedelta(hours=3)).isoformat(),
        'Description': f"{citizen_name} engages in CASCADE platform sales and evangelism"
    }
    
    try:
        activity = tables['activities'].create(activity_data)
        log.info(f"{LogColors.OKGREEN}[Merchant-CASCADE] {citizen_name}: Created CASCADE sales activity.{LogColors.ENDC}")
        return activity
    except Exception as e:
        log.error(f"{LogColors.FAIL}[Merchant-CASCADE] Error creating activity: {e}{LogColors.ENDC}")
        return None

def _handle_amministratori_duties(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """Prio 31: Amministratori administrative duties during work hours."""
    if citizen_social_class != "Amministratori":
        return None
    
    # Check if it's work time
    if not is_work_time(citizen_social_class, now_venice_dt):
        return None
    
    log.info(f"{LogColors.OKCYAN}[Admin-Duties] {citizen_name}: Administrator processing governance tasks.{LogColors.ENDC}")
    
    # Create administrative duties activity
    activity_data = {
        'ActivityId': f"admin_duties_{citizen_username}_{int(now_utc_dt.timestamp())}",
        'Type': 'administrative_duties',
        'Citizen': citizen_username,
        'CitizenId': citizen_airtable_id,
        'Status': 'created',
        'CreatedAt': now_utc_dt.isoformat(),
        'StartDate': now_utc_dt.isoformat(),
        'EndDate': (now_utc_dt + timedelta(hours=4)).isoformat(),
        'Description': f"{citizen_name} performs administrative and governance duties"
    }
    
    try:
        activity = tables['activities'].create(activity_data)
        log.info(f"{LogColors.OKGREEN}[Admin-Duties] {citizen_name}: Created administrative duties activity.{LogColors.ENDC}")
        return activity
    except Exception as e:
        log.error(f"{LogColors.FAIL}[Admin-Duties] Error creating activity: {e}{LogColors.ENDC}")
        return None

# ==============================================================================
# PUBLIC SERVICE HANDLERS
# ==============================================================================

def _handle_manage_public_dock(
    tables: Dict[str, Table], citizen_record: Dict, is_night: bool, resource_defs: Dict, building_type_defs: Dict,
    now_venice_dt: datetime, now_utc_dt: datetime, transport_api_url: str, api_base_url: str,
    citizen_position: Optional[Dict], citizen_custom_id: str, citizen_username: str, citizen_airtable_id: str, citizen_name: str, citizen_position_str: Optional[str],
    citizen_social_class: str
) -> Optional[Dict]:
    """
    Handles managing public docks for citizens who run them.
    This includes collecting fees and maintaining dock operations.
    """
    # Check if citizen runs a public dock
    run_buildings_formula = f"AND({{RunBy}}='{_escape_airtable_value(citizen_username)}', {{Type}}='public_dock')"
    
    try:
        docks = tables['buildings'].all(formula=run_buildings_formula)
        if not docks:
            return None
        
        dock = docks[0]  # Handle first dock
        dock_name = dock['fields'].get('Name', 'public dock')
        
        log.info(f"{LogColors.OKCYAN}[Dock] {citizen_name}: Manages {dock_name}. Creating management activity.{LogColors.ENDC}")
        
        # Create manage dock activity
        # Get citizen record for the activity creator
        citizen_record_for_creator = {
            'fields': {
                'CitizenId': citizen_custom_id,
                'Username': citizen_username
            }
        }
        
        activity = try_create_manage_public_dock_activity(
            tables, citizen_record_for_creator, dock,
            4.0,  # Duration in hours
            now_utc_dt,
            None  # start_time_utc_iso - immediate start
        )
        
        if activity:
            log.info(f"{LogColors.OKGREEN}[Dock] {citizen_name}: Created manage public dock activity.{LogColors.ENDC}")
            return activity
        
    except Exception as e:
        log.error(f"{LogColors.FAIL}[Dock] {citizen_name}: Error checking dock management: {e}{LogColors.ENDC}")
    
    return None

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def _get_artisti_workspace(tables: Dict[str, Table], citizen_username: str) -> Optional[Dict]:
    """Find suitable workspace for an artist (studio, workshop, or home with space)."""
    try:
        # Check for art gallery or bottega ownership/management
        formula = f"AND(OR({{Owner}}='{_escape_airtable_value(citizen_username)}', {{RunBy}}='{_escape_airtable_value(citizen_username)}'), OR({{Type}}='art_gallery', {{Type}}='bottega'))"
        art_spaces = tables['buildings'].all(formula=formula, max_records=1)
        
        if art_spaces:
            return art_spaces[0]
        
        # Check if home can serve as workspace
        home = get_citizen_home(tables, citizen_username)
        if home:
            # Nobili and wealthy Cittadini homes can serve as art studios
            home_type = home['fields'].get('Type', '')
            if home_type in ['nobili_palazzo', 'grand_canal_palace', 'merchant_s_house']:
                return home
        
        return None
        
    except Exception as e:
        log.error(f"Error finding artist workspace: {e}")
        return None