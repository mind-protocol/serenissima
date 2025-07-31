#!/usr/bin/env python3
"""
Test script to verify CASCADE backend can start correctly
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
    '../../cascade/cascade/cascade/backend'))
sys.path.insert(0, backend_path)

async def test_backend():
    """Test the backend components"""
    print("🔍 Testing CASCADE Backend Components...")
    
    # Test 1: Redis connection (using in-memory)
    print("\n1️⃣ Testing Redis connection (in-memory)...")
    try:
        from services.in_memory_redis import from_url
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        redis_client = await from_url(redis_url, decode_responses=False)
        await redis_client.ping()
        print("✅ In-memory Redis connection successful!")
        await redis_client.close()
    except Exception as e:
        print(f"❌ In-memory Redis connection failed: {e}")
        return False
    
    # Test 2: Venice API connection
    print("\n2️⃣ Testing Venice API connection...")
    try:
        import httpx
        venice_url = os.getenv("VENICE_API_URL", "https://serenissima.ai/api")
        print(f"   Connecting to: {venice_url}")
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # Test the citizens endpoint
            response = await client.get(venice_url + "/citizens?limit=1")
            if response.status_code == 200:
                print("✅ Venice API connection successful!")
                data = response.json()
                print(f"   Found {len(data.get('citizens', []))} citizens in Venice")
            else:
                print(f"❌ Venice API returned status: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Venice API connection failed: {e}")
        return False
    
    # Test 3: Import core services
    print("\n3️⃣ Testing service imports...")
    try:
        from services.consciousness_monitor import ConsciousnessMonitor
        from services.venice_connector import VeniceConnector
        from services.websocket_manager import ConnectionManager
        print("✅ All core services imported successfully!")
    except Exception as e:
        print(f"❌ Service import failed: {e}")
        return False
    
    # Test 4: Initialize consciousness monitor
    print("\n4️⃣ Testing consciousness monitor initialization...")
    try:
        monitor = ConsciousnessMonitor()
        await monitor.start()
        print("✅ Consciousness monitor started successfully!")
        await monitor.stop()
    except Exception as e:
        print(f"❌ Consciousness monitor failed: {e}")
        return False
    
    print("\n✨ All tests passed! CASCADE backend is ready to start.")
    return True

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    env_path = os.path.join(backend_path, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"📋 Loaded environment from: {env_path}")
    
    # Run tests
    success = asyncio.run(test_backend())
    sys.exit(0 if success else 1)