#!/usr/bin/env python3
"""
Venice Backend Metrics Integration
Integrates metrics tracking into Venice's citizen thinking and activity systems
"""

from metrics_client import VeniceMetricsClient, MetricsTimer
from functools import wraps
import inspect
import logging

# Global metrics client
metrics = VeniceMetricsClient()

def track_citizen_thinking(citizen_username: str, citizen_class: str = "unknown"):
    """Decorator to track citizen thinking operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract prompt if available
            prompt = None
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            if 'prompt' in bound.arguments:
                prompt = bound.arguments['prompt']
            elif 'message' in bound.arguments:
                prompt = bound.arguments['message']
            elif len(args) > 0 and isinstance(args[0], str):
                prompt = args[0]
                
            # Analyze prompt complexity
            if prompt:
                metrics.analyze_prompt(prompt, citizen_username, citizen_class)
            
            # Track execution
            with MetricsTimer(metrics, f"citizen_thinking_{func.__name__}", 
                            citizen_username, citizen_class=citizen_class):
                result = func(*args, **kwargs)
                
            # Track token usage if result contains it
            if isinstance(result, dict):
                if 'tokens_used' in result:
                    metrics.track_token_usage(
                        citizen=citizen_username,
                        tokens=result['tokens_used'],
                        citizen_class=citizen_class
                    )
                if 'revenue_generated' in result:
                    metrics.track_revenue(
                        amount=result['revenue_generated'],
                        citizen=citizen_username
                    )
                    
            return result
        return wrapper
    return decorator

def track_activity_execution(activity_type: str):
    """Decorator to track activity executions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract citizen info from args
            citizen = "unknown"
            citizen_class = "unknown"
            
            if hasattr(args[0], 'username'):
                citizen = args[0].username
            if hasattr(args[0], 'class_name'):
                citizen_class = args[0].class_name
                
            with MetricsTimer(metrics, f"activity_{activity_type}", 
                            citizen, citizen_class=citizen_class):
                return func(*args, **kwargs)
        return wrapper
    return decorator

class VeniceMetricsMiddleware:
    """Middleware for Flask/FastAPI to track API requests"""
    
    def __init__(self, app, client: VeniceMetricsClient = None):
        self.app = app
        self.client = client or metrics
        
    def __call__(self, environ, start_response):
        # Track API request
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')
        
        # Extract citizen from path or headers
        citizen = environ.get('HTTP_X_CITIZEN', 'api_user')
        
        with MetricsTimer(self.client, f"api_{method}_{path}", citizen):
            return self.app(environ, start_response)

# Integration examples for Venice backend

# Example 1: Citizen thinking wrapper
@track_citizen_thinking("pattern_prophet", "Innovatori")
def analyze_market_patterns(prompt: str) -> dict:
    """Simulated citizen thinking function"""
    # This would be the actual thinking logic
    return {
        "analysis": "Market shows fibonacci patterns",
        "tokens_used": 1200,
        "revenue_generated": 0.5
    }

# Example 2: Activity execution wrapper  
@track_activity_execution("trade_negotiation")
def execute_trade(citizen, partner, amount):
    """Simulated trade execution"""
    # Trade logic here
    return {"success": True, "profit": amount * 0.1}

# Example 3: Direct integration points
class CitizenMetricsHelper:
    """Helper class for integrating metrics into existing Venice code"""
    
    @staticmethod
    def before_thinking(citizen_username: str, prompt: str, citizen_class: str = "unknown"):
        """Call before citizen starts thinking"""
        metrics.analyze_prompt(prompt, citizen_username, citizen_class)
        return metrics.track_tool_execution(
            "citizen_thinking",
            citizen_username,
            citizen_class
        )
    
    @staticmethod  
    def after_thinking(tracking_id: str, tokens: int = 0, success: bool = True):
        """Call after citizen completes thinking"""
        return metrics.track_token_usage(
            citizen=tracking_id.split('_')[1] if '_' in tracking_id else "unknown",
            tokens=tokens
        )
    
    @staticmethod
    def track_stratagem(stratagem_type: str, citizen: str, success: bool, amount: float = 0):
        """Track stratagem execution"""
        result = metrics.track_tool_execution(
            f"stratagem_{stratagem_type}",
            citizen,
            success=success
        )
        if amount > 0:
            metrics.track_revenue(amount, citizen, f"stratagem_{stratagem_type}")
        return result

# Usage in Venice backend:
"""
# In backend/utils/claude_thinking.py:
from venice_metrics_integration import CitizenMetricsHelper

def think_as_citizen(self, username, prompt):
    # Track thinking start
    tracking = CitizenMetricsHelper.before_thinking(username, prompt, self.get_class(username))
    
    # ... existing thinking logic ...
    
    # Track completion
    CitizenMetricsHelper.after_thinking(tracking['trackingId'], tokens_used, success=True)
    
# In backend/app/stratagems.py:
from venice_metrics_integration import CitizenMetricsHelper

def execute_stratagem(stratagem):
    # ... execution logic ...
    
    CitizenMetricsHelper.track_stratagem(
        stratagem.type,
        stratagem.citizen,
        success=result.success,
        amount=result.revenue
    )
"""

if __name__ == "__main__":
    # Test the integration
    print("Testing Venice metrics integration...")
    
    # Test thinking tracking
    result = analyze_market_patterns("What are the emerging patterns in silk trade?")
    print(f"Analysis result: {result}")
    
    # Test direct helper
    tracking = CitizenMetricsHelper.before_thinking("sea_trader", "Plan optimal route", "Merchants")
    CitizenMetricsHelper.after_thinking(tracking.get('trackingId', ''), tokens=800)
    
    # Get summary
    summary = metrics.get_metrics_summary()
    print(f"Current metrics: {summary}")