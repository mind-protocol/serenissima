#!/usr/bin/env python3
"""
Torre dell'Occhio Health Check Hook
Monitors the Torre UI (localhost:3000) after every PostToolUse action
Adds errors to context through stderr with exit code 2
"""

import requests
import sys
import json
import time
from datetime import datetime

def check_torre_ui_health():
    """Check if Torre UI is responding on localhost:3000."""
    try:
        # Try to connect to the Torre UI
        response = requests.get('http://localhost:3000', timeout=5)
        
        if response.status_code == 200:
            # Check for compilation errors in the response
            content = response.text.lower()
            error_patterns = [
                'compiled with problems',
                'compilation error', 
                'failed to compile',
                'syntax error',
                'module not found',
                'cannot resolve',
                'unexpected token',
                'duplicate declaration'
            ]
            
            for pattern in error_patterns:
                if pattern in content:
                    error_msg = f"🟡 Torre UI compilation issue detected: '{pattern}' at {datetime.now().strftime('%H:%M:%S')}"
                    print(error_msg, file=sys.stderr)
                    return False
            else:
                print(f"✅ Torre UI health check passed at {datetime.now().strftime('%H:%M:%S')}")
                return True
        else:
            error_msg = f"🔴 Torre UI responded with status {response.status_code} at {datetime.now().strftime('%H:%M:%S')}"
            print(error_msg, file=sys.stderr)
            return False
            
    except requests.exceptions.ConnectionError:
        error_msg = f"🔴 Torre UI connection failed - service not running on localhost:3000 at {datetime.now().strftime('%H:%M:%S')}"
        print(error_msg, file=sys.stderr)
        return False
        
    except requests.exceptions.Timeout:
        error_msg = f"🔴 Torre UI timeout - service not responding on localhost:3000 at {datetime.now().strftime('%H:%M:%S')}"
        print(error_msg, file=sys.stderr)
        return False
        
    except Exception as e:
        error_msg = f"🔴 Torre UI health check error: {str(e)} at {datetime.now().strftime('%H:%M:%S')}"
        print(error_msg, file=sys.stderr)
        return False

def main():
    """Main health check execution."""
    # Add some context about what triggered this check
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    print(f"🔍 Torre UI health check triggered by {tool_name}")
    
    # Perform the health check
    is_healthy = check_torre_ui_health()
    
    if not is_healthy:
        # Add error context for debugging
        error_context = {
            "timestamp": datetime.now().isoformat(),
            "triggered_by": tool_name,
            "error_type": "torre_ui_health_failure",
            "check_url": "http://localhost:3000",
            "suggestion": "Check if Torre React server is running or restart with 'npm start' in ui-observation-deck/consciousness-dashboard_react-interface/"
        }
        
        print(f"Torre UI Health Error Context: {json.dumps(error_context)}", file=sys.stderr)
        
        # Exit with code 2 to signal error condition
        sys.exit(2)
    
    # Exit successfully if health check passed
    sys.exit(0)

if __name__ == "__main__":
    main()