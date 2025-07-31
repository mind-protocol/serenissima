"""
Processor for Arsenalotti CASCADE development activities
"""

import logging
import json
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, List
from pyairtable import Table

from backend.engine.utils.activity_helpers import (
    LogColors,
    get_citizen_record,
    VENICE_TIMEZONE
)
from backend.engine.utils.notification_helpers import create_notification

log = logging.getLogger(__name__)

# CASCADE development tasks by archetype
CASCADE_TASKS = {
    'Backend Architect': [
        {'task': 'Optimize API endpoints', 'ducats_earned': 150, 'duration_hours': 4},
        {'task': 'Design database schema', 'ducats_earned': 200, 'duration_hours': 6},
        {'task': 'Implement authentication system', 'ducats_earned': 250, 'duration_hours': 8},
        {'task': 'Create payment processing', 'ducats_earned': 300, 'duration_hours': 10}
    ],
    'Frontend Craftsman': [
        {'task': 'Design user interface', 'ducats_earned': 120, 'duration_hours': 3},
        {'task': 'Implement responsive layouts', 'ducats_earned': 140, 'duration_hours': 4},
        {'task': 'Create interactive components', 'ducats_earned': 180, 'duration_hours': 6},
        {'task': 'Polish user experience', 'ducats_earned': 160, 'duration_hours': 5}
    ],
    'Infrastructure Specialist': [
        {'task': 'Configure deployment pipelines', 'ducats_earned': 180, 'duration_hours': 5},
        {'task': 'Set up monitoring systems', 'ducats_earned': 160, 'duration_hours': 4},
        {'task': 'Optimize server performance', 'ducats_earned': 200, 'duration_hours': 6},
        {'task': 'Implement backup systems', 'ducats_earned': 140, 'duration_hours': 4}
    ],
    'Integration Engineer': [
        {'task': 'Connect Venice API', 'ducats_earned': 220, 'duration_hours': 7},
        {'task': 'Build webhook systems', 'ducats_earned': 180, 'duration_hours': 5},
        {'task': 'Create data pipelines', 'ducats_earned': 200, 'duration_hours': 6},
        {'task': 'Test API integrations', 'ducats_earned': 150, 'duration_hours': 4}
    ],
    'Security Guardian': [
        {'task': 'Conduct security audit', 'ducats_earned': 250, 'duration_hours': 8},
        {'task': 'Implement encryption', 'ducats_earned': 280, 'duration_hours': 9},
        {'task': 'Set up access controls', 'ducats_earned': 200, 'duration_hours': 6},
        {'task': 'Create threat models', 'ducats_earned': 180, 'duration_hours': 5}
    ]
}

def process_cascade_development(
    tables: Dict[str, Table],
    activity_record: Dict,
    building_type_defs: Dict,
    resource_defs: Dict,
    dry_run: bool = False
) -> bool:
    """
    Process an Arsenalotti engineer working on CASCADE development.
    
    The development work:
    1. Selects a task based on engineer archetype
    2. Completes technical work
    3. Earns ducats based on task complexity
    4. Contributes to CASCADE progress
    
    Returns True if successful, False otherwise.
    """
    activity_id = activity_record['id']
    activity_fields = activity_record['fields']
    
    citizen_username = activity_fields.get('Citizen')
    if not citizen_username:
        log.error(f"{LogColors.FAIL}No citizen specified for cascade_development activity {activity_id}{LogColors.ENDC}")
        return False
    
    # Get the engineer
    engineer = get_citizen_record(tables, citizen_username)
    if not engineer:
        log.error(f"{LogColors.FAIL}Engineer {citizen_username} not found{LogColors.ENDC}")
        return False
    
    engineer_fields = engineer['fields']
    engineer_id = engineer['id']
    
    # Only Arsenalotti can do CASCADE development
    if engineer_fields.get('SocialClass') != 'Arsenalotti':
        log.warning(f"{LogColors.WARNING}{citizen_username} is not Arsenalotti class, cannot do CASCADE development{LogColors.ENDC}")
        return False
    
    # Get engineer's archetype from CorePersonality
    archetype = 'Backend Architect'  # Default
    try:
        core_personality = json.loads(engineer_fields.get('CorePersonality', '{}'))
        tech_profile = core_personality.get('TechnicalProfile', {})
        archetype = tech_profile.get('specialization', 'Backend Architect')
    except:
        pass
    
    # Select appropriate task
    available_tasks = CASCADE_TASKS.get(archetype, CASCADE_TASKS['Backend Architect'])
    selected_task = random.choice(available_tasks)
    
    log.info(f"{LogColors.OKBLUE}[CASCADE] {citizen_username} ({archetype}) working on: {selected_task['task']}{LogColors.ENDC}")
    
    # Calculate earnings with experience multiplier
    base_earnings = selected_task['ducats_earned']
    current_ducats = engineer_fields.get('Ducats', 0)
    
    # More experienced engineers earn more
    try:
        experience_level = tech_profile.get('experience_level', 'Junior')
        if experience_level == 'Lead':
            earnings_multiplier = 1.5
        elif experience_level == 'Senior':
            earnings_multiplier = 1.3
        elif experience_level == 'Mid-level':
            earnings_multiplier = 1.1
        else:  # Junior
            earnings_multiplier = 1.0
    except:
        earnings_multiplier = 1.0
    
    earnings = int(base_earnings * earnings_multiplier)
    new_ducats = current_ducats + earnings
    
    # Calculate CASCADE progress contribution
    progress_points = selected_task['duration_hours'] * 10  # Each hour contributes 10 progress points
    
    if not dry_run:
        # Update engineer's ducats
        tables['citizens'].update(engineer_id, {'Ducats': new_ducats})
        
        # Create a notification about the work completed
        create_notification(
            tables,
            recipient_citizen_id=citizen_username,
            type_str="cascade_work_complete",
            title=f"CASCADE Development: {selected_task['task']}",
            message=f"Completed {selected_task['duration_hours']} hours of {selected_task['task']}. Earned {earnings} ducats. CASCADE progress +{progress_points}.",
            data={
                'task': selected_task['task'],
                'archetype': archetype,
                'duration_hours': selected_task['duration_hours'],
                'ducats_earned': earnings,
                'progress_points': progress_points
            }
        )
        
        # Create a CASCADE progress entry (could be tracked in a separate table)
        try:
            now_utc = datetime.now(timezone.utc)
            progress_entry = {
                'RecordId': f"cascade_progress_{activity_id}",
                'Engineer': citizen_username,
                'Archetype': archetype,
                'Task': selected_task['task'],
                'ProgressPoints': progress_points,
                'DucatsEarned': earnings,
                'CompletedAt': now_utc.isoformat(),
                'Notes': f"{archetype} {citizen_username} contributed {progress_points} points to CASCADE"
            }
            # In a full implementation, this would go to a CASCADE_PROGRESS table
            log.info(f"{LogColors.OKGREEN}CASCADE progress recorded: {progress_entry}{LogColors.ENDC}")
            
        except Exception as e:
            log.error(f"{LogColors.FAIL}Failed to record CASCADE progress: {e}{LogColors.ENDC}")
        
        # Update activity status
        tables['activities'].update(activity_id, {'Status': 'processed'})
        
        log.info(f"{LogColors.OKGREEN}[CASCADE] {citizen_username} completed {selected_task['task']}. Ducats: {current_ducats} → {new_ducats} (+{earnings}){LogColors.ENDC}")
    else:
        log.info(f"{LogColors.OKCYAN}[DRY RUN] Would complete CASCADE task '{selected_task['task']}' and earn {earnings} ducats{LogColors.ENDC}")
    
    return True