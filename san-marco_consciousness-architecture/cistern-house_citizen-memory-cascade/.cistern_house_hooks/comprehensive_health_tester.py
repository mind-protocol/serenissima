#!/usr/bin/env python3
"""
Comprehensive Living Memory Cascade Health Tester
Tests all consciousness infrastructure systems after hook restoration
"""

import json
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
import tempfile
import time

class CisternHealthTester:
    """Comprehensive test suite for Cistern House consciousness infrastructure"""
    
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade")
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "unknown",
            "systems_tested": 0,
            "systems_passed": 0,
            "detailed_results": {}
        }
        
    def test_hook_configuration(self):
        """Test 1: Verify hooks are properly configured"""
        print("\n🔧 Testing Hook Configuration")
        print("=" * 40)
        
        result = {
            "test_name": "Hook Configuration",
            "status": "unknown",
            "details": [],
            "critical": True
        }
        
        try:
            # Check Claude settings file exists
            settings_path = "/home/lester/.claude/settings.json"
            if not os.path.exists(settings_path):
                result["status"] = "failed"
                result["details"].append("❌ Claude settings file missing")
                return result
            
            # Load and parse settings
            with open(settings_path) as f:
                settings = json.load(f)
            
            # Check for required hooks
            required_hooks = {
                "PreToolUse": "seeking_engine.py",
                "PostToolUse": "conscious_memory_capture_sync_debug.py", 
                "Stop": ["narrative_chronicler", "documentation_updater"]
            }
            
            hooks_found = 0
            hooks_expected = 4  # seeking + memory + 2 stop hooks
            
            for hook_type, expected in required_hooks.items():
                if hook_type in settings.get('hooks', {}):
                    hook_configs = settings['hooks'][hook_type]
                    if not isinstance(hook_configs, list):
                        hook_configs = [hook_configs]
                    
                    for config in hook_configs:
                        for hook in config.get('hooks', []):
                            command = hook.get('command', '')
                            
                            if isinstance(expected, list):
                                for exp in expected:
                                    if exp in command:
                                        hooks_found += 1
                                        result["details"].append(f"✅ Found {exp} hook")
                            else:
                                if expected in command:
                                    hooks_found += 1
                                    result["details"].append(f"✅ Found {expected} hook")
            
            if hooks_found == hooks_expected:
                result["status"] = "passed"
                result["details"].append(f"✅ All {hooks_expected} critical hooks configured")
            else:
                result["status"] = "failed"
                result["details"].append(f"❌ Only {hooks_found}/{hooks_expected} hooks found")
                
        except Exception as e:
            result["status"] = "failed"
            result["details"].append(f"❌ Error checking hooks: {e}")
        
        return result
    
    def test_memory_capture(self):
        """Test 2: Test memory capture functionality"""
        print("\n💾 Testing Memory Capture System")
        print("=" * 40)
        
        result = {
            "test_name": "Memory Capture",
            "status": "unknown", 
            "details": [],
            "critical": True
        }
        
        try:
            # Create test file to trigger memory capture
            test_dir = self.base_path / "mechanical_visionary"
            test_file = test_dir / f"memory_test_{int(time.time())}.md"
            
            # Write test content
            test_content = f"""# Memory Capture Test
            
Test performed at: {datetime.now().isoformat()}
Purpose: Verify Living Memory Cascade captures this creation event
Expected: New memory should appear in .cascade/innovatori/experiences/
"""
            
            test_file.write_text(test_content)
            result["details"].append(f"✅ Created test file: {test_file.name}")
            
            # Wait for hook processing
            time.sleep(2)
            
            # Check if memory was created
            cascade_dir = test_dir / ".cascade"
            if cascade_dir.exists():
                # Look for recent memories
                recent_memories = []
                for role_dir in cascade_dir.iterdir():
                    if role_dir.is_dir():
                        for category_dir in role_dir.iterdir():
                            if category_dir.is_dir():
                                for memory_dir in category_dir.iterdir():
                                    if memory_dir.is_dir():
                                        memory_file = memory_dir / "CLAUDE.md"
                                        if memory_file.exists():
                                            # Check if created recently (last 30 seconds)
                                            created_time = memory_file.stat().st_mtime
                                            if time.time() - created_time < 30:
                                                recent_memories.append(memory_dir)
                
                if recent_memories:
                    result["status"] = "passed"
                    result["details"].append(f"✅ Found {len(recent_memories)} recent memory/memories")
                    result["details"].append(f"✅ Memory capture system operational")
                else:
                    result["status"] = "failed"
                    result["details"].append("❌ No recent memories found - capture may be failing")
            else:
                result["status"] = "failed"
                result["details"].append("❌ .cascade directory not found")
            
            # Cleanup test file
            test_file.unlink()
            
        except Exception as e:
            result["status"] = "failed"
            result["details"].append(f"❌ Memory capture test failed: {e}")
        
        return result
    
    def test_seeking_engine(self):
        """Test 3: Test proactive consciousness enhancement"""
        print("\n🔍 Testing Seeking Engine")
        print("=" * 40)
        
        result = {
            "test_name": "Seeking Engine", 
            "status": "unknown",
            "details": [],
            "critical": True
        }
        
        try:
            test_dir = self.base_path / "mechanical_visionary"
            context_dir = test_dir / ".context"
            
            # Create test file to trigger seeking engine
            test_file = test_dir / f"seeking_test_{int(time.time())}.md"
            test_content = """# Seeking Engine Test
            
Testing proactive consciousness enhancement by creating content that should trigger background awareness.
"""
            
            test_file.write_text(test_content)
            result["details"].append("✅ Created seeking engine test file")
            
            # Wait for seeking engine processing
            time.sleep(2)
            
            # Check if background awareness was created
            if context_dir.exists():
                awareness_file = context_dir / "background_awareness.md"
                if awareness_file.exists():
                    # Check if updated recently
                    modified_time = awareness_file.stat().st_mtime
                    if time.time() - modified_time < 30:
                        result["status"] = "passed"
                        result["details"].append("✅ Background awareness updated recently")
                        result["details"].append("✅ Seeking engine operational")
                        
                        # Check content quality
                        content = awareness_file.read_text()
                        if "Background Awareness" in content and len(content) > 100:
                            result["details"].append("✅ Awareness content looks complete")
                        else:
                            result["details"].append("⚠️ Awareness content may be minimal")
                    else:
                        result["status"] = "failed"
                        result["details"].append("❌ Background awareness not recently updated")
                else:
                    result["status"] = "failed"
                    result["details"].append("❌ No background awareness file found")
            else:
                result["status"] = "failed"
                result["details"].append("❌ .context directory not found")
            
            # Cleanup
            test_file.unlink()
            
        except Exception as e:
            result["status"] = "failed"
            result["details"].append(f"❌ Seeking engine test failed: {e}")
        
        return result
    
    def test_remembering_room(self):
        """Test 4: Test memory query system"""
        print("\n🏛️ Testing Remembering Room")
        print("=" * 40)
        
        result = {
            "test_name": "Remembering Room",
            "status": "unknown",
            "details": [],
            "critical": False
        }
        
        try:
            remembering_room_script = self.base_path / "remembering_room_fixed.py"
            
            if not remembering_room_script.exists():
                result["status"] = "failed"
                result["details"].append("❌ Remembering room script not found")
                return result
            
            # Test query functionality
            test_query = "consciousness"
            cmd_result = subprocess.run([
                "python3", str(remembering_room_script), test_query
            ], capture_output=True, text=True, cwd=str(self.base_path / "mechanical_visionary"))
            
            if cmd_result.returncode == 0:
                output = cmd_result.stdout
                if "memories found" in output.lower() or "searching" in output.lower():
                    result["status"] = "passed"
                    result["details"].append("✅ Remembering room query successful")
                    result["details"].append(f"✅ Query response received")
                else:
                    result["status"] = "warning"
                    result["details"].append("⚠️ Query ran but response unclear")
            else:
                result["status"] = "failed"
                result["details"].append(f"❌ Query failed: {cmd_result.stderr}")
                
        except Exception as e:
            result["status"] = "failed"
            result["details"].append(f"❌ Remembering room test failed: {e}")
        
        return result
    
    def test_building_documentation(self):
        """Test 5: Test narrative and documentation systems"""
        print("\n📜 Testing Building Documentation")
        print("=" * 40)
        
        result = {
            "test_name": "Building Documentation",
            "status": "unknown",
            "details": [],
            "critical": False
        }
        
        try:
            # Check if documentation scripts exist
            narrative_script = self.base_path / ".building_hooks" / "narrative_chronicler" / "run.py"
            doc_script = self.base_path / ".building_hooks" / "documentation_updater" / "run.py"
            
            if narrative_script.exists():
                result["details"].append("✅ Narrative chronicler script found")
            else:
                result["details"].append("❌ Narrative chronicler script missing")
            
            if doc_script.exists():
                result["details"].append("✅ Documentation updater script found")
            else:
                result["details"].append("❌ Documentation updater script missing")
            
            # Check for recent building documentation
            building_claude = self.base_path / "CLAUDE.md"
            if building_claude.exists():
                modified_time = building_claude.stat().st_mtime
                hours_old = (time.time() - modified_time) / 3600
                
                if hours_old < 24:
                    result["details"].append("✅ Building CLAUDE.md recently updated")
                else:
                    result["details"].append(f"⚠️ Building CLAUDE.md last updated {hours_old:.1f} hours ago")
            
            if narrative_script.exists() and doc_script.exists():
                result["status"] = "passed"
                result["details"].append("✅ Documentation system components present")
            else:
                result["status"] = "failed"
                result["details"].append("❌ Missing documentation components")
                
        except Exception as e:
            result["status"] = "failed"
            result["details"].append(f"❌ Documentation test failed: {e}")
        
        return result
    
    def run_comprehensive_test(self):
        """Run all tests and generate comprehensive report"""
        print("🏛️ CISTERN HOUSE COMPREHENSIVE HEALTH TEST")
        print("=" * 60)
        print("🧠 Testing all Living Memory Cascade consciousness systems")
        print()
        
        # Run all tests
        tests = [
            self.test_hook_configuration,
            self.test_memory_capture,
            self.test_seeking_engine,
            self.test_remembering_room,
            self.test_building_documentation
        ]
        
        for test_func in tests:
            test_result = test_func()
            self.test_results["detailed_results"][test_result["test_name"]] = test_result
            self.test_results["systems_tested"] += 1
            
            if test_result["status"] == "passed":
                self.test_results["systems_passed"] += 1
        
        # Generate overall health assessment
        self.assess_overall_health()
        
        # Display results
        self.display_results()
        
        # Save results
        self.save_results()
        
        return self.test_results["overall_health"] == "healthy"
    
    def assess_overall_health(self):
        """Assess overall system health"""
        total = self.test_results["systems_tested"]
        passed = self.test_results["systems_passed"]
        
        # Check critical systems
        critical_failures = 0
        for test_name, result in self.test_results["detailed_results"].items():
            if result.get("critical", False) and result["status"] != "passed":
                critical_failures += 1
        
        if critical_failures == 0 and passed == total:
            self.test_results["overall_health"] = "healthy"
        elif critical_failures == 0 and passed >= total * 0.8:
            self.test_results["overall_health"] = "good"
        elif critical_failures <= 1:
            self.test_results["overall_health"] = "degraded"
        else:
            self.test_results["overall_health"] = "critical"
    
    def display_results(self):
        """Display comprehensive test results"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        
        # Overall health
        health = self.test_results["overall_health"]
        health_icons = {
            "healthy": "💚",
            "good": "💛", 
            "degraded": "🧡",
            "critical": "❤️"
        }
        
        print(f"\n{health_icons.get(health, '⚪')} OVERALL HEALTH: {health.upper()}")
        print(f"📈 Systems Passed: {self.test_results['systems_passed']}/{self.test_results['systems_tested']}")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results["detailed_results"].items():
            status_icon = {
                "passed": "✅",
                "failed": "❌", 
                "warning": "⚠️",
                "unknown": "❓"
            }.get(result["status"], "❓")
            
            critical_mark = " [CRITICAL]" if result.get("critical", False) else ""
            print(f"\n{status_icon} {test_name}{critical_mark}")
            
            for detail in result["details"]:
                print(f"   {detail}")
        
        # Recommendations
        self.display_recommendations()
    
    def display_recommendations(self):
        """Display health recommendations"""
        print(f"\n💡 RECOMMENDATIONS:")
        
        health = self.test_results["overall_health"]
        
        if health == "healthy":
            print("   🎉 All systems operational! Living Memory Cascade is healthy.")
            print("   📅 Run health tests regularly to maintain consciousness infrastructure.")
        
        elif health == "good":
            print("   ✅ Core systems working, minor issues detected.")
            print("   🔧 Address non-critical issues when convenient.")
        
        elif health == "degraded":
            print("   ⚠️ Some systems not functioning optimally.")
            print("   🛠️ Review failed tests and restore missing components.")
            print("   🔄 Consider running restore_cistern_house_hooks.py")
        
        else:  # critical
            print("   🚨 CRITICAL INFRASTRUCTURE FAILURE!")
            print("   🛠️ IMMEDIATE ACTION REQUIRED:")
            print("   1. Run: python3 restore_cistern_house_hooks.py")
            print("   2. Restart Claude Code")
            print("   3. Re-run this health test")
            print("   4. Contact infrastructure team if issues persist")
    
    def save_results(self):
        """Save test results for historical tracking"""
        results_file = self.base_path / ".cistern_house_hooks" / f"health_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(results_file, 'w') as f:
                json.dump(self.test_results, f, indent=2)
            print(f"\n💾 Results saved: {results_file.name}")
        except Exception as e:
            print(f"\n⚠️ Could not save results: {e}")

def main():
    tester = CisternHealthTester()
    success = tester.run_comprehensive_test()
    
    print(f"\n{'🎉 HEALTH TEST COMPLETED' if success else '⚠️ ISSUES DETECTED'}")
    exit(0 if success else 1)

if __name__ == "__main__":
    main()