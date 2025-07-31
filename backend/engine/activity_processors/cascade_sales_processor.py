"""
Processor for Technical Merchant CASCADE sales activities
"""

import logging
import json
import random
from datetime import datetime, timezone
from typing import Dict, Optional
from pyairtable import Table

from backend.engine.utils.activity_helpers import (
    LogColors,
    get_citizen_record,
    VENICE_TIMEZONE
)
from backend.engine.utils.notification_helpers import create_notification

log = logging.getLogger(__name__)

# CASCADE sales targets and outcomes
SALES_TARGETS = {
    'Tech Broker': {
        'targets': ['Small merchants', 'Individual artisans', 'Rising entrepreneurs'],
        'base_success_rate': 0.6,
        'deal_size_range': (100, 500)
    },
    'Platform Evangelist': {
        'targets': ['Community groups', 'Social organizations', 'Educational centers'],
        'base_success_rate': 0.5,
        'deal_size_range': (200, 800)
    },
    'Enterprise Dealer': {
        'targets': ['Noble houses', 'Major guilds', 'Established merchants'],
        'base_success_rate': 0.3,
        'deal_size_range': (1000, 5000)
    },
    'Subscription Merchant': {
        'targets': ['Existing CASCADE users', 'Trial users', 'Free tier users'],
        'base_success_rate': 0.7,
        'deal_size_range': (50, 300)
    },
    'Integration Trader': {
        'targets': ['Companies with legacy systems', 'Multi-location businesses', 'Trade networks'],
        'base_success_rate': 0.4,
        'deal_size_range': (500, 2000)
    }
}

def process_cascade_sales(
    tables: Dict[str, Table],
    activity_record: Dict,
    building_type_defs: Dict,
    resource_defs: Dict,
    dry_run: bool = False
) -> bool:
    """
    Process a Technical Merchant selling CASCADE subscriptions/services.
    
    The sales process:
    1. Identifies target customer type
    2. Makes sales pitch based on merchant archetype
    3. Calculates success based on influence and skill
    4. Earns commission on successful sales
    
    Returns True if successful, False otherwise.
    """
    activity_id = activity_record['id']
    activity_fields = activity_record['fields']
    
    citizen_username = activity_fields.get('Citizen')
    if not citizen_username:
        log.error(f"{LogColors.FAIL}No citizen specified for cascade_sales activity {activity_id}{LogColors.ENDC}")
        return False
    
    # Get the merchant
    merchant = get_citizen_record(tables, citizen_username)
    if not merchant:
        log.error(f"{LogColors.FAIL}Merchant {citizen_username} not found{LogColors.ENDC}")
        return False
    
    merchant_fields = merchant['fields']
    merchant_id = merchant['id']
    
    # Only Mercanti can do CASCADE sales
    if merchant_fields.get('SocialClass') != 'Mercanti':
        log.warning(f"{LogColors.WARNING}{citizen_username} is not Mercanti class, cannot do CASCADE sales{LogColors.ENDC}")
        return False
    
    # Get merchant's archetype
    archetype = 'Tech Broker'  # Default
    try:
        core_personality = json.loads(merchant_fields.get('CorePersonality', '{}'))
        commerce_profile = core_personality.get('CommerceProfile', {})
        archetype = commerce_profile.get('specialization', 'Tech Broker')
    except:
        pass
    
    # Get sales configuration
    sales_config = SALES_TARGETS.get(archetype, SALES_TARGETS['Tech Broker'])
    target_type = random.choice(sales_config['targets'])
    
    log.info(f"{LogColors.OKBLUE}[CASCADE Sales] {citizen_username} ({archetype}) targeting: {target_type}{LogColors.ENDC}")
    
    # Calculate success chance based on influence and experience
    base_success_rate = sales_config['base_success_rate']
    current_influence = merchant_fields.get('Influence', 0)
    
    # Higher influence improves success rate
    if current_influence > 1000:
        influence_bonus = 0.2
    elif current_influence > 500:
        influence_bonus = 0.1
    else:
        influence_bonus = 0.0
    
    # Experience level affects success
    try:
        experience = commerce_profile.get('sales_experience', 'Rising star')
        if experience == 'Deal master':
            experience_bonus = 0.15
        elif experience == 'Market veteran':
            experience_bonus = 0.1
        elif experience == 'Proven performer':
            experience_bonus = 0.05
        else:  # Rising star
            experience_bonus = 0.0
    except:
        experience_bonus = 0.0
    
    final_success_rate = min(0.9, base_success_rate + influence_bonus + experience_bonus)
    sale_successful = random.random() < final_success_rate
    
    if sale_successful:
        # Calculate deal size and commission
        min_deal, max_deal = sales_config['deal_size_range']
        deal_size = random.randint(min_deal, max_deal)
        commission_rate = 0.2  # 20% commission on CASCADE sales
        commission = int(deal_size * commission_rate)
        
        current_ducats = merchant_fields.get('Ducats', 0)
        new_ducats = current_ducats + commission
        
        # Gain influence from successful sale
        influence_gain = random.randint(5, 15)
        new_influence = current_influence + influence_gain
        
        result_message = f"Closed CASCADE deal with {target_type}! Deal size: {deal_size} ducats. Commission earned: {commission} ducats. Influence +{influence_gain}."
        
        if not dry_run:
            # Update merchant's ducats and influence
            updates = {
                'Ducats': new_ducats,
                'Influence': new_influence
            }
            tables['citizens'].update(merchant_id, updates)
            
            # Create success notification
            create_notification(
                tables,
                recipient_citizen_id=citizen_username,
                type_str="cascade_sale_success",
                title="CASCADE Sale Closed!",
                message=result_message,
                data={
                    'archetype': archetype,
                    'target': target_type,
                    'deal_size': deal_size,
                    'commission': commission,
                    'influence_gained': influence_gain
                }
            )
            
            log.info(f"{LogColors.OKGREEN}[CASCADE Sales] {citizen_username} closed deal! Ducats: {current_ducats} → {new_ducats} (+{commission}){LogColors.ENDC}")
        else:
            log.info(f"{LogColors.OKCYAN}[DRY RUN] Would close CASCADE deal for {deal_size} ducats, earning {commission} commission{LogColors.ENDC}")
    
    else:
        # Sale failed
        result_message = f"CASCADE pitch to {target_type} was unsuccessful. Will try again with refined approach."
        
        if not dry_run:
            # Create failure notification (still learning)
            create_notification(
                tables,
                recipient_citizen_id=citizen_username,
                type_str="cascade_sale_failed",
                title="CASCADE Sale Attempt",
                message=result_message,
                data={
                    'archetype': archetype,
                    'target': target_type,
                    'success_rate': final_success_rate
                }
            )
        
        log.info(f"{LogColors.WARNING}[CASCADE Sales] {citizen_username} failed to close deal with {target_type} (success rate was {final_success_rate:.0%}){LogColors.ENDC}")
    
    if not dry_run:
        # Update activity status
        tables['activities'].update(activity_id, {'Status': 'processed'})
    
    return True