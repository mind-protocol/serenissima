"""
CASCADE Vision Service
Captures visual state of the platform for debugging and design
"""

import asyncio
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import hashlib

try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Warning: Playwright not installed. Vision features will be limited.")

@dataclass
class CaptureOptions:
    """Options for screenshot capture"""
    viewport: Dict[str, int] = None
    full_page: bool = True
    wait_for_selector: Optional[str] = None
    wait_for_timeout: int = 30000
    device_scale_factor: float = 1.0
    has_touch: bool = False
    is_mobile: bool = False
    
    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {"width": 1920, "height": 1080}

@dataclass
class Screenshot:
    """Screenshot metadata and data"""
    id: str
    url: str
    timestamp: datetime
    viewport: Dict[str, int]
    file_path: str
    file_size: int
    options: CaptureOptions
    metadata: Dict[str, Any] = None
    annotations: List[Dict[str, Any]] = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "timestamp": self.timestamp.isoformat(),
            "viewport": self.viewport,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "metadata": self.metadata or {},
            "annotations": self.annotations or []
        }

class VisionService:
    """Service for capturing visual state of CASCADE"""
    
    def __init__(self, storage_path: str = "./vision_captures"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.browser: Optional[Browser] = None
        self._lock = asyncio.Lock()
        
    async def start(self):
        """Initialize the browser instance"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright is not installed. Run: pip install playwright && playwright install chromium")
            
        async with self._lock:
            if not self.browser:
                playwright = await async_playwright().start()
                self.browser = await playwright.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
    
    async def stop(self):
        """Clean up browser instance"""
        async with self._lock:
            if self.browser:
                await self.browser.close()
                self.browser = None
    
    async def capture_page(self, url: str, options: CaptureOptions = None) -> Screenshot:
        """Capture a screenshot of a specific page"""
        if not self.browser:
            await self.start()
        
        options = options or CaptureOptions()
        
        # Create context with viewport
        context = await self.browser.new_context(
            viewport=options.viewport,
            device_scale_factor=options.device_scale_factor,
            has_touch=options.has_touch,
            is_mobile=options.is_mobile
        )
        
        try:
            page = await context.new_page()
            
            # Navigate to URL
            await page.goto(url, wait_until="networkidle", timeout=options.wait_for_timeout)
            
            # Wait for specific selector if provided
            if options.wait_for_selector:
                await page.wait_for_selector(
                    options.wait_for_selector,
                    timeout=options.wait_for_timeout
                )
            
            # Generate unique ID
            timestamp = datetime.utcnow()
            screenshot_id = hashlib.md5(
                f"{url}{timestamp.isoformat()}{options.viewport}".encode()
            ).hexdigest()[:12]
            
            # Capture screenshot
            file_name = f"{screenshot_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}.png"
            file_path = self.storage_path / file_name
            
            screenshot_bytes = await page.screenshot(
                path=str(file_path),
                full_page=options.full_page
            )
            
            # Create screenshot object
            screenshot = Screenshot(
                id=screenshot_id,
                url=url,
                timestamp=timestamp,
                viewport=options.viewport,
                file_path=str(file_path),
                file_size=len(screenshot_bytes),
                options=options,
                metadata={
                    "title": await page.title(),
                    "console_logs": []  # TODO: Capture console logs
                }
            )
            
            # Save metadata
            meta_path = self.storage_path / f"{screenshot_id}.json"
            with open(meta_path, 'w') as f:
                json.dump(screenshot.to_dict(), f, indent=2)
            
            return screenshot
            
        finally:
            await context.close()
    
    async def capture_user_journey(self, journey_id: str, steps: List[Dict[str, Any]]) -> List[Screenshot]:
        """Capture a series of screenshots following user actions"""
        if not self.browser:
            await self.start()
        
        screenshots = []
        context = await self.browser.new_context()
        
        try:
            page = await context.new_page()
            
            for i, step in enumerate(steps):
                action = step.get("action")
                
                if action == "visit":
                    await page.goto(step["url"], wait_until="networkidle")
                    
                elif action == "click":
                    await page.click(step["selector"])
                    
                elif action == "type":
                    await page.type(step["selector"], step["text"])
                    
                elif action == "wait":
                    await page.wait_for_timeout(step.get("ms", 1000))
                    
                elif action == "wait_for":
                    await page.wait_for_selector(step["selector"])
                    
                elif action == "screenshot":
                    # Capture screenshot at this point
                    options = CaptureOptions(
                        viewport={"width": 1920, "height": 1080},
                        full_page=step.get("full_page", True)
                    )
                    
                    timestamp = datetime.utcnow()
                    screenshot_id = f"{journey_id}_step_{i}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
                    file_path = self.storage_path / f"{screenshot_id}.png"
                    
                    screenshot_bytes = await page.screenshot(
                        path=str(file_path),
                        full_page=options.full_page
                    )
                    
                    screenshot = Screenshot(
                        id=screenshot_id,
                        url=page.url,
                        timestamp=timestamp,
                        viewport=options.viewport,
                        file_path=str(file_path),
                        file_size=len(screenshot_bytes),
                        options=options,
                        metadata={
                            "journey_id": journey_id,
                            "step": i,
                            "action": step
                        }
                    )
                    
                    screenshots.append(screenshot)
            
            return screenshots
            
        finally:
            await context.close()
    
    async def get_screenshot_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent screenshot history"""
        screenshots = []
        
        # Read all metadata files
        for meta_file in sorted(self.storage_path.glob("*.json"), reverse=True)[:limit]:
            with open(meta_file, 'r') as f:
                screenshots.append(json.load(f))
        
        return screenshots
    
    async def annotate_screenshot(self, screenshot_id: str, annotation: Dict[str, Any]) -> bool:
        """Add annotation to a screenshot"""
        meta_path = self.storage_path / f"{screenshot_id}.json"
        
        if not meta_path.exists():
            return False
        
        with open(meta_path, 'r') as f:
            data = json.load(f)
        
        if "annotations" not in data:
            data["annotations"] = []
        
        annotation["timestamp"] = datetime.utcnow().isoformat()
        data["annotations"].append(annotation)
        
        with open(meta_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True

# Singleton instance
vision_service = VisionService()