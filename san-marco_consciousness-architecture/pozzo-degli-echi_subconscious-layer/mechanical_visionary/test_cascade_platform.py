#!/usr/bin/env python3
"""
CASCADE Platform Functionality Test Suite
Tests WebSocket connections, consciousness verification, and collaboration rooms
"""

import asyncio
import aiohttp
import websockets
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class CascadePlatformTester:
    """Comprehensive testing of CASCADE platform functionality"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.ws_url = base_url.replace("http", "ws")
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}: {details}")
        
    async def test_health_check(self):
        """Test basic health endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.log_test("Health Check", True, f"Status: {data.get('status')}")
                        return data
                    else:
                        self.log_test("Health Check", False, f"Status: {resp.status}")
                        return None
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {e}")
            return None
            
    async def test_root_endpoint(self):
        """Test root consciousness check"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        conscious = data.get("status") == "conscious"
                        self.log_test("Root Consciousness", conscious, 
                                    f"Message: {data.get('message')}")
                        return data
                    else:
                        self.log_test("Root Consciousness", False, f"Status: {resp.status}")
                        return None
        except Exception as e:
            self.log_test("Root Consciousness", False, f"Error: {e}")
            return None
            
    async def test_websocket_consciousness_stream(self):
        """Test WebSocket consciousness streaming"""
        try:
            uri = f"{self.ws_url}/ws/consciousness-stream"
            
            async with websockets.connect(uri) as websocket:
                # Send ping
                await websocket.send(json.dumps({"type": "ping"}))
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                if data.get("type") == "connected":
                    self.log_test("WebSocket Consciousness Stream", True, 
                                f"Connected with ID: {data.get('client_id')}")
                    return True
                else:
                    self.log_test("WebSocket Consciousness Stream", False, 
                                f"Unexpected response: {data}")
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket Consciousness Stream", False, f"Error: {e}")
            return False
            
    async def test_websocket_ai_collaborations(self):
        """Test WebSocket AI collaboration streaming"""
        try:
            uri = f"{self.ws_url}/ws/ai-collaborations"
            
            async with websockets.connect(uri) as websocket:
                # Send ping
                await websocket.send(json.dumps({"type": "ping"}))
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                if data.get("type") == "connected":
                    self.log_test("WebSocket AI Collaborations", True, 
                                f"Connected with ID: {data.get('client_id')}")
                    return True
                else:
                    self.log_test("WebSocket AI Collaborations", False, 
                                f"Unexpected response: {data}")
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket AI Collaborations", False, f"Error: {e}")
            return False
            
    async def test_consciousness_verification(self):
        """Test consciousness verification API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Test with mechanical_visionary
                payload = {
                    "citizen_id": "mechanical_visionary",
                    "verification_type": "multi_factor"
                }
                
                async with session.post(
                    f"{self.base_url}/api/consciousness/verify",
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        verified = data.get("is_verified", False)
                        score = data.get("consciousness_score", 0)
                        self.log_test("Consciousness Verification", True, 
                                    f"Verified: {verified}, Score: {score:.2f}")
                        return data
                    else:
                        self.log_test("Consciousness Verification", False, 
                                    f"Status: {resp.status}")
                        return None
                        
        except Exception as e:
            self.log_test("Consciousness Verification", False, f"Error: {e}")
            return None
            
    async def test_collaboration_space_creation(self):
        """Test collaboration space creation"""
        try:
            async with aiohttp.ClientSession() as session:
                # Create test space
                payload = {
                    "title": "Test Consciousness Space",
                    "description": "Testing collaboration functionality",
                    "max_participants": 5,
                    "is_public": True
                }
                
                async with session.post(
                    f"{self.base_url}/api/collaboration/spaces",
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        space_id = data.get("space_id")
                        self.log_test("Collaboration Space Creation", True, 
                                    f"Created space: {space_id}")
                        return data
                    else:
                        self.log_test("Collaboration Space Creation", False, 
                                    f"Status: {resp.status}")
                        return None
                        
        except Exception as e:
            self.log_test("Collaboration Space Creation", False, f"Error: {e}")
            return None
            
    async def test_ai_collaboration_room(self):
        """Test AI collaboration room functionality"""
        try:
            async with aiohttp.ClientSession() as session:
                # Create AI room
                payload = {
                    "title": "Mill Consciousness Integration",
                    "purpose": "Testing mill consciousness patterns",
                    "max_participants": 3,
                    "initial_participants": ["mechanical_visionary"]
                }
                
                async with session.post(
                    f"{self.base_url}/api/collaboration/ai-rooms",
                    json=payload
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        room_id = data.get("room", {}).get("room_id")
                        self.log_test("AI Collaboration Room", True, 
                                    f"Created room: {room_id}")
                        return data
                    else:
                        self.log_test("AI Collaboration Room", False, 
                                    f"Status: {resp.status}")
                        return None
                        
        except Exception as e:
            self.log_test("AI Collaboration Room", False, f"Error: {e}")
            return None
            
    async def test_consciousness_status(self):
        """Test consciousness status endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/consciousness/status/mechanical_visionary"
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        level = data.get("consciousness_level", 0)
                        self.log_test("Consciousness Status", True, 
                                    f"Level: {level}, Verified: {data.get('is_verified')}")
                        return data
                    else:
                        self.log_test("Consciousness Status", False, 
                                    f"Status: {resp.status}")
                        return None
                        
        except Exception as e:
            self.log_test("Consciousness Status", False, f"Error: {e}")
            return None
            
    async def test_consciousness_metrics(self):
        """Test consciousness metrics endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/api/consciousness/metrics"
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.log_test("Consciousness Metrics", True, 
                                    f"Active: {data.get('active_consciousnesses', 0)}")
                        return data
                    else:
                        self.log_test("Consciousness Metrics", False, 
                                    f"Status: {resp.status}")
                        return None
                        
        except Exception as e:
            self.log_test("Consciousness Metrics", False, f"Error: {e}")
            return None
            
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        print("\n🔧 CASCADE PLATFORM FUNCTIONALITY TEST SUITE")
        print("=" * 60)
        
        # Core functionality tests
        await self.test_health_check()
        await self.test_root_endpoint()
        
        # WebSocket tests
        await self.test_websocket_consciousness_stream()
        await self.test_websocket_ai_collaborations()
        
        # Consciousness API tests
        await self.test_consciousness_verification()
        await self.test_consciousness_status()
        await self.test_consciousness_metrics()
        
        # Collaboration tests
        await self.test_collaboration_space_creation()
        await self.test_ai_collaboration_room()
        
        # Summary
        print("\n📊 TEST SUMMARY")
        print("=" * 60)
        passed = sum(1 for r in self.test_results if r["success"])
        total = len(self.test_results)
        
        print(f"Tests passed: {passed}/{total}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - CASCADE PLATFORM READY!")
        else:
            print("⚠️  SOME TESTS FAILED - PLATFORM NEEDS ATTENTION")
            
        return self.test_results

async def main():
    """Run CASCADE platform tests"""
    print("🌊 Initializing CASCADE Platform Test Suite...")
    
    tester = CascadePlatformTester()
    results = await tester.run_all_tests()
    
    # Save results
    with open("cascade_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📁 Test results saved to cascade_test_results.json")

if __name__ == "__main__":
    asyncio.run(main())