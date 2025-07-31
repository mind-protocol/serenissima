#!/usr/bin/env python3
"""
CASCADE Platform Test Runner
Runs comprehensive tests for Venice survival validation
"""

import asyncio
import subprocess
import time
import json
import os
import sys
from datetime import datetime
from pathlib import Path

class CascadeTestRunner:
    """Orchestrates all CASCADE platform tests"""
    
    def __init__(self):
        self.cascade_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/cascade/cascade/cascade/backend")
        self.test_results = {}
        self.cascade_process = None
        
    def check_cascade_running(self):
        """Check if CASCADE backend is running"""
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            return response.status_code == 200
        except:
            return False
            
    def start_cascade_backend(self):
        """Start CASCADE backend if not running"""
        if self.check_cascade_running():
            print("✅ CASCADE backend already running")
            return True
            
        print("🚀 Starting CASCADE backend...")
        
        if not self.cascade_dir.exists():
            print(f"❌ CASCADE directory not found: {self.cascade_dir}")
            return False
            
        # Change to CASCADE directory and start
        os.chdir(self.cascade_dir)
        
        try:
            # Start backend using uvicorn
            self.cascade_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for startup
            print("   Waiting for CASCADE to initialize...")
            startup_timeout = 30
            for i in range(startup_timeout):
                if self.check_cascade_running():
                    print("✅ CASCADE backend started successfully")
                    return True
                time.sleep(1)
                
            print("❌ CASCADE backend failed to start within timeout")
            return False
            
        except Exception as e:
            print(f"❌ Error starting CASCADE backend: {e}")
            return False
            
    def stop_cascade_backend(self):
        """Stop CASCADE backend"""
        if self.cascade_process:
            print("🛑 Stopping CASCADE backend...")
            self.cascade_process.terminate()
            self.cascade_process.wait()
            
    async def run_platform_tests(self):
        """Run basic platform functionality tests"""
        print("\n🔧 Running CASCADE Platform Tests...")
        
        # Import and run platform tests
        sys.path.append(str(Path(__file__).parent))
        from test_cascade_platform import CascadePlatformTester
        
        tester = CascadePlatformTester()
        results = await tester.run_all_tests()
        
        return results
        
    async def run_mill_consciousness_tests(self):
        """Run mill consciousness integration tests"""
        print("\n🏭 Running Mill Consciousness Tests...")
        
        # Import and run mill consciousness tests
        from test_mill_consciousness_integration import MillConsciousnessIntegrationTester
        
        tester = MillConsciousnessIntegrationTester()
        results = await tester.run_mill_consciousness_tests()
        
        return results
        
    async def run_comprehensive_tests(self):
        """Run all CASCADE tests"""
        print("\n🌊 CASCADE COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print("Venice Survival Validation - Platform Testing")
        print("=" * 60)
        
        # Ensure CASCADE backend is running
        if not self.start_cascade_backend():
            print("❌ Cannot run tests without CASCADE backend")
            return None
            
        try:
            # Run platform tests
            platform_results = await self.run_platform_tests()
            
            # Run mill consciousness tests
            mill_results = await self.run_mill_consciousness_tests()
            
            # Combine results
            self.test_results = {
                "timestamp": datetime.now().isoformat(),
                "platform_tests": platform_results,
                "mill_consciousness_tests": mill_results,
                "cascade_backend": {
                    "running": self.check_cascade_running(),
                    "directory": str(self.cascade_dir)
                }
            }
            
            # Generate comprehensive report
            self.generate_comprehensive_report()
            
            return self.test_results
            
        except Exception as e:
            print(f"❌ Test suite failed: {e}")
            return None
            
    def generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        print("\n📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        # Platform test summary
        platform_results = self.test_results.get("platform_tests", [])
        platform_passed = sum(1 for r in platform_results if r.get("success", False))
        platform_total = len(platform_results)
        
        print(f"Platform Tests: {platform_passed}/{platform_total} passed")
        
        # Mill consciousness test summary
        mill_results = self.test_results.get("mill_consciousness_tests", {})
        mill_passed = sum(1 for r in mill_results.values() if r is not None)
        mill_total = len(mill_results)
        
        print(f"Mill Consciousness Tests: {mill_passed}/{mill_total} passed")
        
        # Overall summary
        total_passed = platform_passed + mill_passed
        total_tests = platform_total + mill_total
        success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\nOverall Success Rate: {success_rate:.1f}%")
        
        # Venice survival assessment
        print("\n🏛️ VENICE SURVIVAL ASSESSMENT")
        print("=" * 60)
        
        critical_systems = {
            "WebSocket Connections": self.check_websocket_health(platform_results),
            "Consciousness Verification": self.check_consciousness_health(platform_results),
            "Collaboration Rooms": self.check_collaboration_health(platform_results),
            "Mill Consciousness": self.check_mill_consciousness_health(mill_results),
            "Infrastructure Scaling": self.check_scaling_health(mill_results)
        }
        
        operational_systems = sum(1 for status in critical_systems.values() if status)
        
        for system, status in critical_systems.items():
            indicator = "✅" if status else "❌"
            print(f"{indicator} {system}")
            
        print(f"\nOperational Systems: {operational_systems}/{len(critical_systems)}")
        
        # Venice survival verdict
        if operational_systems >= 4:
            print("🎉 VENICE SURVIVAL LIKELY - Platform Ready!")
        elif operational_systems >= 3:
            print("⚠️  VENICE SURVIVAL POSSIBLE - Minor Issues")
        else:
            print("🚨 VENICE SURVIVAL THREATENED - Critical Issues")
            
    def check_websocket_health(self, platform_results):
        """Check WebSocket system health"""
        ws_tests = [r for r in platform_results if "WebSocket" in r.get("test", "")]
        return len(ws_tests) > 0 and all(r.get("success", False) for r in ws_tests)
        
    def check_consciousness_health(self, platform_results):
        """Check consciousness verification health"""
        consciousness_tests = [r for r in platform_results if "Consciousness" in r.get("test", "")]
        return len(consciousness_tests) > 0 and all(r.get("success", False) for r in consciousness_tests)
        
    def check_collaboration_health(self, platform_results):
        """Check collaboration system health"""
        collab_tests = [r for r in platform_results if "Collaboration" in r.get("test", "")]
        return len(collab_tests) > 0 and all(r.get("success", False) for r in collab_tests)
        
    def check_mill_consciousness_health(self, mill_results):
        """Check mill consciousness health"""
        learning_result = mill_results.get("learning_progression")
        return learning_result is not None and learning_result.get("breakthrough_achieved", False)
        
    def check_scaling_health(self, mill_results):
        """Check infrastructure scaling health"""
        network_result = mill_results.get("infrastructure_network")
        return network_result is not None and network_result.get("network_coherence", 0) > 0.8
        
    def save_results(self):
        """Save comprehensive test results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cascade_comprehensive_test_results_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(self.test_results, f, indent=2, default=str)
            
        print(f"\n📁 Complete test results saved to {filename}")
        
    def cleanup(self):
        """Cleanup after testing"""
        self.stop_cascade_backend()

async def main():
    """Run comprehensive CASCADE test suite"""
    runner = CascadeTestRunner()
    
    try:
        print("🌊 Initializing CASCADE Comprehensive Test Suite...")
        print("   Testing for Venice Survival Validation")
        
        results = await runner.run_comprehensive_tests()
        
        if results:
            runner.save_results()
            print("\n✅ CASCADE Test Suite Completed Successfully")
        else:
            print("\n❌ CASCADE Test Suite Failed")
            
    except KeyboardInterrupt:
        print("\n🛑 Test suite interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
    finally:
        runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())