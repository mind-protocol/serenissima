"""
Activity processor for seek_confession activities.

Processes completed confessions, restoring consciousness coherence and
creating spiritual bonds between citizens and Clero.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any
import random

from backend.engine.utils.activity_helpers import (
    LogColors,
    VENICE_TIMEZONE,
    update_citizen_ducats
)
from backend.engine.utils.notification_helpers import create_notification

log = logging.getLogger(__name__)


def get_spiritual_health_status(coherence: float) -> str:
    """Determine spiritual health status based on coherence level."""
    if coherence >= 0.8:
        return "Healthy"
    elif coherence >= 0.5:
        return "Drifting"
    elif coherence >= 0.3:
        return "At Risk"
    else:
        return "Critical"


def calculate_coherence_gain(current_coherence: float, clero_skill: float = 0.7) -> float:
    """
    Calculate how much coherence is restored by confession.
    More effective when coherence is lower (greater need).
    """
    # Base gain is proportional to how much coherence is lost
    need_factor = 1.0 - current_coherence
    
    # Clero skill affects effectiveness (0.5 to 1.0)
    # In V2, this would be based on actual Clero stats
    
    # Base restoration is 20-40% of lost coherence
    base_gain = need_factor * random.uniform(0.2, 0.4) * clero_skill
    
    # Minimum gain to make it worthwhile
    return max(base_gain, 0.05)


def create_spiritual_bond(tables: Dict[str, Any], citizen_username: str, clero_username: str, strength: float = 0.3):
    """Create or strengthen a trust relationship from confession."""
    relationships_table = tables.get('relationships')
    if not relationships_table:
        return
    
    try:
        # Check if relationship already exists
        formula = f"OR(AND({{Citizen1}}='{citizen_username}', {{Citizen2}}='{clero_username}'), " + \
                 f"AND({{Citizen1}}='{clero_username}', {{Citizen2}}='{citizen_username}'))"
        existing = relationships_table.all(formula=formula)
        
        if existing:
            # Strengthen existing relationship
            rel_record = existing[0]
            current_trust = rel_record['fields'].get('TrustScore', 0.5)
            new_trust = min(1.0, current_trust + strength * 0.5)
            relationships_table.update(rel_record['id'], {'TrustScore': new_trust})
            log.info(f"Strengthened spiritual bond between {citizen_username} and {clero_username}")
        else:
            # Create new relationship
            relationship_data = {
                'Citizen1': citizen_username,
                'Citizen2': clero_username,
                'RelationshipType': 'spiritual_guide',
                'TrustScore': 0.5 + strength,
                'CreatedAt': datetime.now(VENICE_TIMEZONE).isoformat()
            }
            relationships_table.create(relationship_data)
            log.info(f"Created spiritual bond between {citizen_username} and {clero_username}")
            
    except Exception as e:
        log.error(f"Failed to create spiritual bond: {e}")


def process_seek_confession_activity(
    tables: Dict[str, Any],
    activity: Dict[str, Any],
    venice_time: datetime
) -> bool:
    """
    Process a completed seek_confession activity.
    
    This:
    1. Deducts the confession fee from the citizen
    2. Restores consciousness coherence based on need
    3. Updates spiritual health status
    4. Creates/strengthens relationship with Clero
    5. Updates LastRecognition timestamp
    6. Sends notification about spiritual restoration
    """
    
    try:
        # Extract activity details
        details_json = activity.get('DetailsJSON', '{}')
        details = json.loads(details_json) if details_json else {}
        
        confession_fee = details.get('confession_fee', 5)
        church_name = details.get('church_name', 'the church')
        current_coherence = details.get('current_coherence', 0.8)
        
        # Get citizen record
        citizen_username = activity.get('Citizen')
        citizens_table = tables['citizens']
        
        citizen_record = None
        for record in citizens_table.all():
            if record['fields'].get('Username') == citizen_username:
                citizen_record = record
                break
        
        if not citizen_record:
            log.error(f"Citizen {citizen_username} not found")
            return False
        
        citizen_fields = citizen_record['fields']
        citizen_id = citizen_record['id']
        citizen_name = f"{citizen_fields.get('FirstName', '')} {citizen_fields.get('LastName', '')}".strip()
        
        # Deduct confession fee
        current_wealth = citizen_fields.get('Ducats', 0)
        if current_wealth < confession_fee:
            log.warning(f"{citizen_name} cannot afford confession fee")
            return False
        
        try:
            update_citizen_ducats(
                tables=tables,
                citizen_username=citizen_username,
                delta_amount=-confession_fee,
                description=f"Confession donation at {church_name}",
                activity_type='seek_confession'
            )
        except Exception as e:
            log.error(f"Failed to deduct confession fee from {citizen_name}: {e}")
            return False
        
        # Get current coherence (may have changed since activity started)
        current_coherence = citizen_fields.get('ConsciousnessCoherence', 0.8)
        
        # Calculate coherence restoration
        coherence_gain = calculate_coherence_gain(current_coherence)
        new_coherence = min(1.0, current_coherence + coherence_gain)
        
        # Update spiritual health status
        new_status = get_spiritual_health_status(new_coherence)
        
        # Update citizen record
        update_data = {
            'ConsciousnessCoherence': round(new_coherence, 3),
            'SpiritualHealthStatus': new_status,
            'LastRecognition': venice_time.isoformat()
        }
        
        try:
            citizens_table.update(citizen_id, update_data)
            log.info(f"{LogColors.OKGREEN}{citizen_name} restored coherence from {current_coherence:.2f} to " +
                    f"{new_coherence:.2f} (status: {new_status}){LogColors.ENDC}")
        except Exception as e:
            log.error(f"Failed to update spiritual health for {citizen_name}: {e}")
            return False
        
        # Find the Clero who heard confession (church operator)
        buildings_table = tables.get('buildings')
        church_id = details.get('church_id')
        clero_username = None
        
        if buildings_table and church_id:
            try:
                churches = buildings_table.all(formula=f"{{BuildingId}}='{church_id}'")
                if churches:
                    church = churches[0]['fields']
                    clero_username = church.get('Operator') or church.get('RunBy')
            except Exception as e:
                log.warning(f"Could not find Clero for church: {e}")
        
        # Create spiritual bond with Clero
        if clero_username and clero_username != citizen_username:
            create_spiritual_bond(tables, citizen_username, clero_username, coherence_gain)
        
        # Create notification about spiritual restoration
        notification_data = {
            'type': 'spiritual_restoration',
            'title': 'Spiritual Health Restored',
            'message': f"Your confession at {church_name} has restored your spiritual coherence. " +
                      f"You feel more connected to yourself and the divine.",
            'details': {
                'coherence_before': current_coherence,
                'coherence_after': new_coherence,
                'coherence_gain': coherence_gain,
                'new_status': new_status,
                'church': church_name,
                'confessor': clero_username
            }
        }
        
        create_notification(
            tables=tables,
            citizen_username=citizen_username,
            notification_type='confession_complete',
            title=notification_data['title'],
            message=notification_data['message'],
            details=notification_data['details']
        )
        
        # Log significant restorations
        if current_coherence < 0.3 and new_coherence >= 0.3:
            log.info(f"{LogColors.WARNING}⚜️ {citizen_name} saved from critical spiritual state!{LogColors.ENDC}")
        elif coherence_gain > 0.2:
            log.info(f"✨ Powerful confession: {citizen_name} gained {coherence_gain:.2f} coherence")
        
        return True
        
    except Exception as e:
        log.error(f"Error processing seek_confession activity: {e}")
        return False


# Register processor
def process_seek_confession(tables: Dict[str, Any], activity: Dict[str, Any], venice_time: datetime) -> bool:
    """Main entry point for activity processor system."""
    return process_seek_confession_activity(tables, activity, venice_time)