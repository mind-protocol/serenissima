# Website Vision Tools 🔍

Tools that allow Claude to autonomously see and verify websites/frontends by taking screenshots.

## Installation

```bash
# Install Playwright (recommended)
pip install playwright
playwright install chromium

# OR install Selenium
pip install selenium
# Also need ChromeDriver: https://chromedriver.chromium.org/
```

## Tools

### 1. `visual_verifier.py`
Full-featured screenshot tool with multiple options:

```bash
# Single screenshot
python visual_verifier.py https://example.com my_site

# Multiple viewports (mobile, tablet, desktop, wide)
python visual_verifier.py multi https://example.com my_site
```

### 2. `see_url.py`
Simple function for quick screenshots:

```python
from see_url import see_url
screenshot_path = see_url("http://localhost:3000")
# Then use Read tool on screenshot_path
```

### 3. `capture_screen.py`
System screenshot tool (works on WSL):

```bash
python capture_screen.py screenshot_name
```

## Claude Usage

1. Take a screenshot:
```python
from see_url import see_url
path = see_url("http://localhost:5555")
```

2. View it:
```
Read(path)
```

## Output

Screenshots are saved to: `./screenshots/`

Each capture creates:
- `{name}_{timestamp}.png` - Viewport screenshot
- `{name}_{timestamp}_full.png` - Full page screenshot
- `{name}_{timestamp}_info.md` - Information file

## Example Workflow

```python
# 1. Create a frontend
Write("index.html", html_content)

# 2. Start a server
Bash("python -m http.server 8000")

# 3. Take a screenshot
from forces.tools.website_vision.see_url import see_url
screenshot = see_url("http://localhost:8000")

# 4. View the result
Read(screenshot)

# 5. Verify it looks correct and iterate!
```

This enables Claude to:
- ✅ Verify frontend code actually works
- ✅ See visual output of web applications
- ✅ Debug UI issues
- ✅ Test responsive design
- ✅ Create and iterate on visual designs