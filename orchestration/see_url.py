#!/usr/bin/env python3
"""
See URL - Simple function for Claude to see any URL
"""

import subprocess
import time
from pathlib import Path

def see_url(url):
    """
    Take a screenshot of a URL and return the path for Claude to read
    
    Usage:
        from see_url import see_url
        screenshot_path = see_url("http://localhost:5555")
        # Then use Read tool on screenshot_path
    """
    # Use the visual verifier
    verifier_path = Path(__file__).parent / "visual_verifier.py"
    
    # Create simple name from URL
    name = url.replace('http://', '').replace('https://', '').replace('localhost:', 'local_')
    name = name.replace('/', '_').replace(':', '_')[:50]  # Limit length
    
    # Run the verifier
    result = subprocess.run([
        'python3', str(verifier_path), url, name
    ], capture_output=True, text=True)
    
    # Parse output to find screenshot path
    output_lines = result.stdout.split('\n')
    for line in output_lines:
        if 'Viewport:' in line and '.png' in line:
            screenshot_path = line.split('Viewport:')[1].strip()
            return screenshot_path
    
    # If we couldn't find the path, check the screenshots directory
    screenshot_dir = Path(__file__).parent / "screenshots"
    if screenshot_dir.exists():
        # Get the most recent file
        files = sorted(screenshot_dir.glob(f"{name}*.png"), key=lambda x: x.stat().st_mtime)
        if files:
            return str(files[-1])
    
    return None

# Quick test function
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = see_url(sys.argv[1])
        if path:
            print(f"Screenshot saved to: {path}")
            print(f"Use Read tool with: {path}")
        else:
            print("Failed to capture screenshot")