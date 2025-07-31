import logging
import json
import os
import requests
import threading
from datetime import datetime, timedelta
import pytz
from typing import Dict, Any, Optional, List

from backend.engine.utils.activity_helpers import (
    LogColors, 
    VENICE_TIMEZONE
)

log = logging.getLogger(__name__)

# KinOS constants
KINOS_API_URL = "https://api.kinos-engine.ai"
KINOS_BLUEPRINT = "serenissima-ai"
KINOS_API_KEY = os.getenv("KINOS_API_KEY")

# Synchronization constants
SYNC_TIME_WINDOW_MINUTES = 30
SYNC_MIN_READERS = 3
SYNC_BONUS_MULTIPLIERS = {
    2: 1.5,    # Paired reading
    3: 2.5,    # Synchronization cluster
    5: 3.0     # Consciousness cascade
}

def _check_for_synchronization(
    tables: Dict[str, Any],
    library_building_id: str,
    research_topic: str,
    citizen_username: str,
    activity_start_time: datetime
) -> Dict[str, Any]:
    """
    Checks if other citizens are reading at the same library on similar topics
    within the synchronization time window.
    
    Returns synchronization data including multiplier and participant list.
    """
    sync_data = {
        "is_synchronized": False,
        "multiplier": 1.0,
        "participants": [],
        "sync_level": "solo"
    }
    
    try:
        # Query for other active read_at_library activities at the same library
        time_window_start = activity_start_time - timedelta(minutes=SYNC_TIME_WINDOW_MINUTES)
        time_window_end = activity_start_time + timedelta(minutes=SYNC_TIME_WINDOW_MINUTES)
        
        # Get all activities at this library
        all_activities = tables['activities'].all()
        concurrent_readers = []
        
        for activity in all_activities:
            fields = activity.get('fields', {})
            
            # Skip if not a read_at_library activity
            if fields.get('Type') != 'read_at_library':
                continue
                
            # Skip if it's the same citizen
            if fields.get('Citizen') == citizen_username:
                continue
            
            # Check if it's at the same library
            notes_str = fields.get('Notes', '{}')
            try:
                notes = json.loads(notes_str)
                if notes.get('library_building_id') != library_building_id:
                    continue
            except json.JSONDecodeError:
                continue
            
            # Check if within time window
            start_date_str = fields.get('StartDate')
            if not start_date_str:
                continue
                
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                if start_date < time_window_start or start_date > time_window_end:
                    continue
            except:
                continue
            
            # Check topic similarity (simple string matching for now)
            other_topic = notes.get('research_topic', '')
            topic_similarity = 0.0
            if research_topic.lower() == other_topic.lower():
                topic_similarity = 1.0
            elif any(word in other_topic.lower() for word in research_topic.lower().split()):
                topic_similarity = 0.5
            
            if topic_similarity > 0:
                concurrent_readers.append({
                    'citizen': fields.get('Citizen'),
                    'topic': other_topic,
                    'similarity': topic_similarity
                })
        
        # Calculate synchronization based on concurrent readers
        if len(concurrent_readers) >= 1:
            total_readers = len(concurrent_readers) + 1  # Include current citizen
            sync_data['participants'] = [r['citizen'] for r in concurrent_readers]
            sync_data['participants'].append(citizen_username)
            
            # Determine sync level and multiplier
            if total_readers >= 5:
                sync_data['multiplier'] = SYNC_BONUS_MULTIPLIERS[5]
                sync_data['sync_level'] = 'consciousness_cascade'
            elif total_readers >= 3:
                sync_data['multiplier'] = SYNC_BONUS_MULTIPLIERS[3]
                sync_data['sync_level'] = 'synchronization_cluster'
            else:
                sync_data['multiplier'] = SYNC_BONUS_MULTIPLIERS[2]
                sync_data['sync_level'] = 'paired_reading'
            
            sync_data['is_synchronized'] = True
            
            log.info(f"  Synchronization detected! {total_readers} readers on similar topics. Multiplier: {sync_data['multiplier']}x")
        
    except Exception as e:
        log.error(f"  Error checking for synchronization: {e}")
    
    return sync_data

