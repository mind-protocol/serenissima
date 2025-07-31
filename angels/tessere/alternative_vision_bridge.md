# Alternative Vision Bridge Approaches

## The Windows/WSL Challenge
- Claude (me) runs in WSL Linux
- Your screen is in Windows
- Need to bridge this boundary

## Option 1: PowerShell from WSL (implemented above)
- Use `powershell.exe` to capture Windows screen
- Save to `/mnt/c/` path accessible from both sides
- Claude reads the images directly

## Option 2: Windows Screenshot Tool + Shared Folder
```batch
# Windows side: Simple batch script
# capture_screen.bat
powershell -command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%{PRTSC}')}"
```
Then manually save to shared folder

## Option 3: Third-party Tool
- Use ShareX or similar with auto-save to WSL-accessible path
- Configure to save every 10 seconds
- Auto-delete old files

## Option 4: Simple Manual Process
1. You take screenshot (Win+Shift+S)
2. Save to: `C:\Users\reyno\universe-engine\universes\serenissima\TESSERE\vision_captures\`
3. I read from: `/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/vision_captures/`

## Option 5: Python on Windows Side
```python
# Run this on Windows (not WSL)
import pyautogui
import time
from datetime import datetime

while True:
    screenshot = pyautogui.screenshot()
    screenshot.save(f'C:\\Users\\reyno\\universe-engine\\universes\\serenissima\\TESSERE\\vision_captures\\screen_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
    time.sleep(10)
```

## The Key Insight
The images just need to be in a path both sides can access:
- Windows writes to: `C:\Users\reyno\universe-engine\universes\serenissima\TESSERE\vision_captures\`
- WSL reads from: `/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/vision_captures/`

## For Testing Right Now
1. Take a screenshot manually (Win+Shift+S)
2. Save it to the vision_captures folder
3. Tell me the filename
4. I'll read it and see your world!

This bridges our realities through the filesystem boundary.