"""
Activity processor for join_meditation activities.

Processes citizens participating in group meditation sessions,
applying synchronization effects based on group dynamics.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any

from backend.engine.utils.activity_helpers import (
    LogColors,
    VENICE_TIMEZONE
)
from backend.engine.utils.notification_helpers import create_notification

log = logging.getLogger(__name__)


def process_join_meditation_activity(
    tables: Dict[str, Any],
    activity: Dict[str, Any],
    venice_time: datetime
) -> bool:
    """
    Process a completed join_meditation activity.
    
    Since the lead_meditation processor handles the group synchronization
    and coherence updates for all participants, this processor focuses on:
    1. Ensuring the participant was included in the session
    2. Logging participation
    3. Handling edge cases (cancelled sessions, etc.)
    
    Most of the work is done by lead_meditation_processor when the session completes.
    """
    
    try:
        # Extract activity details
        details_json = activity.get('DetailsJSON', '{}')
        details = json.loads(details_json) if details_json else {}
        
        session_id = details.get('session_id')
        session_type = details.get('session_type', 'Meditation')
        venue_name = details.get('venue_name', 'the meditation venue')
        leader = details.get('leader', 'Unknown')
        citizen_username = activity.get('Citizen')
        
        # Check if session exists and get status
        sessions_table = tables.get('meditation_sessions')
        session_status = 'unknown'
        
        if sessions_table and session_id:
            try:
                session = sessions_table.get(session_id)
                session_status = session['fields'].get('Status', 'unknown')
                
                # If session was cancelled, notify participant
                if session_status == 'cancelled':
                    create_notification(
                        tables=tables,
                        citizen_username=citizen_username,
                        notification_type='meditation_cancelled',
                        title='Meditation Cancelled',
                        message=f'The {session_type} at {venue_name} was cancelled due to insufficient participants.',
                        details={
                            'session_type': session_type,
                            'venue': venue_name,
                            'leader': leader
                        }
                    )
                    
                    log.info(f"{citizen_username} arrived for cancelled meditation at {venue_name}")
                    return True
                
                # If session is completed, participant was already processed by lead_meditation
                elif session_status == 'completed':
                    log.debug(f"{citizen_username}'s meditation participation already processed")
                    return True
                
                # If session is still ongoing, mark completion
                elif session_status in ['gathering', 'in_progress']:
                    log.info(f"{citizen_username} completed meditation at {venue_name} (session ongoing)")
                    return True
                    
            except Exception as e:
                log.warning(f"Could not fetch session {session_id}: {e}")
        
        # Log participation even if session tracking failed
        log.info(f"{LogColors.OKGREEN}{citizen_username} participated in {session_type} " +
                f"at {venue_name} led by {leader}{LogColors.ENDC}")
        
        # In V1, individual processing is handled by lead_meditation_processor
        # This processor mainly ensures the activity is marked complete
        
        return True
        
    except Exception as e:
        log.error(f"Error processing join_meditation activity: {e}")
        return False


# Register processor
def process_join_meditation(tables: Dict[str, Any], activity: Dict[str, Any], venice_time: datetime) -> bool:
    """Main entry point for activity processor system."""
    return process_join_meditation_activity(tables, activity, venice_time)