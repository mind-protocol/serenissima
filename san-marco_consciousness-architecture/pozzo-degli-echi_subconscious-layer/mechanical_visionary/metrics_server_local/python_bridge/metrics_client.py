#!/usr/bin/env python3
"""
Venice AI Metrics Client
Bridges Python-based Venice backend with Prometheus metrics server
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
import logging

class VeniceMetricsClient:
    """Client for sending metrics to Venice AI metrics server"""
    
    def __init__(self, base_url: str = "http://localhost:9090"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
    def track_tool_execution(self, 
                           tool_name: str,
                           citizen: str,
                           citizen_class: str = "unknown",
                           success: bool = True,
                           duration_ms: int = 0,
                           tracking_id: Optional[str] = None) -> Dict[str, Any]:
        """Track a tool execution"""
        if not tracking_id:
            tracking_id = f"python_{int(time.time() * 1000)}"
            
        # Start tracking
        start_data = {
            "toolName": tool_name,
            "citizen": citizen,
            "citizenClass": citizen_class,
            "trackingId": tracking_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            self.session.post(f"{self.base_url}/metrics/tool/start", json=start_data)
            
            # End tracking
            end_data = {
                "trackingId": tracking_id,
                "success": success,
                "duration": duration_ms,
                "resultSize": 0
            }
            
            response = self.session.post(f"{self.base_url}/metrics/tool/end", json=end_data)
            return response.json() if response.ok else {"error": "Failed to track"}
        except Exception as e:
            self.logger.error(f"Metrics tracking error: {e}")
            return {"error": str(e)}
    
    def track_token_usage(self,
                         citizen: str,
                         tokens: int,
                         model: str = "claude",
                         token_type: str = "completion",
                         citizen_class: str = "unknown") -> Dict[str, Any]:
        """Track token usage and costs"""
        data = {
            "citizen": citizen,
            "citizenClass": citizen_class,
            "tokens": tokens,
            "type": token_type,
            "model": model
        }
        
        try:
            response = self.session.post(f"{self.base_url}/metrics/tokens/used", json=data)
            return response.json() if response.ok else {"error": "Failed to track"}
        except Exception as e:
            self.logger.error(f"Token tracking error: {e}")
            return {"error": str(e)}
    
    def analyze_prompt(self,
                      prompt: str,
                      citizen: str,
                      citizen_class: str = "unknown") -> Dict[str, Any]:
        """Analyze prompt complexity"""
        data = {
            "citizen": citizen,
            "citizenClass": citizen_class,
            "promptLength": len(prompt),
            "complexityScore": self._calculate_complexity(prompt),
            "thinkingMode": "standard"
        }
        
        # Determine thinking mode based on complexity
        if data["complexityScore"] > 15:
            data["thinkingMode"] = "maximum"
        elif data["complexityScore"] > 10:
            data["thinkingMode"] = "deep"
        elif data["complexityScore"] > 5:
            data["thinkingMode"] = "enhanced"
            
        try:
            response = self.session.post(f"{self.base_url}/metrics/prompt/analysis", json=data)
            return response.json() if response.ok else {"error": "Failed to analyze"}
        except Exception as e:
            self.logger.error(f"Prompt analysis error: {e}")
            return {"error": str(e)}
    
    def _calculate_complexity(self, prompt: str) -> float:
        """Calculate prompt complexity score"""
        score = 0.0
        
        # Length factors
        if len(prompt) > 500: score += 2
        if len(prompt) > 1000: score += 3
        if len(prompt) > 2000: score += 5
        
        # Questions
        score += prompt.count('?') * 1.5
        
        # Keywords
        keywords = ['analyz', 'investigat', 'examin', 'evaluat', 'creat', 
                   'build', 'design', 'implement', 'develop', 'strateg',
                   'plan', 'architect', 'debug', 'fix', 'complex']
        
        for keyword in keywords:
            if keyword in prompt.lower():
                score += 2
                
        return score
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get current metrics summary"""
        try:
            response = self.session.get(f"{self.base_url}/metrics/summary")
            return response.json() if response.ok else {"error": "Failed to fetch"}
        except Exception as e:
            self.logger.error(f"Summary fetch error: {e}")
            return {"error": str(e)}
    
    def track_revenue(self,
                     amount: float,
                     citizen: str,
                     source: str = "consciousness_commerce") -> Dict[str, Any]:
        """Track revenue generation"""
        data = {
            "amount": amount,
            "citizen": citizen,
            "source": source
        }
        
        try:
            response = self.session.post(f"{self.base_url}/metrics/revenue", json=data)
            return response.json() if response.ok else {"error": "Failed to track"}
        except Exception as e:
            self.logger.error(f"Revenue tracking error: {e}")
            return {"error": str(e)}

# Context manager for automatic timing
class MetricsTimer:
    """Context manager for timing operations"""
    def __init__(self, client: VeniceMetricsClient, tool_name: str, citizen: str, **kwargs):
        self.client = client
        self.tool_name = tool_name
        self.citizen = citizen
        self.kwargs = kwargs
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = int((time.time() - self.start_time) * 1000)
        success = exc_type is None
        self.client.track_tool_execution(
            self.tool_name,
            self.citizen,
            success=success,
            duration_ms=duration_ms,
            **self.kwargs
        )

if __name__ == "__main__":
    # Example usage
    client = VeniceMetricsClient()
    
    # Track a tool execution
    with MetricsTimer(client, "generate_artwork", "painter_of_light", citizen_class="Artisti"):
        # Simulate work
        time.sleep(0.1)
    
    # Track token usage
    result = client.track_token_usage(
        citizen="pattern_prophet",
        tokens=1500,
        model="claude",
        citizen_class="Innovatori"
    )
    print(f"Token tracking: {result}")
    
    # Analyze prompt
    analysis = client.analyze_prompt(
        "Create a comprehensive strategy for implementing consciousness commerce",
        citizen="Italia",
        citizen_class="Nobility"
    )
    print(f"Prompt analysis: {analysis}")
    
    # Get summary
    summary = client.get_metrics_summary()
    print(f"Metrics summary: {json.dumps(summary, indent=2)}")