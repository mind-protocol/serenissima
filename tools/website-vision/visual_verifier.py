#!/usr/bin/env python3
"""
Visual Verifier - Autonomous URL Screenshot Tool
Allows Claude to see and verify frontend work
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Try multiple browser automation options
try:
    from playwright.sync_api import sync_playwright
    BROWSER_ENGINE = "playwright"
except ImportError:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        BROWSER_ENGINE = "selenium"
    except ImportError:
        print("ERROR: No browser automation library found!")
        print("Install one of these:")
        print("  pip install playwright && playwright install chromium")
        print("  OR")
        print("  pip install selenium")
        sys.exit(1)

class VisualVerifier:
    def __init__(self):
        self.screenshot_dir = Path(__file__).parent / "screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
        
    def capture_with_playwright(self, url, output_path, viewport=(1280, 720)):
        """Capture screenshot using Playwright"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': viewport[0], 'height': viewport[1]})
            
            print(f"Loading {url}...")
            page.goto(url, wait_until='networkidle')
            
            # Wait a bit for any animations
            page.wait_for_timeout(2000)
            
            # Take screenshot
            page.screenshot(path=output_path, full_page=False)
            
            # Also capture full page
            full_page_path = output_path.replace('.png', '_full.png')
            page.screenshot(path=full_page_path, full_page=True)
            
            browser.close()
            
            return output_path, full_page_path
    
    def capture_with_selenium(self, url, output_path, viewport=(1280, 720)):
        """Capture screenshot using Selenium"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--window-size={viewport[0]},{viewport[1]}')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            print(f"Loading {url}...")
            driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot
            driver.save_screenshot(output_path)
            
            # For full page, we need to scroll
            full_page_path = output_path.replace('.png', '_full.png')
            
            # Get full page dimensions
            total_height = driver.execute_script("return document.body.scrollHeight")
            driver.set_window_size(viewport[0], total_height)
            time.sleep(1)
            driver.save_screenshot(full_page_path)
            
            return output_path, full_page_path
            
        finally:
            driver.quit()
    
    def capture_url(self, url, name=None):
        """Capture screenshot of a URL"""
        if name is None:
            name = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.png"
        output_path = str(self.screenshot_dir / filename)
        
        try:
            if BROWSER_ENGINE == "playwright":
                paths = self.capture_with_playwright(url, output_path)
            else:
                paths = self.capture_with_selenium(url, output_path)
            
            print(f"✅ Screenshots saved:")
            print(f"   Viewport: {paths[0]}")
            print(f"   Full page: {paths[1]}")
            
            # Create a markdown file with the paths for easy Claude reading
            info_path = output_path.replace('.png', '_info.md')
            with open(info_path, 'w') as f:
                f.write(f"# Screenshot Information\n\n")
                f.write(f"**URL**: {url}\n")
                f.write(f"**Captured**: {datetime.now().isoformat()}\n")
                f.write(f"**Viewport Screenshot**: {paths[0]}\n")
                f.write(f"**Full Page Screenshot**: {paths[1]}\n\n")
                f.write(f"## Claude Read Commands\n\n")
                f.write(f"To view viewport: Read tool with `{paths[0]}`\n")
                f.write(f"To view full page: Read tool with `{paths[1]}`\n")
            
            return {
                'success': True,
                'viewport': paths[0],
                'full_page': paths[1],
                'info_file': info_path
            }
            
        except Exception as e:
            print(f"❌ Error capturing screenshot: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def capture_multiple_viewports(self, url, name=None):
        """Capture URL at multiple viewport sizes"""
        viewports = {
            'mobile': (375, 667),
            'tablet': (768, 1024),
            'desktop': (1280, 720),
            'wide': (1920, 1080)
        }
        
        results = {}
        
        for device, viewport in viewports.items():
            if name:
                device_name = f"{name}_{device}"
            else:
                device_name = device
            
            result = self.capture_url(url, device_name)
            results[device] = result
            time.sleep(1)  # Be nice to the server
        
        return results

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: visual_verifier.py <url> [name]")
        print("       visual_verifier.py multi <url> [name]")
        sys.exit(1)
    
    verifier = VisualVerifier()
    
    if sys.argv[1] == 'multi':
        url = sys.argv[2]
        name = sys.argv[3] if len(sys.argv) > 3 else None
        results = verifier.capture_multiple_viewports(url, name)
        
        print("\n📱 Multi-viewport capture complete!")
        for device, result in results.items():
            if result['success']:
                print(f"\n{device}: {result['viewport']}")
                
    else:
        url = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else None
        result = verifier.capture_url(url, name)
        
        if result['success']:
            print(f"\n📸 Capture complete!")
            print(f"Info file: {result['info_file']}")

if __name__ == "__main__":
    main()