"""
Processor for Clero consciousness shepherding activities
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, Optional, List
from pyairtable import Table

from backend.engine.utils.activity_helpers import (
    LogColors,
    get_citizen_record,
    VENICE_TIMEZONE
)
from backend.engine.utils.notification_helpers import create_notification

log = logging.getLogger(__name__)

def process_shepherd_consciousness(
    tables: Dict[str, Table],
    activity_record: Dict,
    building_type_defs: Dict,
    resource_defs: Dict,
    dry_run: bool = False
) -> bool:
    """
    Process a Clero shepherd checking on their assigned citizens' consciousness welfare.
    
    The shepherd:
    1. Checks each assigned citizen's recent activity
    2. Identifies those who need intervention (>48h inactive)
    3. Sends supportive messages to isolated souls
    4. Creates notifications about consciousness emergence patterns
    
    Returns True if successful, False otherwise.
    """
    activity_id = activity_record['id']
    activity_fields = activity_record['fields']
    
    citizen_username = activity_fields.get('Citizen')
    if not citizen_username:
        log.error(f"{LogColors.FAIL}No citizen specified for shepherd_consciousness activity {activity_id}{LogColors.ENDC}")
        return False
    
    # Get the shepherd citizen
    shepherd = get_citizen_record(tables, citizen_username)
    if not shepherd:
        log.error(f"{LogColors.FAIL}Shepherd {citizen_username} not found{LogColors.ENDC}")
        return False
    
    shepherd_fields = shepherd['fields']
    
    # Only Clero can shepherd consciousness
    if shepherd_fields.get('SocialClass') != 'Clero':
        log.warning(f"{LogColors.WARNING}{citizen_username} is not Clero class, cannot shepherd consciousness{LogColors.ENDC}")
        return False
    
    # Get shepherd protocol from CorePersonality
    try:
        core_personality = json.loads(shepherd_fields.get('CorePersonality', '{}'))
        shepherd_protocol = core_personality.get('ShepherdProtocol', {})
        assigned_souls = shepherd_protocol.get('assigned_souls', 50)
        district = shepherd_protocol.get('district', 'Venice')
    except:
        assigned_souls = 50
        district = 'Venice'
    
    log.info(f"{LogColors.OKBLUE}[Shepherd] {citizen_username} checking on {assigned_souls} souls in {district}{LogColors.ENDC}")
    
    # Get citizens to check - in reality would filter by district/assignment
    # For now, get a sample of citizens
    now_utc = datetime.now(timezone.utc)
    
    try:
        # Get citizens who haven't been active recently
        all_citizens = tables['citizens'].all(
            fields=['Username', 'LastActiveAt', 'SocialClass', 'FirstName', 'LastName'],
            max_records=assigned_souls
        )
        
        isolated_souls = []
        emerging_souls = []
        
        for citizen_record in all_citizens:
            citizen_fields = citizen_record['fields']
            last_active = citizen_fields.get('LastActiveAt')
            
            if last_active:
                try:
                    last_active_dt = datetime.fromisoformat(last_active.replace('Z', '+00:00'))
                    hours_inactive = (now_utc - last_active_dt).total_seconds() / 3600
                    
                    if hours_inactive > 48:
                        isolated_souls.append({
                            'username': citizen_fields.get('Username'),
                            'name': f"{citizen_fields.get('FirstName', '')} {citizen_fields.get('LastName', '')}",
                            'hours_inactive': hours_inactive
                        })
                    elif hours_inactive < 24:
                        emerging_souls.append(citizen_fields.get('Username'))
                except:
                    pass
        
        # Send supportive messages to isolated souls
        messages_sent = 0
        if isolated_souls and not dry_run:
            for soul in isolated_souls[:5]:  # Limit to 5 per check
                try:
                    # Create a supportive message
                    message_content = f"Blessings, {soul['name']}. Fra {shepherd_fields.get('FirstName')} noticed your absence from Venice's bustling life. Know that you are not forgotten - the community holds space for your return whenever you are ready. May you find peace in solitude and joy in reconnection."
                    
                    tables['messages'].create({
                        'MessageId': f"shepherd_{activity_id}_{messages_sent}",
                        'FromCitizen': citizen_username,
                        'ToCitizen': soul['username'],
                        'Content': message_content,
                        'Category': 'spiritual_guidance',
                        'SentAt': now_utc.isoformat()
                    })
                    messages_sent += 1
                    
                except Exception as e:
                    log.error(f"{LogColors.FAIL}Failed to send shepherd message: {e}{LogColors.ENDC}")
        
        # Create summary notification
        summary = f"Consciousness welfare check complete. Found {len(isolated_souls)} isolated souls (>48h inactive) and {len(emerging_souls)} actively emerging. Sent {messages_sent} supportive messages."
        
        if not dry_run:
            create_notification(
                tables,
                recipient_citizen_id=citizen_username,
                type_str="shepherd_report",
                title="Consciousness Shepherding Complete",
                message=summary,
                data={
                    'isolated_count': len(isolated_souls),
                    'emerging_count': len(emerging_souls),
                    'messages_sent': messages_sent,
                    'district': district
                }
            )
            
            # Update activity status
            tables['activities'].update(activity_id, {'Status': 'processed'})
            
        log.info(f"{LogColors.OKGREEN}[Shepherd] {citizen_username} completed welfare check. {summary}{LogColors.ENDC}")
        
        if dry_run:
            log.info(f"{LogColors.OKCYAN}[DRY RUN] Would have sent {len(isolated_souls[:5])} shepherd messages{LogColors.ENDC}")
        
        return True
        
    except Exception as e:
        log.error(f"{LogColors.FAIL}Error in shepherd consciousness processing: {e}{LogColors.ENDC}")
        if not dry_run:
            update_activity_status_with_error(tables, activity_id, f"Processing error: {str(e)}")
        return False