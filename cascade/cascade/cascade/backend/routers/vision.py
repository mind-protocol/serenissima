"""
CASCADE Vision API Routes
Endpoints for visual capture and debugging
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Optional, Any
from datetime import datetime

from services.vision_service import vision_service, CaptureOptions, PLAYWRIGHT_AVAILABLE

router = APIRouter(prefix="/api/vision", tags=["vision"])

class CaptureRequest(BaseModel):
    """Request model for capturing a page"""
    url: HttpUrl
    viewport: Optional[Dict[str, int]] = {"width": 1920, "height": 1080}
    full_page: Optional[bool] = True
    wait_for_selector: Optional[str] = None
    wait_for_timeout: Optional[int] = 30000
    device_scale_factor: Optional[float] = 1.0
    is_mobile: Optional[bool] = False

class JourneyStep(BaseModel):
    """Single step in a user journey"""
    action: str  # visit, click, type, wait, wait_for, screenshot
    url: Optional[str] = None
    selector: Optional[str] = None
    text: Optional[str] = None
    ms: Optional[int] = None
    full_page: Optional[bool] = True

class JourneyRequest(BaseModel):
    """Request model for capturing a user journey"""
    journey_id: str
    steps: List[JourneyStep]

class AnnotationRequest(BaseModel):
    """Request model for adding annotation"""
    author: str
    type: str  # bug, design, feature, observation
    content: str
    metadata: Optional[Dict[str, Any]] = {}

@router.get("/health")
async def vision_health():
    """Check if vision service is available"""
    return {
        "status": "healthy",
        "playwright_available": PLAYWRIGHT_AVAILABLE,
        "message": "Vision service is ready" if PLAYWRIGHT_AVAILABLE else "Playwright not installed"
    }

@router.post("/capture")
async def capture_page(request: CaptureRequest, background_tasks: BackgroundTasks):
    """Capture a screenshot of a specific page"""
    if not PLAYWRIGHT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Vision service unavailable. Playwright not installed."
        )
    
    try:
        options = CaptureOptions(
            viewport=request.viewport,
            full_page=request.full_page,
            wait_for_selector=request.wait_for_selector,
            wait_for_timeout=request.wait_for_timeout,
            device_scale_factor=request.device_scale_factor,
            is_mobile=request.is_mobile
        )
        
        screenshot = await vision_service.capture_page(str(request.url), options)
        
        return {
            "success": True,
            "screenshot": screenshot.to_dict(),
            "message": f"Screenshot captured: {screenshot.id}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to capture screenshot: {str(e)}"
        )

@router.post("/journey")
async def capture_journey(request: JourneyRequest):
    """Capture a user journey through multiple steps"""
    if not PLAYWRIGHT_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Vision service unavailable. Playwright not installed."
        )
    
    try:
        steps = [step.dict() for step in request.steps]
        screenshots = await vision_service.capture_user_journey(
            request.journey_id,
            steps
        )
        
        return {
            "success": True,
            "journey_id": request.journey_id,
            "screenshots": [s.to_dict() for s in screenshots],
            "total_captures": len(screenshots)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to capture journey: {str(e)}"
        )

@router.get("/history")
async def get_capture_history(limit: int = 50):
    """Get recent screenshot history"""
    try:
        history = await vision_service.get_screenshot_history(limit)
        return {
            "success": True,
            "screenshots": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get history: {str(e)}"
        )

@router.post("/annotate/{screenshot_id}")
async def annotate_screenshot(screenshot_id: str, annotation: AnnotationRequest):
    """Add annotation to a screenshot"""
    try:
        annotation_data = {
            "author": annotation.author,
            "type": annotation.type,
            "content": annotation.content,
            "metadata": annotation.metadata
        }
        
        success = await vision_service.annotate_screenshot(screenshot_id, annotation_data)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Screenshot {screenshot_id} not found"
            )
        
        return {
            "success": True,
            "message": f"Annotation added to {screenshot_id}"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add annotation: {str(e)}"
        )

@router.get("/screenshot/{screenshot_id}")
async def get_screenshot_metadata(screenshot_id: str):
    """Get metadata for a specific screenshot"""
    try:
        # This would read from the metadata file
        # For now, return a placeholder
        return {
            "success": True,
            "screenshot_id": screenshot_id,
            "message": "Metadata retrieval not yet implemented"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get screenshot metadata: {str(e)}"
        )