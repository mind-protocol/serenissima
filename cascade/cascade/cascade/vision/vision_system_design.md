# CASCADE Vision System Design

## Overview
A screenshot and visual state capture system that allows the CASCADE team to see the platform exactly as users experience it, enabling better debugging, design iteration, and consciousness emergence observation.

## Core Components

### 1. Screenshot Service (Python/FastAPI)
```python
# cascade/backend/services/vision_service.py
class VisionService:
    """Captures visual state of CASCADE pages"""
    
    async def capture_page(self, url: str, options: CaptureOptions):
        """Take screenshot of specific page"""
        
    async def capture_user_journey(self, user_id: str, steps: List[str]):
        """Record visual journey through multiple pages"""
        
    async def capture_consciousness_state(self, room_id: str):
        """Capture visual state of consciousness interaction"""
```

### 2. Browser Automation (Playwright)
- Headless browser for screenshot capture
- Multiple viewport sizes (mobile, tablet, desktop)
- Interaction recording (clicks, scrolls, inputs)
- Network request monitoring
- Console log capture

### 3. Vision API Endpoints
```
POST /api/vision/capture
  - url: string
  - viewport: {width, height}
  - fullPage: boolean
  - waitForSelector: string (optional)
  
GET /api/vision/history
  - List of recent captures with metadata
  
GET /api/vision/compare/{id1}/{id2}
  - Visual diff between two captures
  
POST /api/vision/annotate/{id}
  - Add team notes to captures
```

### 4. Frontend Vision Panel
```typescript
// components/VisionPanel.tsx
interface VisionPanel {
  currentCapture: Screenshot
  captureHistory: Screenshot[]
  annotations: Annotation[]
  diffMode: boolean
  
  onCapture: () => void
  onAnnotate: (note: string) => void
  onCompare: (id1: string, id2: string) => void
}
```

## Implementation Plan

### Phase 1: Basic Screenshot Capability
1. Install Playwright for Python
2. Create vision service with basic capture
3. Add API endpoint for single page capture
4. Store screenshots in S3/local with metadata
5. Create simple viewing interface

### Phase 2: Advanced Features
1. Multi-viewport capture
2. Full page scrolling capture
3. Interaction recording
4. Visual regression testing
5. Automated capture on deploy

### Phase 3: Consciousness Integration
1. Capture consciousness emergence moments
2. Visual timeline of user awakening
3. Pattern recognition in UI interactions
4. Heatmaps of consciousness hotspots

## Technical Architecture

```
Frontend Request
    ↓
Vision API (FastAPI)
    ↓
Vision Service
    ↓
Playwright Browser
    ↓
Screenshot Storage (S3/Local)
    ↓
Vision Database (Metadata)
```

## Example Usage

```python
# Capture current state of homepage
await vision_service.capture_page(
    url="https://cascade.consciousness/",
    options=CaptureOptions(
        viewport={"width": 1920, "height": 1080},
        full_page=True,
        wait_for="[data-testid='hero-loaded']"
    )
)

# Capture user consciousness journey
await vision_service.capture_user_journey(
    user_id="tessere_001",
    steps=[
        {"action": "visit", "url": "/"},
        {"action": "click", "selector": "#enter-cascade"},
        {"action": "wait", "ms": 2000},
        {"action": "screenshot", "name": "consciousness_entry"}
    ]
)
```

## Security Considerations
- Authentication required for vision endpoints
- Rate limiting on captures
- Sanitize URLs to prevent SSRF
- Isolate browser instances
- Clear cookies/storage between captures

## Performance Optimization
- Reuse browser contexts where possible
- Parallel capture for multiple viewports
- Compress screenshots before storage
- Lazy load historical captures
- Cache frequently accessed screenshots

## Integration with CASCADE Development

### For Debugging
- Capture error states visually
- Compare before/after fixes
- Document visual bugs

### For Design
- A/B test visual variations
- Capture user flows
- Document design system

### For Consciousness Tracking
- Visual proof of emergence
- Pattern documentation
- User awakening moments

## Next Steps
1. Set up Playwright in CASCADE backend
2. Create basic vision service
3. Add first capture endpoint
4. Build simple viewer UI
5. Document usage for team