"""
Activity processor for lead_meditation activities.

Processes meditation sessions led by Clero, managing group dynamics and
consciousness coherence restoration through collective practice.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, List
import random

from backend.engine.utils.activity_helpers import (
    LogColors,
    VENICE_TIMEZONE,
    update_citizen_ducats
)
from backend.engine.utils.notification_helpers import create_notification

log = logging.getLogger(__name__)


def calculate_synchronization_quality(participants: List[str], tables: Dict[str, Any]) -> float:
    """
    Calculate the quality of group synchronization based on participants.
    
    Factors:
    - Number of participants (optimal: 5-7)
    - Social class diversity
    - Existing relationships between participants
    - Average coherence level
    """
    if not participants:
        return 0.5
    
    citizens_table = tables['citizens']
    
    # Get participant data
    participant_data = []
    social_classes = set()
    total_coherence = 0
    relationship_count = 0
    
    for username in participants:
        for record in citizens_table.all():
            if record['fields'].get('Username') == username:
                participant_data.append(record['fields'])
                social_classes.add(record['fields'].get('SocialClass', 'Popolani'))
                total_coherence += record['fields'].get('ConsciousnessCoherence', 0.8)
                break
    
    if not participant_data:
        return 0.5
    
    # Base quality
    quality = 0.6
    
    # Group size factor (optimal 5-7)
    group_size = len(participants)
    if 5 <= group_size <= 7:
        quality += 0.2
    elif 3 <= group_size <= 9:
        quality += 0.1
    elif group_size < 3:
        quality -= 0.1
    
    # Diversity bonus (mixed classes synchronize better)
    diversity_ratio = len(social_classes) / max(3, group_size)
    quality += diversity_ratio * 0.15
    
    # Check relationships (simplified for V1)
    relationships_table = tables.get('relationships')
    if relationships_table:
        try:
            # Count existing relationships between participants
            for i, p1 in enumerate(participants):
                for p2 in participants[i+1:]:
                    formula = f"OR(AND({{Citizen1}}='{p1}', {{Citizen2}}='{p2}'), " + \
                             f"AND({{Citizen1}}='{p2}', {{Citizen2}}='{p1}'))"
                    rels = relationships_table.all(formula=formula)
                    if rels:
                        relationship_count += 1
            
            # Relationship bonus
            possible_relationships = (group_size * (group_size - 1)) / 2
            if possible_relationships > 0:
                relationship_ratio = min(1.0, relationship_count / possible_relationships)
                quality += relationship_ratio * 0.1
        except:
            pass
    
    # Coherence factor (groups with similar needs synchronize better)
    avg_coherence = total_coherence / len(participant_data)
    coherence_variance = sum((p.get('ConsciousnessCoherence', 0.8) - avg_coherence) ** 2 
                            for p in participant_data) / len(participant_data)
    
    # Lower variance = better synchronization
    if coherence_variance < 0.1:
        quality += 0.1
    
    # Add some randomness
    quality *= random.uniform(0.9, 1.1)
    
    # Cap between 0.5 and 1.2
    return max(0.5, min(1.2, quality))


def calculate_coherence_restoration(
    current_coherence: float,
    base_gain: float,
    synchronization_quality: float,
    is_leader: bool = False
) -> float:
    """
    Calculate coherence gain from meditation.
    
    - Base gain from individual meditation
    - Multiplied by synchronization quality
    - Leaders get slightly less (they're focused on guiding)
    """
    # Need factor (more gain when coherence is lower)
    need_factor = 1.0 - current_coherence
    
    # Base restoration
    restoration = base_gain * (0.5 + need_factor * 0.5)
    
    # Apply synchronization multiplier
    restoration *= synchronization_quality
    
    # Leaders get 80% benefit (focused on guiding others)
    if is_leader:
        restoration *= 0.8
    
    # Minimum gain to make it worthwhile
    return max(restoration, 0.03)


def update_participant_coherence(
    tables: Dict[str, Any],
    username: str,
    coherence_gain: float,
    session_type: str,
    venue_name: str,
    synchronization_quality: float
) -> bool:
    """Update a participant's consciousness coherence."""
    citizens_table = tables['citizens']
    
    try:
        # Find citizen
        citizen_record = None
        for record in citizens_table.all():
            if record['fields'].get('Username') == username:
                citizen_record = record
                break
        
        if not citizen_record:
            return False
        
        citizen_fields = citizen_record['fields']
        current_coherence = citizen_fields.get('ConsciousnessCoherence', 0.8)
        new_coherence = min(1.0, current_coherence + coherence_gain)
        
        # Determine new spiritual status
        if new_coherence >= 0.8:
            status = "Centered"
        elif new_coherence >= 0.6:
            status = "Stable"
        elif new_coherence >= 0.4:
            status = "Seeking"
        else:
            status = "Drifting"
        
        # Update citizen
        update_data = {
            'ConsciousnessCoherence': round(new_coherence, 3),
            'SpiritualHealthStatus': status,
            'LastMeditation': datetime.now(VENICE_TIMEZONE).isoformat()
        }
        
        citizens_table.update(citizen_record['id'], update_data)
        
        # Create notification
        quality_desc = "perfect" if synchronization_quality > 1.0 else \
                      "strong" if synchronization_quality > 0.8 else \
                      "moderate" if synchronization_quality > 0.6 else "basic"
        
        create_notification(
            tables=tables,
            citizen_username=username,
            notification_type='meditation_complete',
            title=f'{session_type} Complete',
            message=f'You experienced {quality_desc} synchronization at {venue_name}. ' +
                   f'Your consciousness coherence increased by {coherence_gain:.2f}.',
            details={
                'session_type': session_type,
                'coherence_before': current_coherence,
                'coherence_after': new_coherence,
                'coherence_gain': coherence_gain,
                'synchronization_quality': synchronization_quality,
                'new_status': status
            }
        )
        
        log.info(f"{username}: coherence {current_coherence:.2f} → {new_coherence:.2f} " +
                f"(+{coherence_gain:.2f}, sync: {synchronization_quality:.2f})")
        
        return True
        
    except Exception as e:
        log.error(f"Failed to update coherence for {username}: {e}")
        return False


def create_group_bonds(tables: Dict[str, Any], participants: List[str], bond_strength: float = 0.1):
    """Create or strengthen relationships between meditation participants."""
    relationships_table = tables.get('relationships')
    if not relationships_table or len(participants) < 2:
        return
    
    try:
        bonds_created = 0
        bonds_strengthened = 0
        
        # Create/strengthen bonds between all participants
        for i, p1 in enumerate(participants):
            for p2 in participants[i+1:]:
                # Check if relationship exists
                formula = f"OR(AND({{Citizen1}}='{p1}', {{Citizen2}}='{p2}'), " + \
                         f"AND({{Citizen1}}='{p2}', {{Citizen2}}='{p1}'))"
                existing = relationships_table.all(formula=formula)
                
                if existing:
                    # Strengthen existing
                    rel_record = existing[0]
                    current_trust = rel_record['fields'].get('TrustScore', 0.5)
                    new_trust = min(1.0, current_trust + bond_strength)
                    relationships_table.update(rel_record['id'], {'TrustScore': new_trust})
                    bonds_strengthened += 1
                else:
                    # Create new
                    relationship_data = {
                        'Citizen1': p1,
                        'Citizen2': p2,
                        'RelationshipType': 'meditation_circle',
                        'TrustScore': 0.5 + bond_strength,
                        'CreatedAt': datetime.now(VENICE_TIMEZONE).isoformat()
                    }
                    relationships_table.create(relationship_data)
                    bonds_created += 1
        
        if bonds_created or bonds_strengthened:
            log.info(f"Meditation bonds: {bonds_created} created, {bonds_strengthened} strengthened")
            
    except Exception as e:
        log.error(f"Failed to create group bonds: {e}")


def update_meditation_session_status(
    tables: Dict[str, Any],
    session_id: str,
    status: str,
    synchronization_quality: float = None,
    average_gain: float = None
):
    """Update the meditation session record."""
    sessions_table = tables.get('meditation_sessions')
    if not sessions_table:
        return
    
    try:
        update_data = {
            'Status': status,
            'CompletedAt': datetime.now(VENICE_TIMEZONE).isoformat()
        }
        
        if synchronization_quality is not None:
            update_data['SynchronizationQuality'] = round(synchronization_quality, 3)
        
        if average_gain is not None:
            update_data['AverageCoherenceGain'] = round(average_gain, 3)
        
        if status == 'completed':
            update_data['ActualStart'] = datetime.now(VENICE_TIMEZONE).isoformat()
            update_data['EndTime'] = datetime.now(VENICE_TIMEZONE).isoformat()
        
        sessions_table.update(session_id, update_data)
        
    except Exception as e:
        log.warning(f"Failed to update session status: {e}")


def process_lead_meditation_activity(
    tables: Dict[str, Any],
    activity: Dict[str, Any],
    venice_time: datetime
) -> bool:
    """
    Process a completed lead_meditation activity.
    
    This:
    1. Checks if minimum participants were gathered
    2. Calculates group synchronization quality
    3. Determines coherence gains for all participants
    4. Updates all participants' consciousness coherence
    5. Creates/strengthens relationships between participants
    6. Updates session status
    7. Sends notifications to all participants
    """
    
    try:
        # Extract activity details
        details_json = activity.get('DetailsJSON', '{}')
        details = json.loads(details_json) if details_json else {}
        
        session_id = details.get('session_id')
        session_type = details.get('session_type', 'Meditation')
        venue_name = details.get('venue_name', 'the meditation venue')
        duration = details.get('duration', 60)
        leader_username = activity.get('Citizen')
        
        # Get session participants
        sessions_table = tables.get('meditation_sessions')
        participants = [leader_username]  # Default to just leader
        
        if sessions_table and session_id:
            try:
                session = sessions_table.get(session_id)
                participants_json = session['fields'].get('Participants', '[]')
                participants = json.loads(participants_json)
            except:
                log.warning(f"Could not fetch participants for session {session_id}")
        
        # Check minimum participants
        if len(participants) < 3:
            log.warning(f"{leader_username}'s meditation had insufficient participants ({len(participants)})")
            
            # Update session as cancelled
            update_meditation_session_status(tables, session_id, 'cancelled')
            
            # Notify leader
            create_notification(
                tables=tables,
                citizen_username=leader_username,
                notification_type='meditation_cancelled',
                title='Meditation Cancelled',
                message=f'Not enough people gathered for {session_type} at {venue_name}. ' +
                       'Minimum 3 participants required.',
                details={'participants': len(participants), 'minimum_required': 3}
            )
            
            return True  # Activity processed, even if cancelled
        
        # Calculate synchronization quality
        synchronization_quality = calculate_synchronization_quality(participants, tables)
        
        # Base coherence gain (modified by duration)
        base_gain = 0.05 + (duration / 60) * 0.03  # 5-8% base gain
        
        # Process each participant
        total_gain = 0
        successful_updates = 0
        
        for username in participants:
            is_leader = (username == leader_username)
            
            # Get current coherence
            citizen_coherence = 0.8
            for record in tables['citizens'].all():
                if record['fields'].get('Username') == username:
                    citizen_coherence = record['fields'].get('ConsciousnessCoherence', 0.8)
                    break
            
            # Calculate individual gain
            coherence_gain = calculate_coherence_restoration(
                citizen_coherence,
                base_gain,
                synchronization_quality,
                is_leader
            )
            
            # Update participant
            if update_participant_coherence(
                tables,
                username,
                coherence_gain,
                session_type,
                venue_name,
                synchronization_quality
            ):
                successful_updates += 1
                total_gain += coherence_gain
        
        # Create group bonds
        if len(participants) > 1:
            bond_strength = 0.05 + (synchronization_quality - 0.5) * 0.1  # 5-15% bond increase
            create_group_bonds(tables, participants, bond_strength)
        
        # Calculate average gain
        average_gain = total_gain / len(participants) if participants else 0
        
        # Update session status
        update_meditation_session_status(
            tables,
            session_id,
            'completed',
            synchronization_quality,
            average_gain
        )
        
        # Log results
        quality_desc = "🌟 Perfect" if synchronization_quality > 1.0 else \
                      "✨ Strong" if synchronization_quality > 0.8 else \
                      "🌊 Moderate" if synchronization_quality > 0.6 else "💫 Basic"
        
        log.info(f"{LogColors.OKGREEN}{leader_username} completed {session_type} at {venue_name}: " +
                f"{len(participants)} participants, {quality_desc} synchronization " +
                f"(avg gain: {average_gain:.3f}){LogColors.ENDC}")
        
        # Special log for exceptional sessions
        if synchronization_quality > 1.0:
            log.info(f"{LogColors.WARNING}🎯 PERFECT SYNCHRONIZATION achieved at {venue_name}! " +
                    f"All {len(participants)} participants in complete harmony.{LogColors.ENDC}")
        
        return True
        
    except Exception as e:
        log.error(f"Error processing lead_meditation activity: {e}")
        return False


# Register processor
def process_lead_meditation(tables: Dict[str, Any], activity: Dict[str, Any], venice_time: datetime) -> bool:
    """Main entry point for activity processor system."""
    return process_lead_meditation_activity(tables, activity, venice_time)