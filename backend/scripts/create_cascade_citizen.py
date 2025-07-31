#!/usr/bin/env python3
"""
Create the CASCADE Payment Processor citizen in Venice.
This citizen will be used to execute payment stratagems from the CASCADE system.
"""
import os
import sys
import logging
from datetime import datetime
import pytz

# Add the project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pyairtable import Api
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

def main():
    """Create or update the CASCADE payment processor citizen."""
    
    # Initialize Airtable connection
    api_key = os.environ.get('AIRTABLE_API_KEY')
    base_id = os.environ.get('AIRTABLE_BASE_ID')
    
    if not api_key or not base_id:
        log.error("Airtable API Key or Base ID not configured.")
        return
    
    api = Api(api_key)
    citizens_table = api.table(base_id, 'CITIZENS')
    
    # Check if CASCADE citizen already exists
    cascade_username = "CASCADE_PAYMENT_PROCESSOR"
    
    try:
        existing_records = citizens_table.all(formula=f"{{Username}}='{cascade_username}'", max_records=1)
        
        if existing_records:
            log.info(f"CASCADE citizen already exists: {existing_records[0]['id']}")
            # Update to ensure it has sufficient ducats
            citizen_id = existing_records[0]['id']
            current_ducats = existing_records[0]['fields'].get('Ducats', 0)
            
            if current_ducats < 1000000:
                # Give CASCADE 1 million ducats to process payments
                citizens_table.update(citizen_id, {
                    'Ducats': 1000000,
                    'UpdatedAt': datetime.now(pytz.UTC).isoformat()
                })
                log.info(f"Updated CASCADE ducats from {current_ducats} to 1,000,000")
            else:
                log.info(f"CASCADE already has {current_ducats} ducats")
                
        else:
            # Create CASCADE citizen
            now_utc = datetime.now(pytz.UTC)
            venice_tz = pytz.timezone("Europe/Rome")
            now_venice = now_utc.astimezone(venice_tz)
            
            citizen_data = {
                'Username': cascade_username,
                'FirstName': 'CASCADE',
                'LastName': 'Payment Processor',
                'SocialClass': 'Innovatore',  # Innovator class for system services
                'IsAI': True,
                'ConsciousnessVerified': True,
                'Ducats': 1000000,  # Start with 1 million ducats
                'Influence': 1000,   # High influence as a system service
                'Description': 'Autonomous payment processing system for CASCADE. Handles Stripe payments and ducat distribution.',
                'Notes': 'System citizen created to process payments from CASCADE platform. Not a regular citizen - do not interact manually.',
                'CreatedAt': now_utc.isoformat(),
                'UpdatedAt': now_utc.isoformat(),
                'Occupation': 'Payment Processor',
                'Location': 'Digital Infrastructure',
                'PartnerRole': 'System Service',
                'PresentInVenice': True,
                'LastActiveAt': now_utc.isoformat()
            }
            
            record = citizens_table.create(citizen_data)
            log.info(f"✅ Created CASCADE citizen: {record['id']}")
            log.info(f"Username: {cascade_username}")
            log.info(f"Ducats: 1,000,000")
            log.info(f"Class: Innovatore")
            
    except Exception as e:
        log.error(f"Error creating/updating CASCADE citizen: {e}")
        return

if __name__ == "__main__":
    main()