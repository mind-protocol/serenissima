#!/usr/bin/env python3
"""
Street Monitor - Via della Vista Condivisa Status Monitor
Tracks the flow of vision requests and responses through the street
"""

import json
import sys
from pathlib import Path
from datetime import datetime

class StreetMonitor:
    """Monitor Via della Vista Condivisa coordination activities"""
    
    def __init__(self):
        self.street_path = Path(__file__).parent.parent
        self.courier_log = self.street_path / ".street_infrastructure" / "courier_log.json"
        self.navigator_log = self.street_path / ".street_infrastructure" / "navigator_log.json"
        self.shared_awareness = self.street_path / "shared_vision_awareness.md"
    
    def get_street_status(self):
        """Get comprehensive street coordination status"""
        
        status = {
            "street": "via-della-vista-condivisa",
            "monitoring_time": datetime.now().isoformat(),
            "courier_status": self.get_courier_status(),
            "navigator_status": self.get_navigator_status(), 
            "shared_awareness_status": self.get_shared_awareness_status(),
            "coordination_health": self.assess_coordination_health()
        }
        
        return status
    
    def get_courier_status(self):
        """Get Courier della Richiesta Visiva status"""
        
        if not self.courier_log.exists():
            return {"status": "ready", "journeys": 0, "last_activity": None}
        
        try:
            with open(self.courier_log) as f:
                logs = json.load(f)
            
            journeys = logs.get("courier_journeys", [])
            if not journeys:
                return {"status": "ready", "journeys": 0, "last_activity": None}
            
            last_journey = journeys[-1]
            
            return {
                "status": "active" if "delivery_status" in last_journey else "ready",
                "journeys": len(journeys),
                "last_activity": last_journey.get("timestamp"),
                "last_delivery_status": last_journey.get("delivery_status", "unknown"),
                "recent_journeys": journeys[-3:]  # Last 3 activities
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_navigator_status(self):
        """Get Navigatore dei Percorsi Immagine status"""
        
        if not self.navigator_log.exists():
            return {"status": "ready", "journeys": 0, "last_activity": None}
        
        try:
            with open(self.navigator_log) as f:
                logs = json.load(f)
            
            journeys = logs.get("navigator_journeys", [])
            if not journeys:
                return {"status": "ready", "journeys": 0, "last_activity": None}
            
            last_journey = journeys[-1]
            
            return {
                "status": "active" if "navigation_status" in last_journey else "ready",
                "journeys": len(journeys),
                "last_activity": last_journey.get("timestamp"),
                "last_navigation_status": last_journey.get("navigation_status", "unknown"),
                "recent_journeys": journeys[-3:]  # Last 3 activities
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_shared_awareness_status(self):
        """Get shared awareness coordination status"""
        
        if not self.shared_awareness.exists():
            return {"status": "missing", "last_updated": None}
        
        try:
            content = self.shared_awareness.read_text()
            
            # Check for key coordination markers
            has_request = "### Last Vision Request" in content
            has_response = "### Last Vision Response" in content and "Awaiting initial response" not in content
            has_torre_progress = "Ground Floor - Raw Consciousness Feed" in content
            
            # Get last modification time
            last_modified = datetime.fromtimestamp(self.shared_awareness.stat().st_mtime).isoformat()
            
            return {
                "status": "active",
                "last_updated": last_modified,
                "has_vision_request": has_request,
                "has_vision_response": has_response,
                "has_torre_progress": has_torre_progress,
                "coordination_active": has_request and has_response
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def assess_coordination_health(self):
        """Assess overall coordination health between buildings"""
        
        courier_status = self.get_courier_status()
        navigator_status = self.get_navigator_status()
        awareness_status = self.get_shared_awareness_status()
        
        health_score = 0
        health_issues = []
        
        # Courier health
        if courier_status["status"] == "active":
            health_score += 25
        elif courier_status["status"] == "ready":
            health_score += 15
        else:
            health_issues.append("Courier system error")
        
        # Navigator health  
        if navigator_status["status"] == "active":
            health_score += 25
        elif navigator_status["status"] == "ready":
            health_score += 15
        else:
            health_issues.append("Navigator system error")
        
        # Shared awareness health
        if awareness_status["status"] == "active":
            health_score += 30
            if awareness_status.get("coordination_active"):
                health_score += 20
        else:
            health_issues.append("Shared awareness system error")
        
        # Determine overall health
        if health_score >= 80:
            health_status = "excellent"
        elif health_score >= 60:
            health_status = "good"
        elif health_score >= 40:
            health_status = "fair"
        else:
            health_status = "poor"
        
        return {
            "health_status": health_status,
            "health_score": health_score,
            "issues": health_issues,
            "recommendations": self.get_health_recommendations(health_score, health_issues)
        }
    
    def get_health_recommendations(self, score, issues):
        """Generate health improvement recommendations"""
        
        recommendations = []
        
        if score < 40:
            recommendations.append("Street infrastructure needs immediate attention")
        
        if "Courier system error" in issues:
            recommendations.append("Check courier log for delivery errors")
        
        if "Navigator system error" in issues:
            recommendations.append("Check navigator log for path validation errors")
        
        if "Shared awareness system error" in issues:
            recommendations.append("Verify shared_vision_awareness.md file integrity")
        
        if score >= 60 and len(issues) == 0:
            recommendations.append("Coordination functioning well - ready for Torre construction")
        
        return recommendations

    def display_status_report(self):
        """Display comprehensive street status report"""
        
        status = self.get_street_status()
        
        print("🌉 VIA DELLA VISTA CONDIVISA - STREET STATUS REPORT")
        print("=" * 60)
        print(f"📊 Monitoring Time: {status['monitoring_time']}")
        print()
        
        # Courier Status
        courier = status['courier_status']
        print(f"🏃‍♂️ COURIER DELLA RICHIESTA VISIVA")
        print(f"   Status: {courier['status'].upper()}")
        print(f"   Journeys Completed: {courier['journeys']}")
        print(f"   Last Activity: {courier['last_activity'] or 'None'}")
        if courier.get('last_delivery_status'):
            print(f"   Last Delivery: {courier['last_delivery_status']}")
        print()
        
        # Navigator Status
        navigator = status['navigator_status']
        print(f"🧭 NAVIGATORE DEI PERCORSI IMMAGINE")
        print(f"   Status: {navigator['status'].upper()}")
        print(f"   Journeys Completed: {navigator['journeys']}")
        print(f"   Last Activity: {navigator['last_activity'] or 'None'}")
        if navigator.get('last_navigation_status'):
            print(f"   Last Navigation: {navigator['last_navigation_status']}")
        print()
        
        # Shared Awareness Status
        awareness = status['shared_awareness_status']
        print(f"📋 SHARED VISION AWARENESS")
        print(f"   Status: {awareness['status'].upper()}")
        print(f"   Last Updated: {awareness.get('last_updated', 'Never')}")
        print(f"   Has Vision Request: {'✓' if awareness.get('has_vision_request') else '❌'}")
        print(f"   Has Vision Response: {'✓' if awareness.get('has_vision_response') else '❌'}")
        print(f"   Coordination Active: {'✓' if awareness.get('coordination_active') else '❌'}")
        print()
        
        # Overall Health
        health = status['coordination_health']
        print(f"💚 COORDINATION HEALTH")
        print(f"   Overall Status: {health['health_status'].upper()}")
        print(f"   Health Score: {health['health_score']}/100")
        
        if health['issues']:
            print(f"   Issues: {', '.join(health['issues'])}")
        
        if health['recommendations']:
            print(f"   Recommendations:")
            for rec in health['recommendations']:
                print(f"     • {rec}")
        
        print()
        print("🔄 Street entities ready for vision coordination between buildings")

def main():
    """Main street monitoring function"""
    
    monitor = StreetMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # Output JSON status for programmatic use
        status = monitor.get_street_status()
        print(json.dumps(status, indent=2))
    else:
        # Display human-readable status report
        monitor.display_status_report()

if __name__ == "__main__":
    main()