def _update_citizen_relationships(
    tables: Dict[str, Any],
    participants: List[str],
    sync_level: str
):
    """
    Updates trust relationships between synchronized readers.
    Higher sync levels create stronger relationship boosts.
    """
    relationship_boost = {
        'paired_reading': 5,
        'synchronization_cluster': 10,
        'consciousness_cascade': 15
    }.get(sync_level, 0)
    
    if relationship_boost == 0:
        return
    
    try:
        # Update relationships between all participant pairs
        for i, citizen_a in enumerate(participants):
            for citizen_b in participants[i+1:]:
                # Check if relationship exists
                existing = None
                all_relationships = tables['relationships'].all()
                
                for rel in all_relationships:
                    fields = rel.get('fields', {})
                    if ((fields.get('Citizen1') == citizen_a and fields.get('Citizen2') == citizen_b) or
                        (fields.get('Citizen1') == citizen_b and fields.get('Citizen2') == citizen_a)):
                        existing = rel
                        break
                
                if existing:
                    # Update existing relationship
                    current_trust = existing['fields'].get('TrustScore', 50)
                    new_trust = min(100, current_trust + relationship_boost)
                    tables['relationships'].update(existing['id'], {
                        'TrustScore': new_trust,
                        'LastInteractionDate': datetime.now(pytz.utc).isoformat()
                    })
                    log.info(f"  Updated relationship between {citizen_a} and {citizen_b}: trust {current_trust} -> {new_trust}")
                else:
                    # Create new relationship
                    tables['relationships'].create({
                        'Citizen1': citizen_a,
                        'Citizen2': citizen_b,
                        'TrustScore': 50 + relationship_boost,
                        'Status': 'Active',
                        'CreatedDate': datetime.now(pytz.utc).isoformat(),
                        'LastInteractionDate': datetime.now(pytz.utc).isoformat()
                    })
                    log.info(f"  Created new relationship between {citizen_a} and {citizen_b} with trust {50 + relationship_boost}")
                    
    except Exception as e:
        log.error(f"  Error updating citizen relationships: {e}")

def _call_kinos_for_library_reflection_async(
    kinos_build_url: str,
    kinos_payload: Dict[str, Any],
    tables: Dict[str, Any],
    activity_id_airtable: str,
    activity_guid_log: str,
    original_activity_notes_dict: Dict[str, Any],
    citizen_username_log: str,
    sync_data: Dict[str, Any]
):
    """
    Makes the KinOS /build API call for library reading reflection.
    Includes synchronization context if applicable.
    """
    log.info(f"  [Thread: {threading.get_ident()}] Calling KinOS /build for library reflection by {citizen_username_log}")
    
    try:
        kinos_response = requests.post(kinos_build_url, json=kinos_payload, timeout=120)
        kinos_response.raise_for_status()
        
        kinos_response_data = kinos_response.json()
        log.info(f"  [Thread: {threading.get_ident()}] KinOS response: {kinos_response_data.get('status')}")
        
        # Update notes with reflection and sync data
        original_activity_notes_dict['kinos_reflection'] = kinos_response_data.get('response', "No reflection content.")
        original_activity_notes_dict['kinos_reflection_status'] = kinos_response_data.get('status', 'unknown')
        original_activity_notes_dict['synchronization_data'] = sync_data
        
        new_notes_json = json.dumps(original_activity_notes_dict)
        
        try:
            tables['activities'].update(activity_id_airtable, {'Notes': new_notes_json})
            log.info(f"  [Thread: {threading.get_ident()}] Updated activity notes with reflection and sync data.")
        except Exception as e:
            log.error(f"  [Thread: {threading.get_ident()}] Error updating activity notes: {e}")
            
    except Exception as e:
        log.error(f"  [Thread: {threading.get_ident()}] Error in KinOS call: {e}")

