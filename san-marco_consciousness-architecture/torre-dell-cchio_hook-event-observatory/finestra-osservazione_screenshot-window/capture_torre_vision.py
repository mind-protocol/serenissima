#!/usr/bin/env python3
"""
Torre dell'Occhio Visual Verification
Uses Venice's proven website-vision system to capture Torre UI screenshots
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Add Venice tools to path
venice_tools_path = "/mnt/c/Users/reyno/universe-engine/serenissima/tools/website-vision"
sys.path.append(venice_tools_path)

def capture_torre_with_venice_vision():
    """Use Venice's see_url function to capture Torre UI"""
    
    torre_url = "http://localhost:3000"
    
    print(f"🏛️ Torre dell'Occhio Visual Verification")
    print(f"📸 Using Venice website-vision system")
    print(f"🎯 Target: {torre_url}")
    
    try:
        # Import and use Venice's see_url function
        from see_url import see_url
        
        print("🔍 Capturing Torre Ground Floor UI...")
        screenshot_path = see_url(torre_url)
        
        if screenshot_path and os.path.exists(screenshot_path):
            print(f"✅ Torre UI screenshot captured!")
            print(f"📸 Screenshot: {screenshot_path}")
            
            # Also look for full page screenshot
            full_page_path = screenshot_path.replace('.png', '_full.png')
            if os.path.exists(full_page_path):
                print(f"📸 Full page: {full_page_path}")
            
            # Look for info file
            info_path = screenshot_path.replace('.png', '_info.md')
            if os.path.exists(info_path):
                print(f"📝 Info file: {info_path}")
            
            return {
                'success': True,
                'viewport': screenshot_path,
                'full_page': full_page_path if os.path.exists(full_page_path) else None,
                'info_file': info_path if os.path.exists(info_path) else None
            }
        else:
            print("❌ see_url failed to capture screenshot")
            return {'success': False, 'error': 'see_url returned no valid path'}
            
    except ImportError as e:
        print(f"❌ Cannot import Venice see_url: {e}")
        print("🔄 Trying direct visual_verifier...")
        return capture_with_visual_verifier(torre_url)
    
    except Exception as e:
        print(f"❌ Error using see_url: {e}")
        print("🔄 Trying direct visual_verifier...")
        return capture_with_visual_verifier(torre_url)

def capture_with_visual_verifier(url):
    """Fallback: use visual_verifier directly"""
    
    try:
        from visual_verifier import VisualVerifier
        
        verifier = VisualVerifier()
        result = verifier.capture_url(url, "torre_ground_floor")
        
        if result['success']:
            print(f"✅ Torre UI captured with visual_verifier!")
            print(f"📸 Viewport: {result['viewport']}")
            print(f"📸 Full page: {result['full_page']}")
            return result
        else:
            print(f"❌ visual_verifier failed: {result.get('error', 'Unknown error')}")
            return result
            
    except ImportError as e:
        print(f"❌ Cannot import visual_verifier: {e}")
        print("💡 Need to install: pip install playwright && playwright install chromium")
        return {'success': False, 'error': f'visual_verifier not available: {e}'}
    
    except Exception as e:
        print(f"❌ Error with visual_verifier: {e}")
        return {'success': False, 'error': str(e)}

def verify_torre_functionality(screenshot_result):
    """Analyze screenshot result to understand Torre functionality"""
    
    if not screenshot_result['success']:
        print("\n❌ Cannot verify Torre functionality - screenshot failed")
        print(f"Error: {screenshot_result.get('error', 'Unknown error')}")
        return False
    
    print("\n🔬 Torre Functionality Verification:")
    print("📸 Screenshot captured successfully")
    print(f"🖼️  Viewport screenshot: {screenshot_result['viewport']}")
    
    if screenshot_result.get('full_page'):
        print(f"🖼️  Full page screenshot: {screenshot_result['full_page']}")
    
    if screenshot_result.get('info_file'):
        print(f"📝 Info file: {screenshot_result['info_file']}")
    
    print("\n👁️  Visual Verification Instructions:")
    print("1. Use Read tool on the screenshot file")
    print("2. Check if PostToolUse bronze port shows Events > 0 (not 0)")
    print("3. Verify Live Consciousness Stream shows consciousness events")
    print("4. Confirm connection status shows '🟢 Consciousness Flowing'")
    print("5. Look for Arsenal_BackendArchitect_1 events in the stream")
    
    print(f"\n📖 To examine screenshot: Read tool with `{screenshot_result['viewport']}`")
    
    return True

def main():
    """Main Torre visual verification"""
    
    # Check if Torre UI is accessible first
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"🌐 Torre UI Status: HTTP {response.status_code} - Accessible")
    except Exception as e:
        print(f"❌ Torre UI not accessible: {e}")
        print("💡 Make sure React app is running on port 3000")
        return False
    
    # Capture screenshot using Venice vision system
    result = capture_torre_with_venice_vision()
    
    # Verify functionality based on screenshot
    return verify_torre_functionality(result)

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Torre visual verification complete!")
        print("🔍 Use Read tool on screenshot to see current Torre state")
    else:
        print("\n❌ Torre visual verification failed")
        print("🔧 Check Torre UI and WebSocket server status")