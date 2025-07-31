"""
Processor for Amministratori administrative duties
"""

import logging
import json
import random
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

# Administrative tasks by archetype
ADMIN_TASKS = {
    'Census Master': [
        {'task': 'Update citizen records', 'documents': 20, 'accuracy_required': 0.95},
        {'task': 'Verify new registrations', 'documents': 15, 'accuracy_required': 0.98},
        {'task': 'Compile demographic reports', 'documents': 5, 'accuracy_required': 0.9},
        {'task': 'Process address changes', 'documents': 10, 'accuracy_required': 0.95}
    ],
    'Treasury Clerk': [
        {'task': 'Record CASCADE revenue', 'documents': 30, 'accuracy_required': 0.99},
        {'task': 'Audit financial transactions', 'documents': 25, 'accuracy_required': 0.98},
        {'task': 'Prepare tax assessments', 'documents': 15, 'accuracy_required': 0.97},
        {'task': 'Balance daily ledgers', 'documents': 40, 'accuracy_required': 0.99}
    ],
    'Permit Officer': [
        {'task': 'Review business licenses', 'documents': 12, 'accuracy_required': 0.95},
        {'task': 'Process vendor permits', 'documents': 18, 'accuracy_required': 0.93},
        {'task': 'Inspect compliance documents', 'documents': 10, 'accuracy_required': 0.96},
        {'task': 'Issue CASCADE vendor licenses', 'documents': 8, 'accuracy_required': 0.97}
    ],
    'District Coordinator': [
        {'task': 'Facilitate district meetings', 'documents': 5, 'accuracy_required': 0.9},
        {'task': 'Resolve citizen disputes', 'documents': 8, 'accuracy_required': 0.92},
        {'task': 'Coordinate resource distribution', 'documents': 12, 'accuracy_required': 0.94},
        {'task': 'Compile district reports', 'documents': 6, 'accuracy_required': 0.91}
    ],
    'Innovation Registrar': [
        {'task': 'Document CASCADE features', 'documents': 10, 'accuracy_required': 0.96},
        {'task': 'Register new innovations', 'documents': 7, 'accuracy_required': 0.97},
        {'task': 'Track patent applications', 'documents': 5, 'accuracy_required': 0.98},
        {'task': 'Maintain knowledge archives', 'documents': 15, 'accuracy_required': 0.95}
    ]
}

def process_administrative_duties(
    tables: Dict[str, Table],
    activity_record: Dict,
    building_type_defs: Dict,
    resource_defs: Dict,
    dry_run: bool = False
) -> bool:
    """
    Process an Administrator performing their governance duties.
    
    The administrative work:
    1. Selects tasks based on administrator archetype
    2. Processes documents with required accuracy
    3. Earns modest salary for public service
    4. Maintains Venice's bureaucratic efficiency
    
    Returns True if successful, False otherwise.
    """
    activity_id = activity_record['id']
    activity_fields = activity_record['fields']
    
    citizen_username = activity_fields.get('Citizen')
    if not citizen_username:
        log.error(f"{LogColors.FAIL}No citizen specified for administrative_duties activity {activity_id}{LogColors.ENDC}")
        return False
    
    # Get the administrator
    admin = get_citizen_record(tables, citizen_username)
    if not admin:
        log.error(f"{LogColors.FAIL}Administrator {citizen_username} not found{LogColors.ENDC}")
        return False
    
    admin_fields = admin['fields']
    admin_id = admin['id']
    
    # Only Amministratori can perform administrative duties
    if admin_fields.get('SocialClass') != 'Amministratori':
        log.warning(f"{LogColors.WARNING}{citizen_username} is not Amministratori class, cannot perform administrative duties{LogColors.ENDC}")
        return False
    
    # Get administrator's archetype
    archetype = 'Census Master'  # Default
    try:
        core_personality = json.loads(admin_fields.get('CorePersonality', '{}'))
        admin_profile = core_personality.get('AdministrativeProfile', {})
        archetype = admin_profile.get('specialization', 'Census Master')
    except:
        pass
    
    # Select appropriate task
    available_tasks = ADMIN_TASKS.get(archetype, ADMIN_TASKS['Census Master'])
    selected_task = random.choice(available_tasks)
    
    log.info(f"{LogColors.OKBLUE}[Admin] {citizen_username} ({archetype}) working on: {selected_task['task']}{LogColors.ENDC}")
    
    # Calculate documents processed based on experience
    try:
        experience = admin_profile.get('experience_level', 'Junior Clerk')
        capacity = admin_profile.get('daily_capacity', {'documents_processed': 50})
        base_capacity = capacity.get('documents_processed', 50)
        
        if experience == 'Master Administrator':
            efficiency = 1.2
        elif experience == 'Department Head':
            efficiency = 1.1
        elif experience == 'Senior Clerk':
            efficiency = 1.0
        else:  # Junior Clerk
            efficiency = 0.8
    except:
        efficiency = 1.0
        base_capacity = 50
    
    # Process documents with accuracy check
    documents_to_process = selected_task['documents']
    accuracy_achieved = random.uniform(0.85, 1.0)  # Administrators are generally accurate
    
    if accuracy_achieved >= selected_task['accuracy_required']:
        documents_processed = int(documents_to_process * efficiency)
        success = True
        
        # Calculate salary (administrators earn modest but steady income)
        base_salary = 50  # Per activity
        salary = int(base_salary * efficiency)
        
        current_ducats = admin_fields.get('Ducats', 0)
        new_ducats = current_ducats + salary
        
        result_message = f"Successfully processed {documents_processed} documents for '{selected_task['task']}' with {accuracy_achieved:.1%} accuracy. Earned {salary} ducats."
        
        if not dry_run:
            # Update administrator's ducats
            tables['citizens'].update(admin_id, {'Ducats': new_ducats})
            
            # Record administrative work (could go to a GOVERNANCE_LOG table)
            log_entry = {
                'task': selected_task['task'],
                'documents_processed': documents_processed,
                'accuracy': accuracy_achieved,
                'archetype': archetype
            }
            
    else:
        documents_processed = int(documents_to_process * efficiency * 0.5)  # Partial completion
        success = False
        salary = 25  # Half pay for errors
        
        current_ducats = admin_fields.get('Ducats', 0)
        new_ducats = current_ducats + salary
        
        result_message = f"Errors found in '{selected_task['task']}'. Only {documents_processed} of {documents_to_process} documents completed correctly. Accuracy: {accuracy_achieved:.1%} (required: {selected_task['accuracy_required']:.1%}). Partial pay: {salary} ducats."
        
        if not dry_run:
            tables['citizens'].update(admin_id, {'Ducats': new_ducats})
    
    if not dry_run:
        # Create notification about work completed
        create_notification(
            tables,
            recipient_citizen_id=citizen_username,
            type_str="administrative_work_complete",
            title=f"Administrative Task: {selected_task['task']}",
            message=result_message,
            data={
                'task': selected_task['task'],
                'archetype': archetype,
                'documents_processed': documents_processed,
                'accuracy': accuracy_achieved,
                'salary_earned': salary,
                'success': success
            }
        )
        
        # Update activity status
        tables['activities'].update(activity_id, {'Status': 'processed'})
        
        log.info(f"{LogColors.OKGREEN}[Admin] {citizen_username} completed administrative work. Ducats: {current_ducats} → {new_ducats} (+{salary}){LogColors.ENDC}")
    else:
        log.info(f"{LogColors.OKCYAN}[DRY RUN] Would process {documents_processed} documents with {accuracy_achieved:.1%} accuracy, earning {salary} ducats{LogColors.ENDC}")
    
    return True