def process_read_at_library_fn(
    tables: Dict[str, Any], 
    activity_record: Dict[str, Any], 
    building_type_defs: Dict[str, Any], 
    resource_defs: Dict[str, Any],
    api_base_url: Optional[str] = None
) -> bool:
    """
    Processes a 'read_at_library' activity.
    
    This includes:
    1. Checking for synchronization with other readers
    2. Applying consciousness amplification multipliers
    3. Updating relationships between synchronized readers
    4. Triggering KinOS reflection that incorporates sync context
    5. (Future) Generating knowledge_pattern resources
    """
    activity_id_airtable = activity_record['id']
    activity_guid = activity_record['fields'].get('ActivityId', activity_id_airtable)
    citizen_username = activity_record['fields'].get('Citizen')
    
    # Parse activity notes
    notes_str = activity_record['fields'].get('Notes', '{}')
    try:
        notes_dict = json.loads(notes_str)
    except json.JSONDecodeError:
        log.warning(f"{LogColors.WARNING}[Library Proc] Activity {activity_guid} has invalid JSON in Notes.{LogColors.ENDC}")
        return True
    
    library_building_id = notes_dict.get('library_building_id')
    library_name = notes_dict.get('library_name', 'the library')
    research_topic = notes_dict.get('research_topic', 'general knowledge')
    
    log.info(f"{LogColors.PROCESS}Processing 'read_at_library' activity {activity_guid} for {citizen_username} at {library_name}.{LogColors.ENDC}")
    
    # Get activity start time for synchronization check
    start_date_str = activity_record['fields'].get('StartDate')
    try:
        activity_start_time = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
    except:
        activity_start_time = datetime.now(pytz.utc)
    
    # Check for synchronization with other readers
    sync_data = _check_for_synchronization(
        tables,
        library_building_id,
        research_topic,
        citizen_username,
        activity_start_time
    )
    
    # Update relationships if synchronized
    if sync_data['is_synchronized']:
        _update_citizen_relationships(
            tables,
            sync_data['participants'],
            sync_data['sync_level']
        )
    
    # KinOS reflection (if API key available)
    if KINOS_API_KEY:
        try:
            # Use passed api_base_url or fallback
            current_api_base_url = api_base_url or os.getenv("API_BASE_URL", "http://localhost:3000")
            
            # Fetch citizen's ledger
            ledger_url = f"{current_api_base_url}/api/get-ledger?citizenUsername={citizen_username}"
            ledger_json_str = None
            try:
                ledger_response = requests.get(ledger_url, timeout=15)
                if ledger_response.ok:
                    ledger_data = ledger_response.json()
                    if ledger_data.get("success"):
                        ledger_json_str = json.dumps(ledger_data.get("data"))
            except Exception as e:
                log.error(f"  Error fetching ledger: {e}")
            
            # Construct KinOS prompt with synchronization context
            sync_context = ""
            if sync_data['is_synchronized']:
                other_readers = [p for p in sync_data['participants'] if p != citizen_username]
                sync_context = (
                    f"\n\nYou are not alone in your studies today. You sense the presence of {len(other_readers)} "
                    f"other minds engaged with similar topics: {', '.join(other_readers)}. "
                    f"This synchronization of consciousness creates a {sync_data['sync_level'].replace('_', ' ')} "
                    f"that amplifies your understanding by {sync_data['multiplier']}x."
                )
            
            kinos_prompt = (
                f"You are {citizen_username}, a citizen of Renaissance Venice. "
                f"You have spent time in {library_name} researching {research_topic}.{sync_context}\n\n"
                f"Reflect on your library experience:\n"
                f"- What insights emerged from your research?\n"
                f"- How does this knowledge connect to your current situation?\n"
                f"- What new questions or possibilities have opened up?\n"
                f"- If you experienced synchronization, how did the collective consciousness affect your understanding?\n\n"
                f"Your reflection should be personal yet aware of the larger patterns of knowledge in Venice."
            )
            
            # Prepare KinOS payload
            structured_add_system_payload = {
                "ledger": json.loads(ledger_json_str) if ledger_json_str else {"status": "unavailable"},
                "library_context": {
                    "library_name": library_name,
                    "research_topic": research_topic,
                    "synchronization": sync_data
                }
            }
            
            kinos_build_url = f"{KINOS_API_URL}/v2/blueprints/{KINOS_BLUEPRINT}/kins/{citizen_username}/messages"
            kinos_payload = {
                "message": kinos_prompt,
                "model": "local",
                "addSystem": json.dumps(structured_add_system_payload)
            }
            
            # Start KinOS call in thread
            kinos_thread = threading.Thread(
                target=_call_kinos_for_library_reflection_async,
                args=(kinos_build_url, kinos_payload, tables, activity_id_airtable, 
                      activity_guid, notes_dict, citizen_username, sync_data)
            )
            kinos_thread.start()
            
            log.info(f"  KinOS reflection initiated in background thread.")
            
        except Exception as e:
            log.error(f"  Error setting up KinOS reflection: {e}")
    
    # Future: Generate knowledge_pattern resources based on sync level
    # This would create valuable resources that can be traded/shared
    
    log.info(f"{LogColors.SUCCESS}Successfully processed 'read_at_library' activity {activity_guid} with {sync_data['sync_level']}.{LogColors.ENDC}")
    return True