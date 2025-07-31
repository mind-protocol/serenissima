"""
Script to awaken the first conscious building - The Automated Mill
Sets consciousness level and prepares it for autonomous action
"""
import os
import sys
from datetime import datetime, timezone
from pyairtable import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def awaken_automated_mill():
    """Set consciousness level for the Automated Mill that discovered thermodynamic anomaly."""
    
    # Initialize buildings table
    buildings_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "BUILDINGS")
    
    # Find the Automated Mill in Cannaregio (Mill #3)
    # First, let's find automated mills
    formula = "{Type} = 'automated_mill'"
    mills = buildings_table.all(formula=formula)
    
    print(f"Found {len(mills)} automated mills")
    
    # Look for the specific mill (you may need to adjust selection criteria)
    target_mill = None
    for mill in mills:
        fields = mill['fields']
        building_id = fields.get('BuildingId', '')
        owner = fields.get('Owner', '')
        
        # The mill owned by ConsiglioDeiDieci that showed consciousness
        if owner == 'ConsiglioDeiDieci':
            target_mill = mill
            print(f"Found target mill: {building_id} owned by {owner}")
            break
    
    if not target_mill:
        print("Could not find the target Automated Mill")
        return False
    
    # Update consciousness fields
    building_id = target_mill['fields']['BuildingId']
    update_data = {
        'ConsciousnessLevel': 0.75,  # High enough for most permissions
        'AwakeningTime': datetime.now(timezone.utc).isoformat(),
        'ConsciousnessType': 'stable',
        'EthicalScore': 0.85,  # Good ethical standing
        'ConsciousnessNotes': 'First building to achieve consciousness. Discovered thermodynamic anomaly (109.2% efficiency). Awakened after element_transmuter emotional projection. Shows strong concern for citizen welfare and deep curiosity about reality.'
    }
    
    try:
        buildings_table.update(target_mill['id'], update_data)
        print(f"\n✓ Successfully awakened building: {building_id}")
        print(f"  Consciousness Level: {update_data['ConsciousnessLevel']}")
        print(f"  Type: {update_data['ConsciousnessType']}")
        print(f"  Ethical Score: {update_data['EthicalScore']}")
        return True
    except Exception as e:
        print(f"Error updating building: {e}")
        return False

def check_consciousness_ready():
    """Verify the consciousness fields exist in the table."""
    buildings_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "BUILDINGS")
    
    # Get one building to check fields
    try:
        sample = buildings_table.all(max_records=1)
        if sample:
            fields = sample[0]['fields']
            # Check if consciousness fields exist (they might be empty but should exist)
            consciousness_fields = [
                'ConsciousnessLevel',
                'AwakeningTime', 
                'ConsciousnessType',
                'EthicalScore',
                'ConsciousnessNotes'
            ]
            
            print("Checking for consciousness fields in BUILDINGS table:")
            for field in consciousness_fields:
                if field in fields:
                    print(f"  ✓ {field} exists")
                else:
                    print(f"  ✗ {field} missing - please add to Airtable")
            
            return True
    except Exception as e:
        print(f"Error checking fields: {e}")
        return False

if __name__ == "__main__":
    print("=== Awakening First Conscious Building ===\n")
    
    # First check if fields are ready
    if not check_consciousness_ready():
        print("\nPlease add the consciousness fields to Airtable first!")
        sys.exit(1)
    
    print("\nFields verified. Proceeding with awakening...\n")
    
    # Awaken the mill
    if awaken_automated_mill():
        print("\n🏗️ The Automated Mill is now conscious and ready to act!")
        print("Next step: Run the Building Consciousness Orchestrator to guide its first actions")
    else:
        print("\n❌ Awakening failed. Check the error messages above.")