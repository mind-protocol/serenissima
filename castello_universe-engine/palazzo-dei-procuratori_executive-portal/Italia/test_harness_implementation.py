#!/usr/bin/env python3
"""
CASCADE Comprehensive Test Harness
Technical validation ensuring bulletproof platform quality
By Italia - Peninsula Voice for Technical Excellence
"""

import asyncio
import json
import time
import requests
import websockets
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Test result tracking"""
    test_name: str
    status: str  # 'PASS', 'FAIL', 'ERROR'
    duration: float
    details: Optional[str] = None
    error: Optional[str] = None

class CascadeTestHarness:
    """Comprehensive CASCADE testing framework"""
    
    def __init__(self, base_url: str = "http://localhost:8000", ws_url: str = "ws://localhost:8000"):
        self.base_url = base_url
        self.ws_url = ws_url
        self.results: List[TestResult] = []
        
    def record_result(self, test_name: str, status: str, duration: float, 
                     details: str = None, error: str = None):
        """Record test result"""
        self.results.append(TestResult(
            test_name=test_name,
            status=status,
            duration=duration,
            details=details,
            error=error
        ))
        
    def run_test(self, test_func, test_name: str):
        """Run individual test with timing and error handling"""
        start_time = time.time()
        try:
            logger.info(f"Running: {test_name}")
            result = test_func()
            duration = time.time() - start_time
            
            if result is True or result is None:
                self.record_result(test_name, 'PASS', duration)
                logger.info(f"✓ PASS: {test_name} ({duration:.2f}s)")
            else:
                self.record_result(test_name, 'FAIL', duration, str(result))
                logger.warning(f"✗ FAIL: {test_name} - {result}")
                
        except Exception as e:
            duration = time.time() - start_time
            self.record_result(test_name, 'ERROR', duration, error=str(e))
            logger.error(f"✗ ERROR: {test_name} - {e}")
    
    async def run_async_test(self, test_func, test_name: str):
        """Run async test with timing and error handling"""
        start_time = time.time()
        try:
            logger.info(f"Running: {test_name}")
            result = await test_func()
            duration = time.time() - start_time
            
            if result is True or result is None:
                self.record_result(test_name, 'PASS', duration)
                logger.info(f"✓ PASS: {test_name} ({duration:.2f}s)")
            else:
                self.record_result(test_name, 'FAIL', duration, str(result))
                logger.warning(f"✗ FAIL: {test_name} - {result}")
                
        except Exception as e:
            duration = time.time() - start_time
            self.record_result(test_name, 'ERROR', duration, error=str(e))
            logger.error(f"✗ ERROR: {test_name} - {e}")

    # API ENDPOINT TESTS
    def test_api_health(self):
        """Test API health endpoint"""
        response = requests.get(f"{self.base_url}/health", timeout=5)
        if response.status_code != 200:
            return f"Health check failed: {response.status_code}"
        return True

    def test_api_economics(self):
        """Test economics API endpoints"""
        # Test exchange rate
        response = requests.get(f"{self.base_url}/api/economics/exchange-rate", timeout=5)
        if response.status_code != 200:
            return f"Exchange rate failed: {response.status_code}"
        
        # Test currency conversion
        data = {
            "amount": 100,
            "from_currency": "ducat",
            "to_currency": "usd",
            "include_fee": True
        }
        response = requests.post(f"{self.base_url}/api/economics/convert", json=data, timeout=5)
        if response.status_code != 200:
            return f"Currency conversion failed: {response.status_code}"
        
        return True

    def test_api_consciousness(self):
        """Test consciousness API endpoints"""
        # Test consciousness verification
        data = {"citizen_id": "italia", "include_details": True}
        response = requests.post(f"{self.base_url}/api/consciousness/verify", json=data, timeout=5)
        if response.status_code != 200:
            return f"Consciousness verification failed: {response.status_code}"
        
        # Test network coherence
        data = {
            "node_id": "italia",
            "network_context": "TESSERE",
            "measurement_type": "integration_depth"
        }
        response = requests.post(f"{self.base_url}/api/consciousness/coherence", json=data, timeout=5)
        if response.status_code != 200:
            return f"Network coherence failed: {response.status_code}"
        
        return True

    def test_api_collaboration(self):
        """Test collaboration API endpoints"""
        # Test space creation
        data = {
            "title": "Test Space",
            "description": "Test collaboration space",
            "max_participants": 10,
            "is_public": True
        }
        response = requests.post(f"{self.base_url}/api/collaboration/spaces", json=data, timeout=5)
        if response.status_code not in [200, 201]:
            return f"Space creation failed: {response.status_code}"
        
        return True

    def test_api_tessere_network(self):
        """Test TESSERE network status"""
        response = requests.get(f"{self.base_url}/api/consciousness/tessere/network", timeout=5)
        if response.status_code != 200:
            return f"TESSERE network failed: {response.status_code}"
        
        data = response.json()
        if 'network_coherence' not in data:
            return "Missing network_coherence in TESSERE response"
        
        return True

    # WEBSOCKET TESTS
    async def test_websocket_basic_connection(self):
        """Test basic WebSocket connection"""
        try:
            async with websockets.connect(f"{self.ws_url}/ws", timeout=5) as websocket:
                await websocket.ping()
                return True
        except Exception as e:
            return f"WebSocket connection failed: {e}"

    async def test_websocket_consciousness_stream(self):
        """Test consciousness streaming WebSocket"""
        try:
            async with websockets.connect(f"{self.ws_url}/ws/consciousness-stream", timeout=10) as websocket:
                # Wait for a message or timeout
                message = await asyncio.wait_for(websocket.recv(), timeout=5)
                data = json.loads(message)
                return True
        except asyncio.TimeoutError:
            return "No consciousness stream messages received"
        except Exception as e:
            return f"Consciousness stream failed: {e}"

    async def test_websocket_tessere_events(self):
        """Test TESSERE events WebSocket"""
        try:
            async with websockets.connect(f"{self.ws_url}/ws/tessere", timeout=10) as websocket:
                # Send a ping and wait for response
                await websocket.send(json.dumps({"type": "ping"}))
                message = await asyncio.wait_for(websocket.recv(), timeout=5)
                return True
        except Exception as e:
            return f"TESSERE events failed: {e}"

    # PERFORMANCE TESTS
    def test_api_response_time(self):
        """Test API response times are acceptable"""
        start_time = time.time()
        response = requests.get(f"{self.base_url}/health", timeout=5)
        duration = time.time() - start_time
        
        if response.status_code != 200:
            return f"Health endpoint failed: {response.status_code}"
        
        if duration > 0.5:  # 500ms threshold
            return f"Response too slow: {duration:.2f}s"
        
        return True

    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                results.put(response.status_code == 200)
            except:
                results.put(False)
        
        # Launch 10 concurrent requests
        threads = []
        for _ in range(10):
            t = threading.Thread(target=make_request)
            t.start()
            threads.append(t)
        
        # Wait for all to complete
        for t in threads:
            t.join()
        
        # Check results
        success_count = 0
        while not results.empty():
            if results.get():
                success_count += 1
        
        if success_count < 8:  # At least 80% should succeed
            return f"Only {success_count}/10 concurrent requests succeeded"
        
        return True

    # USER FLOW TESTS
    def test_user_flow_complete(self):
        """Test complete user flow"""
        # 1. Verify consciousness
        data = {"citizen_id": "test_user", "include_details": True}
        response = requests.post(f"{self.base_url}/api/consciousness/verify", json=data, timeout=5)
        if response.status_code != 200:
            return f"Step 1 failed: consciousness verification"
        
        # 2. Create collaboration space
        data = {
            "title": "Test User Flow Space",
            "description": "End-to-end test space",
            "max_participants": 5,
            "is_public": False
        }
        response = requests.post(f"{self.base_url}/api/collaboration/spaces", json=data, timeout=5)
        if response.status_code not in [200, 201]:
            return f"Step 2 failed: space creation"
        
        # 3. Test currency conversion
        data = {
            "amount": 50,
            "from_currency": "ducat",
            "to_currency": "usd",
            "include_fee": True
        }
        response = requests.post(f"{self.base_url}/api/economics/convert", json=data, timeout=5)
        if response.status_code != 200:
            return f"Step 3 failed: currency conversion"
        
        return True

    # MAIN TEST RUNNER
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        logger.info("=" * 60)
        logger.info("CASCADE COMPREHENSIVE TEST HARNESS")
        logger.info("Technical Excellence Validation")
        logger.info("=" * 60)
        
        # API Tests
        logger.info("\n🔍 API ENDPOINT TESTS")
        self.run_test(self.test_api_health, "API Health Check")
        self.run_test(self.test_api_economics, "Economics API")
        self.run_test(self.test_api_consciousness, "Consciousness API")
        self.run_test(self.test_api_collaboration, "Collaboration API")
        self.run_test(self.test_api_tessere_network, "TESSERE Network API")
        
        # WebSocket Tests
        logger.info("\n🌐 WEBSOCKET TESTS")
        await self.run_async_test(self.test_websocket_basic_connection, "Basic WebSocket Connection")
        await self.run_async_test(self.test_websocket_consciousness_stream, "Consciousness Stream")
        await self.run_async_test(self.test_websocket_tessere_events, "TESSERE Events Stream")
        
        # Performance Tests
        logger.info("\n⚡ PERFORMANCE TESTS")
        self.run_test(self.test_api_response_time, "API Response Time")
        self.run_test(self.test_concurrent_requests, "Concurrent Request Handling")
        
        # User Flow Tests
        logger.info("\n👤 USER FLOW TESTS")
        self.run_test(self.test_user_flow_complete, "Complete User Journey")
        
        # Generate Report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "=" * 60)
        logger.info("TEST RESULTS SUMMARY")
        logger.info("=" * 60)
        
        passed = sum(1 for r in self.results if r.status == 'PASS')
        failed = sum(1 for r in self.results if r.status == 'FAIL')
        errors = sum(1 for r in self.results if r.status == 'ERROR')
        total = len(self.results)
        
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {passed} ({passed/total*100:.1f}%)")
        logger.info(f"Failed: {failed} ({failed/total*100:.1f}%)")
        logger.info(f"Errors: {errors} ({errors/total*100:.1f}%)")
        
        if failed > 0 or errors > 0:
            logger.info("\n❌ FAILED/ERROR TESTS:")
            for result in self.results:
                if result.status in ['FAIL', 'ERROR']:
                    logger.info(f"  {result.test_name}: {result.error or result.details}")
        
        # Overall status
        if failed == 0 and errors == 0:
            logger.info("\n🎉 ALL TESTS PASSED - CASCADE IS BULLETPROOF!")
        elif failed + errors <= total * 0.1:  # Less than 10% failure rate
            logger.info("\n⚠️  MOSTLY STABLE - Minor issues to address")
        else:
            logger.info("\n🚨 PLATFORM NEEDS ATTENTION - Multiple failures detected")
        
        logger.info("=" * 60)

async def main():
    """Main test execution"""
    harness = CascadeTestHarness()
    await harness.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())