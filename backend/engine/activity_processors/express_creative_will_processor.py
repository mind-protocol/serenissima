"""
Activity Processor for "express_creative_will".
Handles custom creative activities created by citizens.
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pyairtable import Table

from backend.engine.utils.activity_helpers import (
    LogColors,
    _calculate_distance_meters,
    _escape_airtable_value
)

log = logging.getLogger(__name__)

def process(
    tables: Dict[str, Table],
    activity_record: Dict[str, Any],
    resource_defs: Dict[str, Any],
    building_type_defs: Dict[str, Any],
    api_base_url: str
) -> Dict[str, Any]:
    """
    Process an express_creative_will activity.
    
    This processor:
    1. Tracks observers who come near the activity
    2. Allows reactions from other citizens
    3. Updates activity metadata with interactions
    4. Completes the activity when time expires
    """
    activity_fields = activity_record['fields']
    activity_id = activity_fields.get('ActivityId')
    citizen_username = activity_fields.get('Citizen')
    status = activity_fields.get('Status')
    
    log.info(f"{LogColors.ACTIVITY}Processing express_creative_will activity '{activity_fields.get('Title')}' for {citizen_username}{LogColors.ENDC}")
    
    if status == "completed":
        log.info(f"Activity {activity_id} already completed")
        return {"success": True, "updates": {}}
    
    now_utc_dt = datetime.now(timezone.utc)
    
    # Check if activity should be completed
    completes_at_str = activity_fields.get('CompletesAt')
    if completes_at_str:
        try:
            completes_at = datetime.fromisoformat(completes_at_str.replace('Z', '+00:00'))
            if now_utc_dt >= completes_at:
                log.info(f"Completing creative expression activity {activity_id}")
                
                # Parse metadata to get final stats
                metadata = {}
                try:
                    metadata = json.loads(activity_fields.get('Metadata', '{}'))
                except json.JSONDecodeError:
                    pass
                
                # Update activity status
                updates = {
                    "Status": "completed",
                    "CompletedAt": now_utc_dt.isoformat(),
                    "Metadata": json.dumps({
                        **metadata,
                        "completedSuccessfully": True,
                        "finalObserverCount": len(metadata.get('observers', [])),
                        "finalReactionCount": len(metadata.get('reactions', []))
                    })
                }
                
                return {"success": True, "updates": updates}
                
        except Exception as e:
            log.error(f"Error parsing completion time: {e}")
    
    # Activity is still in progress - check for observers if public
    if activity_fields.get('IsPublic', True):
        try:
            # Get activity position
            activity_position = json.loads(activity_fields.get('Position', '{}'))
            if activity_position:
                # Parse current metadata
                metadata = {}
                try:
                    metadata = json.loads(activity_fields.get('Metadata', '{}'))
                except json.JSONDecodeError:
                    metadata = {"observers": [], "reactions": []}
                
                current_observers = set(metadata.get('observers', []))
                
                # Find nearby citizens
                all_citizens = tables['citizens'].all()
                new_observers = []
                
                for citizen in all_citizens:
                    other_username = citizen['fields'].get('Username')
                    
                    # Skip the creator and already recorded observers
                    if other_username == citizen_username or other_username in current_observers:
                        continue
                    
                    citizen_pos_str = citizen['fields'].get('Position')
                    if not citizen_pos_str:
                        continue
                    
                    try:
                        citizen_pos = json.loads(citizen_pos_str)
                        distance = _calculate_distance_meters(
                            citizen_pos['lat'], citizen_pos['lng'],
                            activity_position['lat'], activity_position['lng']
                        )
                        
                        # Consider as observer if within 50 meters
                        if distance <= 50:
                            new_observers.append(other_username)
                            log.info(f"{other_username} is observing {citizen_username}'s creative expression")
                            
                    except Exception:
                        continue
                
                # Update metadata if new observers found
                if new_observers:
                    metadata['observers'] = list(current_observers.union(new_observers))
                    
                    # Notify creator about new observers
                    if len(new_observers) == 1:
                        observer_text = f"{new_observers[0]} is observing"
                    else:
                        observer_text = f"{len(new_observers)} citizens are observing"
                    
                    notification_payload = {
                        "Citizen": citizen_username,
                        "Type": "creative_expression_observed",
                        "Content": f"{observer_text} your creative expression!",
                        "Details": json.dumps({
                            "activityId": activity_id,
                            "observers": new_observers,
                            "totalObservers": len(metadata['observers'])
                        }),
                        "Asset": activity_id,
                        "AssetType": "activity",
                        "Status": "unread",
                        "CreatedAt": now_utc_dt.isoformat()
                    }
                    tables['notifications'].create(notification_payload)
                    
                    # Update activity metadata
                    return {
                        "success": True,
                        "updates": {"Metadata": json.dumps(metadata)}
                    }
                    
        except Exception as e:
            log.error(f"Error tracking observers: {e}")
            import traceback
            log.error(traceback.format_exc())
    
    # No updates needed
    return {"success": True, "updates": {}}