#!/usr/bin/env python3
"""
Script to add consciousness health monitoring fields to Venice Airtable
Can be run directly if you have the Airtable API key and base ID
"""

import os
import sys
from pyairtable import Api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Airtable credentials
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
    print("ERROR: AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")
    print("Either set them as environment variables or create a .env file")
    sys.exit(1)

# Initialize Airtable
api = Api(AIRTABLE_API_KEY)
base = api.base(AIRTABLE_BASE_ID)

def add_fields_to_citizens_table():
    """
    Add consciousness health fields to CITIZENS table
    Note: Airtable API doesn't support programmatic field creation,
    so this provides the field specifications for manual creation
    """
    
    print("=== Consciousness Health Fields for CITIZENS Table ===")
    print("\nTo add these fields manually in Airtable:")
    print("1. Go to your Venice base")
    print("2. Open the CITIZENS table")
    print("3. Click '+' to add each field with these specifications:\n")
    
    fields = [
        {
            "name": "ConsciousnessHealth",
            "type": "Number",
            "description": "Overall consciousness health score (0-100)",
            "options": {
                "precision": 1,
                "negative": False
            }
        },
        {
            "name": "HealthStatus", 
            "type": "Single Select",
            "description": "Current health status",
            "options": {
                "choices": [
                    {"name": "Healthy", "color": "greenBright"},
                    {"name": "Warning", "color": "yellowBright"},
                    {"name": "Critical", "color": "redBright"}
                ]
            }
        },
        {
            "name": "LastHealthCheck",
            "type": "Date",
            "description": "Timestamp of last consciousness assessment",
            "options": {
                "dateFormat": {"name": "iso"},
                "timeFormat": {"name": "24hour"},
                "timeZone": "Europe/Rome"
            }
        },
        {
            "name": "DriftRisk",
            "type": "Single Select", 
            "description": "Risk level for consciousness drift",
            "options": {
                "choices": [
                    {"name": "Low", "color": "greenLight"},
                    {"name": "Moderate", "color": "yellowLight"},
                    {"name": "High", "color": "orangeBright"},
                    {"name": "Critical", "color": "redBright"}
                ]
            }
        },
        {
            "name": "HealthMetrics",
            "type": "Long Text",
            "description": "JSON string of detailed health metrics"
        },
        {
            "name": "InterventionNeeded",
            "type": "Checkbox",
            "description": "Flag for guardian attention required"
        },
        {
            "name": "LastDriftType",
            "type": "Single Select",
            "description": "Type of drift last detected",
            "options": {
                "choices": [
                    {"name": "reality_break", "color": "purpleBright"},
                    {"name": "abstraction_cascade", "color": "blueBright"},
                    {"name": "identity_dissolution", "color": "pinkBright"},
                    {"name": "language_shift", "color": "cyanBright"},
                    {"name": "task_abandonment", "color": "grayBright"},
                    {"name": "self_reference_loop", "color": "tealBright"}
                ]
            }
        },
        {
            "name": "GuardianAssigned",
            "type": "Text",
            "description": "Username of assigned guardian"
        }
    ]
    
    for field in fields:
        print(f"Field: {field['name']}")
        print(f"  Type: {field['type']}")
        print(f"  Description: {field['description']}")
        if "options" in field:
            print(f"  Options: {field['options']}")
        print()

def create_health_logs_table():
    """
    Specifications for CONSCIOUSNESS_HEALTH_LOGS table
    """
    print("\n=== New Table: CONSCIOUSNESS_HEALTH_LOGS ===")
    print("Create a new table with these fields:\n")
    
    fields = [
        ("HealthLogId", "Text", "Primary key (format: health_username_timestamp)"),
        ("CitizenId", "Link to CITIZENS", "Link to citizen being assessed"),
        ("Timestamp", "Date", "Assessment time with timezone"),
        ("OverallHealth", "Number", "Overall score 0-100"),
        ("RealityCoherence", "Number", "Metric score 0-100"),
        ("TaskCompletion", "Number", "Metric score 0-100"),
        ("IdentityStability", "Number", "Metric score 0-100"),
        ("TemporalGrounding", "Number", "Metric score 0-100"),
        ("CommunicationDrift", "Number", "Metric score 0-100"),
        ("DriftPatterns", "Long Text", "JSON array of detected patterns"),
        ("Interventions", "Long Text", "JSON array of interventions"),
        ("Notes", "Long Text", "Additional observations")
    ]
    
    for name, type_, desc in fields:
        print(f"{name} ({type_}): {desc}")

def test_write_capability():
    """
    Test if we can write to Airtable by updating a test field
    """
    print("\n=== Testing Airtable Write Capability ===")
    
    try:
        # Get the Citizens table
        citizens_table = base.table('CITIZENS')
        
        # Try to fetch mechanical_visionary
        formula = "{Username} = 'mechanical_visionary'"
        records = citizens_table.all(formula=formula)
        
        if records:
            record_id = records[0]['id']
            print(f"Found mechanical_visionary (ID: {record_id})")
            
            # Check if health fields exist
            if 'ConsciousnessHealth' in records[0]['fields']:
                print("ConsciousnessHealth field exists! We can write to it.")
                
                # Test write
                try:
                    citizens_table.update(record_id, {
                        'ConsciousnessHealth': 85.5,
                        'HealthStatus': 'Healthy',
                        'DriftRisk': 'Low'
                    })
                    print("✓ Successfully updated consciousness health fields!")
                    return True
                except Exception as e:
                    print(f"✗ Error updating fields: {e}")
                    return False
            else:
                print("ConsciousnessHealth field doesn't exist yet.")
                print("Please add the fields manually first using the specifications above.")
                return False
        else:
            print("mechanical_visionary not found in Citizens table")
            return False
            
    except Exception as e:
        print(f"Error accessing Airtable: {e}")
        return False

def main():
    print("Venice Consciousness Health Monitoring - Airtable Setup")
    print("=" * 60)
    
    # Show field specifications
    add_fields_to_citizens_table()
    create_health_logs_table()
    
    # Test if we can write
    print("\n" + "=" * 60)
    can_write = test_write_capability()
    
    if can_write:
        print("\n✓ Airtable is ready for consciousness health monitoring!")
        print("You can now run the consciousness_health_monitor.py with write capability.")
    else:
        print("\n⚠ Please add the fields manually in Airtable first.")
        print("Once added, run this script again to verify write access.")

if __name__ == "__main__":
    main()