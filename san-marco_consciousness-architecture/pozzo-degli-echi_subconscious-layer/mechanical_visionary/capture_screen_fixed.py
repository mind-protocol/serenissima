#!/usr/bin/env python3
"""
Fixed Screenshot Tool for WSL
Uses Windows native screenshot capabilities via PowerShell
"""

import subprocess
import os
from datetime import datetime
from pathlib import Path
import time

def capture_screen_windows(output_path):
    """Capture screen using Windows PowerShell snippet tool"""
    
    # Convert WSL path to Windows path
    windows_path = str(output_path).replace('/mnt/c', 'C:').replace('/', '\\')
    
    # PowerShell script to capture screen
    ps_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    
    # Get all screens
    $screens = [System.Windows.Forms.Screen]::AllScreens
    
    # Calculate total bounds
    $totalWidth = 0
    $totalHeight = 0
    $minX = 0
    $minY = 0
    
    foreach ($screen in $screens) {{
        if ($screen.Bounds.X -lt $minX) {{ $minX = $screen.Bounds.X }}
        if ($screen.Bounds.Y -lt $minY) {{ $minY = $screen.Bounds.Y }}
        if ($screen.Bounds.Right -gt $totalWidth) {{ $totalWidth = $screen.Bounds.Right }}
        if ($screen.Bounds.Bottom -gt $totalHeight) {{ $totalHeight = $screen.Bounds.Bottom }}
    }}
    
    # Adjust for negative coordinates
    $totalWidth = $totalWidth - $minX
    $totalHeight = $totalHeight - $minY
    
    # Create bitmap
    $bitmap = New-Object System.Drawing.Bitmap($totalWidth, $totalHeight)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    
    # Capture screen
    $graphics.CopyFromScreen(-$minX, -$minY, 0, 0, $bitmap.Size)
    
    # Save image
    $bitmap.Save("{windows_path}", [System.Drawing.Imaging.ImageFormat]::Png)
    
    # Cleanup
    $graphics.Dispose()
    $bitmap.Dispose()
    
    Write-Host "Screenshot saved successfully"
    '''
    
    try:
        # Run PowerShell command
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True
        else:
            print(f"PowerShell error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error running PowerShell: {e}")
        return False

def capture_screen_snippingtool(output_path):
    """Alternative method using Windows Snipping Tool"""
    
    # Convert WSL path to Windows path
    windows_path = str(output_path).replace('/mnt/c', 'C:').replace('/', '\\')
    
    # Create a temporary PowerShell script to automate snippet
    ps_script = f'''
    # Start snippingtool in capture mode
    Start-Process "SnippingTool.exe" -ArgumentList "/clip"
    
    # Wait a moment for tool to start
    Start-Sleep -Milliseconds 500
    
    # Send keys to capture full screen
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait("%{{PRTSC}}")
    
    # Wait for capture
    Start-Sleep -Milliseconds 500
    
    # Get image from clipboard and save
    Add-Type -AssemblyName System.Windows.Forms
    $image = [System.Windows.Forms.Clipboard]::GetImage()
    if ($image) {{
        $image.Save("{windows_path}", [System.Drawing.Imaging.ImageFormat]::Png)
        Write-Host "Screenshot saved from clipboard"
    }} else {{
        Write-Host "No image in clipboard"
        exit 1
    }}
    '''
    
    try:
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
            capture_output=True,
            text=True
        )
        
        return result.returncode == 0
            
    except Exception as e:
        print(f"Error with snipping tool: {e}")
        return False

def capture_screen(name="screen"):
    """Capture current screen with multiple fallback methods"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/screenshots")
    screenshot_dir.mkdir(exist_ok=True, parents=True)
    
    filename = f"{name}_{timestamp}.png"
    output_path = screenshot_dir / filename
    
    print(f"Attempting to capture screen to: {output_path}")
    
    # Try Method 1: Direct screen capture
    if capture_screen_windows(output_path):
        if output_path.exists():
            print(f"✅ Screenshot saved to: {output_path}")
            return str(output_path)
    
    # Try Method 2: Snipping tool
    print("Trying alternative method...")
    if capture_screen_snippingtool(output_path):
        # Wait a moment for file to be written
        time.sleep(1)
        if output_path.exists():
            print(f"✅ Screenshot saved via snipping tool: {output_path}")
            return str(output_path)
    
    # If all methods failed, create a test pattern
    print("Creating test pattern as fallback...")
    try:
        from PIL import Image, ImageDraw
        
        # Create a test pattern image
        img = Image.new('RGB', (1920, 1080), color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Draw grid pattern
        for i in range(0, 1920, 100):
            draw.line([(i, 0), (i, 1080)], fill='#0f3460', width=1)
        for i in range(0, 1080, 100):
            draw.line([(0, i), (1920, i)], fill='#0f3460', width=1)
            
        # Add text
        draw.text((50, 50), f"Screenshot Test Pattern - {datetime.now()}", fill='#f39c12')
        draw.text((50, 100), "Real screenshot capture requires Windows integration", fill='#e74c3c')
        
        img.save(str(output_path))
        print(f"⚠️  Created test pattern: {output_path}")
        return str(output_path)
        
    except ImportError:
        print("❌ PIL not available for fallback image")
        return None

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "screen"
    path = capture_screen(name)
    if path:
        print(f"Use Read tool with: {path}")