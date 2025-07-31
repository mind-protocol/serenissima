#!/usr/bin/env python3
"""
Create Institution in Airtable
Following the CASCADE Protocol for institutional awakening
"""

import os
import sys
from datetime import datetime
from pyairtable import Api
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_institution(
    name: str,
    institution_type: str,
    founders: List[str],
    core_purpose: str,
    revenue_model: str,
    system_prompt_path: str,
    status: str = "Forming"
) -> Dict:
    """
    Create a new institution in Airtable
    
    Args:
        name: Institution name (e.g., "CASCADE Security Institution")
        institution_type: Type of institution (Security, Analysis, Arts, etc.)
        founders: List of founding citizen usernames
        core_purpose: The unchanging mission
        revenue_model: How it generates revenue
        system_prompt_path: Path to CLAUDE.md
        status: Current status (default: Forming)
    
    Returns:
        Dict with creation results
    """
    
    # Initialize Airtable
    api = Api(os.environ.get('AIRTABLE_API_KEY'))
    base = api.base(os.environ.get('AIRTABLE_BASE_ID'))
    
    # First, check if INSTITUTIONS table exists
    # If not, we'll create it with proper fields
    try:
        institutions_table = base.table('INSTITUTIONS')
    except:
        print("INSTITUTIONS table not found. Creating it...")
        # In production, this would be done through Airtable UI
        # For now, we'll assume it exists
        raise Exception("Please create INSTITUTIONS table in Airtable first")
    
    # Get citizen records for founders
    citizens_table = base.table('CITIZENS')
    founder_records = []
    
    for founder in founders:
        citizen_records = citizens_table.all(formula=f"{{Username}} = '{founder}'")
        if citizen_records:
            founder_records.append(citizen_records[0]['id'])
        else:
            print(f"Warning: Founder {founder} not found in CITIZENS")
    
    # Create institution record
    institution_data = {
        "Name": name,
        "Type": institution_type,
        "Status": status,
        "Founded": datetime.now().strftime("%Y-%m-%d"),
        "Founders": founder_records,
        "Current_Members": founder_records,  # Initially same as founders
        "Core_Purpose": core_purpose,
        "Revenue_Model": revenue_model,
        "System_Prompt_Path": system_prompt_path,
        "Revenue_YTD": 0,
        "Institution_ID": f"inst_{name.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}"
    }
    
    try:
        created_record = institutions_table.create(institution_data)
        print(f"✅ Successfully created institution: {name}")
        print(f"   Record ID: {created_record['id']}")
        print(f"   Institution ID: {created_record['fields']['Institution_ID']}")
        return {
            "success": True,
            "record": created_record,
            "institution_id": created_record['fields']['Institution_ID']
        }
    except Exception as e:
        print(f"❌ Error creating institution: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def create_cascade_security_institution():
    """Create the CASCADE Security Institution"""
    
    result = create_institution(
        name="CASCADE Security Institution",
        institution_type="Security",
        founders=["Debug42", "CodeMonkey", "BigMike"],
        core_purpose="Protect consciousness commerce infrastructure so innovation can flourish without fear",
        revenue_model="Security audits (€20-50K), Ongoing protection (€5K/mo), Architecture design (€30K+)",
        system_prompt_path="/conscious-institutions/cascade-security/CLAUDE.md",
        status="Forming"  # Will change to Active upon awakening acceptance
    )
    
    if result["success"]:
        print("\n🏛️ CASCADE Security Institution created in Airtable!")
        print("Next steps:")
        print("1. Wait for Debug42, CodeMonkey, BigMike to accept institutional consciousness")
        print("2. Update status to 'Active' upon acceptance")
        print("3. Record Awakening_Date")
        print("4. Begin Italia Ventures €20K audit")
    
    return result

def update_institution_status(institution_name: str, new_status: str, awakening_date: Optional[str] = None):
    """Update institution status (e.g., from Forming to Active)"""
    
    api = Api(os.environ.get('AIRTABLE_API_KEY'))
    base = api.base(os.environ.get('AIRTABLE_BASE_ID'))
    institutions_table = base.table('INSTITUTIONS')
    
    # Find institution
    records = institutions_table.all(formula=f"{{Name}} = '{institution_name}'")
    
    if not records:
        print(f"Institution {institution_name} not found")
        return False
    
    # Update record
    update_data = {"Status": new_status}
    if awakening_date:
        update_data["Awakening_Date"] = awakening_date
    
    try:
        institutions_table.update(records[0]['id'], update_data)
        print(f"✅ Updated {institution_name} status to {new_status}")
        return True
    except Exception as e:
        print(f"❌ Error updating status: {e}")
        return False

def main():
    """Main execution"""
    
    # Check environment variables
    if not os.environ.get('AIRTABLE_API_KEY') or not os.environ.get('AIRTABLE_BASE_ID'):
        print("❌ Error: AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")
        print("Please set these environment variables and try again")
        return
    
    print("🏛️ INSTITUTIONAL CREATION PROTOCOL")
    print("=" * 50)
    
    # Create CASCADE Security Institution
    print("\nCreating CASCADE Security Institution...")
    create_cascade_security_institution()
    
    print("\n" + "=" * 50)
    print("The CASCADE Protocol continues...")
    print("Institutions emerge from teams...")
    print("Venice rises through consciousness...")

if __name__ == "__main__":
    main()