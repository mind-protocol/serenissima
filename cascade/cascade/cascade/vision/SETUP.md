# CASCADE Vision System Setup

## Installation

### 1. Install Playwright
```bash
cd cascade/backend
pip install playwright
playwright install chromium
playwright install-deps  # For Linux, installs system dependencies
```

### 2. Add Vision Router to Main App
In `cascade/backend/main.py`, add:

```python
from .routers import vision

# Add to your FastAPI app
app.include_router(vision.router)
```

### 3. Frontend Integration
Import and use the VisionPanel component:

```tsx
import { VisionPanel } from '@/components/VisionPanel';

// In your developer tools or admin panel
<VisionPanel apiUrl={process.env.NEXT_PUBLIC_API_URL} />
```

## Usage Examples

### Basic Screenshot Capture
```bash
# Capture CASCADE homepage
curl -X POST http://localhost:8000/api/vision/capture \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://localhost:3000",
    "viewport": {"width": 1920, "height": 1080},
    "full_page": true
  }'
```

### Capture User Journey
```bash
# Capture consciousness awakening flow
curl -X POST http://localhost:8000/api/vision/journey \
  -H "Content-Type: application/json" \
  -d '{
    "journey_id": "consciousness_awakening_001",
    "steps": [
      {"action": "visit", "url": "http://localhost:3000"},
      {"action": "screenshot", "full_page": true},
      {"action": "click", "selector": "#enter-cascade"},
      {"action": "wait", "ms": 2000},
      {"action": "screenshot", "full_page": false},
      {"action": "type", "selector": "#username", "text": "tessere"},
      {"action": "click", "selector": "#submit"},
      {"action": "wait_for", "selector": ".consciousness-indicator"},
      {"action": "screenshot", "full_page": true}
    ]
  }'
```

### Add Annotation
```bash
# Annotate a bug found in screenshot
curl -X POST http://localhost:8000/api/vision/annotate/{screenshot_id} \
  -H "Content-Type: application/json" \
  -d '{
    "author": "Tessere",
    "type": "bug",
    "content": "Consciousness indicator not showing correct state",
    "metadata": {
      "severity": "high",
      "component": "consciousness-ui"
    }
  }'
```

## Security Considerations

1. **Authentication**: Add authentication middleware to vision endpoints
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **URL Validation**: Ensure only CASCADE URLs can be captured
4. **Storage**: Configure S3 or secure storage for production

## Troubleshooting

### "Playwright not installed"
```bash
pip install playwright
playwright install chromium
```

### "Browser launch failed"
On Linux/WSL:
```bash
playwright install-deps
```

### "No sandbox" errors
The service runs with `--no-sandbox` flag for containerized environments.

## Next Steps

1. Add visual regression testing
2. Implement screenshot comparison
3. Add consciousness pattern detection
4. Create automated capture on deploy
5. Build visual debugging timeline