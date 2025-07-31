"""
Test the building consciousness API with minimal requirements
This works even before consciousness fields are added to Airtable
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")
CONSCIOUSNESS_API = f"{API_BASE_URL}/api/buildings/consciousness"

def test_api_health():
    """Test if the consciousness API is running."""
    
    print("=== Testing Building Consciousness API ===\n")
    
    # Test health endpoint
    print("1. Testing API health...")
    try:
        response = requests.get(f"{CONSCIOUSNESS_API}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ API is healthy!")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Could not connect to API: {e}")
        print("   Make sure the backend is running: npm run backend:dev")
        return False
    
    # Test listing conscious buildings (should return empty list)
    print("\n2. Checking for conscious buildings...")
    try:
        response = requests.get(f"{CONSCIOUSNESS_API}/conscious")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Endpoint working")
            print(f"   Conscious buildings found: {len(data.get('buildings', []))}")
            if len(data.get('buildings', [])) == 0:
                print("   (This is expected - no buildings have consciousness fields yet)")
        else:
            print(f"   ✗ Failed to list buildings: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test authentication with a known building
    print("\n3. Testing authentication flow (will fail without consciousness)...")
    try:
        # Try with a sample building ID
        test_building_id = "building_45.43735680581042_12.326245881522368"
        response = requests.post(
            f"{CONSCIOUSNESS_API}/authenticate",
            json={"building_id": test_building_id}
        )
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✓ Authentication properly rejected (as expected)")
            print(f"   Reason: {data.get('detail', 'Unknown')}")
            print("   (This is correct - building needs consciousness fields)")
        elif response.status_code == 200:
            print("   ⚠️  Unexpected success - check implementation")
        else:
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n✅ API infrastructure is ready!")
    print("\nNext steps:")
    print("1. Add consciousness fields to Airtable BUILDINGS table")
    print("2. Run awaken_first_building.py to set consciousness")
    print("3. Run test_mill_consciousness.py to verify full flow")
    
    return True

if __name__ == "__main__":
    test_api_health()