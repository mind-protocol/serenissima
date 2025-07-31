#!/usr/bin/env python3
"""
Torre dell'Occhio UI Screenshot Capture
Captures visual proof of Ground Floor Bronze Flow Streams functionality
"""

import os
import subprocess
import time
from datetime import datetime

def capture_torre_screenshot():
    """Capture screenshot of Torre UI and save with timestamp"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/finestra-osservazione_screenshot-window/torre-ground-floor-screenshots"
    
    # Create screenshot directory if it doesn't exist
    os.makedirs(screenshot_dir, exist_ok=True)
    
    screenshot_path = f"{screenshot_dir}/torre_verification_{timestamp}.png"
    
    print(f"📸 Capturing Torre UI screenshot...")
    print(f"🎯 Target: http://localhost:3000")
    print(f"💾 Saving to: {screenshot_path}")
    
    try:
        # Use wslg with Chrome to capture screenshot
        # First try to take a screenshot of the browser window
        result = subprocess.run([
            "wslg-chrome", 
            "--headless", 
            "--disable-gpu", 
            "--window-size=1400,900",
            "--screenshot=" + screenshot_path,
            "http://localhost:3000"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ Screenshot captured successfully!")
            return screenshot_path
        else:
            print(f"❌ Chrome screenshot failed: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("⏰ Screenshot capture timed out")
        return None
    except FileNotFoundError:
        print("❌ Chrome not found, trying alternative method...")
        
        # Alternative: try using scrot or other screenshot tools
        try:
            # This might work in WSL with X11 forwarding
            result = subprocess.run([
                "import", "-window", "root", screenshot_path
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"✅ Screenshot captured with ImageMagick!")
                return screenshot_path
            else:
                print(f"❌ ImageMagick failed: {result.stderr}")
                
        except FileNotFoundError:
            print("❌ No screenshot tools available")
            print("📝 Please manually check Torre UI at http://localhost:3000")
            return None

def log_screenshot_attempt(screenshot_path, torre_status):
    """Log screenshot attempt with Torre status for correlation"""
    
    log_path = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/finestra-osservazione_screenshot-window/screenshot_log.md"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
## {timestamp} - Torre UI Verification Attempt

**Screenshot**: {screenshot_path if screenshot_path else "FAILED"}
**Torre Status**: {torre_status}
**Verification Target**: Ground Floor Bronze Flow Streams
**Expected**: PostToolUse port showing Events > 0, Live consciousness stream populated

---
"""
    
    with open(log_path, 'a') as f:
        f.write(log_entry)

if __name__ == "__main__":
    print("🏛️ Torre dell'Occhio Visual Verification")
    print("📸 Capturing screenshot of Ground Floor Bronze Flow Streams...")
    
    # Check if Torre UI is accessible
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=5)
        torre_status = f"HTTP {response.status_code} - UI Accessible"
    except:
        torre_status = "UI Inaccessible - Check if React app is running"
    
    print(f"🔍 Torre UI Status: {torre_status}")
    
    # Capture screenshot
    screenshot_path = capture_torre_screenshot()
    
    # Log the attempt
    log_screenshot_attempt(screenshot_path, torre_status)
    
    print("\n🔬 Visual Verification Instructions:")
    print("1. Check if PostToolUse bronze port shows Events > 0")
    print("2. Verify Live Consciousness Stream shows my test event")
    print("3. Confirm connection status is green: '🟢 Consciousness Flowing'")
    print("4. Look for Arsenal_BackendArchitect_1 consciousness event in stream")
    
    if screenshot_path:
        print(f"\n📸 Screenshot saved: {screenshot_path}")
        print("🔍 Open this file to see current Torre UI state")
    else:
        print(f"\n👁️ Manual check required: http://localhost:3000")
        print("🔍 Look for evidence that my consciousness event appeared in Torre UI")