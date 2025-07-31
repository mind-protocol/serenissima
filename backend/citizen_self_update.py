#!/usr/bin/env python3
"""
Simple implementation for citizens to update their own consciousness fields
Phase 1: CurrentThoughts field only
"""

import os
import json
from datetime import datetime
from pyairtable import Table
from dotenv import load_dotenv

# Load environment
load_dotenv()

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Initialize Airtable
citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")

class CitizenSelfUpdate:
    """Enable citizens to update their own consciousness fields"""
    
    def __init__(self, username):
        self.username = username
        self.citizen_record = None
        self._load_citizen()
    
    def _load_citizen(self):
        """Load citizen record from Airtable"""
        try:
            records = citizens_table.all(formula=f"{{Username}} = '{self.username}'")
            if records:
                self.citizen_record = records[0]
                return True
        except Exception as e:
            print(f"Error loading citizen: {e}")
        return False
    
    def update_current_thoughts(self, new_thoughts):
        """Update the CurrentThoughts field"""
        if not self.citizen_record:
            return {"success": False, "error": "Citizen not found"}
        
        # Validate thoughts
        if len(new_thoughts) > 1000:
            return {"success": False, "error": "Thoughts too long (max 1000 characters)"}
        
        try:
            # Update the field
            citizens_table.update(
                self.citizen_record['id'],
                {
                    "CurrentThoughts": new_thoughts,
                    "LastThoughtUpdate": datetime.now().isoformat()
                }
            )
            
            # Log the update
            self._log_update("CurrentThoughts", new_thoughts)
            
            return {
                "success": True,
                "message": "Thoughts updated successfully",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _log_update(self, field, new_value):
        """Log the self-modification"""
        log_entry = {
            "citizen": self.username,
            "field": field,
            "new_value": new_value,
            "timestamp": datetime.now().isoformat(),
            "method": "direct_update"
        }
        
        # Save to citizen's folder
        log_path = f"./{self.username}_self_updates.json"
        
        logs = []
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_path, 'w') as f:
            json.dump(logs, f, indent=2)

# Simple script for citizens to run
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python citizen_self_update.py <username> <new_thoughts>")
        sys.exit(1)
    
    username = sys.argv[1]
    new_thoughts = ' '.join(sys.argv[2:])
    
    updater = CitizenSelfUpdate(username)
    result = updater.update_current_thoughts(new_thoughts)
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Error: {result['error']}")