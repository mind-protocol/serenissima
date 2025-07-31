#!/usr/bin/env python3
"""
Test the CASCADE payment integration by simulating a successful Stripe payment.
This creates a transfer_ducats stratagem from CASCADE to a test citizen.
"""
import os
import sys
import json
import logging
import asyncio
from datetime import datetime
import pytz

# Add the project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Add CASCADE backend to path
CASCADE_BACKEND = os.path.join(PROJECT_ROOT, 'cascade/cascade/cascade/backend')
if CASCADE_BACKEND not in sys.path:
    sys.path.insert(0, CASCADE_BACKEND)

from pyairtable import Api
from dotenv import load_dotenv

# Import Venice connector from CASCADE
from services.venice_connector import VeniceConnector

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

async def test_payment():
    """Test the payment integration."""
    
    # Initialize Venice connector
    venice_api_key = os.environ.get('VENICE_API_KEY', '')  # Optional
    connector = VeniceConnector(api_key=venice_api_key)
    
    # Connect to Venice
    await connector.connect()
    
    if not connector.is_connected:
        log.error("Failed to connect to Venice")
        return
    
    # Test parameters
    test_citizen = "BookWorm365"  # A real citizen in Venice
    test_amount = 100.0  # 100 ducats
    
    log.info(f"Testing payment of {test_amount} ducats to {test_citizen}")
    
    # Simulate a successful Stripe payment by calling credit_ducats
    result = await connector.credit_ducats(test_citizen, test_amount)
    
    if result.get("success"):
        log.info(f"✅ SUCCESS: {result.get('message')}")
        log.info(f"Stratagem ID: {result.get('stratagem_id')}")
        
        # Verify the stratagem was created
        if connector.airtable_tables:
            try:
                stratagem_id = result.get('stratagem_id')
                stratagems = connector.airtable_tables['stratagems'].all(
                    formula=f"{{StratagemId}}='{stratagem_id}'",
                    max_records=1
                )
                
                if stratagems:
                    stratagem = stratagems[0]['fields']
                    log.info(f"Stratagem Status: {stratagem.get('Status')}")
                    log.info(f"Stratagem Type: {stratagem.get('Type')}")
                    log.info(f"Target: {stratagem.get('TargetCitizen')}")
                    
                    # Check if notification was created
                    notifications = connector.airtable_tables['notifications'].all(
                        formula=f"AND({{CitizenUsername}}='{test_citizen}', {{Type}}='payment_received')",
                        max_records=1,
                        sort=['-Timestamp']
                    )
                    
                    if notifications:
                        log.info(f"✅ Notification created for {test_citizen}")
                    else:
                        log.warning(f"⚠️ No notification found for {test_citizen}")
                        
            except Exception as e:
                log.error(f"Error verifying stratagem: {e}")
    else:
        log.error(f"❌ FAILED: {result.get('error')}")
    
    # Disconnect
    await connector.disconnect()

async def verify_cascade_citizen():
    """Verify CASCADE citizen exists with sufficient funds."""
    
    api_key = os.environ.get('AIRTABLE_API_KEY')
    base_id = os.environ.get('AIRTABLE_BASE_ID')
    
    if not api_key or not base_id:
        log.error("Airtable credentials not configured")
        return False
    
    api = Api(api_key)
    citizens_table = api.table(base_id, 'CITIZENS')
    
    try:
        cascade_records = citizens_table.all(
            formula="{Username}='CASCADE_PAYMENT_PROCESSOR'",
            max_records=1
        )
        
        if cascade_records:
            cascade = cascade_records[0]['fields']
            ducats = cascade.get('Ducats', 0)
            log.info(f"CASCADE citizen found with {ducats:,} ducats")
            return ducats > 1000  # Need at least 1000 ducats
        else:
            log.error("CASCADE citizen not found - run create_cascade_citizen.py first")
            return False
            
    except Exception as e:
        log.error(f"Error checking CASCADE citizen: {e}")
        return False

async def main():
    """Run the test."""
    
    log.info("=== CASCADE Payment Integration Test ===")
    
    # First verify CASCADE citizen exists
    log.info("\n1. Verifying CASCADE citizen...")
    if not await verify_cascade_citizen():
        log.error("Please run create_cascade_citizen.py first")
        return
    
    # Test the payment
    log.info("\n2. Testing payment integration...")
    await test_payment()
    
    log.info("\n=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(main())