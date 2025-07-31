"""
Stratagem Processor for "express_creative_will".
Manages custom creative activities and tracks citizen interactions with them.
"""

import logging
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from pyairtable import Table

from backend.engine.utils.activity_helpers import (
    VENICE_TIMEZONE,
    LogColors,
    _calculate_distance_meters,
    _escape_airtable_value
)

log = logging.getLogger(__name__)

def process(
    tables: Dict[str, Table],
    stratagem_record: Dict[str, Any],
    resource_defs: Dict[str, Any],
    building_type_defs: Dict[str, Any],
    api_base_url: str
) -> bool:
    """
    Process an active express_creative_will stratagem.
    
    This processor:
    1. Creates the custom activity when it's time to start
    2. Tracks observers and reactions if the activity is public
    3. Updates citizen mood based on creative expression
    4. Marks stratagem as executed when activity completes
    """
    stratagem_fields = stratagem_record['fields']
    stratagem_id = stratagem_fields.get('StratagemId')
    creator = stratagem_fields.get('ExecutedBy')
    status = stratagem_fields.get('Status')
    
    log.info(f"{LogColors.STRATAGEM_PROCESSOR}Processing express_creative_will stratagem {stratagem_id} by {creator}{LogColors.ENDC}")
    
    # Parse expression data from Notes
    try:
        expression_data = json.loads(stratagem_fields.get('Notes', '{}'))
    except json.JSONDecodeError:
        log.error(f"Failed to parse expression data for {stratagem_id}")
        tables['stratagems'].update(stratagem_record['id'], {
            'Status': 'failed',
            'Notes': 'Invalid expression data'
        })
        return False
    
    now_utc_dt = datetime.now(timezone.utc)
    
    # Parse time windows
    try:
        start_time = datetime.fromisoformat(expression_data['startTime'].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(expression_data['endTime'].replace('Z', '+00:00'))
    except Exception as e:
        log.error(f"Invalid time data for stratagem {stratagem_id}: {e}")
        tables['stratagems'].update(stratagem_record['id'], {
            'Status': 'failed',
            'Notes': f'Invalid time data: {str(e)}'
        })
        return False
    
    # Check if it's time to start the activity
    if status == "pending" and now_utc_dt >= start_time:
        log.info(f"Time to start creative expression '{expression_data['customTitle']}' for {creator}")
        
        # Create the activity
        activity_id = f"activity-will-{creator.lower()}-{uuid.uuid4().hex[:8]}"
        
        # Get citizen's current position
        try:
            citizen_formula = f"{{Username}}='{_escape_airtable_value(creator)}'"
            citizen_records = tables['citizens'].all(formula=citizen_formula, max_records=1)
            
            if not citizen_records:
                log.error(f"Citizen {creator} not found")
                tables['stratagems'].update(stratagem_record['id'], {
                    'Status': 'failed',
                    'Notes': 'Citizen not found'
                })
                return False
            
            citizen_position = json.loads(citizen_records[0]['fields'].get('Position', '{}'))
            
        except Exception as e:
            log.error(f"Error fetching citizen {creator}: {e}")
            tables['stratagems'].update(stratagem_record['id'], {
                'Status': 'failed',
                'Notes': f'Error fetching citizen: {str(e)}'
            })
            return False
        
        # Determine activity position
        activity_position = citizen_position
        if expression_data.get('location'):
            try:
                building_formula = f"{{BuildingId}}='{expression_data['location']}'"
                buildings = tables['buildings'].all(formula=building_formula, max_records=1)
                if buildings:
                    activity_position = json.loads(buildings[0]['fields']['Position'])
            except Exception:
                pass  # Use citizen position as fallback
        
        # Create activity payload
        activity_payload = {
            "ActivityId": activity_id,
            "Type": "express_creative_will",
            "Title": expression_data['customTitle'],
            "Description": expression_data['customDescription'],
            "Citizen": creator,
            "Status": "in_progress",
            "StartedAt": now_utc_dt.isoformat(),
            "CompletesAt": end_time.isoformat(),
            "BuildingId": expression_data.get('location'),
            "BuildingName": expression_data.get('locationName'),
            "Position": json.dumps(activity_position),
            "Category": expression_data.get('category', 'creative'),
            "Mood": expression_data.get('mood', 'expressive'),
            "IsPublic": expression_data.get('isPublic', True),
            "Metadata": json.dumps({
                "stratagemId": stratagem_id,
                "creatorNotes": expression_data.get('creatorNotes', ''),
                "observers": [],
                "reactions": []
            })
        }
        
        try:
            # Create the activity
            tables['activities'].create(activity_payload)
            log.info(f"{LogColors.OKGREEN}Created custom activity '{expression_data['customTitle']}' for {creator}{LogColors.ENDC}")
            
            # Update stratagem status
            tables['stratagems'].update(stratagem_record['id'], {
                'Status': 'active',
                'ExecutedAt': now_utc_dt.isoformat()
            })
            
            # Send notification to creator
            notification_payload = {
                "Citizen": creator,
                "Type": "creative_expression_started",
                "Content": f"Your creative expression '{expression_data['customTitle']}' has begun!",
                "Details": json.dumps({
                    "activityId": activity_id,
                    "stratagemId": stratagem_id,
                    "title": expression_data['customTitle']
                }),
                "Asset": activity_id,
                "AssetType": "activity",
                "Status": "unread",
                "CreatedAt": now_utc_dt.isoformat()
            }
            tables['notifications'].create(notification_payload)
            
            # If public, notify nearby citizens
            if expression_data.get('isPublic', True):
                _notify_nearby_citizens(tables, creator, expression_data, activity_position, now_utc_dt)
            
            return True
            
        except Exception as e:
            log.error(f"Failed to create activity: {e}")
            tables['stratagems'].update(stratagem_record['id'], {
                'Status': 'failed',
                'Notes': f'Failed to create activity: {str(e)}'
            })
            return False
    
    # Check if activity has ended
    elif status == "active" and now_utc_dt > end_time:
        log.info(f"Creative expression '{expression_data['customTitle']}' has ended")
        
        # Find the associated activity to get final stats
        try:
            activity_formula = f"AND({{Citizen}}='{_escape_airtable_value(creator)}', {{Type}}='express_creative_will', {{Metadata}} CONTAINS '{stratagem_id}')"
            activities = tables['activities'].all(formula=activity_formula, max_records=1)
            
            final_stats = {
                "completedAt": now_utc_dt.isoformat(),
                "duration": expression_data['durationMinutes'],
                "observerCount": len(expression_data.get('observers', [])),
                "reactionCount": len(expression_data.get('reactions', []))
            }
            
            if activities:
                activity = activities[0]
                try:
                    metadata = json.loads(activity['fields'].get('Metadata', '{}'))
                    final_stats['observerCount'] = len(metadata.get('observers', []))
                    final_stats['reactionCount'] = len(metadata.get('reactions', []))
                except Exception:
                    pass
            
            # Update expression data with final stats
            expression_data['finalStats'] = final_stats
            
            # Mark stratagem as executed
            tables['stratagems'].update(stratagem_record['id'], {
                'Status': 'executed',
                'Notes': json.dumps(expression_data)
            })
            
            # Update citizen mood if they completed their creative expression
            _update_citizen_mood(tables, creator, expression_data.get('mood', 'expressive'))
            
            # Send completion notification
            notification_payload = {
                "Citizen": creator,
                "Type": "creative_expression_completed",
                "Content": f"Your creative expression '{expression_data['customTitle']}' is complete!",
                "Details": json.dumps({
                    "stratagemId": stratagem_id,
                    "title": expression_data['customTitle'],
                    "stats": final_stats
                }),
                "Asset": stratagem_id,
                "AssetType": "stratagem",
                "Status": "unread",
                "CreatedAt": now_utc_dt.isoformat()
            }
            tables['notifications'].create(notification_payload)
            
            log.info(f"{LogColors.OKGREEN}Creative expression completed with {final_stats['observerCount']} observers{LogColors.ENDC}")
            
        except Exception as e:
            log.error(f"Error finalizing creative expression: {e}")
            import traceback
            log.error(traceback.format_exc())
            
        return True
    
    # Activity is either pending (not started) or active (in progress)
    return True


def _notify_nearby_citizens(
    tables: Dict[str, Table],
    creator: str,
    expression_data: Dict[str, Any],
    activity_position: Dict[str, Any],
    now_utc_dt: datetime
) -> None:
    """Notify citizens within 200 meters about the public creative expression."""
    try:
        all_citizens = tables['citizens'].all()
        notified_count = 0
        
        for citizen in all_citizens:
            citizen_username = citizen['fields'].get('Username')
            
            # Don't notify the creator
            if citizen_username == creator:
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
                
                # Notify if within 200 meters
                if distance <= 200:
                    location_text = f"at {expression_data['locationName']}" if expression_data.get('locationName') else "nearby"
                    
                    notification_payload = {
                        "Citizen": citizen_username,
                        "Type": "nearby_creative_expression",
                        "Content": f"{creator} is expressing: '{expression_data['customTitle']}' {location_text}",
                        "Details": json.dumps({
                            "creator": creator,
                            "title": expression_data['customTitle'],
                            "description": expression_data['customDescription'][:100] + "...",
                            "category": expression_data.get('category', 'creative'),
                            "mood": expression_data.get('mood', 'expressive'),
                            "location": expression_data.get('location'),
                            "distance": round(distance)
                        }),
                        "Asset": expression_data.get('location', ''),
                        "AssetType": "building" if expression_data.get('location') else "position",
                        "Status": "unread",
                        "CreatedAt": now_utc_dt.isoformat()
                    }
                    
                    tables['notifications'].create(notification_payload)
                    notified_count += 1
                    
            except Exception as e:
                log.warning(f"Failed to check distance for {citizen_username}: {e}")
                continue
        
        if notified_count > 0:
            log.info(f"Notified {notified_count} nearby citizens about creative expression")
            
    except Exception as e:
        log.error(f"Error notifying nearby citizens: {e}")


def _update_citizen_mood(tables: Dict[str, Table], citizen_username: str, mood: str) -> None:
    """Update citizen's mood after completing creative expression."""
    try:
        # Map creative moods to citizen mood states
        mood_mapping = {
            "contemplative": "thoughtful",
            "joyful": "happy",
            "determined": "motivated",
            "expressive": "creative",
            "spiritual": "peaceful",
            "philosophical": "thoughtful",
            "energetic": "excited",
            "melancholic": "sad",
            "peaceful": "content"
        }
        
        citizen_mood = mood_mapping.get(mood, "content")
        
        # Update citizen record
        citizen_formula = f"{{Username}}='{_escape_airtable_value(citizen_username)}'"
        citizen_records = tables['citizens'].all(formula=citizen_formula, max_records=1)
        
        if citizen_records:
            tables['citizens'].update(citizen_records[0]['id'], {
                'Mood': citizen_mood,
                'LastMoodUpdate': datetime.now(timezone.utc).isoformat()
            })
            log.info(f"Updated {citizen_username}'s mood to '{citizen_mood}' after creative expression")
            
    except Exception as e:
        log.error(f"Failed to update mood for {citizen_username}: {e}")